# -*- coding: utf-8 -*-
from registro_usuarios_ctk.model.usuario_model import GestorUsuarios, Usuario
from registro_usuarios_ctk.view.main_view import MainView, AddUserView
from pathlib import Path
from tkinter import messagebox, PhotoImage
import threading
import time


class AppController:
    def __init__(self, root):
        self.root = root
        self.gestor = GestorUsuarios()
        self.view = MainView(root)

        # base dir and assets folder
        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.ASSETS_PATH = self.BASE_DIR / "assets"

        # image cache to keep PhotoImage references
        self.avatar_images = {}

        # state for filtering/search
        self.current_search = ""
        self.current_filter = "Todos"
        self._filtered_indexes = []  # mapea índice visible -> índice en gestor

        # autosave thread control
        self._autosave_thread = None
        self._autosave_stop_event = threading.Event()
        self.autosave_interval = 10  # segundos
        self.autosave_running = False

        # hook exit handler
        self.view.on_exit = self.on_exit

        # connect callbacks from view
        self.view.on_search_change = self.on_search_change
        self.view.on_filter_change = self.on_filter_change
        # conectar toggle auto-guardado si la vista lo expone
        try:
            self.view.on_toggle_autosave = self.toggle_autosave
        except Exception:
            pass

        # initial population
        self.refrescar_lista_usuarios()

        # connect add button
        try:
            self.view.btn_anadir.configure(command=self.abrir_ventana_añadir)
        except Exception:
            pass

        # connect File menu commands
        try:
            self.CSV_PATH = self.BASE_DIR / "data" / "users.csv"
            # Spanish labels: first 'Cargar' then 'Guardar', plus a separator and 'Salir'
            self.view.menu_archivo.add_command(label="Cargar", command=self.cargar_usuarios)
            self.view.menu_archivo.add_command(label="Guardar", command=self.guardar_usuarios)
            self.view.menu_archivo.add_separator()
            self.view.menu_archivo.add_command(label="Salir", command=self.on_exit)
        except Exception:
            pass

        # attempt initial load
        try:
            self.cargar_usuarios()
        except Exception:
            pass

    def refrescar_lista_usuarios(self):
        """Get users from model, apply filters, and update the view with callbacks."""
        usuarios = self.gestor.listar()

        # apply search and filter to build a visible list and mapping
        visible = []
        self._filtered_indexes = []
        s = self.current_search.strip().lower()
        f = self.current_filter
        for idx, u in enumerate(usuarios):
            if f != "Todos" and u.genero and u.genero.lower() != f.lower():
                continue
            if s and s not in u.nombre.lower():
                continue
            visible.append(u)
            self._filtered_indexes.append(idx)

        # update status with counts
        self.view.set_status(f"Mostrando {len(visible)} de {len(usuarios)} usuarios")

        # pass the visible list and callbacks; double click maps visible index -> real index
        self.view.actualizar_lista_usuarios(visible, self.seleccionar_usuario_visible, self.editar_usuario_visible)

    def seleccionar_usuario_visible(self, visible_index: int):
        """Cuando la vista pasa un índice visible, lo convertimos al índice real y mostramos detalles."""
        try:
            real_idx = self._filtered_indexes[visible_index]
        except Exception:
            self.view.mostrar_detalles_usuario(None)
            return
        usuario = self.gestor.get(real_idx)
        if usuario is None:
            self.view.mostrar_detalles_usuario(None)
            return

        # cargar avatar similar a antes
        if usuario.avatar:
            avatar_path = (self.ASSETS_PATH / usuario.avatar).resolve()
            if avatar_path.exists():
                try:
                    img = PhotoImage(file=str(avatar_path))
                    self.avatar_images[usuario.avatar] = img
                    try:
                        self.view.lbl_avatar.configure(image=img, text="")
                    except Exception:
                        self.view.lbl_avatar.configure(text=f"Avatar: {usuario.avatar}")
                except Exception:
                    self.view.lbl_avatar.configure(text=f"Avatar: {usuario.avatar} (could not load)")
            else:
                self.view.lbl_avatar.configure(text=f"Avatar: {usuario.avatar} (not found)")
        else:
            try:
                self.view.lbl_avatar.configure(image="", text="Avatar: -")
            except Exception:
                self.view.lbl_avatar.configure(text="Avatar: -")

        # finally show details
        self.view.mostrar_detalles_usuario(usuario)

    def editar_usuario_visible(self, visible_index: int):
        """Abre modal de edición para el usuario visible, actualiza en el modelo y refresca."""
        try:
            real_idx = self._filtered_indexes[visible_index]
        except Exception:
            return
        usuario = self.gestor.get(real_idx)
        if usuario is None:
            return

        add_view = AddUserView(self.root, usuario=usuario)
        # conectar guardar para actualizar
        def do_update():
            data = add_view.get_data()
            try:
                edad = int(data.get("edad", "0"))
            except ValueError:
                messagebox.showerror("Edad inválida", "La edad debe ser un entero")
                return
            nombre = data.get("nombre")
            genero = data.get("genero")
            avatar = data.get("avatar") or None
            if not nombre:
                messagebox.showerror("Datos incompletos", "El nombre es obligatorio")
                return
            nuevo = Usuario(nombre=nombre, edad=edad, genero=genero, avatar=avatar)
            ok = self.gestor.update(real_idx, nuevo)
            if ok:
                self.view.set_status("Usuario actualizado")
                self.refrescar_lista_usuarios()
                try:
                    add_view.window.destroy()
                except Exception:
                    pass
            else:
                messagebox.showerror("Error", "No se pudo actualizar el usuario")

        add_view.guardar_button.configure(command=do_update)

    def on_search_change(self, text: str):
        self.current_search = text
        self.refrescar_lista_usuarios()

    def on_filter_change(self, value: str):
        self.current_filter = value
        self.refrescar_lista_usuarios()

    def abrir_ventana_añadir(self):
        """Open the AddUser modal and connect save button."""
        add_view = AddUserView(self.root)
        add_view.guardar_button.configure(command=lambda: self.añadir_usuario(add_view))

    def añadir_usuario(self, add_view: AddUserView):
        data = add_view.get_data()
        # validate age
        try:
            edad = int(data.get("edad", "0"))
        except ValueError:
            messagebox.showerror("Invalid age", "Age must be an integer")
            return

        nombre = data.get("nombre")
        genero = data.get("genero")
        avatar = data.get("avatar") or None

        if not nombre:
            messagebox.showerror("Incomplete data", "Name is required")
            return

        # create and add user
        u = Usuario(nombre=nombre, edad=edad, genero=genero, avatar=avatar)
        self.gestor.add(u)

        # refresh view and close modal
        self.refrescar_lista_usuarios()
        try:
            add_view.window.destroy()
        except Exception:
            pass

    def _autosave_loop(self):
        """Función que corre en un hilo y guarda periódicamente el CSV sin bloquear la UI."""
        while not self._autosave_stop_event.wait(self.autosave_interval):
            try:
                self.gestor.guardar_csv(self.CSV_PATH)
            except Exception as e:
                # notificar error en la UI thread
                self.root.after(0, lambda err=e: (messagebox.showerror("Auto-save error", str(err)), self.view.set_status(f"Error auto-guardando: {err}")))
            else:
                # notificar éxito en la UI thread
                self.root.after(0, lambda: self.view.set_status("Auto-guardado: OK"))

    def start_autosave(self):
        if self.autosave_running:
            return
        self._autosave_stop_event.clear()
        self._autosave_thread = threading.Thread(target=self._autosave_loop, daemon=True)
        self._autosave_thread.start()
        self.autosave_running = True
        self.view.set_status("Auto-guardado activado")

    def stop_autosave(self):
        if not self.autosave_running:
            return
        self._autosave_stop_event.set()
        # esperar un corto periodo para que el hilo termine si es necesario
        if self._autosave_thread is not None:
            self._autosave_thread.join(timeout=2)
        self.autosave_running = False
        self.view.set_status("Auto-guardado detenido")

    def toggle_autosave(self, enable: bool = None):
        """Si enable es None, invierte el estado; si es True/False lo aplica explícitamente."""
        if enable is None:
            enable = not self.autosave_running
        if enable:
            self.start_autosave()
        else:
            self.stop_autosave()

    def on_exit(self):
        # detener autosave si está en marcha
        try:
            self.stop_autosave()
        except Exception:
            pass
        if messagebox.askokcancel("Exit", "Do you want to exit the application?"):
            try:
                self.root.destroy()
            except Exception:
                pass

    def guardar_usuarios(self):
        try:
            self.gestor.guardar_csv(self.CSV_PATH)
            messagebox.showinfo("Saved", f"Users saved to {self.CSV_PATH}")
            self.view.set_status("Guardado OK")
        except Exception as e:
            messagebox.showerror("Save error", str(e))
            self.view.set_status(f"Error al guardar: {e}")

    def cargar_usuarios(self):
        try:
            self.gestor.cargar_csv(self.CSV_PATH)
            self.refrescar_lista_usuarios()
            messagebox.showinfo("Loaded", f"Users loaded from {self.CSV_PATH}")
            self.view.set_status("Usuarios cargados")
        except Exception as e:
            messagebox.showerror("Load error", str(e))
            self.view.set_status(f"Error al cargar: {e}")

    def _autosave_loop(self):
        """Hilo que guarda CSV cada self.autosave_interval segundos."""
        while not self._autosave_stop_event.wait(self.autosave_interval):
            try:
                self.gestor.guardar_csv(self.CSV_PATH)
            except Exception as e:
                # informar error en la UI thread
                self.root.after(0, lambda err=e: (
                    messagebox.showerror("Auto-save error", str(err)),
                    self.view.set_status(f"Error auto-guardando: {err}")
                ))
            else:
                self.root.after(0, lambda: self.view.set_status("Auto-guardado: OK"))