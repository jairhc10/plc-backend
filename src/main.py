"""
Punto de entrada de la aplicación
"""
import sys
from pathlib import Path
import socket

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
    app = create_app()
    
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print("\n" + "="*70)
    print("🔥 BACKEND FLASK - SISTEMA MODEPSA")
    print("="*70)
    print(f"🌐 Local:    http://localhost:5000")
    print(f"🌐 Red:      http://{local_ip}:5000")
    print(f"🔍 Health:   http://{local_ip}:5000/health")
    print(f"🧪 Test DB:  http://{local_ip}:5000/test-db")
    print("="*70)
    print("✅ Presiona Ctrl+C para detener\n")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )