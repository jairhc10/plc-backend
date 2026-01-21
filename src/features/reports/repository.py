from sqlalchemy import text
from typing import Optional, List, Dict, Any, Tuple
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
                (
                    SELECT TOP 1 TH.Temp_Horno_01
                    FROM TBL_HISTORICO_TEMPERATURAS TH
                    WHERE TH.Fecha_Hora >= CAST(TB.Fecha_Registro AS DATE)
                      AND TH.Fecha_Hora < DATEADD(DAY, 1, CAST(TB.Fecha_Registro AS DATE))
                    ORDER BY TH.Fecha_Hora
                ) AS [TEMPERATURA HORNO1],
                (
                    SELECT TOP 1 TH.Temp_Horno_02
                    FROM TBL_HISTORICO_TEMPERATURAS TH
                    WHERE TH.Fecha_Hora >= CAST(TB.Fecha_Registro AS DATE)
                      AND TH.Fecha_Hora < DATEADD(DAY, 1, CAST(TB.Fecha_Registro AS DATE))
                    ORDER BY TH.Fecha_Hora
                ) AS [TEMPERATURA HORNO2],
                (
                    SELECT TOP 1 TH.Temp_Horno_03
                    FROM TBL_HISTORICO_TEMPERATURAS TH
                    WHERE TH.Fecha_Hora >= CAST(TB.Fecha_Registro AS DATE)
                      AND TH.Fecha_Hora < DATEADD(DAY, 1, CAST(TB.Fecha_Registro AS DATE))
                    ORDER BY TH.Fecha_Hora
                ) AS [TEMPERATURA HORNO3],
                (
                    SELECT TOP 1 TH.Temp_Horno_04
                    FROM TBL_HISTORICO_TEMPERATURAS TH
                    WHERE TH.Fecha_Hora >= CAST(TB.Fecha_Registro AS DATE)
                      AND TH.Fecha_Hora < DATEADD(DAY, 1, CAST(TB.Fecha_Registro AS DATE))
                    ORDER BY TH.Fecha_Hora
                ) AS [TEMPERATURA HORNO4],
                (
                    SELECT TOP 1 TH.Temp_Horno_05
                    FROM TBL_HISTORICO_TEMPERATURAS TH
                    WHERE TH.Fecha_Hora >= CAST(TB.Fecha_Registro AS DATE)
                      AND TH.Fecha_Hora < DATEADD(DAY, 1, CAST(TB.Fecha_Registro AS DATE))
                    ORDER BY TH.Fecha_Hora
                ) AS [TEMPERATURA HORNO5],
                (
                    SELECT TOP 1 TH.Temp_Horno_06
                    FROM TBL_HISTORICO_TEMPERATURAS TH
                    WHERE TH.Fecha_Hora >= CAST(TB.Fecha_Registro AS DATE)
                      AND TH.Fecha_Hora < DATEADD(DAY, 1, CAST(TB.Fecha_Registro AS DATE))
                    ORDER BY TH.Fecha_Hora
                ) AS [TEMPERATURA HORNO6],
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

    # ✅ PAGINADO COMPATIBLE (SIN OFFSET/FETCH)
    def obtener_reporte_hornos_paginado(
        self,
        fecha_desde: Optional[date] = None,
        fecha_hasta: Optional[date] = None,
        numero_ot: Optional[str] = None,
        page: int = 1,
        size: int = 10
    ) -> Tuple[List[Dict[str, Any]], int]:

        page = max(1, int(page))
        size = max(1, min(100, int(size)))

        start_row = (page - 1) * size + 1
        end_row = page * size

        base_sql = """
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
                (
                    SELECT TOP 1 TH.Temp_Horno_01
                    FROM TBL_HISTORICO_TEMPERATURAS TH
                    WHERE TH.Fecha_Hora >= CAST(TB.Fecha_Registro AS DATE)
                      AND TH.Fecha_Hora < DATEADD(DAY, 1, CAST(TB.Fecha_Registro AS DATE))
                    ORDER BY TH.Fecha_Hora
                ) AS [TEMPERATURA HORNO1],
                (
                    SELECT TOP 1 TH.Temp_Horno_02
                    FROM TBL_HISTORICO_TEMPERATURAS TH
                    WHERE TH.Fecha_Hora >= CAST(TB.Fecha_Registro AS DATE)
                      AND TH.Fecha_Hora < DATEADD(DAY, 1, CAST(TB.Fecha_Registro AS DATE))
                    ORDER BY TH.Fecha_Hora
                ) AS [TEMPERATURA HORNO2],
                (
                    SELECT TOP 1 TH.Temp_Horno_03
                    FROM TBL_HISTORICO_TEMPERATURAS TH
                    WHERE TH.Fecha_Hora >= CAST(TB.Fecha_Registro AS DATE)
                      AND TH.Fecha_Hora < DATEADD(DAY, 1, CAST(TB.Fecha_Registro AS DATE))
                    ORDER BY TH.Fecha_Hora
                ) AS [TEMPERATURA HORNO3],
                (
                    SELECT TOP 1 TH.Temp_Horno_04
                    FROM TBL_HISTORICO_TEMPERATURAS TH
                    WHERE TH.Fecha_Hora >= CAST(TB.Fecha_Registro AS DATE)
                      AND TH.Fecha_Hora < DATEADD(DAY, 1, CAST(TB.Fecha_Registro AS DATE))
                    ORDER BY TH.Fecha_Hora
                ) AS [TEMPERATURA HORNO4],
                (
                    SELECT TOP 1 TH.Temp_Horno_05
                    FROM TBL_HISTORICO_TEMPERATURAS TH
                    WHERE TH.Fecha_Hora >= CAST(TB.Fecha_Registro AS DATE)
                      AND TH.Fecha_Hora < DATEADD(DAY, 1, CAST(TB.Fecha_Registro AS DATE))
                    ORDER BY TH.Fecha_Hora
                ) AS [TEMPERATURA HORNO5],
                (
                    SELECT TOP 1 TH.Temp_Horno_06
                    FROM TBL_HISTORICO_TEMPERATURAS TH
                    WHERE TH.Fecha_Hora >= CAST(TB.Fecha_Registro AS DATE)
                      AND TH.Fecha_Hora < DATEADD(DAY, 1, CAST(TB.Fecha_Registro AS DATE))
                    ORDER BY TH.Fecha_Hora
                ) AS [TEMPERATURA HORNO6],
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
        """

        # 1) TOTAL
        count_query = text(f"SELECT COUNT(1) AS total FROM ({base_sql}) X")
        total = self.connection.execute(count_query, {
            "fecha_desde": fecha_desde,
            "fecha_hasta": fecha_hasta,
            "numero_ot": numero_ot
        }).scalar() or 0

        # 2) DATA PAGINADA (ROW_NUMBER)
        data_query = text(f"""
            WITH Q AS (
                SELECT 
                    X.*,
                    ROW_NUMBER() OVER (ORDER BY X.Fecha_Registro DESC) AS rn
                FROM ({base_sql}) X
            )
            SELECT *
            FROM Q
            WHERE rn BETWEEN :start_row AND :end_row
            ORDER BY rn
        """)

        result = self.connection.execute(data_query, {
            "fecha_desde": fecha_desde,
            "fecha_hasta": fecha_hasta,
            "numero_ot": numero_ot,
            "start_row": start_row,
            "end_row": end_row
        })

        return [dict(row._mapping) for row in result], int(total)
