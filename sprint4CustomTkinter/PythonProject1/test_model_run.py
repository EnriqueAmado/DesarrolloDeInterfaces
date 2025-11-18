from registro_usuarios_ctk.model.usuario_model import GestorUsuarios

if __name__ == '__main__':
    g = GestorUsuarios()
    for i, u in enumerate(g.listar()):
        print(i, u.to_dict())

