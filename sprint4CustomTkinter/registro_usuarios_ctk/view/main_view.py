import customtkinter as ctk
from typing import Callable, Optional, List
from registro_usuarios_ctk.model.usuario_model import Usuario


class MainView:
    """Vista principal: grid de 2 columnas con lista a la izquierda y detalles a la derecha."""

    def __init__(self, root):
        self.root = root
        # callbacks que el controlador asignará
        self.on_seleccionar_usuario: Optional[Callable[[int], None]] = None

        # configurar grid
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=2)
        root.grid_rowconfigure(0, weight=1)

        # panel izquierdo: lista scrollable
        self.lista_usuarios_frame = ctk.CTkFrame(root)
        self.lista_usuarios_frame.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)

        # título para la lista
        self.lbl_usuarios_title = ctk.CTkLabel(self.lista_usuarios_frame, text="Usuarios", font=("Arial", 14, "bold"))
        self.lbl_usuarios_title.pack(anchor="nw", padx=4, pady=(2, 6))

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

    def actualizar_lista_usuarios(self, usuarios: List[Usuario], on_seleccionar_callback: Callable[[int], None]):
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
