# Version 1.1.0

import os
import sys
import logging
import datetime
from opencensus.ext.azure.log_exporter import AzureLogHandler

# TERRA MODULES
from modules import cosmoUtility as cUtil
from modules import cosmoDownload as cDownl
from modules import cosmoProcess as cProc
from modules import cosmoOutput as cOut
from resources import params

def is_application_insight_configured():
    return (
        os.getenv("APPINSIGHTS_INSTRUMENTATIONKEY") != None
        or os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING") != None
    )

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)
if is_application_insight_configured():
    log_handler = AzureLogHandler()
    logger.addHandler(log_handler)
else:
    logger.warning("Application insights is not configured.")



def executeUpdate():
    error = False
    logger.info("executeUpdate ")
    start_time = datetime.datetime.now()
    logger.info("start time: " + start_time.strftime("%H:%M:%S"))
    repo = "start time: " + start_time.strftime("%H:%M:%S") + "<br/>\n"

    try:
        repo += "<!-- 0 --><br/>\n"

        # Create folder structure
        repo += cUtil.createFolderStructure(params.DIRECTORIES)
        repo += "time: " + cUtil.getPassedTime(start_time) + "<br/>\n"

        # Create general info file
        repo += cOut.createGeneralInfoOutput(
            file = params.FILES["GENERAL_INFO"]
        )
        repo += "<!-- 1 --><br/>\n"
        repo += "time: " + cUtil.getPassedTime(start_time) + "<br/>\n"

        # ----------------------------- DOWNLOADS --------------------------------- #

        # Download class initialization
        dataDownloader = cDownl.DownloadAndExtractComextParallel(logger=logger)
        
        # Data Download - Product (Annual)
        repo += dataDownloader.data_download(
            frequency="annual",
            file_type=params.PREFIX_PRODUCT,
            url_download=params.URLS["COMEXT_PRODUCTS"],
            zip_path=params.DIRECTORIES["PRODUCT_ANNUAL_ZIP"],
            out_path=params.DIRECTORIES["PRODUCT_ANNUAL_FILE"]   
        )
        repo += "<!-- 2 --><br/>\n"
        repo += "time: " + cUtil.getPassedTime(start_time) + "<br/>\n"

        # Data Download - Product (Monthly)
        repo += dataDownloader.data_download(
            frequency="monthly",
            file_type=params.PREFIX_PRODUCT,
            url_download=params.URLS["COMEXT_PRODUCTS"],
            zip_path=params.DIRECTORIES["PRODUCT_MONTHLY_ZIP"],
            out_path=params.DIRECTORIES["PRODUCT_MONTHLY_FILE"]    
        )
        repo += "<!-- 3 --><br/>\n"
        repo += "time: " + cUtil.getPassedTime(start_time) + "<br/>\n"

        # Data Download - Transport (Monthly)
        repo += dataDownloader.data_download(
            frequency="monthly",
            file_type=params.PREFIX_TRANSPORT,
            url_download=params.URLS["COMEXT_TR"],
            zip_path=params.DIRECTORIES["TRANSPORT_MONTHLY_ZIP"],
            out_path=params.DIRECTORIES["TRANSPORT_MONTHLY_FILE"]    
        )
        repo += "<!-- 4 --><br/>\n"
        repo += "time: " + cUtil.getPassedTime(start_time) + "<br/>\n"

        # File Download - Product Class
        repo += dataDownloader.download_file(
            url = params.URLS["CLS_PRODUCTS"],
            file = params.FILES["CLS_PRODUCT_DAT"]
        )
        repo += "<!-- 5 --><br/>\n"

        # File Download - CPA Class
        repo += dataDownloader.download_file(
            url = params.URLS["CLS_CPA"],
            file = params.FILES["CLS_CPA"]
        )
        repo += "<!-- 6 --><br/>\n"

        # File Download - 3-Digit CPA Class Ita
        repo += dataDownloader.download_file(
            url = params.URLS["CLS_CPA_3D_ITA"],
            file = params.FILES["CLS_CPA_3D_ITA"]
        )
        repo += "<!-- 6.1 --><br/>\n"

        # File Download - 2-Digit CPA Ita Class
        repo += dataDownloader.download_file(
            url = params.URLS["CLS_CPA_2D_ITA"],
            file = params.FILES["CLS_CPA_2D_ITA"]
        )
        repo += "<!-- 6.2 --><br/>\n"

        # File Download - NSTR Class
        repo += dataDownloader.download_file(
            url = params.URLS["CLS_NSTR"],
            file = params.FILES["CLS_NSTR"]
        )
        repo += "<!-- 7 --><br/>\n"

        # File Download - NSTR Class Ita
        repo += dataDownloader.download_file(
            url = params.URLS["CLS_NSTR_ITA"],
            file = params.FILES["CLS_NSTR_ITA"]
        )
        repo += "<!-- 7.1a --><br/>\n"

        # [Map] File Download - Annual Population
        repo += dataDownloader.download_file(
            url = params.URLS["ANNUAL_POPULATION"],
            file = params.FILES["ANNUAL_POPULATION_CSV"]
        )
        repo += "<!-- 7.1 --><br/>\n"

        # [Map] File Download - Annual Industrial Production
        repo += dataDownloader.download_file(
            url = params.URLS["ANNUAL_INDUSTRIAL_PRODUCTION"],
            file = params.FILES["ANNUAL_INDUSTRIAL_PRODUCTION_CSV"]
        )
        repo += "<!-- 7.2 --><br/>\n"

        # [Map] File Download - Annual Employment
        repo += dataDownloader.download_file(
            url = params.URLS["ANNUAL_UNEMPLOYEMENT"],
            file = params.FILES["ANNUAL_UNEMPLOYEMENT_CSV"]
        )
        repo += "<!-- 7.3 --><br/>\n"

        # ----------------------------- PROCESSING --------------------------------- #

        #[MAP] CREAZIONE FILE PER LA MAPPA INTERATTIVA (IEINFO)
        
        repo += cOut.annualProcessing(
            annual_data_input_path = params.DIRECTORIES["PRODUCT_ANNUAL_FILE"],
            cls_product_data = params.FILES["CLS_PRODUCT_DAT"],
            annual_pop_data = params.FILES["ANNUAL_POPULATION_CSV"],
            annual_ind_prod_data = params.FILES["ANNUAL_INDUSTRIAL_PRODUCTION_CSV"],
            annual_unemp_data = params.FILES["ANNUAL_UNEMPLOYEMENT_CSV"],
            output_file = params.FILES["IEINFO"],
            logger = logger
        )
        repo += "<!-- 8 --><br/>\n"
        repo += "time: " + cUtil.getPassedTime(start_time) + "<br/>\n"

        #[DB] CREAZIONE DB CON TABELLE
        repo += cProc.createMonthlyFULLtable(
            db = params.FILES["SQLLITE_DB"],
            path_to_scan = params.DIRECTORIES["PRODUCT_MONTHLY_FILE"],
            logger = logger
        )
        repo += "<!-- 9 --><br/>\n"
        repo += "time: " + cUtil.getPassedTime(start_time) + "<br/>\n"
       
        #[DB] CREAZIONE TABELLE PER SERIE MAPPA
        repo += cProc.monthlyProcessing(
            db = params.FILES["SQLLITE_DB"],
            logger = logger
        )
        repo += "<!-- 10 --><br/>\n"
        repo += "time: " + cUtil.getPassedTime(start_time) + "<br/>\n"

        # ----------------------------- OUTPUT --------------------------------- #
        
        #[JSON-SERVER/MAP] CREAZIONE FILE JSON PER SERIE IMPORT/EXPORT
        repo += cOut.createMonthlyOutputTimeSeries(
            db = params.FILES["SQLLITE_DB"],
            import_ts = params.FILES["IMPORT_SERIES_JSON"],
            export_ts = params.FILES["EXPORT_SERIES_JSON"],
            logger = logger
        )

        repo += "<!-- 11 --><br/>\n"

        #[JSON-SERVER/TRADE] CREAZIONE FILE JSON PER SERIE IMPORT/EXPORT VALUE
        repo += cOut.createMonthlyOutputVQSTradeValue(
            db = params.FILES["SQLLITE_DB"],
            import_value = params.FILES["IMPORT_VALUE_JSON"],
            export_value = params.FILES["EXPORT_VALUE_JSON"],
            cls_product_data = params.FILES["CLS_CPA"],
            cls_product_2d_data = params.FILES["CLS_CPA_2D_ITA"],
            logger = logger
        )
        repo += "<!-- 12 --><br/>\n"

        #[JSON-SERVER/TRADE] CREAZIONE FILE JSON PER SERIE IMPORT/EXPORT QUANTITY
        repo += cOut.createMonthlyOutputVQSTradeQuantity(
            db = params.FILES["SQLLITE_DB"],
            import_qty = params.FILES["IMPORT_QUANTITY_JSON"],
            export_qty = params.FILES["EXPORT_QUANTITY_JSON"],
            cls_product_data = params.FILES["CLS_CPA"],
            cls_product_2d_data = params.FILES["CLS_CPA_2D_ITA"],
            logger = logger
        )

        repo += "<!-- 12.1 --><br/>\n"
        ## NON USATO
        #repo+=cOut.createMonthlyOutputQuoteSTrade(
        #    db = params.FILES["SQLLITE_DB"],
        #    quote_trade = params.FILES["QUOTE_TRADE_JSON"],
        #    logger = logger
        #)

        #[JSON-SERVER/TRADE] CREAZIONE FILE JSON PER SERIE IMPORT/EXPORT QUOTE VALUE
        repo += cOut.createMonthlyOutputQuoteSTradeValue(
            db = params.FILES["SQLLITE_DB"],
            import_quote_value = params.FILES["IMPORT_QUOTE_VALUE_JSON"],
            export_quote_value = params.FILES["EXPORT_QUOTE_VALUE_JSON"],
            cls_product_data = params.FILES["CLS_CPA"],
            cls_product_2d_data = params.FILES["CLS_CPA_2D_ITA"],
            logger = logger
        )
        repo += "<!-- 12.2 --><br/>\n"

        #[JSON-SERVER/TRADE] CREAZIONE FILE JSON PER SERIE IMPORT/EXPORT QUATE QUANTITY
        repo += cOut.createMonthlyOutputQuoteSTradeQuantity(
            db = params.FILES["SQLLITE_DB"],
            import_quote_qty = params.FILES["IMPORT_QUOTE_QUANTITY_JSON"],
            export_quote_qty = params.FILES["EXPORT_QUOTE_QUANTITY_JSON"],
            cls_product_data = params.FILES["CLS_CPA"],
            cls_product_2d_data = params.FILES["CLS_CPA_2D_ITA"],
            logger = logger
        )
        repo += "<!-- 13 --><br/>\n"

        #[PYTHON-SERVER] CREAZIONE FILE CPA INTRA E CPA PRODUCT CODE
        repo += cOut.createOutputGraphCPAIntraUE(
            db = params.FILES["SQLLITE_DB"],
            cpa_intra = params.FILES["CPA_INTRA_CSV"],
            cpa3_prod_code = params.FILES["CPA3_PRODUCT_CODE_CSV"],
            logger = logger
        )
        repo += "<!-- 14 --><br/>\n"

        #[PYTHON-SERVER] CREAZIONE FILE TR EXTRA UE E TR PRODUCT CODE
        repo += cOut.createOutputGraphExtraUE(
            input_path = params.DIRECTORIES["TRANSPORT_MONTHLY_FILE"],
            output_tr_extra_ue_file = params.FILES["TR_EXTRA_UE_CSV"],
            output_tr_prod_code_file = params.FILES["TR_PRODUCT_CODE_CSV"],
            logger = logger
        )
        repo += "<!-- 15 --><br/>\n"

        #[PYTHON-SERVER] CREAZIONE FILE CPA TRIM
        repo += cOut.createOutputGraphicTrimestre(
            db = params.FILES["SQLLITE_DB"],
            output_cpa_trim = params.FILES["CPA_TRIM_CSV"],
            logger = logger
        )
        repo += "<!-- 16 --><br/>\n"

        #[PYTHON-SERVER] CREAZIONE FILE TR EXTRA UE TRIM
        repo += cOut.createOutputGraphExtraUE_Trim(
            input_path = params.DIRECTORIES["TRANSPORT_MONTHLY_FILE"],
            output_tr_extra_ue_trim = params.FILES["TR_EXTRA_UE_TRIMESTRALI_CSV"],
            logger = logger
        )
        repo += "<!-- 17 --><br/>\n"

        #[R-SERVER] CREAZIONE FILE COMEX IMP/EXP E CPA2 PRODUCT CODE
        repo += cOut.createOutputVariazioniQuoteCPA(
            db = params.FILES["SQLLITE_DB"],
            comext_imp = params.FILES["COMEXT_IMP_CSV"],
            comext_exp = params.FILES["COMEXT_EXP_CSV"],
            cpa2_prod_code =  params.FILES["CPA2_PRODUCT_CODE_CSV"],
            logger = logger
        )
        repo += "<!-- 18 --><br/>\n"
        repo += "time: " + cUtil.getPassedTime(start_time) + "<br/>\n"
        
        #[JSON-SERVER/CLASSIFICATION] CREAZIONE FILE CPA CON PULIZIA
        repo += cOut.createClsNOTEmptyProductsLang(
            digit = 2,
            langs = params.SUPPORTED_LANGUAGES,
            clsfiles = [
                params.FILES["CLS_CPA_2D_ITA"],
                params.FILES["CLS_CPA"],
                ],
            filename = "CPA",
            filterValue = 37,
            fileExistingProducts = params.FILES["CPA2_PRODUCT_CODE_CSV"],
            logger = logger
        )
        repo += "<!-- 19 --><br/>\n"

        #[JSON-SERVER/CLASSIFICATION] CREAZIONE FILE GRAPH INTRA CON PULIZIA
        repo += cOut.createClsNOTEmptyProductsLang(
            digit = 3,
            langs = params.SUPPORTED_LANGUAGES,
            clsfiles = [
                params.FILES["CLS_CPA_3D_ITA"],
                params.FILES["CLS_CPA"]
                ],
            filename = "GraphIntra",
            filterValue = 37,
            fileExistingProducts = params.FILES["CPA3_PRODUCT_CODE_CSV"],
            logger = logger
        )
        repo += "<!-- 20 --><br/>\n"

        #[JSON-SERVER/CLASSIFICATION] CREAZIONE FILE GRAPH EXTRA CON PULIZIA
        repo += cOut.createClsNOTEmptyProductsLang(
            digit = 3,
            langs = params.SUPPORTED_LANGUAGES,
            clsfiles = [
                params.FILES["CLS_NSTR_ITA"],
                params.FILES["CLS_NSTR"]
                ],
            filename = "GraphExtraNSTR",
            filterValue = 999999,
            fileExistingProducts = params.FILES["TR_PRODUCT_CODE_CSV"],
            logger = logger
        )

        repo += "<!-- 21 --><br/>\n"
        repo += cUtil.exportOutputs(logger)
        repo += "<!-- 22 --><br/>\n"

        repo += cUtil.createAndSendBackupFiles(logger)
        repo += "<!-- 22.1 --><br/>\n"
        repo += "time: " + cUtil.getPassedTime(start_time) + "<br/>\n"

        repo += cUtil.deleteFolder(params.DATA_FOLDER , logger)
        repo += "<!-- 23 --><br/>\n"

        repo += cUtil.refreshMicroservicesDATA(logger)
        repo += "<!-- 24 --><br/>\n"
        repo += "time: " + cUtil.getPassedTime(start_time) + "<br/>\n"

        repo += cUtil.checkUPMicroservices(logger)
        repo += "<!-- 25 --><br/>\n"

        repo += "time: " + cUtil.getPassedTime(start_time) + "<br/>\n"

    except BaseException as e:
        repo += "ERROR UPDATE  " + str(e)
        error = True

    finally:
        end_time = datetime.datetime.now()
        logger.info(" end time: " + end_time.strftime("%H:%M:%S"))
        total_time = end_time - start_time
        logger.info("TOTAL time: " + str(total_time))
        repo += "end time: " + end_time.strftime("%H:%M:%S") + "<br/>\n"
        repo += "<br/>\n"
        repo += "TOTAL time: " + str(total_time) + "<br/>\n"
        repo += "<br/>\n"
        repo += cUtil.sendEmailRepo(repo , logger)
        repo += "<br/>\n"
        logger.info("[cosmoUpdateData]: " + repo)

    return error


if __name__ == "__main__":
    if executeUpdate():
        sys.exit(1)
