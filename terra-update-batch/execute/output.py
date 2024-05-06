from resources import params
from modules import cosmoOutput as cOut

def exectuteOutput(logger):
    logger.info('<-- Output -->')
    output_interval = {}

    #[JSON-SERVER/MAP] Creazione file JSON per serie import/export
    try:
        output_interval["timeSeries"] = cOut.createMonthlyOutputTimeSeries(
            db = params.FILES["SQLLITE_DB"],
            import_ts = params.FILES["IMPORT_SERIES_JSON"],
            export_ts = params.FILES["EXPORT_SERIES_JSON"],
            logger = logger
        )
        logger.info(f'Created JSON of monthly import/export time series')
    except Exception as e:
        logger.error(f'Error creating JSON of monthly import/export time series: {str(e)}')

    #[JSON-SERVER/TRADE] Creazione file JSON per serie import/export value
    try:
        output_interval["tradeValue"] = cOut.createMonthlyOutputVQSTradeValue(
            db = params.FILES["SQLLITE_DB"],
            import_value = params.FILES["IMPORT_VALUE_JSON"],
            export_value = params.FILES["EXPORT_VALUE_JSON"],
            cls_product_data = params.FILES["CLS_CPA"],
            cls_product_2d_data = params.FILES["CLS_CPA_2D_ITA"],
            logger = logger
        )
        logger.info(f'Created JSON of import/export value time series')
    except Exception as e:
        logger.error(f'Error creating JSON of import/export value time series: {str(e)}')
        
    #[JSON-SERVER/TRADE] Creazione file JSON per serie import/export quantity
    try:
        output_interval["tradeQty"] = cOut.createMonthlyOutputVQSTradeQuantity(
            db = params.FILES["SQLLITE_DB"],
            import_qty = params.FILES["IMPORT_QUANTITY_JSON"],
            export_qty = params.FILES["EXPORT_QUANTITY_JSON"],
            cls_product_data = params.FILES["CLS_CPA"],
            cls_product_2d_data = params.FILES["CLS_CPA_2D_ITA"],
            logger = logger
        )
        logger.info(f'Created JSON of import/export quantity time series')
    except Exception as e:
        logger.error(f'Error creating JSON of import/export quantity time series: {str(e)}')
    
    #[JSON-SERVER/TRADE] Creazione file JSON per serie import/export quote value
    try:
        output_interval["tradeQuoteValue"] = cOut.createMonthlyOutputQuoteSTradeValue(
            db = params.FILES["SQLLITE_DB"],
            import_quote_value = params.FILES["IMPORT_QUOTE_VALUE_JSON"],
            export_quote_value = params.FILES["EXPORT_QUOTE_VALUE_JSON"],
            cls_product_data = params.FILES["CLS_CPA"],
            cls_product_2d_data = params.FILES["CLS_CPA_2D_ITA"],
            logger = logger
        )
        logger.info(f'Created JSON of import/export quote value time series')
    except Exception as e:
        logger.error(f'Error creating JSON of import/export quote value time series: {str(e)}')

    #[JSON-SERVER/TRADE] Creazione file JSON per serie import/export quote quantity
    try:
        output_interval["tradeQuoteQty"] = cOut.createMonthlyOutputQuoteSTradeQuantity(
            db = params.FILES["SQLLITE_DB"],
            import_quote_qty = params.FILES["IMPORT_QUOTE_QUANTITY_JSON"],
            export_quote_qty = params.FILES["EXPORT_QUOTE_QUANTITY_JSON"],
            cls_product_data = params.FILES["CLS_CPA"],
            cls_product_2d_data = params.FILES["CLS_CPA_2D_ITA"],
            logger = logger
        )
        logger.info(f'Created JSON of import/export quote quantity time series')
    except Exception as e:
        logger.error(f'Error creating JSON of import/export quote value time series: {str(e)}')

    #[PYTHON-SERVER] Creazione file CPA intra e CPA product code
    try:
        output_interval["graphIntra"] = cOut.createOutputGraphCPAIntraUE(
            db = params.FILES["SQLLITE_DB"],
            cpa_intra = params.FILES["CPA_INTRA_CSV"],
            cpa3_prod_code = params.FILES["CPA3_PRODUCT_CODE_CSV"],
            logger = logger
        )
        logger.info(f'Created CPA intra and CPA product code files')
    except Exception as e:
        logger.error(f'Error creating CPA intra and CPA product code files: {str(e)}')

    #[PYTHON-SERVER] Creazione file TR extra-UE, TR product code e TR trimestrali
    try:
        output_interval["graphExtra"] = cOut.createOutputGraphExtraUE(
            input_path = params.DIRECTORIES["TRANSPORT_MONTHLY_FILE"],
            output_tr_extra_ue_file = params.FILES["TR_EXTRA_UE_CSV"],
            output_tr_prod_code_file = params.FILES["TR_PRODUCT_CODE_CSV"],
            output_tr_extra_ue_trim = params.FILES["TR_EXTRA_UE_TRIMESTRALI_CSV"],
            logger = logger
        )
        logger.info(f'Created TR extra and TR product code files')
    except Exception as e:
        logger.error(f'Error creating TR extra, TR product code files and TR trimestrali: {str(e)}')

    #[PYTHON-SERVER] Creazione file CPA trim
    try:
        output_interval["graphIntraTrim"] = cOut.createOutputGraphTrimestre(
            db = params.FILES["SQLLITE_DB"],
            output_cpa_trim = params.FILES["CPA_TRIM_CSV"],
            logger = logger
        )
        logger.info(f'Created quarterly CPA file')
    except Exception as e:
        logger.error(f'Error creating quarterly CPA file: {str(e)}')

    #[R-SERVER] Creazione file Comext IMP/EXP e CPA2 product code
    try:
        output_interval["variazioniCPA"] = cOut.createOutputVariazioniQuoteCPA(
            db = params.FILES["SQLLITE_DB"],
            comext_imp = params.FILES["COMEXT_IMP_CSV"],
            comext_exp = params.FILES["COMEXT_EXP_CSV"],
            cpa2_prod_code =  params.FILES["CPA2_PRODUCT_CODE_CSV"],
            logger = logger
        )
        logger.info(f'Created Comext import/export and CPA2 product code files')
    except Exception as e:
        logger.error(f'Error creating Comext import/export and CPA2 product code files: {str(e)}')
    
    #[JSON-SERVER/CLASSIFICATION] Creazione file CPA con pulizia
    try:
        cOut.createClsNOTEmptyProductsLang(
            digit = 2,
            langs = params.SUPPORTED_LANGUAGES,
            clsfiles = [
                params.FILES["CLS_CPA_2D_ITA"],
                params.FILES["CLS_CPA"],
                ],
            filename = "CPA",
            filterValue = 37,
            fileExistingProducts = params.FILES["CPA2_PRODUCT_CODE_CSV"],
            logger = logger
        )
        logger.info(f'Created clean CPA file')
    except Exception as e:
        logger.error(f'Error creating clean CPA file: {str(e)}')

    #[JSON-SERVER/CLASSIFICATION] Creazione file graph intra-UE con pulizia
    try:
        cOut.createClsNOTEmptyProductsLang(
            digit = 3,
            langs = params.SUPPORTED_LANGUAGES,
            clsfiles = [
                params.FILES["CLS_CPA_3D_ITA"],
                params.FILES["CLS_CPA"]
                ],
            filename = "GraphIntra",
            filterValue = 37,
            fileExistingProducts = params.FILES["CPA3_PRODUCT_CODE_CSV"],
            logger = logger
        )
        logger.info(f'Created clean intra graph file')
    except Exception as e:
        logger.error(f'Error creating clean intra graph file: {str(e)}')

    #[JSON-SERVER/CLASSIFICATION] Creazione file graph extra-UE con pulizia
    try:
        cOut.createClsNOTEmptyProductsLang(
            digit = 3,
            langs = params.SUPPORTED_LANGUAGES,
            clsfiles = [
                params.FILES["CLS_NSTR_ITA"],
                params.FILES["CLS_NSTR"]
                ],
            filename = "GraphExtraNSTR",
            filterValue = 999999,
            fileExistingProducts = params.FILES["TR_PRODUCT_CODE_CSV"],
            logger = logger
        )
        logger.info(f'Created clean extra graph file')
    
    except Exception as e:
        logger.error(f'Error creating clean extra graph file: {str(e)}')

    try:
        cOut.createGeneralInfoOutput(file = params.FILES["GENERAL_INFO"], output_interval = output_interval, logger = logger)
        logger.info('Created general info file')
    except Exception as e:
        logger.error(f'Error creating general info file: {str(e)}')
