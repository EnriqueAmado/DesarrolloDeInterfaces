# -*- coding: utf-8 -*-
from registro_usuarios_ctk.model.usuario_model import GestorUsuarios, Usuario
from registro_usuarios_ctk.view.main_view import MainView, AddUserView
from pathlib import Path
from tkinter import messagebox, PhotoImage


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

        # hook exit handler
        self.view.on_exit = self.on_exit

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
        """Get users from model and update the view with selection callback."""
        usuarios = self.gestor.listar()
        self.view.actualizar_lista_usuarios(usuarios, self.seleccionar_usuario)

    def seleccionar_usuario(self, indice: int):
        """Callback from view with index of selected user."""
        usuarios = self.gestor.listar()
        try:
            usuario = usuarios[indice]
        except Exception:
            # index invalid: show empty details
            self.view.mostrar_detalles_usuario(None)
            return

        # try to load avatar if provided
        if usuario.avatar:
            avatar_path = (self.ASSETS_PATH / usuario.avatar).resolve()
            if avatar_path.exists():
                try:
                    img = PhotoImage(file=str(avatar_path))
                    # keep reference
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
            # remove previous image and show default text
            try:
                self.view.lbl_avatar.configure(image="", text="Avatar: -")
            except Exception:
                self.view.lbl_avatar.configure(text="Avatar: -")

        # finally show details (text labels)
        self.view.mostrar_detalles_usuario(usuario)

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

    def on_exit(self):
        if messagebox.askokcancel("Exit", "Do you want to exit the application?"):
            try:
                self.root.destroy()
            except Exception:
                pass

    def guardar_usuarios(self):
        try:
            self.gestor.guardar_csv(self.CSV_PATH)
            messagebox.showinfo("Saved", f"Users saved to {self.CSV_PATH}")
        except Exception as e:
            messagebox.showerror("Save error", str(e))

    def cargar_usuarios(self):
        try:
            self.gestor.cargar_csv(self.CSV_PATH)
            self.refrescar_lista_usuarios()
            messagebox.showinfo("Loaded", f"Users loaded from {self.CSV_PATH}")
        except Exception as e:
            messagebox.showerror("Load error", str(e))
