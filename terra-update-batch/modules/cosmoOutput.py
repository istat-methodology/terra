import os
import pandas as pd
import numpy as np
import json
import sqlite3

# TERRA MODULES
from resources import params
from modules import cosmoUtility as cUtil

# [JSON] METADATA
def createGeneralInfoOutput(file, output_interval, logger):
    info_processing = {}
    info_processing["processingDay"] = params.processing_day.strftime("%d-%m-%Y")
    info_processing["annualCurrentYear"] = params.annual_current_year
    info_processing["annualPreviousYear"] = params.annual_previous_year
    info_processing["lastLoadedData"] = params.end_data_DOWNLOAD.strftime("%m, %Y")
    info_processing["appVersion"] = "1.0.0"

    values = {}
    time_map_start = {}
    time_map_end = {}    

    values["timeSelected"] = str(output_interval["timeSeries"][1])  
    time_map_start["year"] = int(str(output_interval["timeSeries"][0])[:4])
    time_map_start["month"] = int(str(output_interval["timeSeries"][0])[-2:])
    values["timeStart"] = time_map_start
    time_map_end["year"] = int(str(output_interval["timeSeries"][1])[:4])
    time_map_end["month"] = int(str(output_interval["timeSeries"][1])[-2:])
    values["timeEnd"] = time_map_end
    info_processing["map"] = values

    values["timeSelected"] = str(output_interval["graphIntra"][1])  
    time_map_start["year"] = int(str(output_interval["graphIntra"][0])[:4])
    time_map_start["month"] = int(str(output_interval["graphIntra"][0])[-2:])
    values["timeStart"] = time_map_start
    time_map_end["year"] = int(str(output_interval["graphIntra"][1])[:4])
    time_map_end["month"] = int(str(output_interval["graphIntra"][1])[-2:])
    values["timeEnd"] = time_map_end
    info_processing["graph"] = values

    values["timeSelected"] = str(output_interval["graphExtra"][1])  
    time_map_start["year"] = int(str(output_interval["graphExtra"][0])[:4])
    time_map_start["month"] = int(str(output_interval["graphExtra"][0])[-2:])
    values["timeStart"] = time_map_start
    time_map_end["year"] = int(str(output_interval["graphExtra"][1])[:4])
    time_map_end["month"] = int(str(output_interval["graphExtra"][1])[-2:])
    values["timeEnd"] = time_map_end
    info_processing["graphPlus"] = values

    values["timeSelected"] = str(output_interval["tradeValue"][1])  
    time_map_start["year"] = int(str(output_interval["tradeValue"][0])[:4])
    time_map_start["month"] = int(str(output_interval["tradeValue"][0])[-2:])
    values["timeStart"] = time_map_start
    time_map_end["year"] = int(str(output_interval["tradeValue"][1])[:4])
    time_map_end["month"] = int(str(output_interval["tradeValue"][1])[-2:])
    values["timeEnd"] = time_map_end
    info_processing["trade"] = values

    with open(file, "w") as f:
        json.dump(info_processing, f, ensure_ascii=False, indent=1, cls=cUtil.NpEncoder)

    return "Info general OK, created file: " + file

# [JSON MAP]
def annualProcessing(annual_data_input_path, cls_product_data, annual_pop_data, annual_ind_prod_data, annual_unemp_data, output_file, logger):
    logger.info("annualProcessing()")

    ieinfo = []
    current_filename = (
        annual_data_input_path
        + os.sep
        + params.PREFIX_PRODUCT
        + str(params.annual_current_year)
        + "52.dat"
    )
    previous_filename = (
        annual_data_input_path
        + os.sep
        + params.PREFIX_PRODUCT
        + str(params.annual_previous_year)
        + "52.dat"
    )

    logger.info("loading.. " + cls_product_data)
    cls_products = pd.read_csv(
        cls_product_data,
        sep="\t",
        low_memory=True,
        header=None,
        keep_default_na=False,
        na_values=[""],
        encoding="latin-1",
    )

    logger.info("loading.. " + annual_pop_data)
    # ANNUAL_POPULATION_CSV
    annual_population = pd.read_csv(
        annual_pop_data, sep=",", keep_default_na=False, na_values=[""]
    )
    # FIX Greece code EL in GR
    annual_population["geo"] = annual_population["geo"].replace(["EL"], "GR")

    logger.info("loading.. " + annual_ind_prod_data)
    # ANNUAL_INDUSTRIAL_PRODUCTION_FILE_CSV
    annual_industrial_production = pd.read_csv(
        annual_ind_prod_data,
        sep=",",
        keep_default_na=False,
        na_values=[""],
    )
    # FIX Greece code EL in GR
    annual_industrial_production["geo"] = annual_industrial_production["geo"].replace(
        ["EL"], "GR"
    )

    logger.info("loading.. " + annual_unemp_data)
    # ANNUAL_UNEMPLOYEMENT_FILE_CSV
    annual_unemployement = pd.read_csv(
        annual_unemp_data, sep=",", keep_default_na=False, na_values=[""]
    )
    # FIX Greece code EL in GR
    annual_unemployement["geo"] = annual_unemployement["geo"].replace(["EL"], "GR")

    logger.info("loading.. " + previous_filename)
    data_annual_previous_year = pd.read_csv(
        previous_filename,
        sep=",",
        names=params.PRODUCT_COLNAMES,
        header=0,
        low_memory=True,
        keep_default_na=False,
        na_values=[""],
    )
    logger.info("loading.. " + current_filename)
    data_annual_current_year = pd.read_csv(
        current_filename,
        sep=",",
        names=params.PRODUCT_COLNAMES,
        header=0,
        low_memory=True,
        keep_default_na=False,
        na_values=[""],
    )

    logger.info("previous_filename: " + previous_filename)
    logger.info("current_filename: " + current_filename)

    countries = sorted(pd.unique(data_annual_current_year["DECLARANT_ISO"]))
    logger.info("countries: " + " ".join(countries))
    n_rows = 3

    for country in countries:
        logger.info("country: " + country)
        ieinfo_country = {}
        ieinfo_country["Country_Code"] = country

        # Main information
        minfo = []

        summary_population = {}
        summary_population["Year"] = "Population"

        summary_population[str(params.annual_previous_year)] = cUtil.getValueFromList(
            annual_population[
                (annual_population["indic_de"] == "JAN")
                & (annual_population["geo"] == country)
                & (annual_population["TIME_PERIOD"] == params.annual_previous_year)
            ],
            np.int64(0),
            6,
        ).astype(np.int64)
        summary_population[str(params.annual_current_year)] = cUtil.getValueFromList(
            annual_population[
                (annual_population["indic_de"] == "JAN")
                & (annual_population["geo"] == country)
                & (annual_population["TIME_PERIOD"] == params.annual_current_year)
            ],
            np.int64(0),
            6,
        ).astype(np.int64)
        minfo.append(summary_population)

        summary_industrial_production = {}
        summary_industrial_production["Year"] = "Industrial Production"

        summary_industrial_production[str(params.annual_previous_year)] = cUtil.getValueFromList(
            annual_industrial_production[
                (annual_industrial_production["nace_r2"] == "B-D")
                & (annual_industrial_production["s_adj"] == "CA")
                & (annual_industrial_production["unit"] == "I15")
                & (annual_industrial_production["geo"] == country)
                & (annual_industrial_production["TIME_PERIOD"] == params.annual_previous_year)
            ],
            "",
            9,
        )
        summary_industrial_production[str(params.annual_current_year)] = cUtil.getValueFromList(
            annual_industrial_production[
                (annual_industrial_production["nace_r2"] == "B-D")
                & (annual_industrial_production["s_adj"] == "CA")
                & (annual_industrial_production["unit"] == "I15")
                & (annual_industrial_production["geo"] == country)
                & (annual_industrial_production["TIME_PERIOD"] == params.annual_current_year)
            ],
            "",
            9,
        )
        minfo.append(summary_industrial_production)

        summary_unemployement = {}
        summary_unemployement["Year"] = "Unemployment"

        summary_unemployement[str(params.annual_previous_year)] = cUtil.getValueFromList(
            annual_unemployement[
                (annual_unemployement["sex"] == "T")
                & (annual_unemployement["unit"] == "PC_ACT")
                & (annual_unemployement["age"] == "Y15-74")
                & (annual_unemployement["geo"] == country)
                & (annual_unemployement["TIME_PERIOD"] == params.annual_previous_year)
            ],
            "",
            8,
        )
        summary_unemployement[str(params.annual_current_year)] = cUtil.getValueFromList(
            annual_unemployement[
                (annual_unemployement["sex"] == "T")
                & (annual_unemployement["unit"] == "PC_ACT")
                & (annual_unemployement["age"] == "Y15-74")
                & (annual_unemployement["geo"] == country)
                & (annual_unemployement["TIME_PERIOD"] == params.annual_current_year)
            ],
            "",
            8,
        )
        minfo.append(summary_unemployement)

        minfo_imp = {}
        minfo_imp["Year"] = "Import"
        minfo_imp[str(params.annual_previous_year)] = data_annual_previous_year[
            (data_annual_previous_year["DECLARANT_ISO"] == country)
            & (data_annual_previous_year["FLOW"] == params.FLOW_IMPORT)
            & (data_annual_previous_year["PRODUCT_NC"].str.strip().str.len() == 8)
        ]["VALUE_IN_EUROS"].sum()
        minfo_imp[str(params.annual_current_year)] = data_annual_current_year[
            (data_annual_current_year["DECLARANT_ISO"] == country)
            & (data_annual_current_year["FLOW"] == params.FLOW_IMPORT)
            & (data_annual_current_year["PRODUCT_NC"].str.strip().str.len() == 8)
        ]["VALUE_IN_EUROS"].sum()
        minfo.append(minfo_imp)

        minfo_exp = {}
        minfo_exp["Year"] = "Export"
        minfo_exp[str(params.annual_previous_year)] = data_annual_previous_year[
            (data_annual_previous_year["DECLARANT_ISO"] == country)
            & (data_annual_previous_year["FLOW"] == params.FLOW_EXPORT)
            & (data_annual_previous_year["PRODUCT_NC"].str.strip().str.len() == 8)
        ]["VALUE_IN_EUROS"].sum()
        minfo_exp[str(params.annual_current_year)] = data_annual_current_year[
            (data_annual_current_year["DECLARANT_ISO"] == country)
            & (data_annual_current_year["FLOW"] == params.FLOW_EXPORT)
            & (data_annual_current_year["PRODUCT_NC"].str.strip().str.len() == 8)
        ]["VALUE_IN_EUROS"].sum()
        minfo.append(minfo_exp)
        ieinfo_country["Main information"] = minfo
        # Main Import partner
        mips_j = []
        logger.info("# Main Import partner")
        mips_previous = (
            data_annual_previous_year[
                (data_annual_previous_year["DECLARANT_ISO"] == country)
                & (data_annual_previous_year["FLOW"] == params.FLOW_IMPORT)
                & (data_annual_previous_year["PRODUCT_NC"].str.strip().str.len() == 8)
            ]
            .groupby(["PARTNER_ISO"])["VALUE_IN_EUROS"]
            .sum()
            .nlargest(3)
            .reset_index()
        )
        mips_current = (
            data_annual_current_year[
                (data_annual_current_year["DECLARANT_ISO"] == country)
                & (data_annual_current_year["FLOW"] == params.FLOW_IMPORT)
                & (data_annual_current_year["PRODUCT_NC"].str.strip().str.len() == 8)
            ]
            .groupby(["PARTNER_ISO"])["VALUE_IN_EUROS"]
            .sum()
            .nlargest(3)
            .reset_index()
        )

        for index in range(n_rows):
            mip_j = {}
            mip_j["Main partner " + str(params.annual_previous_year)] = mips_previous.loc[
                index, "PARTNER_ISO"
            ]
            mip_j["Total import " + str(params.annual_previous_year)] = mips_previous.loc[
                index, "VALUE_IN_EUROS"
            ]
            mip_j["Main partner " + str(params.annual_current_year)] = mips_current.loc[
                index, "PARTNER_ISO"
            ]
            mip_j["Total import " + str(params.annual_current_year)] = mips_current.loc[
                index, "VALUE_IN_EUROS"
            ]
            mips_j.append(mip_j)

        ieinfo_country["Main Import Partners"] = mips_j
        # Main Export partner
        meps_j = []
        meps_previous = (
            data_annual_previous_year[
                (data_annual_previous_year["DECLARANT_ISO"] == country)
                & (data_annual_previous_year["FLOW"] == params.FLOW_EXPORT)
                & (data_annual_previous_year["PRODUCT_NC"].str.strip().str.len() == 8)
            ]
            .groupby(["PARTNER_ISO"])["VALUE_IN_EUROS"]
            .sum()
            .nlargest(3)
            .reset_index()
        )
        meps_current = (
            data_annual_current_year[
                (data_annual_current_year["DECLARANT_ISO"] == country)
                & (data_annual_current_year["FLOW"] == params.FLOW_EXPORT)
                & (data_annual_current_year["PRODUCT_NC"].str.strip().str.len() == 8)
            ]
            .groupby(["PARTNER_ISO"])["VALUE_IN_EUROS"]
            .sum()
            .nlargest(3)
            .reset_index()
        )
        logger.info(" Main Export Partners ...")
        for index2 in range(n_rows):
            mep_j = {}
            mep_j["Main partner " + str(params.annual_previous_year)] = meps_previous.loc[
                index2, "PARTNER_ISO"
            ]
            mep_j["Total export " + str(params.annual_previous_year)] = meps_previous.loc[
                index2, "VALUE_IN_EUROS"
            ]
            mep_j["Main partner " + str(params.annual_current_year)] = meps_current.loc[
                index2, "PARTNER_ISO"
            ]
            mep_j["Total export " + str(params.annual_current_year)] = meps_current.loc[
                index2, "VALUE_IN_EUROS"
            ]
            meps_j.append(mep_j)

        ieinfo_country["Main Export Partners"] = meps_j
        logger.info('"Main Import Goods ...')
        # Main Import good
        migs_j = []
        migs_previous = (
            data_annual_previous_year[
                (data_annual_previous_year["DECLARANT_ISO"] == country)
                & (data_annual_previous_year["FLOW"] == params.FLOW_IMPORT)
                & (data_annual_previous_year["PRODUCT_NC"].str.strip().str.len() == 8)
            ]
            .groupby(["PRODUCT_NC"])["VALUE_IN_EUROS"]
            .sum()
            .nlargest(3)
            .reset_index()
        )
        migs_current = (
            data_annual_current_year[
                (data_annual_current_year["DECLARANT_ISO"] == country)
                & (data_annual_current_year["FLOW"] == params.FLOW_IMPORT)
                & (data_annual_current_year["PRODUCT_NC"].str.strip().str.len() == 8)
            ]
            .groupby(["PRODUCT_NC"])["VALUE_IN_EUROS"]
            .sum()
            .nlargest(3)
            .reset_index()
        )

        for index in range(n_rows):
            previous_product = migs_previous.loc[index, "PRODUCT_NC"]
            current_product = migs_current.loc[index, "PRODUCT_NC"]
            mig_j = {}
            mig_j["Main good " + str(params.annual_previous_year)] = cUtil.getClsProduct(
                cls_products[
                    (cls_products[0] == previous_product)
                    & (
                        pd.to_datetime(
                            cls_products[1], errors="coerce", format="%d/%m/%y"
                        ).dt.year.fillna(0)
                        <= params.annual_previous_year
                    )
                    & (
                        pd.to_datetime(
                            cls_products[2], errors="coerce", format="%d/%m/%y"
                        ).dt.year.fillna(2500)
                        >= params.annual_previous_year
                    )
                ],
                previous_product,
            )
            mig_j["Total import " + str(params.annual_previous_year)] = migs_previous.loc[
                index, "VALUE_IN_EUROS"
            ]
            mig_j["Main good " + str(params.annual_current_year)] = cUtil.getClsProduct(
                cls_products[
                    (cls_products[0] == current_product)
                    & (
                        pd.to_datetime(
                            cls_products[1], errors="coerce", format="%d/%m/%y"
                        ).dt.year.fillna(0)
                        <= params.annual_current_year
                    )
                    & (
                        pd.to_datetime(
                            cls_products[2], errors="coerce", format="%d/%m/%y"
                        ).dt.year.fillna(2500)
                        >= params.annual_current_year
                    )
                ],
                current_product,
            )
            mig_j["Total import " + str(params.annual_current_year)] = migs_current.loc[
                index, "VALUE_IN_EUROS"
            ]
            migs_j.append(mig_j)

        ieinfo_country["Main Import Goods"] = migs_j
        logger.info("Main Export Goods ...")
        # Main Export partner
        megs_j = []
        megs_previous = (
            data_annual_previous_year[
                (data_annual_previous_year["DECLARANT_ISO"] == country)
                & (data_annual_previous_year["FLOW"] == params.FLOW_EXPORT)
                & (data_annual_previous_year["PRODUCT_NC"].str.strip().str.len() == 8)
            ]
            .groupby(["PRODUCT_NC"])["VALUE_IN_EUROS"]
            .sum()
            .nlargest(3)
            .reset_index()
        )
        megs_current = (
            data_annual_current_year[
                (data_annual_current_year["DECLARANT_ISO"] == country)
                & (data_annual_current_year["FLOW"] == params.FLOW_EXPORT)
                & (data_annual_current_year["PRODUCT_NC"].str.strip().str.len() == 8)
            ]
            .groupby(["PRODUCT_NC"])["VALUE_IN_EUROS"]
            .sum()
            .nlargest(3)
            .reset_index()
        )

        for index in range(n_rows):
            previous_product = megs_previous.loc[index, "PRODUCT_NC"]
            current_product = megs_current.loc[index, "PRODUCT_NC"]
            meg_j = {}
            meg_j["Main good " + str(params.annual_previous_year)] = cUtil.getClsProduct(
                cls_products[
                    (cls_products[0] == previous_product)
                    & (
                        pd.to_datetime(
                            cls_products[1], errors="coerce", format="%d/%m/%y"
                        ).dt.year.fillna(0)
                        <= params.annual_previous_year
                    )
                    & (
                        pd.to_datetime(
                            cls_products[2], errors="coerce", format="%d/%m/%y"
                        ).dt.year.fillna(2500)
                        >= params.annual_previous_year
                    )
                ],
                previous_product,
            )
            meg_j["Total export " + str(params.annual_previous_year)] = megs_previous.loc[
                index, "VALUE_IN_EUROS"
            ]
            meg_j["Main good " + str(params.annual_current_year)] = cUtil.getClsProduct(
                cls_products[
                    (cls_products[0] == current_product)
                    & (
                        pd.to_datetime(
                            cls_products[1], errors="coerce", format="%d/%m/%y"
                        ).dt.year.fillna(0)
                        <= params.annual_current_year
                    )
                    & (
                        pd.to_datetime(
                            cls_products[2], errors="coerce", format="%d/%m/%y"
                        ).dt.year.fillna(2500)
                        >= params.annual_current_year
                    )
                ],
                current_product,
            )
            meg_j["Total export " + str(params.annual_current_year)] = megs_current.loc[
                index, "VALUE_IN_EUROS"
            ]
            megs_j.append(meg_j)

        ieinfo_country["Main Export Goods"] = megs_j
        logger.info("annual file ...")
        ieinfo.append(ieinfo_country)

    with open(output_file, "w") as f:
        json.dump(ieinfo, f, ensure_ascii=False, indent=4, cls=cUtil.NpEncoder)

    return "Annual processing ok: file created " + output_file


def createMonthlyOutputTimeSeries(db, import_ts, export_ts, logger):
    logger.info("createMonthlyOutputTimeSeries START")

    # import export series
    logger.info("import export series")
    iesFiles = {}
    iesFiles[params.FLOW_IMPORT] = import_ts
    iesFiles[params.FLOW_EXPORT] = export_ts
    ieFlows = {}

    conn = sqlite3.connect(db)

    serie = pd.read_sql_query("SELECT * from serie_per_mappa", conn)
    countries = sorted(pd.unique(serie["DECLARANT_ISO"]))
    for flow in [params.FLOW_IMPORT, params.FLOW_EXPORT]:
        ieSeries = []
        for country in countries:
            logger.debug("country: " + country)
            ieIseries_country = {}
            ieIseries_country["country"] = country
            serie_country = serie[
                (serie["DECLARANT_ISO"] == country) & (serie["FLOW"] == flow)
            ]

            for index, row in serie_country.iterrows():
                ieIseries_country[str(row["PERIOD"])] = row["TENDENZIALE"]
            ieSeries.append(ieIseries_country)
        ieFlows[flow] = ieSeries

    if conn:
        conn.close()

    for flow in [params.FLOW_IMPORT, params.FLOW_EXPORT]:
        logger.info("File " + iesFiles[flow])
        with open(iesFiles[flow], "w") as f:
            json.dump(ieFlows[flow], f, ensure_ascii=False, indent=4, cls=cUtil.NpEncoder)
    
    time_range = list(serie[serie["FLOW"].isin([params.FLOW_IMPORT, params.FLOW_EXPORT])]["PERIOD"].agg(['min', 'max']))
    return time_range
    #return (
    #    "TIME SERIES processing OK; files created: "
    #    + import_ts
    #    + " and "
    #    + export_ts
    #)


def createMonthlyOutputVQSTradeValue(db, import_value, export_value, cls_product_data, cls_product_2d_data, logger):
    logger.info("createMonthlyOutputVQSTrade START")
    iesVQSFiles = {}
    iesVQSFiles[params.FLOW_IMPORT] = import_value
    iesVQSFiles[params.FLOW_EXPORT] = export_value
    ieVQSFlows = {}

    cls_products_cpa_en = pd.read_csv(
        cls_product_data,
        sep="\t",
        low_memory=True,
        header=None,
        keep_default_na=False,
        na_values=[""],
    )
    cls_products_cpa_it = pd.read_csv(
        cls_product_2d_data,
        sep="\t",
        low_memory=True,
        header=None,
        keep_default_na=False,
        na_values=[""],
        dtype=str,
    )
    cls_products_cpa_langs = {}
    cls_products_cpa_langs["it"] = cls_products_cpa_it
    cls_products_cpa_langs["en"] = cls_products_cpa_en
    logger.info("cls_products: " + cls_product_data)

    conn = sqlite3.connect(db)
    variazioni = pd.read_sql_query(
        "SELECT DECLARANT_ISO, FLOW,cpa2 as PRODUCT, PERIOD, var_val_basket var_basket FROM variazioni where (1* cpa2 >0 and 1* cpa2 <37)  order by PERIOD ASC;",
        conn,
    )
    countries = sorted(pd.unique(variazioni["DECLARANT_ISO"]))

    for flow in [params.FLOW_IMPORT, params.FLOW_EXPORT]:
        logger.info("FLOW_IMPORT,FLOW_EXPORT: " + str(flow))
        ieVQS = []

        for country in countries:
            for lang in params.SUPPORTED_LANGUAGES:
                cls_products_cpa = cls_products_cpa_langs[lang]
                logger.info("country: " + country)
                ieVQS_country = {}
                ieVQS_country["id"] = country
                ieVQS_country["lang"] = lang
                dataVQSs = []
                vqs_country = variazioni[
                    (variazioni["DECLARANT_ISO"] == country)
                    & (variazioni["FLOW"] == flow)
                ]

                products_country = sorted(pd.unique(vqs_country["PRODUCT"]))
                for product in products_country:
                    logger.debug("product: " + product)
                    dataVQS = {}

                    dataVQS["productID"] = product
                    dataVQS["dataname"] = cUtil.getClsProductByCode(
                        cls_products_cpa, product, 1
                    )
                    valuesVQS = []
                    vqs = vqs_country[vqs_country["PRODUCT"] == product].fillna("NA")
                    for indexp, row_vqs in vqs.iterrows():
                        valuesVQS.append(row_vqs["var_basket"])

                    dataVQS["value"] = valuesVQS
                    dataVQSs.append(dataVQS)

                ieVQS_country["data"] = dataVQSs
                ieVQS.append(ieVQS_country)
        ieVQSFlows[flow] = ieVQS

    if conn:
        conn.close()

    for flow in [params.FLOW_IMPORT, params.FLOW_EXPORT]:
        logger.info("File " + iesVQSFiles[flow])
        with open(iesVQSFiles[flow], "w") as f:
            json.dump(ieVQSFlows[flow], f, ensure_ascii=False, indent=1, cls=cUtil.NpEncoder)

    time_range = list(variazioni[variazioni["FLOW"].isin([params.FLOW_IMPORT, params.FLOW_EXPORT])]["PERIOD"].agg(['min', 'max']))
    return time_range
    #return (
    #    "VQS VALUE TRADE processing OK; files created: "
    #    + import_value
    #    + " and "
    #    + export_value
    #)


def createMonthlyOutputVQSTradeQuantity(db, import_qty, export_qty, cls_product_data, cls_product_2d_data, logger):
    logger.info("createMonthlyOutputVQSTrade START")
    iesVQSFiles = {}
    iesVQSFiles[params.FLOW_IMPORT] = import_qty
    iesVQSFiles[params.FLOW_EXPORT] = export_qty
    ieVQSFlows = {}

    cls_products_cpa_en = pd.read_csv(
        cls_product_data,
        sep="\t",
        low_memory=True,
        header=None,
        keep_default_na=False,
        na_values=[""],
    )
    cls_products_cpa_it = pd.read_csv(
        cls_product_2d_data,
        sep="\t",
        low_memory=True,
        header=None,
        keep_default_na=False,
        na_values=[""],
        dtype=str,
    )
    cls_products_cpa_langs = {}
    cls_products_cpa_langs["it"] = cls_products_cpa_it
    cls_products_cpa_langs["en"] = cls_products_cpa_en
    logger.info("cls_products: " + cls_product_data)

    conn = sqlite3.connect(db)
    variazioni = pd.read_sql_query(
        "SELECT DECLARANT_ISO, FLOW,cpa2 as PRODUCT, PERIOD, var_qua_basket as var_basket FROM variazioni where (1* cpa2 >0 and 1* cpa2 <37)  order by PERIOD ASC;",
        conn,
    )
    countries = sorted(pd.unique(variazioni["DECLARANT_ISO"]))

    for flow in [params.FLOW_IMPORT, params.FLOW_EXPORT]:
        logger.info("FLOW_IMPORT,FLOW_EXPORT: " + str(flow))
        ieVQS = []

        for country in countries:
            for lang in params.SUPPORTED_LANGUAGES:
                cls_products_cpa = cls_products_cpa_langs[lang]
                logger.info("country: " + country)
                ieVQS_country = {}
                ieVQS_country["id"] = country
                ieVQS_country["lang"] = lang
                dataVQSs = []
                vqs_country = variazioni[
                    (variazioni["DECLARANT_ISO"] == country)
                    & (variazioni["FLOW"] == flow)
                ]

                products_country = sorted(pd.unique(vqs_country["PRODUCT"]))
                for product in products_country:
                    logger.debug("product: " + product)
                    dataVQS = {}

                    dataVQS["productID"] = product
                    dataVQS["dataname"] = cUtil.getClsProductByCode(
                        cls_products_cpa, product, 1
                    )
                    valuesVQS = []
                    vqs = vqs_country[vqs_country["PRODUCT"] == product].fillna("NA")
                    for indexp, row_vqs in vqs.iterrows():
                        valuesVQS.append(row_vqs["var_basket"])

                    dataVQS["value"] = valuesVQS
                    dataVQSs.append(dataVQS)

                ieVQS_country["data"] = dataVQSs
                ieVQS.append(ieVQS_country)
        ieVQSFlows[flow] = ieVQS

    if conn:
        conn.close()

    for flow in [params.FLOW_IMPORT, params.FLOW_EXPORT]:
        logger.info("File " + iesVQSFiles[flow])
        with open(iesVQSFiles[flow], "w") as f:
            json.dump(ieVQSFlows[flow], f, ensure_ascii=False, indent=1, cls=cUtil.NpEncoder)

    time_range = list(variazioni[variazioni["FLOW"].isin([params.FLOW_IMPORT, params.FLOW_EXPORT])]["PERIOD"].agg(['min', 'max']))
    return time_range
    #return (
    #    "VQS QUANTITY TRADE processing OK; files created: "
    #    + import_qty
    #    + " and "
    #    + export_qty
    #)


def createMonthlyOutputQuoteSTrade(db, quote_trade, logger):
    logger.info("createMonthlyOutputQuoteSTrade quote START")
    conn = sqlite3.connect(db)
    quote = pd.read_sql_query(
        "SELECT DECLARANT_ISO as id, FLOW,cpa2 as PRODUCT, PERIOD, q_val_cpa as quote_valore, q_qua_cpa as quote_quantita FROM quote_cpa where (1* cpa2 >0 and 1* cpa2 <37)  order by PERIOD ASC;",
        conn,
    )

    if conn:
        conn.close()

    quote.to_json(quote_trade, orient="records")

    return "Quote  TRADE processing OK; files created: " + quote_trade


def createMonthlyOutputQuoteSTradeValue(db, import_quote_value, export_quote_value, cls_product_data, cls_product_2d_data, logger):
    logger.info("createMonthlyOutputQuoteSTrade START")
    iesVQSFiles = {}
    iesVQSFiles[params.FLOW_IMPORT] = import_quote_value
    iesVQSFiles[params.FLOW_EXPORT] = export_quote_value
    ieVQSFlows = {}

    cls_products_cpa_en = pd.read_csv(
        cls_product_data,
        sep="\t",
        low_memory=True,
        header=None,
        keep_default_na=False,
        na_values=[""],
    )
    cls_products_cpa_it = pd.read_csv(
        cls_product_2d_data,
        sep="\t",
        low_memory=True,
        header=None,
        keep_default_na=False,
        na_values=[""],
        dtype=str,
    )
    cls_products_cpa_langs = {}
    cls_products_cpa_langs["it"] = cls_products_cpa_it
    cls_products_cpa_langs["en"] = cls_products_cpa_en
    logger.info("cls_products: " + cls_product_data)

    conn = sqlite3.connect(db)
    quote = pd.read_sql_query(
        "SELECT DECLARANT_ISO, FLOW,cpa2 as PRODUCT, PERIOD, q_val_cpa as q_val_basket FROM quote_cpa where (1* cpa2 >0 and 1* cpa2 <37)  order by PERIOD ASC;",
        conn,
    )
    countries = sorted(pd.unique(quote["DECLARANT_ISO"]))

    for flow in [params.FLOW_IMPORT, params.FLOW_EXPORT]:
        logger.info("FLOW_IMPORT,FLOW_EXPORT: " + str(flow))
        ieVQS = []

        for country in countries:
            for lang in params.SUPPORTED_LANGUAGES:
                cls_products_cpa = cls_products_cpa_langs[lang]
                logger.info("country: " + country)
                ieVQS_country = {}
                ieVQS_country["id"] = country
                ieVQS_country["lang"] = lang
                dataVQSs = []
                vqs_country = quote[
                    (quote["DECLARANT_ISO"] == country) & (quote["FLOW"] == flow)
                ]

                products_country = sorted(pd.unique(vqs_country["PRODUCT"]))
                for product in products_country:
                    logger.debug("product: " + product)
                    dataVQS = {}

                    dataVQS["productID"] = product
                    dataVQS["dataname"] = cUtil.getClsProductByCode(
                        cls_products_cpa, product, 1
                    )
                    valuesVQS = []
                    vqs = vqs_country[vqs_country["PRODUCT"] == product].fillna("NA")
                    for indexp, row_vqs in vqs.iterrows():
                        valuesVQS.append(row_vqs["q_val_basket"])

                    dataVQS["value"] = valuesVQS
                    dataVQSs.append(dataVQS)

                ieVQS_country["data"] = dataVQSs
                ieVQS.append(ieVQS_country)
        ieVQSFlows[flow] = ieVQS

    if conn:
        conn.close()

    for flow in [params.FLOW_IMPORT, params.FLOW_EXPORT]:
        logger.info("File " + iesVQSFiles[flow])
        with open(iesVQSFiles[flow], "w") as f:
            json.dump(ieVQSFlows[flow], f, ensure_ascii=False, indent=1, cls=cUtil.NpEncoder)

    time_range = list(quote[quote["FLOW"].isin([params.FLOW_IMPORT, params.FLOW_EXPORT])]["PERIOD"].agg(['min', 'max']))
    return time_range
    #return (
    #    "Quote VALUE TRADE processing OK; files created: "
    #    + import_quote_value
    #    + " and "
    #    + export_quote_value
    #)


def createMonthlyOutputQuoteSTradeQuantity(db, import_quote_qty, export_quote_qty, cls_product_data, cls_product_2d_data, logger):
    logger.info("createMonthlyOutputQuoteSTrade START")
    iesVQSFiles = {}
    iesVQSFiles[params.FLOW_IMPORT] = import_quote_qty
    iesVQSFiles[params.FLOW_EXPORT] = export_quote_qty
    ieVQSFlows = {}

    cls_products_cpa_en = pd.read_csv(
        cls_product_data,
        sep="\t",
        low_memory=True,
        header=None,
        keep_default_na=False,
        na_values=[""],
    )
    cls_products_cpa_it = pd.read_csv(
        cls_product_2d_data,
        sep="\t",
        low_memory=True,
        header=None,
        keep_default_na=False,
        na_values=[""],
        dtype=str,
    )
    cls_products_cpa_langs = {}
    cls_products_cpa_langs["it"] = cls_products_cpa_it
    cls_products_cpa_langs["en"] = cls_products_cpa_en
    logger.info("cls_products: " + cls_product_data)

    conn = sqlite3.connect(db)
    quote = pd.read_sql_query(
        "SELECT DECLARANT_ISO, FLOW,cpa2 as PRODUCT, PERIOD, q_qua_cpa as q_qua_basket FROM quote_cpa where (1* cpa2 >0 and 1* cpa2 <37)  order by PERIOD ASC;",
        conn,
    )
    countries = sorted(pd.unique(quote["DECLARANT_ISO"]))

    for flow in [params.FLOW_IMPORT, params.FLOW_EXPORT]:
        logger.info("FLOW_IMPORT,FLOW_EXPORT: " + str(flow))
        ieVQS = []

        for country in countries:
            for lang in params.SUPPORTED_LANGUAGES:
                cls_products_cpa = cls_products_cpa_langs[lang]
                logger.info("country: " + country)
                ieVQS_country = {}
                ieVQS_country["id"] = country
                ieVQS_country["lang"] = lang
                dataVQSs = []
                vqs_country = quote[
                    (quote["DECLARANT_ISO"] == country) & (quote["FLOW"] == flow)
                ]

                products_country = sorted(pd.unique(vqs_country["PRODUCT"]))
                for product in products_country:
                    logger.debug("product: " + product)
                    dataVQS = {}

                    dataVQS["productID"] = product
                    dataVQS["dataname"] = cUtil.getClsProductByCode(
                        cls_products_cpa, product, 1
                    )
                    valuesVQS = []
                    vqs = vqs_country[vqs_country["PRODUCT"] == product].fillna("NA")
                    for indexp, row_vqs in vqs.iterrows():
                        valuesVQS.append(row_vqs["q_qua_basket"])

                    dataVQS["value"] = valuesVQS
                    dataVQSs.append(dataVQS)

                ieVQS_country["data"] = dataVQSs
                ieVQS.append(ieVQS_country)
        ieVQSFlows[flow] = ieVQS

    if conn:
        conn.close()

    for flow in [params.FLOW_IMPORT, params.FLOW_EXPORT]:
        logger.info("File " + iesVQSFiles[flow])
        with open(iesVQSFiles[flow], "w") as f:
            json.dump(ieVQSFlows[flow], f, ensure_ascii=False, indent=1, cls=cUtil.NpEncoder)

    time_range = list(quote[quote["FLOW"].isin([params.FLOW_IMPORT, params.FLOW_EXPORT])]["PERIOD"].agg(['min', 'max']))
    return time_range
    #return (
    #    "QUOTE S QUANTITY TRADE processing OK; files created: "
    #    + import_quote_qty
    #    + " and "
    #    + export_quote_qty
    #)


def createOutputVariazioniQuoteCPA(db, comext_imp, comext_exp, cpa2_prod_code, logger):
    # import export variazioni quote CPA
    logger.info("createOutputVariazioniQuoteCPA START")
    logger.info("import export variazioni quote CPA")
    iesVQSFiles = {}
    iesVQSFiles[params.FLOW_IMPORT] = comext_imp
    iesVQSFiles[params.FLOW_EXPORT] = comext_exp

    conn = sqlite3.connect(db)
    time_range = []

    for flow in [params.FLOW_IMPORT, params.FLOW_EXPORT]:
        variazioni = pd.read_sql_query(
            "SELECT DECLARANT_ISO, PARTNER_ISO, FLOW, trim(cpa) as cpa, PERIOD, val_cpa, q_kg  FROM variazioni_cpa WHERE FLOW="
            + str(flow)
            + " and (length(trim(cpa))==2 or trim(cpa) in ('061','062') ) order by PERIOD ASC;",
            conn,
        )
        variazioni.to_csv(iesVQSFiles[flow], sep=",", index=False)
        time_range.append(variazioni["PERIOD"].min())
        time_range.append(variazioni["PERIOD"].max())

    pd.read_sql_query(
        "SELECT distinct trim(cpa) as PRODUCT FROM variazioni_cpa WHERE (length(trim(cpa))==2 or trim(cpa) in ('061','062') );",
        conn,
    ).to_csv(cpa2_prod_code, sep=",", index=False)

    if conn:
        conn.close()

    logger.info("createMonthlyOutput END")
    return [min(time_range),max(time_range)]
    #return (
    #    "Variazioni quote CPA processing OK; files created: "
    #    + comext_imp
    #    + " and "
    #    + comext_exp
    #)


def createOutputGraphCPAIntraUE(db, cpa_intra, cpa3_prod_code, logger):
    logger.info("createOutputGraphCPAIntraUE START")
    # import export variazioni quote CPA
    logger.info("import export variazioni quote CPA INTRA")

    #  end_data_lclearoad=datetime.datetime.strptime(str(this_year_month), "%Y%m")- relativedelta(months=offset_m)
    # last_12_months=datetime.datetime.strptime(( str(end_data_load.year)+"-"+str(end_data_load.month)- relativedelta(months=12)), "%Y%m")

    filter_yyymm = str(params.start_data_PAGE_GRAPH_INTRA_UE.year - 1) + str(
        "%02d" % params.start_data_PAGE_GRAPH_INTRA_UE.month
    )
    logger.info("last_months: " + filter_yyymm)
    conn = sqlite3.connect(db)
    result = pd.read_sql_query(
        "SELECT DECLARANT_ISO, PARTNER_ISO, FLOW, PRODUCT, PERIOD, VALUE_IN_EUROS  FROM (SELECT DECLARANT_ISO, PARTNER_ISO, FLOW, cpa as PRODUCT, PERIOD, val_cpa as VALUE_IN_EUROS  FROM base_grafi_cpa WHERE PERIOD>"
        + filter_yyymm
        + " and length(trim(cpa))==3 union SELECT DECLARANT_ISO, PARTNER_ISO, FLOW, 'TOT' as PRODUCT, PERIOD, val_cpa as VALUE_IN_EUROS  FROM base_grafi_cpa WHERE PERIOD>"
        + filter_yyymm
        + " and  trim(cpa)=='00')   order by PERIOD ASC;",
        conn,
    )
    result.to_csv(cpa_intra, sep=",", index=False)
    pd.read_sql_query(
        "SELECT distinct cpa as PRODUCT  FROM base_grafi_cpa WHERE PERIOD>"
        + filter_yyymm
        + " and length(trim(cpa))==3;",
        conn,
    ).to_csv(cpa3_prod_code, sep=",", index=False)
    if conn:
        conn.close()

    logger.info("createOutputGraphCPAIntraUE END")

    time_range = list(result["PERIOD"].agg(['min', 'max']))
    return time_range
    #return "CPA Graphic INTRA UE OK; files created: " + cpa_intra


def createOutputGraphTrimestre(db, output_cpa_trim, logger):
    logger.info("createOutputGraphicTrimestre START")
    # import export variazioni quote CPA
    logger.info("import export variazioni quote CPA INTRA TRim")

    conn = sqlite3.connect(db)
    result = pd.read_sql_query(
        "SELECT declarant_iso, partner_iso, flow,  cpa, trimestre,   val_cpa,   q_kg  FROM base_grafi_cpa_trim WHERE length(trim(cpa))==3 union SELECT declarant_iso, partner_iso, flow,  'TOT' as cpa, trimestre,   val_cpa,   q_kg  FROM base_grafi_cpa_trim WHERE trim(cpa)=='00' order by trimestre ASC;",
        conn,
    )
    result.to_csv(output_cpa_trim, sep=",", index=False)

    if conn:
        conn.close()

    logger.info("createOutputGraphicTrimestre END")

    time_range = list(result["trimestre"].agg(['min', 'max']))
    return time_range
    #return "CPA Graphic INTRA TRIMESTRE UE OK; files created: " + output_cpa_trim


def createOutputGraphExtraUE(input_path, output_tr_extra_ue_file, output_tr_prod_code_file, output_tr_extra_ue_trim, logger):
    logger.info("createOutputGraphExtraUE START")
    logger.info("Reading from " + input_path)

    listDataframes = []
    for f in os.listdir(input_path):
        if f.endswith(params.DATA_EXTENTION):
            appo = pd.read_csv(
                input_path + os.sep + f,
                sep=params.SEP,
                low_memory=False,
                keep_default_na=False,
                na_values=[""],
            )
            listDataframes.append(appo)

    df = pd.concat(listDataframes, axis=0)
    # df=df[df["PRODUCT_NST07_NST07"]!="TOT"]
    df = df[df["DECLARANT_ISO"] != "EU"]
    df = df[df["PARTNER_ISO"] != "EU"]
    df = df[
        [
            "PRODUCT_NST07_NST07",
            "DECLARANT_ISO",
            "PARTNER_ISO",
            "PERIOD",
            "TRANSPORT_MODE",
            "FLOW",
            "VALUE_IN_EUROS",
            "QUANTITY_IN_KG",
        ]
    ]
    df.rename(columns={'PRODUCT_NST07_NST07': 'PRODUCT_NSTR'}, inplace=True)
    df_tot = df.groupby([
        "DECLARANT_ISO",
        "PARTNER_ISO",
        "PERIOD",
        "TRANSPORT_MODE",
        "FLOW"
        ]).sum().reset_index()[["DECLARANT_ISO","PARTNER_ISO","PERIOD","TRANSPORT_MODE","FLOW","VALUE_IN_EUROS","QUANTITY_IN_KG"]]
    df_tot["PRODUCT_NSTR"] = "TOT"
    df = pd.concat([df, df_tot], ignore_index=True)
    df.to_csv(output_tr_extra_ue_file, sep=",", index=False)

    # PRODUCT CODE
    pd.DataFrame({"PRODUCT": df["PRODUCT_NSTR"].astype(str).unique()}).to_csv(
        output_tr_prod_code_file, sep=",", index=False
    )

    logger.info("tr_extra_ue file: " + output_tr_extra_ue_file)
    logger.info("createOutputGraph END ")
    
    # TRIMESTRALI
    logger.info("createOutputGraphExtraUE TRIM START")
    df["TRIMESTRE"] = df["PERIOD"]
    df["TRIMESTRE"] = df["TRIMESTRE"].apply(
        lambda x: str(x)[0:4] + "T1"
        if str(x)[4:6] in ["01", "02", "03"]
        else str(x)[0:4] + "T2"
        if str(x)[4:6] in ["04", "05", "06"]
        else str(x)[0:4] + "T3"
        if str(x)[4:6] in ["07", "08", "09"]
        else str(x)[0:4] + "T4"
        if str(x)[4:6] in ["10", "11", "12"]
        else x
    )

    df_trim = (
        df.groupby(
            [
                "PRODUCT_NSTR",
                "DECLARANT_ISO",
                "PARTNER_ISO",
                "TRIMESTRE",
                "TRANSPORT_MODE",
                "FLOW",
            ]
        )[["VALUE_IN_EUROS", "QUANTITY_IN_KG"]]
        .sum()
        .reset_index()
    )

    df_trim.to_csv(output_tr_extra_ue_trim, sep=",", index=False)
    logger.info("tr_extra_ue TRIMESTRALI file: " + output_tr_extra_ue_trim)
    logger.info("createOutputGraph TRIM END ")

    time_range = list(df["PERIOD"].agg(['min', 'max']))
    return time_range
    #return "CPA Graphic EXTRE UE OK; files created: " + output_tr_extra_ue_file

def createClsNOTEmptyProductsLang(
    digit, langs, clsfiles, filename, filterValue, fileExistingProducts, logger
):
    logger.info("createCls START")
    cls_products_cpa_langs = pd.DataFrame()
    for i in range(len(langs)):
        lang = langs[i]
        clsfile = clsfiles[i]
        cls_products_cpa = pd.read_csv(
            clsfile,
            sep="\t",
            low_memory=True,
            names=["id", "descr"],
            keep_default_na=False,
            na_values=[""],
            dtype={"id": str},
        )
        cls_products_cpa["lang"] = lang
        logger.info("cls_products: " + clsfile)

        cls_products_cpa = cls_products_cpa[
            (cls_products_cpa["id"].str.len() == digit)
            & (cls_products_cpa["id"].str.isnumeric())
            & (
                pd.to_numeric(cls_products_cpa["id"].str.slice(stop=2), errors="coerce")
                .fillna(999)
                .astype(int)
                < filterValue
            )
        ]
        if fileExistingProducts:
            products = pd.read_csv(
                fileExistingProducts, sep=",", low_memory=True, dtype={"PRODUCT": str}
            )
            cls_products_cpa = pd.merge(
                cls_products_cpa, products, left_on="id", right_on="PRODUCT"
            )
            cls_products_cpa = cls_products_cpa[["id", "descr", "lang"]]

        if digit == 2:
            # cls_products_cpa.insert(0,{"id":"00","descr":"All Products" })
            if lang == "it":
                cls_products_cpa = pd.concat(
                    [
                        pd.DataFrame(
                            {"id": "00", "descr": "Tutti i prodotti", "lang": "it"},
                            index=[0],
                        ),
                        cls_products_cpa,
                    ]
                ).reset_index(drop=True)
                cls_products_cpa = pd.concat(
                    [
                        pd.DataFrame(
                            {"id": "061", "descr": "Petrolio greggio", "lang": "it"},
                            index=[0],
                        ),
                        cls_products_cpa,
                    ]
                ).reset_index(drop=True)
                cls_products_cpa = pd.concat(
                    [
                        pd.DataFrame(
                            {
                                "id": "062",
                                "descr": "Gas naturale, liquefatto o allo stato gassoso",
                                "lang": "it",
                            },
                            index=[0],
                        ),
                        cls_products_cpa,
                    ]
                ).reset_index(drop=True)
            else:
                cls_products_cpa = pd.concat(
                    [
                        pd.DataFrame(
                            {"id": "00", "descr": "All Products", "lang": "en"},
                            index=[0],
                        ),
                        cls_products_cpa,
                    ]
                ).reset_index(drop=True)
                cls_products_cpa = pd.concat(
                    [
                        pd.DataFrame(
                            {"id": "061", "descr": "Crude petroleum", "lang": "en"},
                            index=[0],
                        ),
                        cls_products_cpa,
                    ]
                ).reset_index(drop=True)
                cls_products_cpa = pd.concat(
                    [
                        pd.DataFrame(
                            {
                                "id": "062",
                                "descr": "Natural gas, liquefied or in gaseous state",
                                "lang": "en",
                            },
                            index=[0],
                        ),
                        cls_products_cpa,
                    ]
                ).reset_index(drop=True)
            cls_products_cpa = cls_products_cpa.sort_values("id")
            cls_products_cpa = cls_products_cpa.reset_index(drop=True)

        if digit == 3:
            if lang == "it":
                cls_products_cpa = pd.concat(
                    [
                        cls_products_cpa,
                        pd.DataFrame(
                            {"id": "TOT", "descr": "Tutti i prodotti", "lang": "it"},
                            index=[0],
                        ),
                    ]
                ).reset_index(drop=True)
            else:
                # cls_products_cpa.append({"id":"TOT","descr":"All Products" })
                cls_products_cpa = pd.concat(
                    [
                        cls_products_cpa,
                        pd.DataFrame(
                            {"id": "TOT", "descr": "All Products", "lang": "en"},
                            index=[0],
                        ),
                    ]
                ).reset_index(drop=True)
        cls_products_cpa_langs = pd.concat(
            [cls_products_cpa_langs, cls_products_cpa], axis=0
        ).reset_index(drop=True)

    temp = params.DIRECTORIES["CLASSIFICATION"] + os.sep + "clsProducts" + filename + ".json"
    cls_products_cpa_langs.to_json(
        temp, orient="records", default_handler=None, lines=False, indent=1
    )
    logger.info("cls_products created: " + temp)
    return "cls_products created: " + temp