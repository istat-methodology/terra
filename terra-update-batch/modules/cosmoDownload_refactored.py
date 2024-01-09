import os
import urllib.request
import py7zr
from functools import partial
import multiprocessing as mp
from datetime import datetime

# custom TERRA modules
import params
from modules import cosmoUtility as cUtil

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


class downloadAndExtractComextParallel():

    def __init__(
            self,
            parameters,
            url_download: str,
            prefix_file : tuple,
            logger
    ):
        
        self.parameters = parameters
        self.url_download = url_download
        self.logger = logger
        self.processing_day = datetime.today()
    
    def data_download(
            self,
            frequency  : str,
            file_type  : str,
            out_path : str,
            zip_path : str
    ):
        params = self.parameters  
        self.logger.info("Path: " + zip_path)

        count_downloaded, count_extracted, count_errors = 0
        
        paths = []

        if file_type == params.PREFIX_MAP["full"]:
            prefix_file = params.PREFIX_PRODUCT
        elif file_type == params.PREFIX_MAP["tr"]:
            prefix_file == params.PREFIX_TRANSPORT

        if frequency == 'monthly':
            date_list = cUtil.month_iter(start_date.month, start_date.year, end_date.month, end_date.year)
        elif frequency == 'annual':
            date_list = [params.annual_previous_year, params.annual_current_year]

        if frequency == 'monthly':
            # considerare in futuro diverse date per diverse rappresentazioni
            start_date = params.start_data_load
            end_date = params.end_data_load

            date_list = cUtil.month_iter(start_date.month, start_date.year, end_date.month, end_date.year)

            for month, year in date_list:
                filenameZip = f'{prefix_file}{year}{month}.7z'

                url_file = self.url_download + filenameZip
                fileMonthlyZip = f'{zip_path}{os.sep}{filenameZip}'
                
                paths.append((url_file, fileMonthlyZip)) 
        
        elif frequency == 'annual':
            
            for year in [params.annual_previous_year, params.annual_current_year]:
                filenameZip = f'{prefix_file}{str(year)}52.7z'

                url_file = self.url_download + filenameZip
                fileAnnualZip = f'{zip_path}{os.sep}{filenameZip}'

                self.logger.info(f'File: {url_file}')
                self.logger.info(f'Downloading...')
                paths.append((url_file, fileAnnualZip))


            
        self.logger.info(f'Number of processors: {mp.cpu_count()}')
        pool = mp.Pool(mp.cpu_count())

        results = pool.map(
            partial(downloadAndExtractFile, extract_path=out_path, logger=self.logger), paths
        )

        count_downloaded, count_extracted, count_errors = map(sum, zip(*results))

        info_string = (
            "Monthly files repo: "
            + str(count_downloaded)
            + " downloaded, "
            + str(count_extracted)
            + " extracted "
            + str(count_errors)
            + " errors"
        )

        self.logger.info(info_string)

        return info_string



