import os
import logging
from resources import params
from datetime import datetime
from opencensus.ext.azure.log_exporter import AzureLogHandler
from modules import cosmoUtility as cUtil

def is_application_insight_configured():
        return (
            os.getenv("APPINSIGHTS_INSTRUMENTATIONKEY") != None
            or os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING") != None
        )


def get_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"        
    )
    logger = logging.getLogger(__name__)

    if is_application_insight_configured():
        log_handler = AzureLogHandler()
        logger.addHandler(log_handler)
    else:
        logger.warning("Application insights is not configured.")

    return logger


def executePreliminaries(logger, start_time: datetime):
    logger.info('<-- Preliminaries -->')

    logger.info(f'start time: {start_time.strftime("%H:%M:%S")}')

    cUtil.createFolderStructure(params.DIRECTORIES)
    logger.info('Created folder structure')

    cUtil.sanityCheckAzureFolderStructure(logger)
    logger.info('Sanity check done!')

    return start_time


def executeUtils(logger):
    logger.info('<-- Utilities -->')

    start_time = datetime.now()
    cUtil.exportOutputs(logger)
    logger.info(f'Outputs exported - time: {cUtil.getPassedTime(start_time)})')

    start_time = datetime.now()
    cUtil.createAndSendBackupFiles(logger)
    logger.info(f'Backup files created and sent - time: {cUtil.getPassedTime(start_time)})')

    cUtil.deleteFolder(params.DATA_FOLDER , logger)
    logger.info(f'Folder deleted')

    start_time = datetime.now()
    cUtil.refreshMicroservicesDATA(logger)
    logger.info(f'Microservice data refreshed - time: {cUtil.getPassedTime(start_time)})')

    start_time = datetime.now()
    cUtil.checkUPMicroservices(logger)
    logger.info(f'UPM microservices checked - time: {cUtil.getPassedTime(start_time)})')


def executeFinals(logger, start_time: datetime):
    logger.info('<-- Finals -->')
    
    end_time = datetime.now()
    logger.info(f'end time: {end_time.strftime("%H:%M:%S")}')
    logger.info(f'TOTAL time: {str(end_time - start_time)}')

    cUtil.sendEmailRepo(f'[Update batch: TOTAL time: {str(end_time - start_time)}]', logger)