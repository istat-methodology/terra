# Version 2.0.1

import os
import re
import sys
from datetime import datetime
from resources import params
from execute import download, processing, output, misc
from dotenv import load_dotenv

load_dotenv()

logger = misc.get_logger()

if os.getenv("AZ_BATCH_APP_PACKAGE_cosmoDataUpdate", "") != "":
    text = os.getenv("AZ_BATCH_APP_PACKAGE_cosmoDataUpdate", "")
    pattern = r"cosmodataupdate(.*)\d{4}-\d{2}-\d{2}-\d{2}-\d{2}$"
    match = re.search(pattern, text)
    if match:    
        version = match.group(1)
        logger.info(f"Package version: {version}")

if os.getenv("AZ_BATCH_TASK_WORKING_DIR", "") != "":
    print("AZ_BATCH_TASK_WORKING_DIR: "+os.getenv("AZ_BATCH_TASK_WORKING_DIR", ""))
    os.symlink(
        params.DATA_FOLDER_PARENT,
        os.environ["AZ_BATCH_TASK_WORKING_DIR"] + os.sep + "data",
    )
    logger.info(f"symlink created: {params.DATA_FOLDER_PARENT} -> {os.environ['AZ_BATCH_TASK_WORKING_DIR'] + os.sep + 'data'}")


def executeUpdate():
    start_time = datetime.now()
    try:
        misc.executePreliminaries(logger, start_time)

        if params.RUN_DOWNLOAD:
            download.executeDownload(logger)

        if params.RUN_ANNUAL_PROCESSING:
            processing.executeAnnualProcessing(logger)
        if params.RUN_MONTHLY_PROCESSING:
            processing.executeMonthlyProcessing(logger)
        
        if params.RUN_OUTPUT:
            output.exectuteOutput(logger)

        if params.RUN_UTILS:
            misc.executeUtils(logger)

    except Exception as e:
        logger.error(f'Error executing update: {str(e)}')
        raise
    
    finally:
        misc.executeFinals(logger, start_time)

if __name__ == '__main__':
    try:
        executeUpdate()
    except Exception:
        sys.exit(1)