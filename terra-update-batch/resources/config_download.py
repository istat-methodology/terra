from resources import params

DATA_DOWNLOAD = [
    {
        "variable": "Product (Annual)",
        "frequency": 'annual',
        "file_type": params.PREFIX_PRODUCT,
        "url_download": params.URLS["COMEXT_PRODUCTS"],
        "zip_path": params.DIRECTORIES["PRODUCT_ANNUAL_ZIP"],
        "out_path": params.DIRECTORIES["PRODUCT_ANNUAL_FILE"]
     },

     {
        "variable": "Product (Monthly)",
        "frequency": 'monthly',
        "file_type": params.PREFIX_PRODUCT,
        "url_download": params.URLS["COMEXT_PRODUCTS"],
        "zip_path": params.DIRECTORIES["PRODUCT_MONTHLY_ZIP"],
        "out_path": params.DIRECTORIES["PRODUCT_MONTHLY_FILE"]
     },

     {
        "variable": "Transport (Monthly)",
        "frequency": 'monthly',
        "file_type": params.PREFIX_TRANSPORT,
        "url_download": params.URLS["COMEXT_TR"],
        "zip_path": params.DIRECTORIES["TRANSPORT_MONTHLY_ZIP"],
        "out_path": params.DIRECTORIES["TRANSPORT_MONTHLY_FILE"]
     }
]


FILE_DOWNLOAD = [
    {
        "variable": "CLS_PRODUCT",
        "file": params.FILES["CLS_PRODUCT_DAT"],
        "url_download": params.URLS["CLS_PRODUCTS"]
    },

    {
        "variable": "CLS_CPA",
        "file": params.FILES["CLS_CPA"],
        "url_download": params.URLS["CLS_CPA"]
    },

    {
        "variable": "CLS_CPA_2D_ITA",
        "file": params.FILES["CLS_CPA_2D_ITA"],
        "url_download": params.URLS["CLS_CPA_2D_ITA"]
    },

    {
        "variable": "CLS_NSTR",
        "file": params.FILES["CLS_NSTR"],
        "url_download": params.URLS["CLS_NSTR"]
    },

    {
        "variable": "CLS_NSTR_ITA",
        "file": params.FILES["CLS_NSTR_ITA"],
        "url_download": params.URLS["CLS_NSTR_ITA"]
    },

    {
        "variable": "ANNUAL_POPULATION",
        "file": params.FILES["ANNUAL_POPULATION_CSV"],
        "url_download": params.URLS["ANNUAL_POPULATION"]
    },

    {
        "variable": "ANNUAL_INDUSTRIAL_PRODUCTION",
        "file": params.FILES["ANNUAL_INDUSTRIAL_PRODUCTION_CSV"],
        "url_download": params.URLS["ANNUAL_INDUSTRIAL_PRODUCTION"]
    },

    {
        "variable": "ANNUAL_UNEMPLOYEMENT",
        "file": params.FILES["ANNUAL_UNEMPLOYEMENT_CSV"],
        "url_download": params.URLS["ANNUAL_UNEMPLOYEMENT"]
    },
]