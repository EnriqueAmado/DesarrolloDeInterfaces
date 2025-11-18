from registro_usuarios_ctk.model.usuario_model import GestorUsuarios
from registro_usuarios_ctk.view.main_view import MainView


class AppController:
    def __init__(self, root):
        self.root = root
        self.gestor = GestorUsuarios()
        self.view = MainView(root)

        # inicializar lista en la vista
        self.refrescar_lista_usuarios()

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
        self.view.mostrar_detalles_usuario(usuario)
