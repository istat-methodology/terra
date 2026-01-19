import os
import datetime
from dateutil.relativedelta import relativedelta
import numpy as np

RUN_DOWNLOAD          : bool = os.getenv("RUN_DOWNLOAD", "1") == "1"
RUN_ANNUAL_PROCESSING : bool = os.getenv("RUN_ANNUAL_PROCESSING", "1") == "1"
RUN_MONTHLY_PROCESSING: bool = os.getenv("RUN_MONTHLY_PROCESSING", "1") == "1"
RUN_OUTPUT            : bool = os.getenv("RUN_OUTPUT", "1") == "1"
RUN_UTILS             : bool = os.getenv("RUN_UTILS", "1") == "1"

WORKING_FOLDER        : str  = os.environ['WORKING_FOLDER']

KEY_VAULT_NAME        : str  = os.getenv("KEY_VAULT_NAME", "")
SECRETNAME_ACCOUNTKEY : str  = "cosmostoragekey"

URL_JSONDATA_SERVER         : str  = "https://api.cosmo.statlab.it/cls"
URL_PYTHON_SERVER_TS        : str  = "https://api.cosmo.statlab.it/time-series"
URL_PYTHON_SERVER_GRAPH     : str  = "https://api.cosmo.statlab.it/graph"

SHARE_NAME : dict[str, str] = {
    "JSON": os.getenv("SHARENAME_PREFIX", "istat-cosmo-data-") + "json"
}

DB_SETTINGS : dict[str, str] = {
    "DB_PROVIDER" : os.getenv('DB_PROVIDER', 'mssql+pyodbc'),
    "DB_SERVER" : os.getenv('DB_SERVER'),
    "DB_NAME" : os.getenv('DB_NAME'),
    "DB_DRIVER" : os.getenv('DB_DRIVER'),
    "DB_USER" : os.getenv('DB_USER'),
    "DB_PASS" : os.getenv('DB_PASS'),
    "DB_CONNECTIONSTRING_SECRET": os.getenv('DB_CONNECTIONSTRING_SECRET', '')
}

DB_SCHEMAS : dict[str, str] = {
    "STAGING" : "raw",
    "TEMP" : "temp",
    "PROD" : "dbo"
}

MAIL_SETTINGS         : dict[str, str]  = {
    "URL": os.getenv("LOGICAPP_URL"),
    "TO" : os.getenv("MAIL_RECIPIENTS"),
    "SUBJECT" : os.getenv("MAIL_SUBJECT", "Repo from cosmo update")
}

# SET TIME INTERVAL (IN MONTHS) FOR DOWNLOAD
OFFSET_M                          : int = int(os.getenv("OFFSET_M", "3"))
DOWNLOAD_TIME_INTERVAL_PRODUCT_M  : int = int(os.getenv("DOWNLOAD_TIME_INTERVAL_PRODUCT_M", "144"))
DOWNLOAD_TIME_INTERVAL_TRANSPORT_M: int = int(os.getenv("DOWNLOAD_TIME_INTERVAL_TRANSPORT_M", "60"))
MAX_RETRY                         : int = int(os.getenv("MAX_RETRY", "5"))
RETRY_WAIT                        : int = int(os.getenv("RETRY_WAIT", "5"))

# TIME INTERVAL FOR PROCESSING
PAGE_MAP_TIME_INTERVAL_M           : int = int(os.getenv("PAGE_MAP_TIME_INTERVAL_M", "60"))
PAGE_TIME_SERIES_TIME_INTERVAL_M   : int = int(os.getenv("PAGE_TIME_SERIES_TIME_INTERVAL_M", "60"))
PAGE_GRAPH_EXTRA_UE_TIME_INTERVAL_M: int = int(os.getenv("PAGE_GRAPH_EXTRA_UE_TIME_INTERVAL_M", "60"))
PAGE_GRAPH_INTRA_UE_TIME_INTERVAL_M: int = int(os.getenv("PAGE_GRAPH_INTRA_UE_TIME_INTERVAL_M", "60"))
PAGE_BASKET_TIME_INTERVAL_M        : int = int(os.getenv("PAGE_BASKET_TIME_INTERVAL_M", "60"))

PREFIX_PRODUCT  : str = "full_v2_"
PREFIX_TRANSPORT: str = "nst07_extra_v2_"
PREFIX_MAP      : dict[str, str] = {
  "nst07_extra_v2_": "transport",
  "full_v2_": "product"
}

FLOW_IMPORT        : int = 1
FLOW_EXPORT        : int = 2
COLS_CLS_PRODUCTS  : int = 4
SUPPORTED_LANGUAGES: list[str] = ["it", "en"]
DATA_EXTENTION     : str = ".dat"
SEP                : str = ","

job_id = os.getenv("AZ_BATCH_JOB_ID", "").replace(":", "_")
DATA_FOLDER_PARENT = (
    WORKING_FOLDER + os.sep + "data" + (("__" + job_id) if (job_id != "") else "")
)

processing_day = datetime.datetime.today()  - relativedelta(years=4)
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

start_data_DOWNLOAD_PRODUCT = (
    datetime.datetime.strptime(str(this_year_month), "%Y%m")
    - relativedelta(months=OFFSET_M)
    - relativedelta(months=DOWNLOAD_TIME_INTERVAL_PRODUCT_M - 1)
)
start_data_DOWNLOAD_TRANSPORT = (
    datetime.datetime.strptime(str(this_year_month), "%Y%m")
    - relativedelta(months=OFFSET_M)
    - relativedelta(months=DOWNLOAD_TIME_INTERVAL_TRANSPORT_M - 1)
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

DATA_FOLDER: str = DATA_FOLDER_PARENT + os.sep + str(this_year_month)

URLS: dict[str] = {
    "ANNUAL_POPULATION" : "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/DEMO_GIND/?format=SDMX-CSV&i",
    "ANNUAL_INDUSTRIAL_PRODUCTION" : "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/STS_INPR_A/?format=SDMX-CSV&i",
    "ANNUAL_UNEMPLOYEMENT" : "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/UNE_RT_A/?format=SDMX-CSV&i",

    "COMEXT_PRODUCTS" : "https://ec.europa.eu/eurostat/api/dissemination/files/?sort=1&downfile=comext%2FCOMEXT_DATA%2FPRODUCTS%2F",
    "COMEXT_TR" : "https://ec.europa.eu/eurostat/api/dissemination/files/?sort=1&file=comext%2FCOMEXT_DATA%2FTRANSPORT_NST07%2F",

    "CLS_PRODUCTS" : "https://ec.europa.eu/eurostat/api/dissemination/files/?sort=1&file=comext%2FCOMEXT_METADATA%2FCLASSIFICATIONS_AND_RELATIONS%2FCLASSIFICATIONS%2FENGLISH%2FCN.txt",
    
    "CLS_NSTR" : "https://ec.europa.eu/eurostat/api/dissemination/files/?sort=1&file=comext%2FCOMEXT_METADATA%2FCLASSIFICATIONS_AND_RELATIONS%2FCLASSIFICATIONS%2FENGLISH%2FNST2007.txt",
    "CLS_NSTR_ITA" : "https://raw.githubusercontent.com/istat-methodology/terra/main/cls/Prodotti_NSTR_2007_ita.csv",
    
    "CLS_CPA" : "https://ec.europa.eu/eurostat/api/dissemination/files/?sort=1&file=comext%2FCOMEXT_METADATA%2FCLASSIFICATIONS_AND_RELATIONS%2FCLASSIFICATIONS%2FENGLISH%2FCPA21.txt",
    "CLS_CPA_3D_ITA" : "https://raw.githubusercontent.com/istat-methodology/terra/main/cls/CPA_2_1_3digits_ita.csv",
    "CLS_CPA_2D_ITA" : "https://raw.githubusercontent.com/istat-methodology/terra/main/cls/cpa2.1_2digit_ita.csv"   
}

DIRECTORIES: dict[str] = {
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

FILENAMES: dict[str] = {
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

FILES: dict[str] = {
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

STORAGE_ACCOUNT_FOLDER_LIST: dict[str, list[str]] = {
        f"{SHARE_NAME['JSON']}": ['map', 'trade', 'classification', 'general']
    }

DB_FILE_MAPPING: dict[str] = {
    FILES["COMEXT_IMP_CSV"] : "comext_imp",
    FILES["COMEXT_EXP_CSV"] : "comext_exp",
    FILES["CPA_INTRA_CSV"] : "cpa_intra",
    FILES["CPA_TRIM_CSV"] : "cpa_trim",
    FILES["TR_EXTRA_UE_CSV"] : "tr_extra_ue",
    FILES["TR_EXTRA_UE_TRIMESTRALI_CSV"] : "tr_extra_ue_trim"
}

PRODUCT_COLNAMES = [
    "DECLARANT_ISO",
    "PARTNER_ISO",
    "TRADE_TYPE",
    "PRODUCT_NC",
    "PRODUCT_SITC",
    "PRODUCT_CPA2_1",
    "PRODUCT_CPA2_2",
    "PRODUCT_BEC",
    "PRODUCT_BEC5",
    "PRODUCT_SECTION",
    "FLOW",
    "STAT_REGIME",
    "SUPP_UNIT",
    "PERIOD",
    "VALUE_IN_EUROS",
    "VALUE_NAC",
    "QUANTITY_IN_KG",
    "SUP_QUANTITY"
]

TRANSPORT_COLNAMES = [
    "DECLARANT_ISO",
    "PARTNER_ISO",
    "PRODUCT_NSTR",
    "FLOW",
    "TRANSPORT_MODE",
    "CONTAINER",
    "PERIOD",
    "VALUE_IN_EUROS",
    "VALUE_NAC",
    "QUANTITY_IN_KG"
]

DB_COLUMN_TYPE = {
    'comext_imp': {
        'DECLARANT_ISO': str,
        'PARTNER_ISO': str,
        'FLOW': int,
        'cpa': str,
        'PERIOD': int,
        'val_cpa': np.float64,
        'q_kg': np.float64
        },
    'comext_exp': {
        'DECLARANT_ISO': str,
        'PARTNER_ISO': str,
        'FLOW': int,
        'cpa': str,
        'PERIOD': int,
        'val_cpa': np.float64,
        'q_kg': np.float64
        },
    'cpa_intra': {
        'DECLARANT_ISO': str,
        'PARTNER_ISO': str,
        'FLOW': int,
        'PRODUCT': str,
        'PERIOD': np.float64,
        'VALUE_IN_EUROS': np.float64
        },
    'cpa_trim': {
        'DECLARANT_ISO': str,
        'PARTNER_ISO': str,
        'FLOW': int,
        'cpa': str,
        'trimestre': str,
        'val_cpa': np.float64,
        'q_kg': np.float64
        },
    'tr_extra_ue': {
        'PRODUCT_NSTR': str,
        'DECLARANT_ISO': str,
        'PARTNER_ISO': str,
        'PERIOD': int,
        'TRANSPORT_MODE': int,
        'FLOW': int,
        'VALUE_IN_EUROS': np.float64,
        'QUANTITY_IN_KG': np.float64
        },
    'tr_extra_ue_trim': {
        'PRODUCT_NSTR': str,
        'DECLARANT_ISO': str,
        'PARTNER_ISO': str,
        'TRIMESTRE': str,
        'TRANSPORT_MODE': int,
        'FLOW': int,
        'VALUE_IN_EUROS': np.float64,
        'QUANTITY_IN_KG': np.float64
        },
}
