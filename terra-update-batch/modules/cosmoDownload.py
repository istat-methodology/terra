import os
import urllib.request
import py7zr
from functools import partial
import multiprocessing as mp

# TERRA MODULES
import params
from modules import cosmoUtility as cUtil

# [TODO]: CREARE UNA CLASSE DOWNLOAD CHE RAZIONALIZZI IL DOWNLOAD

def downloadAndExtractFile(param, extract_path, logger):
    url_file = param[0]
    file_zip = param[1]
    count_downloaded = 0
    count_extracted = 0
    count_error = 0

    logger.info("File: " + url_file)
    logger.info("File zip: " + file_zip)
    logger.info("extract path: " + extract_path)
    logger.info("Downloading....")

    try:
        urllib.request.urlretrieve(url_file, file_zip)
        count_downloaded += 1
        with py7zr.SevenZipFile(file_zip) as z:
            z.extractall(path=extract_path)
            count_extracted += 1
    except BaseException as err:
        logger.error("Unexpected " + str(err) + " ; type: " + str(type(err)))
        count_error += 1
    else:
        logger.info("File loaded and extracted: " + file_zip)

    return (count_downloaded, count_extracted, count_error)


def downloadAndExtractComextMonthlyDATAParallel(
    url_download, zip_folder, file_folder, prefix_file, start_data, end_data, logger
):
    logger.info("Path: " + zip_folder)

    count_downloaded = 0
    count_extracted = 0
    count_error = 0
    urls = []
    for current_month in cUtil.month_iter(
        start_data.month, start_data.year, end_data.month, end_data.year
    ):
        current_month_month = current_month[0]
        current_month_year = current_month[1]

        filenameZip = (
            prefix_file + str(current_month_year) + str(current_month_month) + ".7z"
        )
        url_file = url_download + filenameZip
        fileMonthlyZip = zip_folder + os.sep + filenameZip
        urls.append((url_file, fileMonthlyZip))

    # spark
    # spark = SparkSession.builder.getOrCreate()
    # listing = spark.sparkContext.parallelize(urls)
    # ris=listing.map(lambda url: downloadAndExtractFile(url[0],url[1], DATA_FOLDER_MONTHLY_DATS)).collect()

    # mp
    logger.info("Number of processors: {}".format(mp.cpu_count()))
    pool = mp.Pool(mp.cpu_count())

    # [TODO]: CAMBIARE NOMI (urls/params) PER RENDERLI PIù PARLANTI. URLS è UNA TUPLA DI URL E ZIP FILENAME
    ris = pool.map(
        partial(downloadAndExtractFile, extract_path = file_folder, logger = logger), urls
    )

    count_downloaded, count_extracted, count_error = map(sum, zip(*ris))

    logger.info(
        "Monthly files repo: "
        + str(count_downloaded)
        + " downloaded, "
        + str(count_extracted)
        + " extracted "
        + str(count_error)
        + " error"
    )

    return (
        "Monthly files repo: "
        + str(count_downloaded)
        + " downloaded, "
        + str(count_extracted)
        + " extracted "
        + str(count_error)
        + " error "
    )


#def downloadAndExtractComextMonthlyDATA(
#    url_download, prefix_file, start_data, end_data
#):
#    DATA_FOLDER_WORKING = DATA_FOLDER_MONTHLY + os.sep + prefix_file
#    DATA_FOLDER_MONTHLY_DATS = DATA_FOLDER_WORKING + os.sep + "files"
#    DATA_FOLDER_MONTHLY_ZIPS = DATA_FOLDER_WORKING + os.sep + "zips"
#    # createFolder(DATA_FOLDER_MONTHLY_DATS)
#    # createFolder(DATA_FOLDER_MONTHLY_ZIPS)
#
#    logger.info("Path: " + DATA_FOLDER_WORKING)
#
#    count_downloaded = 0
#    count_extracted = 0
#    count_error = 0
#    for current_month in month_iter(
#        start_data.month, start_data.year, end_data.month, end_data.year
#    ):
#        current_month_month = current_month[0]
#        current_month_year = current_month[1]
#
#        logger.info(str(current_month_year) + " " + str(current_month_month))
#        filenameZip = (
#            prefix_file + str(current_month_year) + str(current_month_month) + ".7z"
#        )
#
#        url_file = url_download + filenameZip
#        fileMonthlyZip = DATA_FOLDER_MONTHLY_ZIPS + os.sep + filenameZip
#
#        logger.info("File: " + url_file)
#        logger.info("Downloading....")
#
#        try:
#            urllib.request.urlretrieve(url_file, fileMonthlyZip)
#            count_downloaded += 1
#            with py7zr.SevenZipFile(fileMonthlyZip) as z:
#                z.extractall(path=DATA_FOLDER_MONTHLY_DATS)
#                count_extracted += 1
#        except BaseException as err:
#            logger.error("Unexpected " + str(err) + " ; type: " + str(type(err)))
#            count_error += 1
#        else:
#            logger.info("File loaded: " + filenameZip)
#
#    logger.info(
#        "Monthly files repo: "
#        + str(count_downloaded)
#        + " downloaded, "
#        + str(count_extracted)
#        + " extracted "
#        + str(count_error)
#        + " error"
#    )
#
#    return (
#        "Monthly files repo: "
#        + str(count_downloaded)
#        + " downloaded, "
#        + str(count_extracted)
#        + " extracted "
#        + str(count_error)
#        + " error "
#    )


#def downloadAndExtractComextAnnualDATA():
#    # createFolder(DATA_FOLDER_ANNUAL_DATS)
#    # createFolder(DATA_FOLDER_ANNUAL_ZIPS)
#
#    count_downloaded = 0
#    count_extracted = 0
#    count_error = 0
#
#    for current_year in [annual_previous_year, annual_current_year]:
#        filenameZip = "full" + str(current_year) + "52.7z"
#
#        url_file = URL_COMEXT_PRODUCTS + filenameZip
#        fileAnnualZip = DATA_FOLDER_ANNUAL_ZIPS + os.sep + filenameZip
#
#        logger.info("File: " + url_file)
#        logger.info("Downloading....")
#
#        try:
#            urllib.request.urlretrieve(url_file, fileAnnualZip)
#            count_downloaded += 1
#            with py7zr.SevenZipFile(fileAnnualZip) as z:
#                z.extractall(path=DATA_FOLDER_ANNUAL_DATS)
#                count_extracted += 1
#        except BaseException as err:
#            logger.error("Unexpected " + str(err) + " ; type: " + str(type(err)))
#            count_error += 1
#        else:
#            logger.info("File loaded: " + filenameZip)
#
#    logger.info(
#        "Annual files repo: "
#        + str(count_downloaded)
#        + " downloaded, "
#        + str(count_extracted)
#        + " extracted "
#        + str(count_error)
#        + " error"
#    )
#
#    return (
#        "Annual files repo: "
#        + str(count_downloaded)
#        + " downloaded, "
#        + str(count_extracted)
#        + " extracted "
#        + str(count_error)
#        + " error "
#    )


def downloadAndExtractComextAnnualDATAParallel(url, prefix, zip_folder, data_folder, logger):
    count_downloaded = 0
    count_extracted = 0
    count_error = 0
    urls = []
    for current_year in [params.annual_previous_year, params.annual_current_year]:
        filenameZip = prefix + str(current_year) + "52.7z"

        url_file = url + filenameZip
        fileAnnualZip = zip_folder + os.sep + filenameZip

        logger.info("File: " + url_file)
        logger.info("Downloading....")
        urls.append((url_file, fileAnnualZip))

    # spark version
    # spark = SparkSession.builder.getOrCreate()
    # listing = spark.sparkContext.parallelize(urls)
    # ris=listing.map(lambda url: downloadAndExtractFile(url, data_folder)).collect()

    # mp<
    logger.info("Number of processors: {}".format(mp.cpu_count()))
    pool = mp.Pool(mp.cpu_count())
    ris = pool.map(
        partial(downloadAndExtractFile, extract_path = data_folder, logger = logger), urls
    )
    count_downloaded, count_extracted, count_error = map(sum, zip(*ris))

    logger.info(
        "Annual files repo: "
        + str(count_downloaded)
        + " downloaded, "
        + str(count_extracted)
        + " extracted "
        + str(count_error)
        + " error"
    )

    return (
        "Annual files repo: "
        + str(count_downloaded)
        + " downloaded, "
        + str(count_extracted)
        + " extracted "
        + str(count_error)
        + " error "
    )


def downloadfile(url, file, logger):
    try:
        urllib.request.urlretrieve(url, file)
    except BaseException as err:
        logger.error("Unexpected " + str(err) + " ; type: " + str(type(err)))
    else:
        logger.info("File loaded: " + file)
    return "File loaded: " + file
