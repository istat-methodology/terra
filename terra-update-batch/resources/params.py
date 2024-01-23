import os
import datetime
from dateutil.relativedelta import relativedelta

RUN_DOWNLOAD = True
RUN_PROCESSING = True
RUN_ANNUAL_PROCESSING = False
RUN_OUTPUT = True

#WORKING_FOLDER=os.environ['WORKING_FOLDER']
WORKING_FOLDER = "C:" + os.sep + "Users" + os.sep + "UTENTE" + os.sep + "terra_output"

KEY_VAULT_NAME = "statlab-key-vault"
SECRETNAME_ACCOUNTKEY = "cosmostoragekey"

URL_JSONDATA_SERVER = "https://api.cosmo.statlab.it/cls"
URL_RDATA_SERVER = "https://api.cosmo.statlab.it/time-series"
URL_PYTHONDATA_SERVER = "https://api.cosmo.statlab.it/graph"

MAIL_SETTINGS = {
    "SERVER": "https://prod-190.westeurope.logic.azure.com:443/workflows/52cafc0d0f2d4dd08ee290a5d367f109/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=PFatjXjc32cpXZqX-KFBkn0a7ZKgT1q5iR2hI07NR4w",
    "TO" : "giulio.massacci@istat.it",
    "SUBJECT" : "Repo from cosmo update"
}

# SET TIME INTERVAL (IN MONTHS) FOR DOWNLOAD
OFFSET_M = 15
DOWNLOAD_TIME_INTERVAL_M = 3
MAX_RETRY = 5
RETRY_WAIT = 1

# TIME INTERVAL FOR PROCESSING
PAGE_MAP_TIME_INTERVAL_M = 36
PAGE_TIME_SERIES_TIME_INTERVAL_M = 36
PAGE_GRAPH_EXTRA_UE_TIME_INTERVAL_M = 36
PAGE_GRAPH_INTRA_UE_TIME_INTERVAL_M = 36
PAGE_BASKET_TIME_INTERVAL_M = 36


PREFIX_PRODUCT = "full"
PREFIX_TRANSPORT = "tr"
PREFIX_MAP = {
  "tr": "transport",
  "full": "product"
}

FLOW_IMPORT = 1
FLOW_EXPORT = 2
COLS_CLS_PRODUCTS = 4
SUPPORTED_LANGUAGES = ["it", "en"]
DATA_EXTENTION = ".dat"
SEP = ","

job_id = os.getenv("AZ_BATCH_JOB_ID", "").replace(":", "_")
DATA_FOLDER_PARENT = (
    WORKING_FOLDER + os.sep + "data" + (("__" + job_id) if (job_id != "") else "")
)

processing_day = datetime.datetime.today()
#this_year = processing_day.year
#this_month = "%02d" % processing_day.month
this_year_month = processing_day.year * 100 + processing_day.month

annual_new_data = (
    1 if (processing_day < datetime.datetime(processing_day.year, 3, 20)) else 0
)
annual_current_year = (
    datetime.datetime.strptime(str(processing_day.year), "%Y")
    - relativedelta(years=annual_new_data)
    - relativedelta(years=1)
).year
annual_previous_year = (
    datetime.datetime.strptime(str(processing_day.year), "%Y")
    - relativedelta(years=annual_new_data)
    - relativedelta(years=2)
).year

start_data_DOWNLOAD = (
    datetime.datetime.strptime(str(this_year_month), "%Y%m")
    - relativedelta(months=OFFSET_M)
    - relativedelta(months=DOWNLOAD_TIME_INTERVAL_M - 1)
)
end_data_DOWNLOAD = datetime.datetime.strptime(
    str(this_year_month), "%Y%m"
) - relativedelta(months=OFFSET_M)

##### SET START DATE FOR PAGES #####
start_data_PAGE_MAP = (
    datetime.datetime.strptime(str(this_year_month), "%Y%m")
    - relativedelta(months=OFFSET_M)
    - relativedelta(months=PAGE_MAP_TIME_INTERVAL_M - 1)
)
start_data_PAGE_TIME_SERIES = (
    datetime.datetime.strptime(str(this_year_month), "%Y%m")
    - relativedelta(months=OFFSET_M)
    - relativedelta(months=PAGE_TIME_SERIES_TIME_INTERVAL_M - 1)
)
start_data_PAGE_GRAPH_EXTRA_UE = (
    datetime.datetime.strptime(str(this_year_month), "%Y%m")
    - relativedelta(months=OFFSET_M)
    - relativedelta(months=PAGE_GRAPH_EXTRA_UE_TIME_INTERVAL_M - 1)
)
start_data_PAGE_GRAPH_INTRA_UE = (
    datetime.datetime.strptime(str(this_year_month), "%Y%m")
    - relativedelta(months=OFFSET_M)
    - relativedelta(months=PAGE_GRAPH_INTRA_UE_TIME_INTERVAL_M - 1)
)
start_data_PAGE_BASKET = (
    datetime.datetime.strptime(str(this_year_month), "%Y%m")
    - relativedelta(months=OFFSET_M)
    - relativedelta(months=PAGE_BASKET_TIME_INTERVAL_M - 1)
)

DATA_FOLDER = DATA_FOLDER_PARENT + os.sep + str(this_year_month)

URLS = {
    "ANNUAL_POPULATION" : "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/DEMO_GIND/?format=SDMX-CSV&i",
    "ANNUAL_INDUSTRIAL_PRODUCTION" : "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/STS_INPR_A/?format=SDMX-CSV&i",
    "ANNUAL_UNEMPLOYEMENT" : "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/UNE_RT_A/?format=SDMX-CSV&i",

    "COMEXT_PRODUCTS" : "https://ec.europa.eu/eurostat/api/dissemination/files/?sort=1&downfile=comext%2FCOMEXT_DATA%2FPRODUCTS%2F",
    
    # NEW ENDPOINT: https://ec.europa.eu/eurostat/api/dissemination/files/?sort=1&dir=comext%2FCOMEXT_DATA%2FTRANSPORT_NSTR
    # ACTUAL USED ENDPOINT: "https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?sort=1&file=comext%2FCOMEXT_DATA%2FTRANSPORT_NSTR%2F"
    # "https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?sort=1&file=comext%2FCOMEXT_HISTORICAL_DATA%2FTRANSPORT_BY_NSTR%2F"
    "COMEXT_TR" : "https://ec.europa.eu/eurostat/api/dissemination/files?sort=1&file=comext%2FCOMEXT_HISTORICAL_DATA%2FTRANSPORT_BY_NSTR%2F",

    "CLS_PRODUCTS" : "https://ec.europa.eu/eurostat/api/dissemination/files/?sort=1&file=comext%2FCOMEXT_METADATA%2FCLASSIFICATIONS_AND_RELATIONS%2FCLASSIFICATIONS%2FENGLISH%2FCN.txt",
    
    "CLS_NSTR" : "https://ec.europa.eu/eurostat/api/dissemination/files/?sort=1&file=comext%2FCOMEXT_METADATA%2FCLASSIFICATIONS_AND_RELATIONS%2FCLASSIFICATIONS%2FENGLISH%2FNSTR.txt",
    "CLS_NSTR_ITA" : "https://raw.githubusercontent.com/istat-methodology/terra/main/cls/Prodotti_NSTR_ita.csv",
    
    "CLS_CPA" : "https://ec.europa.eu/eurostat/api/dissemination/files/?sort=1&file=comext%2FCOMEXT_METADATA%2FCLASSIFICATIONS_AND_RELATIONS%2FCLASSIFICATIONS%2FENGLISH%2FCPA21.txt",
    "CLS_CPA_3D_ITA" : "https://raw.githubusercontent.com/istat-methodology/terra/main/cls/CPA_2_1_3digits_ita.csv",
    "CLS_CPA_2D_ITA" : "https://raw.githubusercontent.com/istat-methodology/terra/main/cls/cpa2.1_2digit_ita.csv"   
}

DIRECTORIES = {
    "ROOT" : DATA_FOLDER,
    "CLASSIFICATION" : DATA_FOLDER + os.sep + "classification",
    "UTILS" : DATA_FOLDER + os.sep + "utils",

    "PRODUCT" : DATA_FOLDER + os.sep + "comext" + os.sep + PREFIX_MAP[PREFIX_PRODUCT],
    "PRODUCT_ANNUAL_ZIP" : DATA_FOLDER + os.sep + "comext" + os.sep + PREFIX_MAP[PREFIX_PRODUCT] + os.sep + "annual" + os.sep + "zip",
    "PRODUCT_ANNUAL_FILE" : DATA_FOLDER + os.sep + "comext" + os.sep + PREFIX_MAP[PREFIX_PRODUCT] + os.sep + "annual" + os.sep + "file",
    "PRODUCT_ANNUAL_OUTPUT" : DATA_FOLDER + os.sep + "comext" + os.sep + PREFIX_MAP[PREFIX_PRODUCT] + os.sep + "annual" + os.sep + "output",
    "PRODUCT_MONTHLY" : DATA_FOLDER + os.sep + "comext" + os.sep + PREFIX_MAP[PREFIX_PRODUCT] + os.sep + "monthly",
    "PRODUCT_MONTHLY_ZIP" : DATA_FOLDER + os.sep + "comext" + os.sep + PREFIX_MAP[PREFIX_PRODUCT] + os.sep + "monthly" + os.sep + "zip",
    "PRODUCT_MONTHLY_FILE" : DATA_FOLDER + os.sep + "comext" + os.sep + PREFIX_MAP[PREFIX_PRODUCT] + os.sep + "monthly" + os.sep + "file",
    "PRODUCT_MONTHLY_OUTPUT" : DATA_FOLDER + os.sep + "comext" + os.sep + PREFIX_MAP[PREFIX_PRODUCT] + os.sep + "monthly" + os.sep + "output",

    "TRANSPORT_MONTHLY_ZIP" : DATA_FOLDER + os.sep + "comext" + os.sep + PREFIX_MAP[PREFIX_TRANSPORT] + os.sep + "monthly" + os.sep + "zip",
    "TRANSPORT_MONTHLY_FILE" : DATA_FOLDER + os.sep + "comext" + os.sep + PREFIX_MAP[PREFIX_TRANSPORT] + os.sep + "monthly" + os.sep + "file",
    "TRANSPORT_MONTHLY_OUTPUT" : DATA_FOLDER + os.sep + "comext" + os.sep + PREFIX_MAP[PREFIX_TRANSPORT] + os.sep + "monthly" + os.sep + "output",
}

FILENAMES = {
    "SQLLITE_DB" : "comext.db",

    "GENERAL_INFO": "metadata.json",

    "IEINFO" : "ieinfo.json",

    "IMPORT_SERIES_JSON" : "importseries.json",
    "EXPORT_SERIES_JSON" : "exportseries.json",
    "QUOTE_TRADE_JSON" : "quoteTrade.json",
    "IMPORT_QUANTITY_JSON" : "importQuantity.json",
    "EXPORT_QUANTITY_JSON" : "exportQuantity.json",
    "IMPORT_QUOTE_QUANTITY_JSON" : "importQuoteQuantity.json",
    "EXPORT_QUOTE_QUANTITY_JSON" : "exportQuoteQuantity.json",
    "IMPORT_VALUE_JSON" : "importValue.json",
    "EXPORT_VALUE_JSON" : "exportValue.json",
    "IMPORT_QUOTE_VALUE_JSON" : "importQuoteValue.json",
    "EXPORT_QUOTE_VALUE_JSON" : "exportQuoteValue.json",

    "COMEXT_IMP_CSV" : "comext_imp.csv",
    "COMEXT_EXP_CSV" : "comext_exp.csv",
    "CPA_INTRA_CSV" : "cpa_intra.csv",
    "CPA_TRIM_CSV" : "cpa_trim.csv",
    "CPA2_PRODUCT_CODE_CSV" : "cpa2_products.csv",
    "CPA3_PRODUCT_CODE_CSV" : "cpa3_products.csv",

    "CLS_PRODUCT_DAT" : "cls_products.dat",
    "CLS_CPA" : "cls_products_CPA21.txt",
    "CLS_CPA_3D_ITA" : "cls_products_CPA21_3D_ITA.txt",
    "CLS_CPA_2D_ITA" : "cls_products_CPA21_2D_ITA.txt",
    "CLS_NSTR" : "NSTR.txt",
    "CLS_NSTR_ITA" : "NSTR_ITA.txt",

    "TR_EXTRA_UE_CSV" : "tr_extra_ue.csv",
    "TR_PRODUCT_CODE_CSV" : "tr_products_code.csv",
    "TR_EXTRA_UE_TRIMESTRALI_CSV" : "tr_extra_ue_trim.csv",

    "ANNUAL_POPULATION_CSV" : "annual_population.csv",
    "ANNUAL_INDUSTRIAL_PRODUCTION_CSV" : "annual_industrial_production.csv",
    "ANNUAL_UNEMPLOYEMENT_CSV" : "annual_unemployment.csv"
}

FILES = {
    "GENERAL_INFO" : DIRECTORIES["ROOT"] + os.sep + FILENAMES["GENERAL_INFO"],

    "SQLLITE_DB" : DIRECTORIES["PRODUCT"] + os.sep + FILENAMES["SQLLITE_DB"],

    "CLS_PRODUCT_DAT" : DIRECTORIES["CLASSIFICATION"] + os.sep + FILENAMES["CLS_PRODUCT_DAT"],
    "CLS_CPA" : DIRECTORIES["CLASSIFICATION"] + os.sep + FILENAMES["CLS_CPA"],
    "CLS_CPA_3D_ITA" : DIRECTORIES["CLASSIFICATION"] + os.sep + FILENAMES["CLS_CPA_3D_ITA"],
    "CLS_CPA_2D_ITA" : DIRECTORIES["CLASSIFICATION"] + os.sep + FILENAMES["CLS_CPA_2D_ITA"],
    "CLS_NSTR" : DIRECTORIES["CLASSIFICATION"] + os.sep + FILENAMES["CLS_NSTR"],
    "CLS_NSTR_ITA" : DIRECTORIES["CLASSIFICATION"] + os.sep + FILENAMES["CLS_NSTR_ITA"],
    
    "ANNUAL_POPULATION_CSV" : DIRECTORIES["UTILS"] + os.sep + FILENAMES["ANNUAL_POPULATION_CSV"],
    "ANNUAL_INDUSTRIAL_PRODUCTION_CSV" : DIRECTORIES["UTILS"] + os.sep + FILENAMES["ANNUAL_INDUSTRIAL_PRODUCTION_CSV"],
    "ANNUAL_UNEMPLOYEMENT_CSV" : DIRECTORIES["UTILS"] + os.sep + FILENAMES["ANNUAL_UNEMPLOYEMENT_CSV"],

    "IEINFO" : DIRECTORIES["PRODUCT_ANNUAL_OUTPUT"] + os.sep + FILENAMES["IEINFO"],

    "COMEXT_IMP_CSV" : DIRECTORIES["PRODUCT_MONTHLY_OUTPUT"] + os.sep + FILENAMES["COMEXT_IMP_CSV"],
    "COMEXT_EXP_CSV" : DIRECTORIES["PRODUCT_MONTHLY_OUTPUT"] + os.sep + FILENAMES["COMEXT_EXP_CSV"],
    "CPA_INTRA_CSV" : DIRECTORIES["PRODUCT_MONTHLY_OUTPUT"] + os.sep + FILENAMES["CPA_INTRA_CSV"],
    "CPA_TRIM_CSV" : DIRECTORIES["PRODUCT_MONTHLY_OUTPUT"] + os.sep + FILENAMES["CPA_TRIM_CSV"],
    "CPA2_PRODUCT_CODE_CSV" : DIRECTORIES["PRODUCT_MONTHLY_OUTPUT"] + os.sep + FILENAMES["CPA2_PRODUCT_CODE_CSV"],
    "CPA3_PRODUCT_CODE_CSV" : DIRECTORIES["PRODUCT_MONTHLY_OUTPUT"] + os.sep + FILENAMES["CPA3_PRODUCT_CODE_CSV"],

    "IMPORT_SERIES_JSON" : DIRECTORIES["PRODUCT_MONTHLY_OUTPUT"] + os.sep + FILENAMES["IMPORT_SERIES_JSON"],
    "EXPORT_SERIES_JSON" : DIRECTORIES["PRODUCT_MONTHLY_OUTPUT"] + os.sep + FILENAMES["EXPORT_SERIES_JSON"],
    "QUOTE_TRADE_JSON" : DIRECTORIES["PRODUCT_MONTHLY_OUTPUT"] + os.sep + FILENAMES["QUOTE_TRADE_JSON"],
    "IMPORT_QUANTITY_JSON" : DIRECTORIES["PRODUCT_MONTHLY_OUTPUT"] + os.sep + FILENAMES["IMPORT_QUANTITY_JSON"],
    "EXPORT_QUANTITY_JSON" : DIRECTORIES["PRODUCT_MONTHLY_OUTPUT"] + os.sep + FILENAMES["EXPORT_QUANTITY_JSON"],
    "IMPORT_QUOTE_QUANTITY_JSON" : DIRECTORIES["PRODUCT_MONTHLY_OUTPUT"] + os.sep + FILENAMES["IMPORT_QUOTE_QUANTITY_JSON"],
    "EXPORT_QUOTE_QUANTITY_JSON" : DIRECTORIES["PRODUCT_MONTHLY_OUTPUT"] + os.sep + FILENAMES["EXPORT_QUOTE_QUANTITY_JSON"],
    "IMPORT_VALUE_JSON" : DIRECTORIES["PRODUCT_MONTHLY_OUTPUT"] + os.sep + FILENAMES["IMPORT_VALUE_JSON"],
    "EXPORT_VALUE_JSON" : DIRECTORIES["PRODUCT_MONTHLY_OUTPUT"] + os.sep + FILENAMES["EXPORT_VALUE_JSON"],
    "IMPORT_QUOTE_VALUE_JSON" : DIRECTORIES["PRODUCT_MONTHLY_OUTPUT"] + os.sep + FILENAMES["IMPORT_QUOTE_VALUE_JSON"],
    "EXPORT_QUOTE_VALUE_JSON" : DIRECTORIES["PRODUCT_MONTHLY_OUTPUT"] + os.sep + FILENAMES["EXPORT_QUOTE_VALUE_JSON"],

    "TR_EXTRA_UE_CSV" : DIRECTORIES["TRANSPORT_MONTHLY_OUTPUT"] + os.sep + FILENAMES["TR_EXTRA_UE_CSV"],
    "TR_PRODUCT_CODE_CSV" : DIRECTORIES["TRANSPORT_MONTHLY_OUTPUT"] + os.sep + FILENAMES["TR_PRODUCT_CODE_CSV"],
    "TR_EXTRA_UE_TRIMESTRALI_CSV" : DIRECTORIES["TRANSPORT_MONTHLY_OUTPUT"] + os.sep + FILENAMES["TR_EXTRA_UE_TRIMESTRALI_CSV"],
}
