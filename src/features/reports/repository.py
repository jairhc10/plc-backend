from sqlalchemy import text
from typing import Optional, List, Dict, Any
from datetime import date

class ReporteHornosRepository:
    def __init__(self, connection):
        self.connection = connection
    
    def obtener_reporte_hornos(
        self,
        fecha_desde: Optional[date] = None,
        fecha_hasta: Optional[date] = None,
        numero_ot: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Obtiene el reporte de hornos con filtros opcionales
        Incluye la lógica de reinterpretación de fechas con CROSS APPLY
        """
        query = text("""
            SELECT 
                TB.Fecha_Registro,
                TB.Numero_OT, 
                TB.Peso_Unitario,
                TB.Peso_Total,
                TB.Fecha_Fin_Manual,
                TB.Fecha_Fin_Auto,
                TB.Modo_Ingreso_Carga,
                TB.Dureza_1,
                TB.Dureza_2,
                TB.Dureza_3,
                TB.Fecha_Modificacion,
                TB.Usuario,
                -- HORNO 1
                (
                    SELECT TOP 1 TH.Temp_Horno_01
                    FROM TBL_HISTORICO_TEMPERATURAS TH
                    WHERE TH.Fecha_Hora >= CAST(TB.Fecha_Registro AS DATE)
                      AND TH.Fecha_Hora < DATEADD(DAY, 1, CAST(TB.Fecha_Registro AS DATE))
                    ORDER BY TH.Fecha_Hora
                ) AS [TEMPERATURA HORNO1],
                -- HORNO 2
                (
                    SELECT TOP 1 TH.Temp_Horno_02
                    FROM TBL_HISTORICO_TEMPERATURAS TH
                    WHERE TH.Fecha_Hora >= CAST(TB.Fecha_Registro AS DATE)
                      AND TH.Fecha_Hora < DATEADD(DAY, 1, CAST(TB.Fecha_Registro AS DATE))
                    ORDER BY TH.Fecha_Hora
                ) AS [TEMPERATURA HORNO2],
                -- HORNO 3
                (
                    SELECT TOP 1 TH.Temp_Horno_03
                    FROM TBL_HISTORICO_TEMPERATURAS TH
                    WHERE TH.Fecha_Hora >= CAST(TB.Fecha_Registro AS DATE)
                      AND TH.Fecha_Hora < DATEADD(DAY, 1, CAST(TB.Fecha_Registro AS DATE))
                    ORDER BY TH.Fecha_Hora
                ) AS [TEMPERATURA HORNO3],
                -- HORNO 4
                (
                    SELECT TOP 1 TH.Temp_Horno_04
                    FROM TBL_HISTORICO_TEMPERATURAS TH
                    WHERE TH.Fecha_Hora >= CAST(TB.Fecha_Registro AS DATE)
                      AND TH.Fecha_Hora < DATEADD(DAY, 1, CAST(TB.Fecha_Registro AS DATE))
                    ORDER BY TH.Fecha_Hora
                ) AS [TEMPERATURA HORNO4],
                -- HORNO 5
                (
                    SELECT TOP 1 TH.Temp_Horno_05
                    FROM TBL_HISTORICO_TEMPERATURAS TH
                    WHERE TH.Fecha_Hora >= CAST(TB.Fecha_Registro AS DATE)
                      AND TH.Fecha_Hora < DATEADD(DAY, 1, CAST(TB.Fecha_Registro AS DATE))
                    ORDER BY TH.Fecha_Hora
                ) AS [TEMPERATURA HORNO5],
                -- HORNO 6
                (
                    SELECT TOP 1 TH.Temp_Horno_06
                    FROM TBL_HISTORICO_TEMPERATURAS TH
                    WHERE TH.Fecha_Hora >= CAST(TB.Fecha_Registro AS DATE)
                      AND TH.Fecha_Hora < DATEADD(DAY, 1, CAST(TB.Fecha_Registro AS DATE))
                    ORDER BY TH.Fecha_Hora
                ) AS [TEMPERATURA HORNO6],
                -- HORNO 7
                (
                    SELECT TOP 1 TH.Temp_Horno_07
                    FROM TBL_HISTORICO_TEMPERATURAS TH
                    WHERE TH.Fecha_Hora >= CAST(TB.Fecha_Registro AS DATE)
                      AND TH.Fecha_Hora < DATEADD(DAY, 1, CAST(TB.Fecha_Registro AS DATE))
                    ORDER BY TH.Fecha_Hora
                ) AS [TEMPERATURA HORNO7]
            FROM TBL_DATOS_PROCESO TB
            CROSS APPLY (
                SELECT
                    DATEADD(
                        MONTH, DAY(TB.Fecha_Registro) - 1,
                        DATEADD(
                            DAY, MONTH(TB.Fecha_Registro) - 1,
                            CAST(CAST(YEAR(TB.Fecha_Registro) AS char(4)) + '0101' AS date)
                        )
                    ) AS Fecha_Reinterpretada
            ) F
            WHERE
                (:fecha_desde IS NULL OR F.Fecha_Reinterpretada >= :fecha_desde)
            AND (:fecha_hasta IS NULL OR F.Fecha_Reinterpretada < DATEADD(DAY, 1, :fecha_hasta))
            AND (
                    :numero_ot IS NULL
                    OR :numero_ot = '*'
                    OR TB.Numero_OT = :numero_ot
                )
            ORDER BY TB.Fecha_Registro DESC
        """)
        
        result = self.connection.execute(
            query,
            {
                "fecha_desde": fecha_desde,
                "fecha_hasta": fecha_hasta,
                "numero_ot": numero_ot
            }
        )
        
        return [dict(row._mapping) for row in result]