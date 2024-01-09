import os
import json
import pandas as pd
import numpy as np
from dateutil.rrule import rrule, MONTHLY
import datetime
import zipfile
import urllib.request
import time
import shutil

try:
    from azure.storage.file import FileService
    from azure.keyvault.secrets import SecretClient
    from azure.identity import DefaultAzureCredential
except:
    print('Azure libraries not imported')

import params

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)

def month_iter(start_month, start_year, end_month, end_year):
    start = datetime.datetime(start_year, start_month, 1)
    end = datetime.datetime(end_year, end_month, 1)
    return (('%02d' %d.month, d.year) for d in rrule(MONTHLY, dtstart=start, until=end))

def createFolder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def createFolderStructure(folderDict):
    for key, value in folderDict.items():
        createFolder(value)
    
    return "Folder structure created"

def getPassedTime(initial_time):
    return str(datetime.datetime.now() - initial_time)

def getValueFromList(clsRow, code, position):
    ret = ""
    if (len(clsRow) > 0) & (len(clsRow.columns) >= position):
        ret = clsRow.iat[0, position]
    else:
        ret = code
    return "" if pd.isnull(ret) else ret

def getClsProduct(clsRow, codeProduct, position=(params.COLS_CLS_PRODUCTS - 1)):
    if (len(clsRow) > 0) & (len(clsRow.columns) >= position):
        return clsRow.iat[0, position]
    else:
        return codeProduct

def getClsProductByCode(cls_products, product, position=(params.COLS_CLS_PRODUCTS - 1)):
    return getClsProduct(cls_products[cls_products[0] == product], product, position)

##### AZURE UTILS #####
def copyFileToAzure(storage, folder, path_file_source, logger):
    logger.info("copyFileToAzure START:" + os.path.basename(path_file_source))

    storage_account_key = os.getenv("STORAGE_ACCOUNT_KEY", "")
    if storage_account_key == "":
        kvclient = SecretClient(
            vault_url=f"https://{params.KEY_VAULT_NAME}.vault.azure.net",
            credential=DefaultAzureCredential(),
        )
        storage_account_key = kvclient.get_secret(params.SECRETNAME_ACCOUNTKEY).value

    fileService = FileService(
        account_name=os.environ["STORAGE_ACCOUNT_NAME"], account_key=storage_account_key
    )
    fileService.create_file_from_path(
        storage, folder, os.path.basename(path_file_source), path_file_source
    )
    logger.info("copyFileToAzure END: " + os.path.basename(path_file_source))
    return "copyFileToAzure END: " + os.path.basename(path_file_source)


def exportOutputs(logger):
    logger.info("exportOutputs START")

    # LOCAL FOLDER
    OUTPUT_CLASS_FOLDER = params.DIRECTORIES["CLASSIFICATION"] + os.sep

    # JSON-SERVER
    copyFileToAzure("istat-cosmo-data-json", "general", params.FILES["GENERAL_INFO"] , logger)
    copyFileToAzure("istat-cosmo-data-json", "map", params.FILES["IEINFO"] , logger)
    copyFileToAzure("istat-cosmo-data-json", "map", params.FILES["IMPORT_SERIES_JSON"] , logger)
    copyFileToAzure("istat-cosmo-data-json", "map", params.FILES["EXPORT_SERIES_JSON"] , logger)

    copyFileToAzure("istat-cosmo-data-json", "trade", params.FILES["IMPORT_QUANTITY_JSON"] , logger)
    copyFileToAzure("istat-cosmo-data-json", "trade", params.FILES["EXPORT_QUANTITY_JSON"] , logger)
    copyFileToAzure("istat-cosmo-data-json", "trade", params.FILES["IMPORT_VALUE_JSON"] , logger)
    copyFileToAzure("istat-cosmo-data-json", "trade", params.FILES["EXPORT_VALUE_JSON"] , logger)

    copyFileToAzure("istat-cosmo-data-json", "trade", params.FILES["IMPORT_QUOTE_QUANTITY_JSON"] , logger)
    copyFileToAzure("istat-cosmo-data-json", "trade", params.FILES["EXPORT_QUOTE_QUANTITY_JSON"] , logger)
    copyFileToAzure("istat-cosmo-data-json", "trade", params.FILES["IMPORT_QUOTE_VALUE_JSON"] , logger)
    copyFileToAzure("istat-cosmo-data-json", "trade", params.FILES["EXPORT_QUOTE_VALUE_JSON"] , logger)

    copyFileToAzure("istat-cosmo-data-json", "classification", OUTPUT_CLASS_FOLDER + "clsProductsCPA.json" , logger)
    copyFileToAzure("istat-cosmo-data-json","classification",OUTPUT_CLASS_FOLDER + "clsProductsGraphExtraNSTR.json" , logger)
    copyFileToAzure("istat-cosmo-data-json","classification",OUTPUT_CLASS_FOLDER + "clsProductsGraphIntra.json" , logger)

    # R-SERVER
    copyFileToAzure("istat-cosmo-data-r", None, params.FILES["COMEXT_IMP_CSV"] , logger)
    copyFileToAzure("istat-cosmo-data-r", None, params.FILES["COMEXT_EXP_CSV"] , logger)

    # Python-SERVER
    copyFileToAzure("istat-cosmo-data-python", None, params.FILES["CPA_INTRA_CSV"] , logger)
    copyFileToAzure("istat-cosmo-data-python", None, params.FILES["CPA_TRIM_CSV"] , logger)
    copyFileToAzure("istat-cosmo-data-python", None, params.FILES["TR_EXTRA_UE_CSV"] , logger)
    copyFileToAzure("istat-cosmo-data-python", None, params.FILES["TR_EXTRA_UE_TRIMESTRALI_CSV"] , logger)

    logger.info("exportOutputs END")
    return "exportOutputs END"

def createAndSendBackupFiles(logger):
    logger.info("createAndSendBackupFiles START")

    OUTPUT_ROOT_FOLDER = params.DATA_FOLDER + os.sep
    OUTPUT_CLASS_FOLDER = params.DIRECTORIES["CLASSIFICATION"] + os.sep

    listFiles = [
        params.FILES["GENERAL_INFO"],
        params.FILES["IEINFO"],
        params.FILES["IMPORT_SERIES_JSON"],
        params.FILES["EXPORT_SERIES_JSON"],
        params.FILES["IMPORT_QUANTITY_JSON"],
        params.FILES["EXPORT_QUANTITY_JSON"],
        params.FILES["IMPORT_VALUE_JSON"],
        params.FILES["EXPORT_VALUE_JSON"],
        params.FILES["IMPORT_QUOTE_QUANTITY_JSON"],
        params.FILES["EXPORT_QUOTE_QUANTITY_JSON"],
        params.FILES["IMPORT_QUOTE_VALUE_JSON"],
        params.FILES["EXPORT_QUOTE_VALUE_JSON"],
        OUTPUT_CLASS_FOLDER + "clsProductsCPA.json",
        OUTPUT_CLASS_FOLDER + "clsProductsGraphExtraNSTR.json",
        OUTPUT_CLASS_FOLDER + "clsProductsGraphIntra.json",
        params.FILES["COMEXT_IMP_CSV"],
        params.FILES["COMEXT_EXP_CSV"],
        params.FILES["CPA_INTRA_CSV"],
        params.FILES["CPA_TRIM_CSV"],
        params.FILES["TR_EXTRA_UE_CSV"],
        params.FILES["TR_EXTRA_UE_TRIMESTRALI_CSV"],
    ]

    fileZip = (
        OUTPUT_ROOT_FOLDER + "backup_" + str(params.this_year) + str(params.this_month) + ".zip"
    )
    print(fileZip)
    with zipfile.ZipFile(fileZip, "w", zipfile.ZIP_DEFLATED) as zipObj:
        # Iterate over all the files in list
        for filename in listFiles:
            zipObj.write(filename)

    copyFileToAzure("istat-cosmo-data-backup", "files", fileZip , logger)

    logger.info("createAndSendBackupFiles END")
    return "createAndSendBackupFiles END"


def deleteFolder(folder , logger):
    logger.info("deleteFolder ... " + folder)
    shutil.rmtree(folder, ignore_errors=True)
    return "Folder removed: " + folder + "<br/>\n"

# [MICROSERVICES] START AND STOP MICROSERVICES
def refreshMicroservicesDATA(logger):
    logger.info("refreshMicroservices DATA START")
    resultRefresh = ""
    try:
        contents = urllib.request.urlopen(
            params.URL_RDATA_SERVER + "/load-comext", timeout=300
        ).read()
        resultRefresh += "Refresh DATA R-SERVER OK<br/>\n"
        contents = urllib.request.urlopen(
            params.URL_JSONDATA_SERVER + "/stop", timeout=300
        ).read()
        resultRefresh += "Refresh DATA JSON-SERVER OK<br/>\n"
        contents = urllib.request.urlopen(
            params.URL_PYTHONDATA_SERVER + "/refreshdata", timeout=500
        ).read()
        resultRefresh += "Refresh DATA PYTHON-SERVER OK<br/>\n"
        time.sleep(30)
    except BaseException as e:
        resultRefresh += "ERRROR Refresh " + str(e)
    return resultRefresh


def checkUPMicroservices(logger):
    logger.info("checkUPMicroservices START")
    resultCall = ""
    try:
        call = urllib.request.urlopen(params.URL_RDATA_SERVER + "/hello", timeout=30).read()
        logger.info(str(call))
        resultCall += " Check UP R-SERVER OK<br/>\n"
        call = urllib.request.urlopen(params.URL_JSONDATA_SERVER + "/hello", timeout=30).read()
        logger.info(str(call))
        resultCall += " Check UP JSON-SERVER OK<br/>\n"
        call = urllib.request.urlopen(
            params.URL_PYTHONDATA_SERVER + "/hello", timeout=30
        ).read()
        logger.info(str(call))
        resultCall += " Check UP PYTHON-SERVER OK<br/>\n"
    except BaseException as e:
        resultCall += " ERRROR Refresh: " + str(e) + "<br/>\n"
        logger.info(" ERRROR Refresh: " + str(e) + "<br/>\n")

    logger.info("checkUPMicroservices END")

    return resultCall


def sendEmailRepo(report_text , logger):
    logger.info("sendEmailRepo START")
    url_Email_service = params.MAIL_SETTINGS["SERVER"]
    body_msg = {
        "to": params.MAIL_SETTINGS["TO"],
        "subject": params.MAIL_SETTINGS["SUBJECT"],
        "body": report_text,
    }

    req = urllib.request.Request(url_Email_service, method="POST")
    req.add_header("Content-Type", "application/json")

    data = json.dumps(body_msg)
    data = data.encode()
    r = urllib.request.urlopen(req, data=data)
    logger.info("sendEmailRepo END")

    return "sendEmailRepo END"
