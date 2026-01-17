from flask import Blueprint, request, jsonify
# from flask_jwt_extended import jwt_required
from core.database.connection import db
from .repository import ReporteHornosRepository
from .service import ReporteHornosService

reportes_bp = Blueprint('reportes', __name__, url_prefix='/api/reportes')

@reportes_bp.route('/hornos', methods=['GET', 'POST'])
# @jwt_required()
def obtener_reporte_hornos():
    """
    GET /api/reportes/hornos?fecha_desde=2025-01-01&fecha_hasta=2026-01-31&numero_ot=OT-12345
    POST /api/reportes/hornos
    Body JSON:
    {
        "fecha_desde": "2026-01-01",
        "fecha_hasta": "2026-01-31",
        "numero_ot": "OT-12345"
    }
    """
    try:
        # Determinar si es GET o POST y obtener parámetros
        if request.method == 'GET':
            # Obtener parámetros de query string
            fecha_desde = request.args.get('fecha_desde')
            fecha_hasta = request.args.get('fecha_hasta')
            numero_ot = request.args.get('numero_ot')
        else:  # POST
            # Verificar si hay JSON en el body
            if request.is_json:
                data = request.get_json()
                fecha_desde = data.get('fecha_desde')
                fecha_hasta = data.get('fecha_hasta')
                numero_ot = data.get('numero_ot')
            else:
                # Fallback a query params si no hay JSON
                fecha_desde = request.args.get('fecha_desde')
                fecha_hasta = request.args.get('fecha_hasta')
                numero_ot = request.args.get('numero_ot')
        
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
