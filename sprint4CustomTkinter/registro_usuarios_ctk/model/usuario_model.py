from __future__ import annotations

from typing import List, Optional


class Usuario:
    """Clase simple que representa un usuario con nombre, edad, genero y avatar."""

    def __init__(self, nombre: str, edad: int, genero: str, avatar: Optional[str] = None):
        self.nombre = nombre
        self.edad = edad
        self.genero = genero
        self.avatar = avatar

    def __repr__(self):
        return f"Usuario(nombre={self.nombre!r}, edad={self.edad!r}, genero={self.genero!r}, avatar={self.avatar!r})"


class GestorUsuarios:
    """Gestor sencillo que mantiene una lista de usuarios y carga datos de ejemplo."""

    def __init__(self):
        self._usuarios: List[Usuario] = []
        self._cargar_datos_de_ejemplo()

    def _cargar_datos_de_ejemplo(self) -> None:
        # Añadir 3 usuarios de ejemplo
        self._usuarios.append(Usuario("Alicia", 30, "Femenino", "avatar1.png"))
        self._usuarios.append(Usuario("Bruno", 25, "Masculino", "avatar2.png"))
        self._usuarios.append(Usuario("Carla", 28, "Femenino", None))

    def listar(self) -> List[Usuario]:
        """Devuelve la lista de usuarios."""
        return list(self._usuarios)
