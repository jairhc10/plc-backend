from flask import Blueprint, request, jsonify
from core.database.connection import db
from .repository import ReporteHornosRepository
from .service import ReporteHornosService

reportes_bp = Blueprint('reportes', __name__, url_prefix='/api/reportes')

@reportes_bp.route('/hornos', methods=['POST'])
def obtener_reporte_hornos():
    """
    POST /api/reportes/hornos
    Body JSON:
    {
        "fecha_desde": "2026-01-01",
        "fecha_hasta": "2026-01-31",
        "numero_ot": "OT-12345"
    }
    """
    try:
        # Obtener parámetros del body JSON
        data = request.get_json()
        
        fecha_desde = data.get('fecha_desde') if data else None
        fecha_hasta = data.get('fecha_hasta') if data else None
        numero_ot = data.get('numero_ot') if data else None
        
        # Obtener conexión
        with db.get_connection() as conn:
            # Crear repository y service
            repository = ReporteHornosRepository(conn)
            service = ReporteHornosService(repository)
            
            # Generar reporte
            resultado = service.generar_reporte(
                fecha_desde=fecha_desde,
                fecha_hasta=fecha_hasta,
                numero_ot=numero_ot
            )
            
            return jsonify(resultado), 200
            
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": f"Error en formato de fecha: {str(e)}"
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500