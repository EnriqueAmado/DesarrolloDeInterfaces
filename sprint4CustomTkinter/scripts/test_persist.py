from pathlib import Path
import sys
# add project root to sys.path so imports work when running this script
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from registro_usuarios_ctk.model.usuario_model import GestorUsuarios

p = PROJECT_ROOT / 'data' / 'test_users.csv'
print('CSV path:', p)

g = GestorUsuarios()
print('Initial count:', len(g.listar()))
for u in g.listar():
    print('-', u)

# Save
print('Saving to CSV...')
g.guardar_csv(p)
print('Saved.')

# Load into a fresh gestor
g2 = GestorUsuarios()
print('Before load, count g2:', len(g2.listar()))
print('Loading from CSV...')
g2.cargar_csv(p)
print('After load, count g2:', len(g2.listar()))
for u in g2.listar():
    print('Loaded -', u)
