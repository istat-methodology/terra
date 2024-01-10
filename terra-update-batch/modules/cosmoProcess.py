import os
import sqlite3
import pandas as pd
import params

def createMonthlyFULLtable(db, path_to_scan, logger):
    logger.info(db)
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    logger.info("Creating table  comext_full ")
    cur.execute("DROP TABLE IF EXISTS comext_full;")
    cur.execute(
        "CREATE TABLE comext_full (DECLARANT_ISO TEXT,PARTNER_ISO TEXT,PRODUCT_NC TEXT,PRODUCT_CPA2_1 TEXT,PRODUCT_BEC TEXT,FLOW INTEGER,PERIOD INTEGER, VALUE_IN_EUROS INTEGER, QUANTITY_IN_KG INTEGER,CPA2 TEXT,CPA23 TEXT,CPA3 TEXT,IS_PRODUCT INTEGER DEFAULT 0)"
    )

    logger.info("SCANNED PATH: " + path_to_scan)
    count = 0
    index = 0
    for filedat in os.scandir(path_to_scan):
        if filedat.is_file():
            comext_monthly_data = pd.read_csv(
                filedat, sep=",", low_memory=True, keep_default_na=False, na_values=[""]
            )
            length = len(comext_monthly_data.index)
            count += length
            index += 1
            logger.info(
                str(index)
                + ") loaded rows:"
                + str(length)
                + " count:"
                + str(count)
                + "  file: "
                + filedat.name
            )
            comext_monthly_data[
                [
                    "DECLARANT_ISO",
                    "PARTNER_ISO",
                    "PRODUCT_NC",
                    "PRODUCT_CPA2_1",
                    "PRODUCT_BEC",
                    "FLOW",
                    "PERIOD",
                    "VALUE_IN_EUROS",
                    "QUANTITY_IN_KG",
                ]
            ].to_sql(
                "comext_full", conn, if_exists="append", index=False, chunksize=10000
            )

    for row in cur.execute("SELECT count(*) FROM comext_full "):
        logger.info("from count:" + str(count))
        logger.info("from DB:" + str(row))

    logger.info("UPDATE TABLE comext_full A CPA2, CPA23 CPA3 TEXT")
    cur.execute(
        """UPDATE comext_full SET CPA2=substr(product_cpa2_1,1,2), CPA23=substr(product_cpa2_1,1,2)||' ', CPA3=substr(product_cpa2_1,1,3),IS_PRODUCT=1  WHERE length(product_nc)==8;"""
    )
    conn.commit()
    if conn:
        conn.close()

    return "TABLE comext_full created!"


def monthlyProcessing(db, logger):
    conn = sqlite3.connect(db)

    cur = conn.cursor()

    # Create table Series
    ## considero un 1 anno prima es 48 per 36 mesi
    filter_yyymm = str(params.start_data_PAGE_MAP.year - 1) + str(
        "%02d" % params.start_data_PAGE_MAP.month
    )
    logger.info("Creating Series table ")
    cur.execute("DROP TABLE IF EXISTS serie_per_mappa0;")
    cur.execute(
        "Create table serie_per_mappa0 as select declarant_iso, period, flow, sum(value_in_euros) as value_in_euros from comext_full where product_nc= 'TOTAL' and period>="
        + filter_yyymm
        + " group by declarant_iso, period,flow;"
    )
    cur.execute("DROP TABLE IF EXISTS serie_per_mappa;")
    cur.execute(
        "Create table serie_per_mappa as select a.declarant_iso, a.period, a.flow, round(100.00*( (a.value_in_euros-b.value_in_euros)*1.0  / b.value_in_euros ),2) as TENDENZIALE from serie_per_mappa0 a, serie_per_mappa0 b where a.flow=b.flow and a.declarant_iso=b.declarant_iso and a.period=(b.period+100);"
    )
    conn.commit()

    # /* calcolo i valori per cpa */

    ## considero un 1 anno prima es 48 per 36 mesi
    filter_yyymm = str(params.start_data_PAGE_BASKET.year - 1) + str(
        "%02d" % params.start_data_PAGE_BASKET.month
    )
    logger.info("Creating aggr_cpa table ")
    cur.execute("DROP TABLE IF EXISTS aggr_cpa;")
    cur.execute(
        "create table aggr_cpa as select declarant_iso, flow, cpa2, period, sum(value_in_euros) as val_cpa, sum(quantity_in_kg) as q_cpa  from comext_full  WHERE IS_PRODUCT==1 and period>="
        + filter_yyymm
        + " group by declarant_iso, flow, cpa2, period order by declarant_iso, flow, cpa2, period;"
    )

    conn.commit()

    # /* calcolo il valore totale */
    logger.info("Creating aggr_tot table ")
    cur.execute("DROP TABLE IF EXISTS aggr_tot;")
    cur.execute(
        "create table aggr_tot as select declarant_iso, flow, period, sum(val_cpa) as val_tot, sum(q_cpa) as q_tot from aggr_cpa group by declarant_iso, flow, period order by declarant_iso, flow, period;"
    )
    conn.commit()

    # /* calcolo le quote */
    logger.info("Creating quote_cpa table ")
    cur.execute("DROP TABLE IF EXISTS quote_cpa;")
    cur.execute(
        "create table quote_cpa as select a.declarant_iso, a.flow, a.cpa2, a.period, a.val_cpa, b.val_tot, a.q_cpa, b.q_tot, 100.0*a.val_cpa/b.val_tot as q_val_cpa, 100.0*a.q_cpa/b.q_tot as q_qua_cpa  from aggr_cpa a, aggr_tot b where a.declarant_iso=b.declarant_iso and a.flow=b.flow and a.period=b.period;"
    )

    # /* calcolo le variazioni */
    logger.info("Creating variazioni table ")
    cur.execute("DROP TABLE IF EXISTS variazioni;")
    cur.execute(
        "create table variazioni as select a.declarant_iso, a.flow, a.cpa2, a.period, a.val_cpa, round(100.0*(a.val_cpa-b.val_cpa)/b.val_cpa,2) as var_val_cpa, round(100.0*(a.q_val_cpa-b.q_val_cpa)/b.q_val_cpa,2) as var_val_basket, a.q_cpa, round(100.0*(a.q_cpa-b.q_cpa)/b.q_cpa,2) as var_q_cpa, round(100.0*(a.q_qua_cpa-b.q_qua_cpa)/b.q_qua_cpa,2) as var_qua_basket from quote_cpa a, quote_cpa b where a.declarant_iso=b.declarant_iso and a.flow=b.flow and a.cpa2=b.cpa2 and a.period=(b.period+100);"
    )

    ## grafi in classificazione CPA e scambi tra paesi intra-UE

    # /* aggrego per cpa2 */
    logger.info("Creating table aggr_cpa2 ")
    cur.execute("DROP TABLE IF EXISTS aggr_cpa2;")
    cur.execute(
        "create table aggr_cpa2 as select declarant_iso, partner_iso, flow, cpa23 as cpa, period, sum(value_in_euros) as val_cpa, sum(quantity_in_kg) as q_kg from comext_full  WHERE IS_PRODUCT==1 group by declarant_iso, partner_iso, flow, cpa23, period order by declarant_iso, partner_iso, flow, cpa23, period;"
    )

    # /* aggrego per cpa3 */
    logger.info("Creating table aggr_cpa3 ")
    cur.execute("DROP TABLE IF EXISTS aggr_cpa3;")
    cur.execute(
        "create table aggr_cpa3 as select declarant_iso, partner_iso, flow, cpa3 as cpa, period, sum(value_in_euros) as val_cpa, sum(quantity_in_kg) as q_kg from comext_full  WHERE IS_PRODUCT==1 group by declarant_iso, partner_iso, flow, cpa3, period order by declarant_iso, partner_iso, flow, cpa3, period;"
    )

    # /* aggrego per cpa TOTAL 00 */
    logger.info("Creating table aggr_cpa_tot ")
    cur.execute("DROP TABLE IF EXISTS aggr_cpa_tot;")
    cur.execute(
        "create table aggr_cpa_tot as select declarant_iso, partner_iso, flow, '00' as cpa, period, sum(value_in_euros) as val_cpa, sum(quantity_in_kg) as q_kg from comext_full WHERE product_nc= 'TOTAL' group by declarant_iso, partner_iso, flow,  cpa, period;"
    )

    # /*  view */
    logger.info("Creating table base_grafi_cpa ")
    cur.execute("DROP TABLE IF EXISTS base_grafi_cpa;")
    cur.execute(
        "create table base_grafi_cpa as select * from  aggr_cpa2 where (1* substr(cpa,1,2) >0 and 1* substr(cpa,1,2) <37) union select * from  aggr_cpa3 where (1* substr(cpa,1,3) >0 and 1* substr(cpa,1,3) <370) union  select * from aggr_cpa_tot;"
    )

    # /*  create table WORLD for all partners * add ALL COUNTRIES AC
    logger.info("Creating table base_grafi_cpa_wo ")
    cur.execute("DROP TABLE IF EXISTS base_grafi_cpa_wo;")
    cur.execute(
        "create table base_grafi_cpa_wo as select declarant_iso, 'AC' as partner_iso, flow, cpa, period, sum(val_cpa) as val_cpa,sum(q_kg) as q_kg from base_grafi_cpa group by declarant_iso, flow, cpa, period order by declarant_iso, flow, cpa, period; "
    )

    # /*  view */
    logger.info("Creating table variazioni_cpa ")
    cur.execute("DROP TABLE IF EXISTS variazioni_cpa;")
    cur.execute(
        "create table variazioni_cpa as select a.declarant_iso, a.partner_iso, a.flow, a.cpa, a.period, a.val_cpa, round(100.00*((a.val_cpa-b.val_cpa)*1.00/b.val_cpa),2) as var_cpa, a.q_kg, round(100.00*(a.q_kg-b.q_kg)/b.q_kg,2)  as var_q_cpa  from base_grafi_cpa a, base_grafi_cpa b where a.declarant_iso=b.declarant_iso and a.partner_iso=b.partner_iso and a.flow=b.flow and a.cpa=b.cpa and a.period=(b.period+100) union all select a.declarant_iso, a.partner_iso,a.flow, a.cpa, a.period, a.val_cpa, 100*(a.val_cpa-b.val_cpa)/b.val_cpa as var_cpa, a.q_kg, 100*(a.q_kg-b.q_kg)/b.q_kg  as var_q_cpa from base_grafi_cpa_wo a, base_grafi_cpa_wo b where a.declarant_iso = b.declarant_iso 	and a.flow = b.flow and a.cpa = b.cpa and a.period =(b.period + 100) ; "
    )

    filter_yyymm = str(params.start_data_PAGE_GRAPH_INTRA_UE.year - 1) + str(
        "%02d" % params.start_data_PAGE_GRAPH_INTRA_UE.month
    )
    # /*  basi trimestrali */
    logger.info("Creating table per_trimestri  ")
    cur.execute("DROP TABLE IF EXISTS per_trimestri;")
    cur.execute(
        "create table per_trimestri as select *, substr(period,1,4)||'T1' as trimestre from base_grafi_cpa where substr(period,5,2) in ('01', '02','03') and period >= "
        + filter_yyymm
        + " union select *, substr(period,1,4)||'T2' as trimestre from base_grafi_cpa where substr(period,5,2) in ('04', '05','06') and period >= "
        + filter_yyymm
        + " union select *, substr(period,1,4)||'T3' as trimestre from base_grafi_cpa where substr(period,5,2) in ('07', '08','09') and period > "
        + filter_yyymm
        + " union select *, substr(period,1,4)||'T4' as trimestre from base_grafi_cpa where substr(period,5,2) in ('10', '11','12') and period > "
        + filter_yyymm
        + ""
    )

    # /*  basi trimestrali */
    logger.info("Creating table base_grafi_cpa_trim  ")
    cur.execute("DROP TABLE IF EXISTS base_grafi_cpa_trim;")
    cur.execute(
        "create table base_grafi_cpa_trim as select declarant_iso, partner_iso, flow,  cpa, trimestre, sum(val_cpa) as val_cpa, sum(q_kg) as q_kg from per_trimestri group by declarant_iso, partner_iso, flow, cpa, trimestre;"
    )

    logger.info("Creating END ")
    if conn:
        conn.close()

    return "Monthly processing on DB OK!"