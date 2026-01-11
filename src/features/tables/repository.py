#ACCESO A DATOS
"""
Repositorio: Capa de acceso a datos para tablas
"""
from typing import List, Dict
from sqlalchemy import text
from core.database.connection import db
from core.exceptions.custom_exceptions import DatabaseException

class TablesRepository:
    """Maneja las operaciones de base de datos para tablas"""
    
    def get_all_tables(self) -> List[str]:
        """
        Obtener lista de todas las tablas de la BD
        
        Returns:
            List[str]: Nombres de las tablas
        """
        try:
            with db.get_connection() as conn:
                query = text("""
                    SELECT TABLE_NAME 
                    FROM INFORMATION_SCHEMA.TABLES 
                    WHERE TABLE_TYPE = 'BASE TABLE'
                    ORDER BY TABLE_NAME
                """)
                result = conn.execute(query)
                return [row[0] for row in result]
        
        except Exception as e:
            raise DatabaseException(f"Error al obtener tablas: {str(e)}")
    
    def get_table_structure(self, table_name: str) -> List[Dict]:
        """
        Obtener estructura (columnas) de una tabla
        
        Args:
            table_name: Nombre de la tabla
            
        Returns:
            List[Dict]: Información de cada columna
        """
        try:
            with db.get_connection() as conn:
                query = text("""
                    SELECT 
                        COLUMN_NAME,
                        DATA_TYPE,
                        CHARACTER_MAXIMUM_LENGTH,
                        IS_NULLABLE,
                        COLUMN_DEFAULT
                    FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE TABLE_NAME = :table_name
                    ORDER BY ORDINAL_POSITION
                """)
                result = conn.execute(query, {"table_name": table_name})
                
                columns = []
                for row in result:
                    columns.append({
                        "name": row[0],
                        "type": row[1],
                        "max_length": row[2],
                        "nullable": row[3] == "YES",
                        "default": row[4]
                    })
                
                return columns
        
        except Exception as e:
            raise DatabaseException(f"Error al obtener estructura: {str(e)}")
    
    def count_records(self, table_name: str) -> int:
        """
        Contar registros de una tabla
        
        Args:
            table_name: Nombre de la tabla
            
        Returns:
            int: Total de registros
        """
        try:
            with db.get_connection() as conn:
                query = text(f"SELECT COUNT(*) FROM [{table_name}]")
                return conn.execute(query).scalar()
        
        except Exception as e:
            raise DatabaseException(f"Error al contar registros: {str(e)}")
    
    def get_table_data(
        self, 
        table_name: str, 
        limit: int = 100, 
        offset: int = 0
    ) -> tuple:
        """
        Obtener datos de una tabla con paginación
        
        Args:
            table_name: Nombre de la tabla
            limit: Número de registros a retornar
            offset: Desde qué registro empezar
            
        Returns:
            tuple: (columnas, datos)
        """
        try:
            with db.get_connection() as conn:
                query = text(f"""
                    SELECT * FROM [{table_name}]
                    ORDER BY (SELECT NULL)
                    OFFSET :offset ROWS
                    FETCH NEXT :limit ROWS ONLY
                """)
                result = conn.execute(query, {"offset": offset, "limit": limit})
                
                columns = list(result.keys())
                rows = result.fetchall()
                
                return columns, rows
        
        except Exception as e:
            raise DatabaseException(f"Error al obtener datos: {str(e)}")
        
