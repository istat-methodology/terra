import os
import datetime

WORKING_FOLDER=os.environ['WORKING_FOLDER']
#WORKING_FOLDER = "C:" + os.sep + "Users" + os.sep + "UTENTE" + os.sep + "terra_output"
PREFIX_FULL = "full"
PREFIX_TRANSPORT = "tr"
PREFIX_MAP = {
  "tr": "transport",
  "full": "product"
}
job_id = os.getenv("AZ_BATCH_JOB_ID", "").replace(":", "_")
DATA_FOLDER_PARENT = (
    WORKING_FOLDER + os.sep + "data" + (("__" + job_id) if (job_id != "") else "")
)

processing_day = datetime.datetime.today()
this_year = processing_day.year
this_month = "%02d" % processing_day.month
DATA_FOLDER = DATA_FOLDER_PARENT + os.sep + str(this_year) + str(this_month)

URLS = {
    "ANNUAL_POPULATION" : "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/DEMO_GIND/?format=SDMX-CSV&i",
    "ANNUAL_INDUSTRIAL_PRODUCTION" : "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/STS_INPR_A/?format=SDMX-CSV&i",
    "ANNUAL_UNEMPLOYEMENT" : "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/UNE_RT_A/?format=SDMX-CSV&i",

    # NEW ENDPOINT: https://ec.europa.eu/eurostat/api/dissemination/files/?sort=1&dir=comext%2FCOMEXT_DATA%2FPRODUCTS
    "COMEXT_PRODUCTS" : "https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?sort=1&file=comext%2FCOMEXT_DATA%2FPRODUCTS%2F",
    
    # NEW ENDPOINT: https://ec.europa.eu/eurostat/api/dissemination/files/?sort=1&dir=comext%2FCOMEXT_DATA%2FTRANSPORT_NSTR
    "COMEXT_TR" : "https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?sort=1&file=comext%2FCOMEXT_DATA%2FTRANSPORT_NSTR%2F",
    
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
    "dir_classification" : DATA_FOLDER + os.sep + "classification",

    "dir_utils" : DATA_FOLDER + os.sep + "utils",

    "dir_product_annual_zip" : DATA_FOLDER + os.sep + "comext" + os.sep + PREFIX_MAP[PREFIX_FULL] + os.sep + "annual" + os.sep + "zip",
    "dir_product_annual_file" : DATA_FOLDER + os.sep + "comext" + os.sep + PREFIX_MAP[PREFIX_FULL] + os.sep + "annual" + os.sep + "file",
    "dir_product_annual_output" : DATA_FOLDER + os.sep + "comext" + os.sep + PREFIX_MAP[PREFIX_FULL] + os.sep + "annual" + os.sep + "output",

    "dir_product_monthly_zip" : DATA_FOLDER + os.sep + "comext" + os.sep + PREFIX_MAP[PREFIX_FULL] + os.sep + "monthly" + os.sep + "zip",
    "dir_product_monthly_file" : DATA_FOLDER + os.sep + "comext" + os.sep + PREFIX_MAP[PREFIX_FULL] + os.sep + "monthly" + os.sep + "file",
    "dir_product_monthly_output" : DATA_FOLDER + os.sep + "comext" + os.sep + PREFIX_MAP[PREFIX_FULL] + os.sep + "monthly" + os.sep + "output",

    "dir_transport_montly_zip" : DATA_FOLDER + os.sep + "comext" + os.sep + PREFIX_MAP[PREFIX_TRANSPORT] + os.sep + "monthly" + os.sep + "zip",
    "dir_transport_montly_file" : DATA_FOLDER + os.sep + "comext" + os.sep + PREFIX_MAP[PREFIX_TRANSPORT] + os.sep + "monthly" + os.sep + "file",
    "dir_transport_montly_output" : DATA_FOLDER + os.sep + "comext" + os.sep + PREFIX_MAP[PREFIX_TRANSPORT] + os.sep + "monthly" + os.sep + "output",
}

FILENAMES = {
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

    "TR_EXTRA_UE_CSV" : "tr_extra_ue.csv",
    "TR_PRODUCT_CODE_CSV" : "tr_products_code.csv",
    "TR_EXTRA_UE_TRIMESTRALI_CSV" : "tr_extra_ue_trim.csv",

    "ANNUAL_POPULATION_CSV" : "annual_population.csv",
    "ANNUAL_INDUSTRIAL_PRODUCTION_CSV" : "annual_industrial_production.csv",
    "ANNUAL_UNEMPLOYEMENT_FILE_CSV" : "annual_unemployment.csv"
}
