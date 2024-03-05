# Version 1.2.0

import sys
from datetime import datetime
from resources import params
from execute import download, processing, output, misc

logger = misc.get_logger()

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