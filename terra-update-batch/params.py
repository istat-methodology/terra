import os
import datetime
from dateutil.relativedelta import relativedelta

# SET TIME INTERVAL (IN MONTHS)
time_interval_m = 1
offset_m = 15

#WORKING_FOLDER=os.environ['WORKING_FOLDER']
WORKING_FOLDER = "C:" + os.sep + "Users" + os.sep + "UTENTE" + os.sep + "terra_output"
PREFIX_FULL = "full"
PREFIX_TRANSPORT = "tr"
PREFIX_MAP = {
  "tr": "transport",
  "full": "product"
}

FLOW_IMPORT = 1
FLOW_EXPORT = 2

SUPPORTED_LANGUAGES = ["it", "en"]

DATA_EXTENTION = ".dat"
SEP = ","

job_id = os.getenv("AZ_BATCH_JOB_ID", "").replace(":", "_")
DATA_FOLDER_PARENT = (
    WORKING_FOLDER + os.sep + "data" + (("__" + job_id) if (job_id != "") else "")
)

processing_day = datetime.datetime.today()
# processing_day = datetime.datetime.today() - relativedelta(months=1)
this_year = processing_day.year
this_month = "%02d" % processing_day.month
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

start_data_load = (
    datetime.datetime.strptime(str(this_year) + "-" + str(this_month), "%Y-%m")
    - relativedelta(months=offset_m)
    - relativedelta(months=time_interval_m - 1)
)
end_data_load = datetime.datetime.strptime(
    str(this_year) + "-" + str(this_month), "%Y-%m"
) - relativedelta(months=offset_m)

##### SET DATES FOR PAGES #####
start_data_PAGE_MAP = start_data_load
start_data_PAGE_TIME_SERIES = start_data_load
start_data_PAGE_GRAPH_EXTRA_UE = start_data_load
start_data_PAGE_GRAPH_INTRA_UE = start_data_load
start_data_PAGE_BASKET = start_data_load

DATA_FOLDER = DATA_FOLDER_PARENT + os.sep + str(this_year) + str(this_month)

URLS = {
    "ANNUAL_POPULATION" : "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/DEMO_GIND/?format=SDMX-CSV&i",
    "ANNUAL_INDUSTRIAL_PRODUCTION" : "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/STS_INPR_A/?format=SDMX-CSV&i",
    "ANNUAL_UNEMPLOYEMENT" : "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/UNE_RT_A/?format=SDMX-CSV&i",

    # NEW ENDPOINT: https://ec.europa.eu/eurostat/api/dissemination/files/?sort=1&dir=comext%2FCOMEXT_DATA%2FPRODUCTS
    "COMEXT_PRODUCTS" : "https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?sort=1&file=comext%2FCOMEXT_DATA%2FPRODUCTS%2F",
    
    # NEW ENDPOINT: https://ec.europa.eu/eurostat/api/dissemination/files/?sort=1&dir=comext%2FCOMEXT_DATA%2FTRANSPORT_NSTR
    # ACTUAL USED ENDPOINT: "https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?sort=1&file=comext%2FCOMEXT_DATA%2FTRANSPORT_NSTR%2F"
    "COMEXT_TR" : "https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?sort=1&file=comext%2FCOMEXT_HISTORICAL_DATA%2FTRANSPORT_BY_NSTR%2F",

    # NEW ENDPOINT: https://ec.europa.eu/eurostat/api/dissemination/files/?sort=1&file=comext%2FCOMEXT_METADATA%2FCLASSIFICATIONS_AND_RELATIONS%2FCLASSIFICATIONS%2FENGLISH%2FCN.txt
    "CLS_PRODUCTS" : "https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?sort=1&file=comext%2FCOMEXT_METADATA%2FCLASSIFICATIONS_AND_RELATIONS%2FCLASSIFICATIONS%2FENGLISH%2FCN.txt",
    
    # NEW ENDPOINT: https://ec.europa.eu/eurostat/api/dissemination/files/?sort=1&file=comext%2FCOMEXT_METADATA%2FCLASSIFICATIONS_AND_RELATIONS%2FCLASSIFICATIONS%2FENGLISH%2FNSTR.txt
    "CLS_NSTR" : "https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?sort=1&file=comext%2FCOMEXT_METADATA%2FCLASSIFICATIONS_AND_RELATIONS%2FCLASSIFICATIONS%2FENGLISH%2FNSTR.txt",
    "CLS_NSTR_ITA" : "https://raw.githubusercontent.com/istat-methodology/terra/main/cls/Prodotti_NSTR_ita.csv",

    # NEW ENDPOINT: https://ec.europa.eu/eurostat/api/dissemination/files/?sort=1&file=comext%2FCOMEXT_METADATA%2FCLASSIFICATIONS_AND_RELATIONS%2FCLASSIFICATIONS%2FENGLISH%2FCPA21.txt
    "CLS_CPA" : "https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?sort=1&file=comext%2FCOMEXT_METADATA%2FCLASSIFICATIONS_AND_RELATIONS%2FCLASSIFICATIONS%2FENGLISH%2FCPA21.txt",
    "CLS_CPA_3D_ITA" : "https://raw.githubusercontent.com/istat-methodology/terra/main/cls/CPA_2_1_3digits_ita.csv",
    "CLS_CPA_2D_ITA" : "https://raw.githubusercontent.com/istat-methodology/terra/main/cls/cpa2.1_2digit_ita.csv"   
}

DIRECTORIES = {
    "CLASSIFICATION" : DATA_FOLDER + os.sep + "classification",

    "UTILS" : DATA_FOLDER + os.sep + "utils",

    "PRODUCT_ANNUAL_ZIP" : DATA_FOLDER + os.sep + "comext" + os.sep + PREFIX_MAP[PREFIX_FULL] + os.sep + "annual" + os.sep + "zip",
    "PRODUCT_ANNUAL_FILE" : DATA_FOLDER + os.sep + "comext" + os.sep + PREFIX_MAP[PREFIX_FULL] + os.sep + "annual" + os.sep + "file",
    "PRODUCT_ANNUAL_OUTPUT" : DATA_FOLDER + os.sep + "comext" + os.sep + PREFIX_MAP[PREFIX_FULL] + os.sep + "annual" + os.sep + "output",

    "PRODUCT_MONTHLY" : DATA_FOLDER + os.sep + "comext" + os.sep + PREFIX_MAP[PREFIX_FULL] + os.sep + "monthly",
    "PRODUCT_MONTHLY_ZIP" : DATA_FOLDER + os.sep + "comext" + os.sep + PREFIX_MAP[PREFIX_FULL] + os.sep + "monthly" + os.sep + "zip",
    "PRODUCT_MONTHLY_FILE" : DATA_FOLDER + os.sep + "comext" + os.sep + PREFIX_MAP[PREFIX_FULL] + os.sep + "monthly" + os.sep + "file",
    "PRODUCT_MONTHLY_OUTPUT" : DATA_FOLDER + os.sep + "comext" + os.sep + PREFIX_MAP[PREFIX_FULL] + os.sep + "monthly" + os.sep + "output",

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
    "IMPORT_QUOTE_QUANTITY_JSON" : "exportQuoteQuantity.json",
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

    "ANNUAL_POPULATION" : "annual_population.csv",
    "ANNUAL_INDUSTRIAL_PRODUCTION" : "annual_industrial_production.csv",
    "ANNUAL_UNEMPLOYEMENT" : "annual_unemployment.csv",

    "TR_EXTRA_UE_CSV" : "tr_extra_ue.csv",
    "TR_PRODUCT_CODE_CSV" : "tr_products_code.csv",
    "TR_EXTRA_UE_TRIMESTRALI_CSV" : "tr_extra_ue_trim.csv",

    "ANNUAL_POPULATION_CSV" : "annual_population.csv",
    "ANNUAL_INDUSTRIAL_PRODUCTION_CSV" : "annual_industrial_production.csv",
    "ANNUAL_UNEMPLOYEMENT_FILE_CSV" : "annual_unemployment.csv"
}
