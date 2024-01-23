import params
from modules import cosmoOutput as cOut
from modules import cosmoUtility as cUtil

def exectuteOutput(logger, repo, start_time):
    logger.info('<-- Output -->')

    #[JSON-SERVER/MAP] Creazione file JSON per serie import/export
    repo += cOut.createMonthlyOutputTimeSeries(
        db = params.FILES["SQLLITE_DB"],
        import_ts = params.FILES["IMPORT_SERIES_JSON"],
        export_ts = params.FILES["EXPORT_SERIES_JSON"],
        logger = logger
    )
    repo += "<!-- 11 --><br/>\n"

    #[JSON-SERVER/TRADE] Creazione file JSON per serie import/export value
    repo += cOut.createMonthlyOutputVQSTradeValue(
        db = params.FILES["SQLLITE_DB"],
        import_value = params.FILES["IMPORT_VALUE_JSON"],
        export_value = params.FILES["EXPORT_VALUE_JSON"],
        cls_product_data = params.FILES["CLS_CPA"],
        cls_product_2d_data = params.FILES["CLS_CPA_2D_ITA"],
        logger = logger
    )
    repo += "<!-- 12 --><br/>\n"

    #[JSON-SERVER/TRADE] Creazione file JSON per serie import/export quantity
    repo += cOut.createMonthlyOutputVQSTradeQuantity(
        db = params.FILES["SQLLITE_DB"],
        import_qty = params.FILES["IMPORT_QUANTITY_JSON"],
        export_qty = params.FILES["EXPORT_QUANTITY_JSON"],
        cls_product_data = params.FILES["CLS_CPA"],
        cls_product_2d_data = params.FILES["CLS_CPA_2D_ITA"],
        logger = logger
    )
    repo += "<!-- 12.1 --><br/>\n"

    #[JSON-SERVER/TRADE] Creazione file JSON per serie import/export quote value
    repo += cOut.createMonthlyOutputQuoteSTradeValue(
        db = params.FILES["SQLLITE_DB"],
        import_quote_value = params.FILES["IMPORT_QUOTE_VALUE_JSON"],
        export_quote_value = params.FILES["EXPORT_QUOTE_VALUE_JSON"],
        cls_product_data = params.FILES["CLS_CPA"],
        cls_product_2d_data = params.FILES["CLS_CPA_2D_ITA"],
        logger = logger
    )
    repo += "<!-- 12.2 --><br/>\n"

    #[JSON-SERVER/TRADE] Creazione file JSON per serie import/export quote quantity
    repo += cOut.createMonthlyOutputQuoteSTradeQuantity(
        db = params.FILES["SQLLITE_DB"],
        import_quote_qty = params.FILES["IMPORT_QUOTE_QUANTITY_JSON"],
        export_quote_qty = params.FILES["EXPORT_QUOTE_QUANTITY_JSON"],
        cls_product_data = params.FILES["CLS_CPA"],
        cls_product_2d_data = params.FILES["CLS_CPA_2D_ITA"],
        logger = logger
    )
    repo += "<!-- 13 --><br/>\n"

    #[PYTHON-SERVER] Creazione file CPA intra e CPA product code
    repo += cOut.createOutputGraphCPAIntraUE(
        db = params.FILES["SQLLITE_DB"],
        cpa_intra = params.FILES["CPA_INTRA_CSV"],
        cpa3_prod_code = params.FILES["CPA3_PRODUCT_CODE_CSV"],
        logger = logger
    )
    repo += "<!-- 14 --><br/>\n"

    #[PYTHON-SERVER] Creazione file TR extra-UE e TR product code
    repo += cOut.createOutputGraphExtraUE(
        input_path = params.DIRECTORIES["TRANSPORT_MONTHLY_FILE"],
        output_tr_extra_ue_file = params.FILES["TR_EXTRA_UE_CSV"],
        output_tr_prod_code_file = params.FILES["TR_PRODUCT_CODE_CSV"],
        logger = logger
    )
    repo += "<!-- 15 --><br/>\n"

    #[PYTHON-SERVER] Creazione file CPA trim
    repo += cOut.createOutputGraphicTrimestre(
        db = params.FILES["SQLLITE_DB"],
        output_cpa_trim = params.FILES["CPA_TRIM_CSV"],
        logger = logger
    )
    repo += "<!-- 16 --><br/>\n"

    #[PYTHON-SERVER] Creazione file TR extra-UE trim
    repo += cOut.createOutputGraphExtraUE_Trim(
        input_path = params.DIRECTORIES["TRANSPORT_MONTHLY_FILE"],
        output_tr_extra_ue_trim = params.FILES["TR_EXTRA_UE_TRIMESTRALI_CSV"],
        logger = logger
    )
    repo += "<!-- 17 --><br/>\n"

    #[R-SERVER] Creazione file Comext IMP/EXP e CPA2 product code
    repo += cOut.createOutputVariazioniQuoteCPA(
        db = params.FILES["SQLLITE_DB"],
        comext_imp = params.FILES["COMEXT_IMP_CSV"],
        comext_exp = params.FILES["COMEXT_EXP_CSV"],
        cpa2_prod_code =  params.FILES["CPA2_PRODUCT_CODE_CSV"],
        logger = logger
    )
    repo += "<!-- 18 --><br/>\n"
    repo += f'time: {cUtil.getPassedTime(start_time)} <br/>\n'
    
    #[JSON-SERVER/CLASSIFICATION] Creazione file CPA con pulizia
    repo += cOut.createClsNOTEmptyProductsLang(
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
    repo += "<!-- 19 --><br/>\n"

    #[JSON-SERVER/CLASSIFICATION] Creazione file graph intra-UE con pulizia
    repo += cOut.createClsNOTEmptyProductsLang(
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
    repo += "<!-- 20 --><br/>\n"

    #[JSON-SERVER/CLASSIFICATION] Creazione file graph extra-UE con pulizia
    repo += cOut.createClsNOTEmptyProductsLang(
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

    return repo