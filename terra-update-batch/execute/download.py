from modules import cosmoDownload as cDownl
from resources import config_download

def executeDownload(logger):
    logger.info('<-- Download -->')
    
    dataDownloader =cDownl.DownloadAndExtractComextParallel(logger=logger)

    for data_category in config_download.DATA_DOWNLOAD:
        try:
            dataDownloader.data_download(
                frequency=data_category['frequency'],
                file_type=data_category['file_type'],
                url_download=data_category['url_download'],
                zip_path=data_category['zip_path'],
                out_path=data_category['out_path']
            )
            logger.info(f'Downloaded {data_category["variable"]}')
        except Exception as e:
            logger.error(f'Error while downloading {data_category["variable"]}: {str(e)}')
    
    for file_category in config_download.FILE_DOWNLOAD:
        try:
            dataDownloader.file_download(
                url=file_category['url_download'],
                file=file_category['file']
            )
            logger.info(f'Downloaded {file_category["variable"]}')
        except Exception as e:
            logger.error(f'Error while downloading {file_category["variable"]}: {str(e)}')
