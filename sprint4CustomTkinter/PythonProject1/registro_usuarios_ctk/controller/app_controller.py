from registro_usuarios_ctk.model.usuario_model import GestorUsuarios

# Intentamos importar la vista; si falla (entorno sin GUI) la dejaremos como None
try:
    from registro_usuarios_ctk.view.main_view import MainView
except Exception:
    MainView = None


class AppController:
    def __init__(self, root):
        """Controlador que orquesta Modelo <-> Vista.

        Crea el modelo y, si es posible, la vista. Después actualiza la lista
        inicial en la vista llamando a `refrescar_lista_usuarios`.
        """
        self.root = root
        # Modelo
        self.model = GestorUsuarios()
        # Vista (puede ser None si no hay entorno GUI)
        self.view = None

        if MainView is not None:
            try:
                self.view = MainView(root, controller=self)
            except Exception:
                # Si la vista falla al inicializar, nos quedamos sin ella pero el
                # controlador sigue funcionando en modo no-GUI.
                self.view = None

        # Llamada inicial para poblar la lista (si la vista existe se actualizará)
        try:
            self.refrescar_lista_usuarios()
        except Exception:
            # No queremos que errores en la vista impidan que el controlador
            # funcione en modo de pruebas o headless.
            pass

    def refrescar_lista_usuarios(self):
        """Devuelve la lista de usuarios y actualiza la vista si existe.

        Returns:
            list: lista de objetos Usuario.
        """
        usuarios = self.model.listar()
        if self.view:
            try:
                # La vista espera recibir la lista y un callback para selección
                self.view.actualizar_lista_usuarios(usuarios, self.seleccionar_usuario)
            except Exception:
                # No propagamos errores de la vista
                pass
        return usuarios

    def seleccionar_usuario(self, indice: int):
        """Callback: recibe índice, solicita el usuario al modelo y pide a la
        vista que muestre los detalles del usuario seleccionado.
        """
        try:
            usuario_seleccionado = self.model.obtener_por_indice(indice)
        except Exception:
            usuario_seleccionado = None

        if self.view:
            try:
                self.view.mostrar_detalles_usuario(usuario_seleccionado)
            except Exception:
                pass

        return usuario_seleccionado

    # Helpers / compatibility aliases para pruebas
    def handle_listar(self):
        """Alias para compatibilidad: devuelve la lista y actualiza la vista si existe."""
        return self.refrescar_lista_usuarios()

    def handle_seleccionar(self, idx: int):
        """Alias para compatibilidad: selecciona y muestra detalles."""
        return self.seleccionar_usuario(idx)
