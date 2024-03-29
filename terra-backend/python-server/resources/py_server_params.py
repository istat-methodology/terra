import os
import numpy as np

product_digits: int = 3

######## ENVIRONMENT VARIABLES #########

RUN_LOCAL = True

DB_SETTINGS : dict = {
    "DB_PROVIDER" : '',
    "DB_SERVER" : '',
    "DB_NAME" : '',
    "DB_DRIVER" : '',
    "DB_USER" : '',
    "DB_PASS" : ''
}

########################################

ENDPOINT_SETTINGS: dict = {
    "CRITERION": "VALUE_IN_EUROS", # VALUE IN EUROS | QUANTITY_IN_KG
    "MAX_NODES": 70,
    "CHUNK_SIZE": 5
}

file_names = {
    "Intra File"           : "INTRA_FILE",
    "Intra Quarterly File" : "INTRA_QUARTERLY_FILE",
    "Extra File"           : "EXTRA_FILE",
    "Extra Quarterly File" : "EXTRA_QUARTERLY_FILE",
}

abs_data_path = f"{os.path.dirname(os.getcwd())}{os.sep}terra{os.sep}terra-backend{os.sep}python-server{os.sep}data"

file_paths = {
    file_names['Intra File']           : abs_data_path + os.sep + "cpa_intra.csv",
    file_names['Extra File']           : abs_data_path + os.sep + "tr_extra_ue.csv",
    file_names['Intra Quarterly File'] : abs_data_path + os.sep + "cpa_trim.csv",
    file_names["Extra Quarterly File"] : abs_data_path + os.sep + "tr_extra_ue_trim.csv"   
}

file_dtypes = {
    file_names['Intra File']           : {"PRODUCT": object, "FLOW": np.int8, "PERIOD": np.int32, "TRANSPORT_MODE": np.int8},
    file_names['Extra File']           : {"PRODUCT_NSTR": object, "FLOW": np.int8, "PERIOD": np.int32, "TRANSPORT_MODE": np.int8},
    file_names['Intra Quarterly File'] : {"cpa": object, "FLOW": np.int8},
    file_names["Extra Quarterly File"] : {"PRODUCT_NSTR": object, "FLOW": np.int8}
}

file_labels = {
    "Declarant"      : "DECLARANT_ISO",
    "Partner"        : "PARTNER_ISO",
    "Transport"      : "TRANSPORT_MODE",
    "Flow"           : "FLOW",
    "Date"           : "PERIOD",
    "Product"        : "PRODUCT",
    "Value"          : "VALUE_IN_EUROS",
    "Quantity"       : "QUANTITY_IN_KG"
}

file_column_names = {
    
    file_names['Intra File'] : {
        "DECLARANT_ISO"  : file_labels["Declarant"],
        "PARTNER_ISO"    : file_labels["Partner"],
        "FLOW"           : file_labels["Flow"],
        "PRODUCT"        : file_labels["Product"],
        "PERIOD"         : file_labels["Date"],
        "VALUE_IN_EUROS" : file_labels["Value"]
    },

    file_names['Intra Quarterly File'] : {
        "DECLARANT_ISO"  : file_labels["Declarant"], 
        "PARTNER_ISO"    : file_labels["Partner"], 
        "FLOW"           : file_labels["Flow"], 
        "cpa"            : file_labels["Product"], 
        "trimestre"      : file_labels["Date"], 
        "val_cpa"        : file_labels["Value"]
        },
    
    file_names['Extra File'] : {
        "DECLARANT_ISO"  : file_labels["Declarant"],
        "PARTNER_ISO"    : file_labels["Partner"],
        "TRANSPORT_MODE" : file_labels["Transport"],
        "FLOW"           : file_labels["Flow"],
        "PRODUCT_NSTR"   : file_labels["Product"],
        "PERIOD"         : file_labels["Date"],
        "VALUE_IN_EUROS" : file_labels["Value"],
        "QUANTITY_IN_KG" : file_labels["Quantity"]
    },

    file_names['Extra Quarterly File'] : {
        "DECLARANT_ISO"  : file_labels["Declarant"],
        "PARTNER_ISO"    : file_labels["Partner"],
        "TRANSPORT_MODE" : file_labels["Transport"],
        "FLOW"           : file_labels["Flow"],
        "PRODUCT_NSTR"   : file_labels["Product"],
        "TRIMESTRE"      : file_labels["Date"],
        "VALUE_IN_EUROS" : file_labels["Value"]
    },
}