"""
Punto de entrada de la aplicación
"""
import sys
from pathlib import Path

# Agregar src/ al path de Python
src_path = Path(__file__).parent
sys.path.insert(0, str(src_path))

from api.app import create_app
from config.settings import settings

# Validar configuración antes de iniciar
try:
    settings.validate()
except ValueError as e:
    print(f"\n{e}\n")
    print("Por favor, configura tu archivo .env correctamente")
    exit(1)

# Crear aplicación
app = create_app()

if __name__ == '__main__':
    print("\n" + "="*60)
    print("INICIANDO BACKEND FLASK")
    print("="*60)
    print(f"Base de Datos: {settings.DB_NAME}")
    print(f"Servidor: {settings.DB_SERVER}")
    print(f"Puerto: {settings.FLASK_PORT}")
    print(f"Debug: {settings.FLASK_DEBUG}")
    print("="*60 + "\n")
    
    app.run(
        debug=settings.FLASK_DEBUG,
        host='0.0.0.0',
        port=settings.FLASK_PORT
    )