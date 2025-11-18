import customtkinter as ctk

class MainView(ctk.CTkFrame):
    def __init__(self, master, controller=None):
        super().__init__(master)
        self.master = master
        self.controller = controller
        self.grid(row=0, column=0, sticky="nsew")

        # Configurar grid del master para que la vista se expanda
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)

        # Layout interior: 2 columnas
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Columna izquierda: lista scrollable
        self.lista_frame = ctk.CTkScrollableFrame(self, width=300)
        self.lista_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Encabezado para la lista de usuarios
        # Usamos un font básico; si el sistema no soporta la tupla, CTkLabel la ignorará.
        try:
            encabezado_font = ("Arial", 14, "bold")
        except Exception:
            encabezado_font = None
        self.label_usuarios = ctk.CTkLabel(self.lista_frame, text="Usuarios", font=encabezado_font)
        self.label_usuarios.pack(anchor="w", padx=5, pady=(0, 8))

        # Contenedor donde se añadirán los botones de usuarios
        self.lista_usuarios_container = ctk.CTkFrame(self.lista_frame)
        self.lista_usuarios_container.pack(fill="both", expand=True, padx=5, pady=5)

        # Columna derecha: detalles
        self.detalles_frame = ctk.CTkFrame(self)
        self.detalles_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Encabezado para la sección de detalles
        self.label_detalles_titulo = ctk.CTkLabel(self.detalles_frame, text="Detalles del Usuario", font=encabezado_font)
        self.label_detalles_titulo.pack(anchor="w", pady=(0, 8))

        self.label_nombre = ctk.CTkLabel(self.detalles_frame, text="Nombre: ")
        self.label_edad = ctk.CTkLabel(self.detalles_frame, text="Edad: ")
        self.label_genero = ctk.CTkLabel(self.detalles_frame, text="Género: ")
        self.label_avatar = ctk.CTkLabel(self.detalles_frame, text="Avatar: ")

        self.label_nombre.pack(anchor="w", pady=5)
        self.label_edad.pack(anchor="w", pady=5)
        self.label_genero.pack(anchor="w", pady=5)
        self.label_avatar.pack(anchor="w", pady=5)

    def actualizar_lista_usuarios(self, usuarios, on_seleccionar_callback):
        """Actualiza la lista de usuarios en el scrollable frame.

        usuarios: lista de objetos Usuario o dicts con al menos `nombre`.
        on_seleccionar_callback: función que recibe el índice y realiza la acción.
        """
        # Limpiar contenedor actual
        for child in self.lista_usuarios_container.winfo_children():
            child.destroy()

        for i, usuario in enumerate(usuarios):
            nombre = getattr(usuario, "nombre", str(usuario))
            btn = ctk.CTkButton(
                self.lista_usuarios_container,
                text=nombre,
                command=lambda idx=i: on_seleccionar_callback(idx)
            )
            btn.pack(fill="x", padx=5, pady=2)

    def mostrar_detalles_usuario(self, usuario):
        """Actualiza los labels de detalle con la información del usuario.

        Si `usuario` es None limpiará los labels.
        """
        if not usuario:
            self.label_nombre.configure(text="Nombre: ")
            self.label_edad.configure(text="Edad: ")
            self.label_genero.configure(text="Género: ")
            self.label_avatar.configure(text="Avatar: ")
            return

        nombre = getattr(usuario, "nombre", "")
        edad = getattr(usuario, "edad", "")
        genero = getattr(usuario, "genero", "")
        avatar = getattr(usuario, "avatar", "")

        self.label_nombre.configure(text=f"Nombre: {nombre}")
        self.label_edad.configure(text=f"Edad: {edad}")
        self.label_genero.configure(text=f"Género: {genero}")
        self.label_avatar.configure(text=f"Avatar: {avatar}")
