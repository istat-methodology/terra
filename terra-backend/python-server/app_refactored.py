from resources import py_server_params
from execute.py_server_execute import data_loading
from modules.py_server_functions import PyServerLogger, ApplicationInsightsSetup

# CONFIGS
FILE_SEP    = ","
PROD_DIGITS = 3  # number of digits to classify transports
MAX_NODES   = 70
CHUNCK_SIZE = 5

CRITERION       = "VALUE_IN_EUROS"  # VALUE_IN_EUROS QUANTITY_IN_KG

# Preliminaries
logger = PyServerLogger.get_logger()
ApplicationInsightsSetup.azure_setup(logger=logger)

# Data Loading
dfs, info = data_loading(
    logger=logger,
    paths=py_server_params.file_paths,
    filenames=py_server_params.file_names,
    labels=py_server_params.file_labels,
    column_names=py_server_params.file_column_names,
    dtypes=py_server_params.file_dtypes,
    product_digits=py_server_params.product_digits
)

print(info)