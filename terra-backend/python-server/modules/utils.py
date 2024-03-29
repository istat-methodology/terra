import os
import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler

def is_application_insight_configured():
    return (
        os.getenv("APPINSIGHTS_INSTRUMENTATIONKEY") != None
        or os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING") != None
    )

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
    if is_application_insight_configured():
        log_handler = AzureLogHandler()
        log_handler.add_telemetry_processor(ai_callback_function)
        logger.addHandler(log_handler)
    else:
        logger.warning("Application insights is not configured.")