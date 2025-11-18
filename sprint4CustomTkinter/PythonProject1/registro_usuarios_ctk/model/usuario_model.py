class Usuario:
    """Modelo simple de Usuario con nombre, edad, genero y avatar."""
    def __init__(self, nombre: str, edad=None, genero=None, avatar=None):
        if not nombre or not str(nombre).strip():
            raise ValueError("El nombre no puede estar vacío")
        self.nombre = str(nombre).strip()
        try:
            self.edad = int(edad) if edad is not None and edad != "" else None
        except ValueError:
            raise ValueError("La edad debe ser un número entero")
        self.genero = str(genero).strip() if genero is not None else None
        self.avatar = str(avatar) if avatar else None

    def __repr__(self):
        return f"Usuario(nombre={self.nombre!r}, edad={self.edad!r}, genero={self.genero!r}, avatar={self.avatar!r})"

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "edad": self.edad,
            "genero": self.genero,
            "avatar": self.avatar,
        }

    @classmethod
    def from_dict(cls, d: dict):
        return cls(nombre=d.get("nombre"), edad=d.get("edad"), genero=d.get("genero"), avatar=d.get("avatar"))


class GestorUsuarios:
    """Gestor sencillo de usuarios en memoria con datos de ejemplo."""
    def __init__(self):
        self._usuarios = []
        self._cargar_datos_de_ejemplo()

    def _cargar_datos_de_ejemplo(self):
        """Añade 2-3 usuarios de ejemplo a la lista interna."""
        u1 = Usuario(nombre="Ana Pérez", edad=28, genero="F", avatar=None)
        u2 = Usuario(nombre="Miguel López", edad=34, genero="M", avatar=None)
        u3 = Usuario(nombre="Carla Ruiz", edad=22, genero="F", avatar=None)
        self._usuarios.extend([u1, u2, u3])

    def listar(self):
        """Devuelve la lista de usuarios (referencia a la lista interna).

        Si se desea evitar modificación externa, devolver una copia: list(self._usuarios)
        """
        return list(self._usuarios)

    def obtener_por_indice(self, idx: int):
        try:
            return self._usuarios[idx]
        except Exception:
            return None
