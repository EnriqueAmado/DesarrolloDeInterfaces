from registro_usuarios_ctk.model.usuario_model import GestorUsuarios, Usuario
from registro_usuarios_ctk.view.main_view import MainView, AddUserView
from pathlib import Path
from tkinter import messagebox, PhotoImage


class AppController:
    def __init__(self, root):
        self.root = root
        self.gestor = GestorUsuarios()
        self.view = MainView(root)

        # carpeta base y assets
        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.ASSETS_PATH = self.BASE_DIR / "assets"

        # caché de imágenes para evitar que la GC las elimine
        self.avatar_images = {}

        # conectar botón salir si queremos manejar confirmación
        self.view.on_exit = self.on_exit

        # inicializar lista en la vista
        self.refrescar_lista_usuarios()

        # conectar botón añadir
        try:
            self.view.btn_anadir.configure(command=self.abrir_ventana_añadir)
        except Exception:
            pass

    def refrescar_lista_usuarios(self):
        """Pide los usuarios al modelo y actualiza la vista, pasando el callback de selección."""
        usuarios = self.gestor.listar()
        # pasar el método seleccionar_usuario como callback
        self.view.actualizar_lista_usuarios(usuarios, self.seleccionar_usuario)

    def seleccionar_usuario(self, indice: int):
        """Callback llamado desde la vista con el índice del usuario seleccionado."""
        usuarios = self.gestor.listar()
        try:
            usuario = usuarios[indice]
        except Exception:
            # índice inválido: mostrar detalles vacíos
            self.view.mostrar_detalles_usuario(None)
            return
        # mostrar detalles y, si tiene avatar, cargar imagen
        if usuario.avatar:
            avatar_path = (self.ASSETS_PATH / usuario.avatar).resolve()
            if avatar_path.exists():
                try:
                    img = PhotoImage(file=str(avatar_path))
                    # mantener referencia
                    self.avatar_images[usuario.avatar] = img
                    # asignar la imagen en la vista (añadir comportamiento en la vista: configure con image)
                    try:
                        self.view.lbl_avatar.configure(image=img, text="")
                    except Exception:
                        # si la vista no soporta image, fallback a texto
                        self.view.lbl_avatar.configure(text=f"Avatar: {usuario.avatar}")
                except Exception:
                    self.view.lbl_avatar.configure(text=f"Avatar: {usuario.avatar} (no se pudo cargar)")
            else:
                self.view.lbl_avatar.configure(text=f"Avatar: {usuario.avatar} (no encontrado)")
        else:
            # eliminar imagen previa y mostrar texto por defecto
            try:
                self.view.lbl_avatar.configure(image="", text="Avatar: -")
            except Exception:
                self.view.lbl_avatar.configure(text="Avatar: -")

        self.view.mostrar_detalles_usuario(usuario)

    def abrir_ventana_añadir(self):
        """Crea y muestra la ventana modal para añadir un usuario, y conecta el botón Guardar."""
        add_view = AddUserView(self.root)
        add_view.guardar_button.configure(command=lambda: self.añadir_usuario(add_view))

    def añadir_usuario(self, add_view: AddUserView):
        data = add_view.get_data()
        # validar edad
        try:
            edad = int(data.get("edad", "0"))
        except ValueError:
            messagebox.showerror("Edad inválida", "La edad debe ser un número entero")
            return

        nombre = data.get("nombre")
        genero = data.get("genero")
        avatar = data.get("avatar") or None

        if not nombre:
            messagebox.showerror("Datos incompletos", "El nombre es obligatorio")
            return

        # crear Usuario y añadir al modelo
        u = Usuario(nombre=nombre, edad=edad, genero=genero, avatar=avatar)
        self.gestor.add(u)

        # refrescar vista
        self.refrescar_lista_usuarios()

        # cerrar modal
        try:
            add_view.window.destroy()
        except Exception:
            pass

    def on_exit(self):
        if messagebox.askokcancel("Salir", "¿Deseas salir de la aplicación?"):
            try:
                self.root.destroy()
            except Exception:
                pass
