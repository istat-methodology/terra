import sys
from resources import params
from execute import download, processing, output, misc

logger = misc.get_logger()

def executeUpdate():
    try:
        error, start_time, repo = misc.executePreliminaries(logger)

        if params.RUN_DOWNLOAD:
            download.executeDownload(logger)

        if params.RUN_PROCESSING:
            processing.executeProcessing(logger)
        
        if params.RUN_OUTPUT:
            output.exectuteOutput(logger)

        misc.executeUtils(logger=logger, repo=repo, start_time=start_time)

    except Exception as e:
        logger.error(f'Error executing update: {str(e)}')
        error = True
    
    finally:
        repo = misc.executeFinals(logger=logger, repo=repo, start_time=start_time)

    return error


if __name__ == '__main__':
    if executeUpdate():
        sys.exit(1)