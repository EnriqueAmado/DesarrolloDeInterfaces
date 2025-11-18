print('DEBUG: iniciando test_simple_ctrl')
from registro_usuarios_ctk.controller.app_controller import AppController

if __name__ == '__main__':
    print('DEBUG: antes de instanciar AppController', flush=True)
    ctrl = AppController(root=None)
    print('DEBUG: controlador instanciado:', type(ctrl), flush=True)
    usuarios = ctrl.refrescar_lista_usuarios()
    print('Número de usuarios en el modelo:', len(usuarios), flush=True)
    for u in usuarios:
        print('-', u, flush=True)
