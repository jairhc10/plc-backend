#LOGICA DE NEGOCIO
"""
Servicio: Lógica de negocio para tablas
"""
from typing import Dict
from features.tables.repository import TablesRepository
from shared.utils.validators import SQLValidator
from shared.utils.data_converter import DataConverter
from core.exceptions.custom_exceptions import NotFoundException

class TablesService:
    """Servicio que maneja la lógica de negocio de tablas"""
    
    def __init__(self):
        self.repository = TablesRepository()
    
    def list_tables(self) -> Dict:
        """
        Listar todas las tablas
        
        Returns:
            Dict: Información de tablas
        """
        tables = self.repository.get_all_tables()
        
        return {
            "total": len(tables),
            "tables": tables
        }
    
    def get_table_info(self, table_name: str) -> Dict:
        """
        Obtener información completa de una tabla
        
        Args:
            table_name: Nombre de la tabla
            
        Returns:
            Dict: Información detallada
        """
        # Validar nombre
        table_name = SQLValidator.validate_table_name(table_name)
        
        # Verificar que existe
        all_tables = self.repository.get_all_tables()
        if table_name not in all_tables:
            raise NotFoundException(f"tabla '{table_name}'")
        
        # Obtener información
        structure = self.repository.get_table_structure(table_name)
        total_records = self.repository.count_records(table_name)
        
        return {
            "table_name": table_name,
            "total_records": total_records,
            "total_columns": len(structure),
            "columns": structure
        }
    
    def get_table_data(
        self, 
        table_name: str, 
        limit: int = 100, 
        offset: int = 0
    ) -> Dict:
        """
        Obtener datos de una tabla
        
        Args:
            table_name: Nombre de la tabla
            limit: Registros por página
            offset: Desde qué registro
            
        Returns:
            Dict: Datos de la tabla
        """
        # Validar
        table_name = SQLValidator.validate_table_name(table_name)
        
        # Verificar existencia
        all_tables = self.repository.get_all_tables()
        if table_name not in all_tables:
            raise NotFoundException(f"tabla '{table_name}'")
        
        # Obtener datos
        columns, rows = self.repository.get_table_data(table_name, limit, offset)
        total = self.repository.count_records(table_name)
        
        # Convertir a diccionarios
        data = DataConverter.rows_to_dict_list(rows, columns)
        
        return {
            "table_name": table_name,
            "total_records": total,
            "showing": len(data),
            "offset": offset,
            "limit": limit,
            "columns": columns,
            "data": data
        }