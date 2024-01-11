import os
import urllib.request
import py7zr
from functools import partial
import multiprocessing as mp

# custom TERRA modules
import params
from modules import cosmoUtility as cUtil

class DownloadAndExtractComextParallel():
    """
    A class for downloading and extracting .7z files from a specified url.

    Args:
        logger: A logger object for logging messages.
    """

    def __init__(self, logger=None):
        self.logger = logger
    
    def download_and_extract_file(self, paths: tuple[str], extract_path: str):
        """
        Downloads and extracts a single .7z file.

        Args:
            paths: A tuple containing the url of the file to be downloaded (file_url) and the path to the downloaded file (zip_file_url).
            extract_path: The path where the extracted files will be saved.

        Returns:
            A tuple containing the number of files downloaded, extracted, and with errors.
        """
        file_url, zip_file_url = paths[0], paths[1]
        n_downloaded, n_extracted, n_errors = 0
        
        if self.logger is not None:
            self.logger.info(f"file url: {file_url}")
            self.logger.info(f"zip file url: {zip_file_url}")
            self.logger.info(f"extract path: {extract_path}")
            self.logger.info("Downloading....")

        try:
            urllib.request.urlretrieve(file_url, zip_file_url)
            n_downloaded += 1
            with py7zr.SevenZipFile(zip_file_url) as z:
                z.extractall(path=extract_path)
                n_extracted += 1
        except BaseException as e:
            if self.logger is not None:
                self.logger.error(f"Unexpected {str(e)}; type: {str(type(e))}")
            n_errors += 1
        else:
            if self.logger is not None:
                self.logger.info("File loaded and extracted: " + zip_file_url)

        return (n_downloaded, n_extracted, n_errors)
    
    
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

        if self.logger is not None:
            self.logger.info("Path: " + zip_path)

        paths = []

        prefix_file = params.PREFIX_MAP.get(file_type)
        if prefix_file is None:
            raise ValueError(f"Invalid file type: '{file_type}', admissible file types are: {list(params.PREFIX_MAP.keys())}")

        if frequency == 'monthly':
            start_date = params.start_data_load
            end_date = params.end_data_load
            date_tuple = cUtil.month_iter(start_date.month, start_date.year, end_date.month, end_date.year)
            file_extension = '.7z'
        elif frequency == 'annual':
            date_list = [params.annual_previous_year, params.annual_current_year]
            date_tuple = ('', *date_list)
            file_extension = '52.7z'
        else:
            raise ValueError("Invalid frequency. Please use 'monthly' or 'annual'.")

        for date in date_tuple:
            filename_zip = f"{prefix_file}{date[1]}{date[0]}{file_extension}"
            url_file = url_download + filename_zip
            file_zip_path = f'{zip_path}{os.sep}{filename_zip}'
            
            if self.logger is not None:
                self.logger.info(f'File: {url_file}')
                self.logger.info(f'Downloading...')
            
            paths.append((url_file, file_zip_path))

        if self.logger is not None:   
            self.logger.info(f'Number of processors: {mp.cpu_count()}')

        with mp.Pool(mp.cpu_count()) as pool:
            results = pool.map(partial(self.data_download, extract_path=out_path, logger=self.logger), paths)

        n_downloaded, n_extracted, n_errors = map(sum, zip(*results))

        info_string = f"Monthly files repo: {str(n_downloaded)} downloaded | {str(n_extracted)} extracted | {str(n_errors)} errors."

        if self.logger is not None:
            self.logger.info(info_string)

        return info_string
