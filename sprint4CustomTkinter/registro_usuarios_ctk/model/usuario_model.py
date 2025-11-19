from __future__ import annotations

from typing import List, Optional
from pathlib import Path
import csv


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

    def add(self, usuario: Usuario) -> None:
        """Añade un nuevo usuario a la lista."""
        self._usuarios.append(usuario)

    def get(self, index: int) -> Optional[Usuario]:
        if 0 <= index < len(self._usuarios):
            return self._usuarios[index]
        return None

    def remove(self, index: int) -> bool:
        """Elimina el usuario en la posición index. Devuelve True si se eliminó, False si no existe."""
        if 0 <= index < len(self._usuarios):
            del self._usuarios[index]
            return True
        return False

    def guardar_csv(self, path: Path) -> None:
        """Guarda los usuarios en CSV en la ruta indicada.
        Formato de columnas: nombre,edad,genero,avatar
        """
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["nombre", "edad", "genero", "avatar"])
            for u in self._usuarios:
                writer.writerow([u.nombre, str(u.edad), u.genero or "", u.avatar or ""])

    def cargar_csv(self, path: Path) -> None:
        """Carga usuarios desde un CSV. Si no existe el archivo, no lanza excepción.
        Ignora filas corruptas pero continúa procesando el resto.
        """
        if not path.exists():
            # No hay archivo: mantén la lista tal cual (o limpia si prefieres)
            return
        try:
            with path.open("r", encoding="utf-8", newline="") as f:
                reader = csv.reader(f)
                try:
                    header = next(reader)
                except StopIteration:
                    return
                # limpiar lista actual
                self._usuarios.clear()
                for row in reader:
                    try:
                        if not row or len(row) < 3:
                            continue
                        nombre = row[0].strip()
                        edad = int(row[1]) if row[1].strip() else 0
                        genero = row[2].strip() if len(row) > 2 else ""
                        avatar = row[3].strip() if len(row) > 3 and row[3].strip() else None
                        self._usuarios.append(Usuario(nombre, edad, genero, avatar))
                    except Exception:
                        # fila corrupta: ignorar y continuar
                        continue
        except FileNotFoundError:
            # si no existe, no hacemos nada
            return
