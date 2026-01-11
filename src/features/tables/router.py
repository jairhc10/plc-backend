#RUTAS DE TABLAS
"""
Router: Rutas HTTP para tablas
"""
from flask import Blueprint, request
from features.tables.service import TablesService
from shared.responses.response_builder import ResponseBuilder
from core.exceptions.custom_exceptions import AppException

# Crear blueprint
tables_bp = Blueprint('tables', __name__, url_prefix='/api/tables')

# Instanciar servicio
service = TablesService()

@tables_bp.route('/', methods=['GET'])
def list_tables():
    """
    Listar todas las tablas
    
    GET /api/tables/
    
    Response:
        {
            "status": "success",
            "data": {
                "total": 10,
                "tables": ["tabla1", "tabla2", ...]
            }
        }
    """
    try:
        result = service.list_tables()
        return ResponseBuilder.success(
            data=result,
            message="Tablas obtenidas exitosamente"
        )
    
    except AppException as e:
        return ResponseBuilder.error(e.message, e.status_code)
    
    except Exception as e:
        return ResponseBuilder.error(f"Error inesperado: {str(e)}")

@tables_bp.route('/<table_name>', methods=['GET'])
def get_table_info(table_name: str):
    """
    Obtener información de una tabla
    
    GET /api/tables/{table_name}
    
    Response:
        {
            "status": "success",
            "data": {
                "table_name": "Usuarios",
                "total_records": 150,
                "total_columns": 5,
                "columns": [...]
            }
        }
    """
    try:
        result = service.get_table_info(table_name)
        return ResponseBuilder.success(
            data=result,
            message=f"Información de '{table_name}' obtenida"
        )
    
    except AppException as e:
        return ResponseBuilder.error(e.message, e.status_code)
    
    except Exception as e:
        return ResponseBuilder.error(f"Error inesperado: {str(e)}")

@tables_bp.route('/<table_name>/data', methods=['GET'])
def get_table_data(table_name: str):
    """
    Obtener datos de una tabla
    
    GET /api/tables/{table_name}/data?limit=50&offset=0
    
    Query params:
        - limit: Registros por página (default: 100)
        - offset: Desde qué registro (default: 0)
    
    Response:
        {
            "status": "success",
            "data": {
                "table_name": "Usuarios",
                "total_records": 1500,
                "showing": 50,
                "data": [...]
            }
        }
    """
    try:
        # Obtener parámetros
        limit = request.args.get('limit', 100, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        result = service.get_table_data(table_name, limit, offset)
        
        return ResponseBuilder.success(
            data=result,
            message=f"Datos de '{table_name}' obtenidos"
        )
    
    except AppException as e:
        return ResponseBuilder.error(e.message, e.status_code)
    
    except Exception as e:
        return ResponseBuilder.error(f"Error inesperado: {str(e)}")