from resources import params
from modules import cosmoProcess as cProc
from modules import cosmoOutput as cOut

def executeProcessing(logger):
    logger.info('<-- Processing -->')

    # [MAP] Annual Processing
    if params.RUN_ANNUAL_PROCESSING is True:
        try:
            cOut.annualProcessing(
                annual_data_input_path = params.DIRECTORIES["PRODUCT_ANNUAL_FILE"],
                cls_product_data = params.FILES["CLS_PRODUCT_DAT"],
                annual_pop_data = params.FILES["ANNUAL_POPULATION_CSV"],
                annual_ind_prod_data = params.FILES["ANNUAL_INDUSTRIAL_PRODUCTION_CSV"],
                annual_unemp_data = params.FILES["ANNUAL_UNEMPLOYEMENT_CSV"],
                output_file = params.FILES["IEINFO"],
                logger = logger
            )
            logger.info(f'Processed Product (Annual) table')
        except Exception as e:
            logger.error(f'Error processing Product (Annual) table: {str(e)}')

    # [DB] Database Creation
    try:
        cProc.createMonthlyFULLtable(
            db = params.FILES["SQLLITE_DB"],
            path_to_scan = params.DIRECTORIES["PRODUCT_MONTHLY_FILE"],
            logger = logger
        )
        logger.info(f'Created DB table (Monthly)')
    except Exception as e:
        logger.error(f'Error creating DB table (Monthly): {str(e)}')

    #[DB] Creazione tabelle per serie mappa
    try:
        cProc.monthlyProcessing(
            db = params.FILES["SQLLITE_DB"],
            logger = logger
        )
        logger.info(f'Processed Monthly Data')
    except Exception as e:
        logger.error(f'Error processing Monthly Data: {str(e)}')
