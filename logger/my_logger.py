
import logging
import logger.logger_settings as logger_settings
def init_logger(filename = logger_settings.DFT_PATH):
    # set up logging to file - see previous section for more details
    logging.basicConfig(level = logging.DEBUG,
                        format = logger_settings.FORMAT,
                        datefmt = logger_settings.DATE_FORMAT,
                        #maxBytes = logger_settings.MAX_SIZE_BYTES,
                        filename = filename,
                        filemode = logger_settings.FILEMODE)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter(logger_settings.CONSOLE_FORMAT)
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)
    return logging