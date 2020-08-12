import logging, os
from logging.handlers import RotatingFileHandler

class TICSLogger:
    def __init__(self):
        
        self.log_formatter = logging.Formatter('%(asctime)s - <%(funcName)s> - %(levelname)s - %(message)s')

        # Try to get configurations from os environment variables
        log_file_name = os.environ['LOG_FILENAME'] if 'LOG_FILENAME' in os.environ else 'TICSLog.log'
        directory = os.environ['LOG_FILE_DIR'] if 'LOG_FILE_DIR' in os.environ else '.\\'
        max_filesize_str = os.environ['LOG_MAXSIZE'] if 'LOG_MAXSIZE' in os.environ else ''
        backupCount_str = os.environ['LOG_BACKUP_COUNT'] if 'LOG_BACKUP_COUNT' in os.environ else ''
        loggername = os.environ['LOGGER_NAME'] if 'LOGGER_NAME' in os.environ else 'TICSLog'
        try:
            max_filesize = int(max_filesize_str)
        except:
            max_filesize = 5242880
        try:
            backupCount = int(backupCount_str)
        except:
            backupCount = 10
        logFile = os.path.join(directory,log_file_name) if os.path.exists(directory) else log_file_name
        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(logging.DEBUG)
        self.console_handler.setFormatter(self.log_formatter)
        self.file_handler = RotatingFileHandler(logFile, mode='a', maxBytes=max_filesize,   # Max log file size: 5 MB (5242880 B) (5*1024*1024)
                                        backupCount=backupCount, encoding=None, delay=0)
        self.file_handler.setFormatter(self.log_formatter)
        self.file_handler.setLevel(logging.DEBUG)

        self.TICSLog = logging.getLogger(loggername)
        self.TICSLog.setLevel(logging.DEBUG)

        self.TICSLog.addHandler(self.file_handler)
        self.TICSLog.addHandler(self.console_handler)

    def set_debug(self):
        self.TICSLog.setLevel(logging.DEBUG)
        
    def set_info(self):
        self.TICSLog.setLevel(logging.INFO)

    def set_warning(self):
        self.TICSLog.setLevel(logging.WARNING)

    def set_error(self):
        self.TICSLog.setLevel(logging.ERROR)

    def set_critical(self):
        self.TICSLog.setLevel(logging.CRITICAL)
    
    def set_maxSize(self, maxBytes):
        self.file_handler.maxBytes = maxBytes

    def set_backupCount(self, backupCount):
        self.file_handler.backupCount = backupCount