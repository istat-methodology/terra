from resources import params
import duckdb


def monthlyProcessing(path_to_scan, logger):
    logger.info("SCANNED PATH: " + path_to_scan)
    with duckdb.connect() as con:
        con.execute(
            f"""
            CREATE TEMP TABLE comext_full AS
            select DECLARANT_ISO, PARTNER_ISO, FLOW, PERIOD, VALUE_IN_EUROS, QUANTITY_IN_KG,
                CASE
                    WHEN length(CAST(PRODUCT_NC AS VARCHAR)) = 8
                    THEN SUBSTR(CAST(PRODUCT_CPA2_1 AS VARCHAR), 1, 2)
                    ELSE ''
                END AS CPA2,
                CASE
                    WHEN length(CAST(PRODUCT_NC AS VARCHAR)) = 8
                    THEN SUBSTR(CAST(PRODUCT_CPA2_1 AS VARCHAR), 1, 2) || ' '
                    ELSE ''
                END AS CPA23,
                CASE
                    WHEN length(CAST(PRODUCT_NC AS VARCHAR)) = 8
                    THEN SUBSTR(CAST(PRODUCT_CPA2_1 AS VARCHAR), 1, 3)
                    ELSE ''
                END AS CPA3,
                CASE
                    WHEN length(CAST(PRODUCT_NC AS VARCHAR)) = 8 AND TRY_CAST(SUBSTR(REPLACE(PRODUCT_CPA2_1, 'X', ''), 1, 2) AS INTEGER) BETWEEN 1 AND 36
                    THEN 1
                    ELSE 0
                END AS IS_CPA_1_36,
                CASE
                    WHEN length(CAST(PRODUCT_NC AS VARCHAR)) = 8 AND TRY_CAST(SUBSTR(REPLACE(PRODUCT_CPA2_1, 'X', ''), 1, 3) AS INTEGER) BETWEEN 1 AND 369
                    THEN 1
                    ELSE 0
                END AS IS_CPA_1_369,
                CASE
                    WHEN length(CAST(PRODUCT_NC AS VARCHAR)) = 8
                    THEN 'CPA'
                    WHEN product_nc= 'TOTAL'
                    THEN 'TOTAL'
                    ELSE 'OTHER'
                END AS PRODUCT_TYPE
            from read_csv('{path_to_scan}/*.dat', sep=',', header=False, skip=1, column_names={params.PRODUCT_COLNAMES}, column_types={params.PRODUCT_COLTYPES}, nullstr=['']) as comext_monthly_data
            WHERE length(TRY_CAST(PRODUCT_NC AS VARCHAR)) = 8 OR product_nc= 'TOTAL'
        """
        )
        rows = con.execute("SELECT count(DECLARANT_ISO) FROM comext_full").fetchall()
        logger.info("Monthly data rows: " + str(rows[0][0]))
        # Create table Series
        ## considero un 1 anno prima es 48 per 36 mesi
        filter_yyymm = str(params.start_data_PAGE_MAP.year - 1) + str(
            "%02d" % params.start_data_PAGE_MAP.month
        )

        logger.info("Creating series file")
        con.execute(
            f"""
            COPY (
            WITH base AS (
                SELECT declarant_iso, period, flow, SUM(value_in_euros) AS value_in_euros
                FROM comext_full
                WHERE PRODUCT_TYPE = 'TOTAL'
                AND period >= {filter_yyymm}
                GROUP BY declarant_iso, period, flow
            )
            SELECT a.declarant_iso, a.period, a.flow,
            ROUND(100.0 * ((a.value_in_euros - b.value_in_euros) / NULLIF(b.value_in_euros, 0)), 2) AS TENDENZIALE
            FROM base a JOIN base b
            ON a.declarant_iso = b.declarant_iso
            AND a.flow = b.flow
            AND a.period = b.period + 100
            )
            TO '{params.FILES["PROCESS_MAP_SERIES"]}'
            (FORMAT PARQUET)
            """
        )
        # /* calcolo i valori per cpa */
        ## considero un 1 anno prima es 48 per 36 mesi
        filter_yyymm = str(params.start_data_PAGE_BASKET.year - 1) + str(
            "%02d" % params.start_data_PAGE_BASKET.month
        )
        con.execute(
            f"""
            CREATE TEMP VIEW quote_cpa AS
            SELECT declarant_iso, flow, cpa2, IS_CPA_1_36, period, val_cpa,
                SUM(val_cpa) OVER (PARTITION BY declarant_iso, flow, period) AS val_tot,
                q_cpa,
                SUM(q_cpa) OVER (PARTITION BY declarant_iso, flow, period) AS q_tot,
                ROUND(100.0 * val_cpa / SUM(val_cpa) OVER (PARTITION BY declarant_iso, flow, period), 2) AS q_val_cpa,
                ROUND(100.0 * q_cpa / SUM(q_cpa) OVER (PARTITION BY declarant_iso, flow, period), 2) AS q_qua_cpa
            FROM (
                SELECT declarant_iso, flow, cpa2, period, IS_CPA_1_36, SUM(value_in_euros) AS val_cpa, SUM(quantity_in_kg) AS q_cpa
                FROM comext_full
                WHERE PRODUCT_TYPE = 'CPA'
                AND period >= {filter_yyymm}
                GROUP BY declarant_iso, flow, cpa2, period, IS_CPA_1_36
            ) as aggr_cpa
        """
        )
        logger.info("Creating cpa quotes file")
        con.execute(
            f"""
            COPY (
                SELECT DECLARANT_ISO, FLOW, cpa2 as PRODUCT, PERIOD, q_val_cpa, q_qua_cpa FROM quote_cpa WHERE IS_CPA_1_36 = 1
            )
            TO '{params.FILES["PROCESS_CPA_QUOTES"]}'
            (FORMAT PARQUET)
        """
        )
        # /* calcolo le variazioni */
        logger.info("Creating variations file")
        con.execute(
            f"""
            COPY (
                SELECT a.DECLARANT_ISO, a.FLOW, a.cpa2 as PRODUCT, a.PERIOD,
                ROUND(100.0 * (a.q_val_cpa - b.q_val_cpa) / NULLIF(b.q_val_cpa, 0), 2) AS var_val_basket,
                ROUND(100.0 * (a.q_qua_cpa - b.q_qua_cpa) / NULLIF(b.q_qua_cpa, 0), 2) AS var_qua_basket
                FROM quote_cpa a JOIN quote_cpa b
                ON a.declarant_iso = b.declarant_iso
                AND a.flow = b.flow
                AND a.cpa2 = b.cpa2
                AND a.period = b.period + 100
                AND a.IS_CPA_1_36 = 1
            )
            TO '{params.FILES["PROCESS_VARIATIONS"]}'
            (FORMAT PARQUET)
        """
        )
        ## grafi in classificazione CPA e scambi tra paesi intra-UE
        # /* aggrego per cpa2 */
        con.execute(
            f"""
            create TEMP TABLE base_grafi_cpa as
            select declarant_iso, partner_iso, flow, cpa23 as cpa, period, sum(value_in_euros) as val_cpa, sum(quantity_in_kg) as q_kg
            from comext_full
            WHERE IS_CPA_1_36 = 1
            group by declarant_iso, partner_iso, flow, cpa23, period
            UNION ALL
            select declarant_iso, partner_iso, flow, cpa3 as cpa, period, sum(value_in_euros) as val_cpa, sum(quantity_in_kg) as q_kg
            from comext_full
            WHERE IS_CPA_1_369 = 1
            group by declarant_iso, partner_iso, flow, cpa3, period
            UNION ALL
            select declarant_iso, partner_iso, flow, '00' as cpa, period, sum(value_in_euros) as val_cpa, sum(quantity_in_kg) as q_kg
            from comext_full
            WHERE PRODUCT_TYPE = 'TOTAL'
            group by declarant_iso, partner_iso, flow, cpa, period
        """
        )
        # /*  create table WORLD for all partners * add ALL COUNTRIES AC
        con.execute(
            f"""
            create TEMP VIEW base_grafi_cpa_wo as 
            select declarant_iso, 'AC' as partner_iso, flow, cpa, period, sum(val_cpa) as val_cpa,sum(q_kg) as q_kg
            from base_grafi_cpa
            group by declarant_iso, flow, cpa, period
        """
        )
        con.execute(
            f"""
            create TEMP VIEW variazioni_cpa as
            SELECT a.declarant_iso, a.partner_iso, a.flow, a.cpa, a.period, a.val_cpa,
            ROUND(100.0 * (a.val_cpa - b.val_cpa) / NULLIF(b.val_cpa, 0), 2) AS var_cpa,
            a.q_kg,
            ROUND(100.0 * (a.q_kg - b.q_kg) / NULLIF(b.q_kg, 0), 2) AS var_q_cpa
            FROM base_grafi_cpa a JOIN base_grafi_cpa b
            ON a.declarant_iso = b.declarant_iso
            AND a.partner_iso = b.partner_iso
            AND a.flow = b.flow
            AND a.cpa = b.cpa
            AND a.period = b.period + 100
            union all
            SELECT a.declarant_iso, a.partner_iso, a.flow, a.cpa, a.period, a.val_cpa,
            ROUND(100.0 * (a.val_cpa - b.val_cpa) / NULLIF(b.val_cpa, 0), 2) AS var_cpa,
            a.q_kg,
            ROUND(100.0 * (a.q_kg - b.q_kg) / NULLIF(b.q_kg, 0), 2) AS var_q_cpa
            FROM base_grafi_cpa_wo a JOIN base_grafi_cpa_wo b
            ON a.declarant_iso = b.declarant_iso
            AND a.partner_iso = b.partner_iso
            AND a.flow = b.flow
            AND a.cpa = b.cpa
            AND a.period = b.period + 100
        """
        )
        logger.info("Creating cpa_variations file")
        con.execute(
            f"""
            COPY (
                SELECT DECLARANT_ISO, PARTNER_ISO, FLOW, trim(cpa) as PRODUCT, PERIOD, val_cpa, q_kg FROM variazioni_cpa WHERE (length(trim(cpa))==2 or trim(cpa) in ('061','062') )
            )
            TO '{params.FILES["PROCESS_CPA_VARIATIONS"]}'
            (FORMAT PARQUET)
        """
        )
        filter_yyymm = str(params.start_data_PAGE_GRAPH_INTRA_UE.year - 1) + str(
            "%02d" % params.start_data_PAGE_GRAPH_INTRA_UE.month
        )
        logger.info("Creating base_graph_cpa file")
        con.execute(
            f"""
            COPY (
                SELECT DECLARANT_ISO, PARTNER_ISO, FLOW,
                CASE
                    WHEN length(trim(cpa)) = 3 THEN 1
                    WHEN trim(cpa) = '00' THEN 0
                    ELSE -1
                END as IS_PRODUCT,
                CASE
                    WHEN length(trim(cpa)) = 3 THEN cpa
                    WHEN trim(cpa) = '00' THEN 'TOT'
                    ELSE '---'
                END as PRODUCT,
                PERIOD, val_cpa as VALUE_IN_EUROS, q_kg as QUANTITY_IN_KG
                FROM base_grafi_cpa
                WHERE PERIOD>{filter_yyymm}
                and (length(trim(cpa)) = 3 or trim(cpa) = '00')
            )
            TO '{params.FILES["PROCESS_BASE_GRAPH_CPA"]}'
            (FORMAT PARQUET)
        """
        )
        # /*  basi trimestrali */
        logger.info("Creating base_graph_cpa_trim file")
        con.execute(
            f"""
            COPY (
                select declarant_iso, partner_iso, flow, cpa, trimestre, sum(val_cpa) as val_cpa, sum(q_kg) as q_kg
                from (
                    select declarant_iso, partner_iso, flow, val_cpa, q_kg,
                    CASE
                        WHEN length(trim(cpa)) = 3 THEN cpa
                        WHEN trim(cpa) = '00' THEN 'TOT'
                        ELSE '---'
                    END as cpa,
                    CAST(period / 100 AS INT) || 'T' || CAST(FLOOR(((period % 100 -1) / 3) + 1) AS INT) AS trimestre
                    from base_grafi_cpa
                    where period > {filter_yyymm}
                    and (length(trim(cpa)) = 3 or trim(cpa) = '00')
                ) as per_trimestri
                group by declarant_iso, partner_iso, flow, cpa, trimestre
            )
            TO '{params.FILES["PROCESS_BASE_GRAPH_CPA_TRIM"]}'
            (FORMAT PARQUET)
        """
        )
        con.close()
        logger.info("END Creating monthly processing done")
    return "Monthly processing on DB OK!"