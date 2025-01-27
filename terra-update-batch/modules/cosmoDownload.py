import os
import urllib.request
import py7zr
import time
import multiprocessing as mp
from functools import partial

# custom TERRA modules
from resources import params
from modules import cosmoUtility as cUtil

class DownloadAndExtractComextParallel():
    """
    A class for downloading and extracting .7z files from a specified url.

    Args:
        logger: A logger object for logging messages.
    """

    def __init__(self, logger):
        self.logger = logger
    
    def file_download(self, url: str, file: str):
        """
        Downloads a file from url
        """
        try:
            urllib.request.urlretrieve(url, file)
        except Exception as e:
            self.logger.error(f'Unexpected {str(e)}; type: {str(type(e))}')
        else:
            self.logger.info(f'File loaded: {file}')
    
    def download_and_extract_file(self, paths: tuple[str], extract_path: str):
        """
        Downloads and extracts a single .7z file.

        Args:
            paths: A tuple containing the url of the file to be downloaded (file_url) and the path to the downloaded file (zip_file_url).
            extract_path: The path where the extracted files will be saved.

        Returns:
            A tuple containing the number of files downloaded, extracted, and with errors.
        """
        file_url, zip_file_url, filename = paths[0], paths[1], paths[2]
        n_downloaded, n_extracted, n_errors = 0, 0, 0
        
        self.logger.info(f"file url: {file_url}")
        self.logger.info(f"zip file url: {zip_file_url}")
        self.logger.info(f"extract path: {extract_path}")
        self.logger.info("Downloading....")

        n_attempts = 0
        for attempt in range(params.MAX_RETRY):
            n_attempts+=1
            try:
                urllib.request.urlretrieve(file_url, zip_file_url)
                n_downloaded += 1
                with py7zr.SevenZipFile(zip_file_url) as z:
                    z.extractall(path=extract_path)
                    n_extracted += 1
            except Exception as e:
                self.logger.error(f'{filename}: Attempt {n_attempts}/{params.MAX_RETRY} failed. Unexpected {str(e)}; type: {str(type(e))}')
                if attempt == params.MAX_RETRY - 1:
                    n_errors += 1
                    self.logger.error(f'Failed to download: {filename}')
                else:
                    time.sleep(params.RETRY_WAIT)
            else:
                self.logger.info(f'{filename}: File loaded and extracted after {n_attempts} attempt(s): {zip_file_url}')
                break

        return (n_downloaded, n_extracted, n_errors, filename if n_errors != 0 else '')
    
    
    def data_download(self, frequency: str, file_type: str, url_download: str, out_path: str, zip_path: str):
        """
        Downloads and extracts multiple .7z files from a specified url.

        Args:
            frequency: The frequency of the files to be downloaded (monthly or annual).
            file_type: The type of files to be downloaded ('full' or 'nst07_extra').
            url_download: The url of the files to be downloaded.
            out_path: The path where the extracted files will be saved.
            zip_path: The path where the zipped files will be saved.

        Returns:
            A string summarizing the download and extraction results.
        """

        self.logger.info(f'Path: {zip_path}')

        paths = []

        if file_type not in list(params.PREFIX_MAP.keys()):
            raise ValueError(f"Invalid file type: '{file_type}', admissible file types are: {list(params.PREFIX_MAP.keys())}")

        if frequency == 'monthly':
            if file_type == 'full_v2_':
                start_date = params.start_data_DOWNLOAD_PRODUCT
            else: 
                start_date = params.start_data_DOWNLOAD_TRANSPORT

            end_date = params.end_data_DOWNLOAD
            date_tuple = cUtil.month_iter(start_date.month, start_date.year, end_date.month, end_date.year)
            file_extension = '.7z'
        elif frequency == 'annual':
            date_tuple = [('',params.annual_previous_year), ('',params.annual_current_year)]
            file_extension = '52.7z'
        else:
            raise ValueError("Invalid frequency. Please use 'monthly' or 'annual'.")

        for date in date_tuple:
            filename_zip = f"{file_type}{date[1]}{date[0]}{file_extension}"
            url_file = url_download + filename_zip
            file_zip_path = f'{zip_path}{os.sep}{filename_zip}'
            
            self.logger.info(f'File: {url_file}')
            self.logger.info(f'Downloading...')
            
            paths.append((url_file, file_zip_path, filename_zip))

        self.logger.info(f'Number of processors: {mp.cpu_count()}')

        with mp.Pool(mp.cpu_count()) as pool:
            results = pool.map(partial(self.download_and_extract_file, extract_path=out_path), paths)

        n_downloaded, n_extracted, n_errors, error_list = [sum(filter(lambda x: isinstance(x, int), col)) if isinstance(col[0], int) else '|'.join(col) for col in zip(*results)]
        

        self.logger.info(f"Monthly files repo: {str(n_downloaded)} downloaded | {str(n_extracted)} extracted | {str(n_errors)} errors.")
        self.logger.warning(f"Files failed to download: {error_list}")
