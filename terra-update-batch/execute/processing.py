from resources import params
from modules import cosmoProcess as cProc
from modules import cosmoOutput as cOut

def executeAnnualProcessing(logger):
    logger.info('<-- Processing (Annual) -->')

    # [MAP] Annual Processing
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

def executeMonthlyProcessing(logger):
    logger.info('<-- Processing (Monthly) -->')
    try:
        cProc.monthlyProcessing(
            path_to_scan = params.DIRECTORIES["PRODUCT_MONTHLY_FILE"],
            logger = logger
        )
        logger.info(f'Processed Monthly Data')
    except Exception as e:
        logger.error(f'Error processing Monthly Data: {str(e)}')
