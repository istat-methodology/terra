import os
import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler

def ai_callback_function(envelope):
    if os.getenv("CLOUD_ROLE") != None:
        envelope.tags["ai.cloud.role"] = os.getenv("CLOUD_ROLE")

def get_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    return logging.getLogger(__name__)

def execute_preliminaries(logger):
    try:
        log_handler = AzureLogHandler()
        log_handler.add_telemetry_processor(ai_callback_function)
        logger.addHandler(log_handler)
    except BaseException as e:
        logger.warning(e)