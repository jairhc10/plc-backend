# GESTION DE LA BASE DE DATOS
"""
Gestión de la conexión a la base de datos
Singleton pattern para manejar una única instancia
"""
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from typing import Generator
from config.database import get_database_url

class DatabaseConnection:
    """Singleton para gestionar la conexión a la base de datos"""
    
    _instance = None
    _engine: Engine = None
    _SessionLocal = None
    
    def __new__(cls):
        """Patrón Singleton - solo una instancia"""
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance
    
    def initialize(self, echo: bool = False):
        """
        Inicializar la conexión a la base de datos
        
        Args:
            echo: Si True, muestra las consultas SQL en consola
        """
        if self._engine is None:
            database_url = get_database_url()
            
            self._engine = create_engine(
                database_url,
                echo=echo,
                pool_pre_ping=True,  # Verifica conexión antes de usar
                pool_size=5,          # Número de conexiones en pool
                max_overflow=10       # Conexiones adicionales permitidas
            )
            
            self._SessionLocal = sessionmaker(
                bind=self._engine,
                autocommit=False,
                autoflush=False
            )
            
            print("✅ Motor de base de datos inicializado")
    
    @property
    def engine(self) -> Engine:
        """Obtener el motor de base de datos"""
        if self._engine is None:
            raise RuntimeError(
                "❌ Database no inicializada. Llama a db.initialize() primero."
            )
        return self._engine
    
    @contextmanager
    def get_connection(self) -> Generator:
        """
        Context manager para obtener una conexión
        
        Uso:
            with db.get_connection() as conn:
                result = conn.execute(query)
        """
        connection = self.engine.connect()
        try:
            yield connection
        finally:
            connection.close()
    
    def test_connection(self) -> dict:
        """
        Probar la conexión a la base de datos
        
        Returns:
            dict: Resultado de la prueba con información del servidor
        """
        try:
            with self.get_connection() as conn:
                # Obtener fecha del servidor
                result = conn.execute(text("SELECT GETDATE() AS fecha"))
                fecha = result.scalar()
                
                # Obtener versión de SQL Server
                result_version = conn.execute(text("SELECT @@VERSION AS version"))
                version = result_version.scalar()
            
            return {
                "success": True,
                "message": "✅ Conexión exitosa a SQL Server",
                "server_time": str(fecha),
                "server_version": version[:100] + "..." if len(version) > 100 else version
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": "❌ Error de conexión",
                "error": str(e)
            }

# Instancia global única
db = DatabaseConnection()