from registro_usuarios_ctk.controller.app_controller import AppController

class DummyView:
    def __init__(self):
        self.last_list = None
        self.last_details = None
        self.last_message = None

    def actualizar_lista_usuarios(self, usuarios, callback):
        self.last_list = usuarios
        # Guardamos el callback para poder llamarlo manualmente si hace falta
        self._callback = callback

    def mostrar_detalles_usuario(self, usuario):
        self.last_details = usuario

    def mostrar_mensaje(self, texto, tipo="info"):
        self.last_message = (texto, tipo)

if __name__ == '__main__':
    ctrl = AppController(root=None)
    dummy = DummyView()
    ctrl.set_view(dummy)

    # Listar
    usuarios = ctrl.handle_listar()
    print('Usuarios listados (desde controlador):', [u.to_dict() for u in usuarios])
    print('DummyView.last_list length:', len(dummy.last_list) if dummy.last_list else 0)

    # Seleccionar índice 1
    u = ctrl.handle_seleccionar(1)
    print('Usuario seleccionado:', u.to_dict() if u else None)
    print('DummyView.last_details:', dummy.last_details.to_dict() if dummy.last_details else None)

