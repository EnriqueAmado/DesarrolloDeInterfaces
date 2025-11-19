import customtkinter as ctk
from typing import Callable, Optional, List
from registro_usuarios_ctk.model.usuario_model import Usuario
import tkinter


class MainView:
    """Vista principal: grid de 2 columnas con lista a la izquierda y detalles a la derecha."""

    def __init__(self, root):
        self.root = root
        # crear la barra de menú (la vista sólo crea los contenedores)
        self.menubar = tkinter.Menu(root)
        root.config(menu=self.menubar)
        self.menu_archivo = tkinter.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Archivo", menu=self.menu_archivo)

        # callbacks que el controlador asignará
        self.on_seleccionar_usuario: Optional[Callable[[int], None]] = None
        self.on_exit: Optional[Callable[[], None]] = None
        self.on_search_change: Optional[Callable[[str], None]] = None
        self.on_filter_change: Optional[Callable[[str], None]] = None
        self.on_double_click: Optional[Callable[[int], None]] = None

        # configurar grid
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=2)
        root.grid_rowconfigure(0, weight=1)
        root.grid_rowconfigure(1, weight=0)

        # panel izquierdo: lista scrollable
        self.lista_usuarios_frame = ctk.CTkFrame(root)
        self.lista_usuarios_frame.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)

        # título para la lista
        self.lbl_usuarios_title = ctk.CTkLabel(self.lista_usuarios_frame, text="Usuarios", font=("Arial", 14, "bold"))
        self.lbl_usuarios_title.pack(anchor="nw", padx=4, pady=(2, 6))

        # Search and filter container
        controls_frame = ctk.CTkFrame(self.lista_usuarios_frame)
        controls_frame.pack(fill="x", padx=4, pady=(0, 6))

        # búsqueda
        search_lbl = ctk.CTkLabel(controls_frame, text="Buscar:")
        search_lbl.pack(side="left", padx=(4, 6))
        self.search_var = tkinter.StringVar()
        self.search_entry = ctk.CTkEntry(controls_frame, textvariable=self.search_var)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 6))

        # filtro de género
        self.gender_var = tkinter.StringVar(value="Todos")
        self.filter_option = ctk.CTkOptionMenu(controls_frame, values=["Todos", "Masculino", "Femenino", "Otro"], variable=self.gender_var, command=self._on_filter_selected)
        self.filter_option.pack(side="left", padx=(0, 4))

        # conectar trace para búsqueda
        self.search_var.trace_add("write", lambda *_: self._on_search_text_changed())

        self.lista_usuarios_scrollable = ctk.CTkScrollableFrame(self.lista_usuarios_frame)
        self.lista_usuarios_scrollable.pack(fill="both", expand=True, padx=4, pady=4)

        # panel derecho: detalles
        self.detalles_frame = ctk.CTkFrame(root)
        self.detalles_frame.grid(row=0, column=1, sticky="nsew", padx=8, pady=8)

        # título para detalles
        self.lbl_detalles_title = ctk.CTkLabel(self.detalles_frame, text="Detalles del Usuario", font=("Arial", 14, "bold"))
        self.lbl_detalles_title.pack(anchor="nw", pady=(2, 6))

        self.lbl_nombre = ctk.CTkLabel(self.detalles_frame, text="Nombre: -")
        self.lbl_nombre.pack(anchor="nw", pady=4)

        self.lbl_edad = ctk.CTkLabel(self.detalles_frame, text="Edad: -")
        self.lbl_edad.pack(anchor="nw", pady=4)

        self.lbl_genero = ctk.CTkLabel(self.detalles_frame, text="Género: -")
        self.lbl_genero.pack(anchor="nw", pady=4)

        self.lbl_avatar = ctk.CTkLabel(self.detalles_frame, text="Avatar: -")
        self.lbl_avatar.pack(anchor="nw", pady=4)

        # footer: ocupar la segunda fila (row=1) y spanear ambas columnas
        self.footer_frame = ctk.CTkFrame(root)
        self.footer_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=8, pady=(0, 8))

        # status label a la izquierda
        self.status_var = tkinter.StringVar(value="Listo")
        self.status_label = ctk.CTkLabel(self.footer_frame, textvariable=self.status_var, anchor="w")
        self.status_label.pack(side="left", padx=8)

        # botón Salir a la derecha
        self.btn_salir = ctk.CTkButton(self.footer_frame, text="Salir", command=self._on_exit_clicked)
        self.btn_salir.pack(side="right", padx=8, pady=4)

        # botón Añadir a la izquierda del centro
        self.btn_anadir = ctk.CTkButton(self.footer_frame, text="Añadir")
        self.btn_anadir.pack(side="right", padx=8, pady=4)

        self.autosave_var = ctk.BooleanVar(value=False)
        self.autosave_switch = ctk.CTkSwitch(
            self.footer_frame, text="Auto-guardar cada 10s",
            variable=self.autosave_var,
            command=self._on_toggle_autosave
        )
        self.autosave_switch.pack(side="right", padx=8)

    def _on_exit_clicked(self):
        if self.on_exit:
            try:
                self.on_exit()
                return
            except Exception:
                # si el callback falla, fallback a cerrar la ventana
                pass
        try:
            self.root.destroy()
        except Exception:
            pass

    def _on_search_text_changed(self):
        if self.on_search_change:
            try:
                self.on_search_change(self.search_var.get())
            except Exception:
                pass

    def _on_filter_selected(self, value: str):
        if self.on_filter_change:
            try:
                self.on_filter_change(value)
            except Exception:
                pass

    def _on_toggle_autosave(self):
        if self.on_toggle_autosave:
            try:
                self.on_toggle_autosave(self.autosave_var.get())
            except Exception:
                pass


    def actualizar_lista_usuarios(self, usuarios: List[Usuario], on_seleccionar_callback: Callable[[int], None], on_double_click_callback: Optional[Callable[[int], None]] = None):
        """Rellena el CTkScrollableFrame con botones para cada usuario.
        Cada botón llama al callback pasado con el índice del usuario.
        """
        # limpiar contenido previo
        for child in self.lista_usuarios_scrollable.winfo_children():
            child.destroy()

        for i, usuario in enumerate(usuarios):
            btn = ctk.CTkButton(
                self.lista_usuarios_scrollable,
                text=usuario.nombre,
                command=lambda idx=i: on_seleccionar_callback(idx),
            )
            # bind doble clic si nos dieron el callback
            if on_double_click_callback:
                try:
                    btn.bind("<Double-Button-1>", lambda e, idx=i: on_double_click_callback(idx))
                except Exception:
                    # algunos widgets podrían no soportar bind en ciertas versiones, ignorar
                    pass
            btn.pack(fill="x", padx=5, pady=2)

    def mostrar_detalles_usuario(self, usuario: Optional[Usuario]):
        """Actualiza los CTkLabel con los datos del usuario."""
        if usuario is None:
            self.lbl_nombre.configure(text="Nombre: -")
            self.lbl_edad.configure(text="Edad: -")
            self.lbl_genero.configure(text="Género: -")
            self.lbl_avatar.configure(text="Avatar: -")
            return

        self.lbl_nombre.configure(text=f"Nombre: {usuario.nombre}")
        self.lbl_edad.configure(text=f"Edad: {usuario.edad}")
        self.lbl_genero.configure(text=f"Género: {usuario.genero}")
        self.lbl_avatar.configure(text=f"Avatar: {usuario.avatar or '-'}")

    def set_status(self, message: str):
        """Actualiza la barra de estado (izquierda)."""
        try:
            self.status_var.set(message)
        except Exception:
            pass


class AddUserView:
    """Ventana modal para añadir un nuevo usuario."""

    def __init__(self, master, usuario: Optional[Usuario] = None):
        self.window = ctk.CTkToplevel(master)
        self.window.title("Añadir Nuevo Usuario" if usuario is None else "Editar Usuario")
        self.window.geometry("320x300")
        self.window.grab_set()  # la hace modal

        # campos
        ctk.CTkLabel(self.window, text="Nombre:").pack(anchor="w", padx=8, pady=(8, 2))
        self.nombre_entry = ctk.CTkEntry(self.window)
        self.nombre_entry.pack(fill="x", padx=8, pady=(0, 8))

        ctk.CTkLabel(self.window, text="Edad:").pack(anchor="w", padx=8, pady=(0, 2))
        self.edad_entry = ctk.CTkEntry(self.window)
        self.edad_entry.pack(fill="x", padx=8, pady=(0, 8))

        ctk.CTkLabel(self.window, text="Género:").pack(anchor="w", padx=8, pady=(0, 2))
        self.genero_entry = ctk.CTkEntry(self.window)
        self.genero_entry.pack(fill="x", padx=8, pady=(0, 8))

        ctk.CTkLabel(self.window, text="Avatar (nombre de archivo en assets/):").pack(anchor="w", padx=8, pady=(0, 2))
        self.avatar_entry = ctk.CTkEntry(self.window)
        self.avatar_entry.pack(fill="x", padx=8, pady=(0, 8))

        # botones
        self.guardar_button = ctk.CTkButton(self.window, text="Guardar")
        self.guardar_button.pack(side="right", padx=8, pady=12)

        self.cancelar_button = ctk.CTkButton(self.window, text="Cancelar", command=self.window.destroy)
        self.cancelar_button.pack(side="right", padx=(0, 8), pady=12)

        # si nos pasaron un usuario, prefilling
        if usuario is not None:
            try:
                self.nombre_entry.insert(0, usuario.nombre)
                self.edad_entry.insert(0, str(usuario.edad))
                self.genero_entry.insert(0, usuario.genero)
                if usuario.avatar:
                    self.avatar_entry.insert(0, usuario.avatar)
                self.guardar_button.configure(text="Actualizar")
            except Exception:
                pass

    def get_data(self) -> dict:
        """Devuelve los valores del formulario como dict."""
        return {
            "nombre": self.nombre_entry.get().strip(),
            "edad": self.edad_entry.get().strip(),
            "genero": self.genero_entry.get().strip(),
            "avatar": self.avatar_entry.get().strip(),
        }



