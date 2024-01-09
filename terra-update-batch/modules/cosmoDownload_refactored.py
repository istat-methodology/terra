import os
import urllib.request
import py7zr
from functools import partial
import multiprocessing as mp
from datetime import datetime

# custom TERRA modules
import params
from modules import cosmoUtility as cUtil

class downloadAndExtractComextParallel():
    """
    A class for downloading and extracting .7z files from a specified url.

    Args:
        parameters: A .py file of parameters for the download and extraction process.
        prefix_file: A tuple of file prefixes for the files to be downloaded.
        logger: A logger object for logging messages.
    """

    def __init__(self, parameters, prefix_file: tuple, logger):
        self.parameters = parameters
        self.logger = logger
    
    def downloadAndExtractFile(self, paths, extract_path: str, logger):
        """
        Downloads and extracts a single .7z file.

        Args:
            paths: A tuple containing the url of the file to be downloaded (url_file) and the path to the downloaded file (file_zip).
            extract_path: The path where the extracted files will be saved.
            logger: A logger object for logging messages.

        Returns:
            A tuple containing the number of files downloaded, extracted, and with errors.
        """
        url_file = paths[0]
        file_zip = paths[1]
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
    
    
    def data_download(self, frequency: str, file_type: str, url_download: str, out_path: str, zip_path: str):
        """
        Downloads and extracts multiple .7z files from a specified url.

        Args:
            frequency: The frequency of the files to be downloaded (monthly or annual).
            file_type: The type of files to be downloaded (full or tr).
            url_download: The url of the files to be downloaded.
            out_path: The path where the extracted files will be saved.
            zip_path: The path where the zipped files will be saved.

        Returns:
            A string summarizing the download and extraction results.
        """

        params = self.parameters  
        self.logger.info("Path: " + zip_path)

        count_downloaded, count_extracted, count_errors = 0
        
        paths = []

        if file_type == params.PREFIX_MAP["full"]:
            prefix_file = params.PREFIX_PRODUCT
        elif file_type == params.PREFIX_MAP["tr"]:
            prefix_file == params.PREFIX_TRANSPORT

        if frequency == 'monthly':
            start_date = params.start_data_load
            end_date = params.end_data_load
            date_tuple = cUtil.month_iter(start_date.month, start_date.year, end_date.month, end_date.year)
            file_extension = '.7z'
        elif frequency == 'annual':
            date_list = [params.annual_previous_year, params.annual_current_year]
            date_tuple = ('', *date_list)
            file_extension = '52.7z'

        for date in date_tuple:
            filename_zip = f"{prefix_file}{date[1]}{date[0]}{file_extension}"
            url_file = url_download + filename_zip
            file_zip_path = f'{zip_path}{os.sep}{filename_zip}'
            
            self.logger.info(f'File: {url_file}')
            self.logger.info(f'Downloading...')
            
            paths.append((url_file, file_zip_path))
            
        self.logger.info(f'Number of processors: {mp.cpu_count()}')
        pool = mp.Pool(mp.cpu_count())

        results = pool.map(partial(self.downloadAndExtractFile, extract_path=out_path, logger=self.logger), paths)

        count_downloaded, count_extracted, count_errors = map(sum, zip(*results))

        info_string = "Monthly files repo: " + str(count_downloaded) + " downloaded, " + str(count_extracted) + " extracted " + str(count_errors) + " errors"

        self.logger.info(info_string)

        return info_string
