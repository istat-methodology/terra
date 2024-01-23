import os
import logging
import params
from datetime import datetime
from opencensus.ext.azure.log_exporter import AzureLogHandler
from modules import cosmoUtility as cUtil
from modules import cosmoOutput as cOut

def get_logger():

    def is_application_insight_configured():
        return (
            os.getenv("APPINSIGHTS_INSTRUMENTATIONKEY") != None
            or os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING") != None
        )
    
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


def executePreliminaries(logger):

    error = False
    logger.info('exectuteUpdate')
    start_time = datetime.now()
    logger.info(f'start time: {start_time.strftime("%H:%M:%S")}')
    repo = f'start time: {start_time.strftime("%H:%M:%S")} <br/>\n'

    # Create folder structure
    repo += cUtil.createFolderStructure(params.DIRECTORIES)
    repo += f'time: {cUtil.getPassedTime(start_time)} <br/>\n'

    # Create general info file
    repo += cOut.createGeneralInfoOutput(
        file = params.FILES["GENERAL_INFO"]
    )
    repo += "<!-- 1 --><br/>\n"
    repo += f'time: {cUtil.getPassedTime(start_time)} <br/>\n'

    return error, start_time, repo


def executeUtils(logger, repo, start_time):

    repo += "<!-- 21 --><br/>\n"
    repo += cUtil.exportOutputs(logger)
    repo += "<!-- 22 --><br/>\n"

    repo += cUtil.createAndSendBackupFiles(logger)
    repo += "<!-- 22.1 --><br/>\n"
    repo += "time: " + cUtil.getPassedTime(start_time) + "<br/>\n"

    repo += cUtil.deleteFolder(params.DATA_FOLDER , logger)
    repo += "<!-- 23 --><br/>\n"

    repo += cUtil.refreshMicroservicesDATA(logger)
    repo += "<!-- 24 --><br/>\n"
    repo += "time: " + cUtil.getPassedTime(start_time) + "<br/>\n"

    repo += cUtil.checkUPMicroservices(logger)
    repo += "<!-- 25 --><br/>\n"

    repo += f'time: {cUtil.getPassedTime(start_time)} <br/>\n'

    return repo


def executeFinals(logger, repo, start_time):
    
    end_time = datetime.now()
    logger.info(" end time: " + end_time.strftime("%H:%M:%S"))
    total_time = end_time - start_time
    logger.info("TOTAL time: " + str(total_time))
    repo += "end time: " + end_time.strftime("%H:%M:%S") + "<br/>\n"
    repo += "<br/>\n"
    repo += "TOTAL time: " + str(total_time) + "<br/>\n"
    repo += "<br/>\n"
    repo += cUtil.sendEmailRepo(repo , logger)
    repo += "<br/>\n"
    logger.info("[cosmoUpdateData]: " + repo)

    return repo