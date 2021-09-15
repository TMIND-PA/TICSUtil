import logging, os
from logging.handlers import RotatingFileHandler
# from rich.logging import RichHandler
import __main__

class ConsoleFormatter(logging.Formatter):
    
    grey = "\x1b[38;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    bold_green = "\x1b[32;21m"
    reverse = "\x1b[7m"
    bold = "\x1b[1m"
    underline = "\x1b[4m"
    reset = "\x1b[0m"
    format_str = "{asctime}.{msecs:03.0f} - {funcName:^16s} - {lineno:04d} - {levelname:^9s} - {message}"

    FORMATS = {
        logging.DEBUG: grey + format_str + reset,
        logging.INFO: bold_green + format_str + reset,
        logging.WARNING: yellow + format_str + reset,
        logging.ERROR: red + underline + format_str + reset,
        logging.CRITICAL: bold_red + reverse + format_str + reset
    }

    def set_format_str(self, str):
        self.FORMATS = {
        logging.DEBUG: self.grey + str + self.reset,
        logging.INFO: self.bold_green + str + self.reset,
        logging.WARNING: self.yellow + str + self.reset,
        logging.ERROR: self.red + self.underline + str + self.reset,
        logging.CRITICAL: self.bold_red + self.reverse + str + self.reset
    }
        

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, style="{", datefmt="%Y-%b-%d %H:%M:%S")
        return formatter.format(record)

class TICSLogger:
    def __init__(self, logger = None, filename =  None, dir = None, max_size = "5242880", max_num = "10"):
        
        if filename is None:
            full_path = __main__.__file__
            script_name = os.path.basename(os.path.realpath(full_path))
            print(f"{script_name = }")    
            filename = script_name[:-3] + ".log"

        if dir is None:
            full_path = __main__.__file__
            dir = os.path.dirname(os.path.realpath(full_path))

        if not os.path.exists(dir):
            os.makedirs(dir, exist_ok=True)

        if logger is None:
            full_path = __main__.__file__
            script_name = os.path.basename(os.path.realpath(full_path))
            logger = script_name[:-3]

        # logging.basicConfig(datefmt="%d-%m-%Y %H:%M:%S")

        # self.log_formatter = logging.Formatter("%(asctime)s - [%(funcName)-16s] - [%(lineno)4d] - [%(levelname)8s] - %(message)s")
        # self.log_formatter = logging.Formatter("[{asctime}.{msecs:03.0f}] [{funcName:^16s}] [{lineno:04d}] [{levelname:^9s}] {message}", style="{", datefmt="%Y-%m-%d %H:%M:%S")
        self.format_str = "{asctime}.{msecs:03.0f} | {funcName:^16s} | {lineno:04d} | {levelname:^9s} | {message}"
        self.style = "{"
        self.datefmt = "%Y-%m-%d %H:%M:%S"
        self.log_formatter = logging.Formatter(self.format_str , style=self.style, datefmt=self.datefmt)
        # self.log_fmt_console = logging.Formatter(self.format_str , style=self.style, datefmt=self.datefmt)

        # Try to get configurations from os environment variables

        log_file_name = os.environ["LOG_FILENAME"] if "LOG_FILENAME" in os.environ else filename
        directory = os.environ["LOG_FILE_DIR"] if "LOG_FILE_DIR" in os.environ else dir
        max_filesize_str = os.environ["LOG_MAXSIZE"] if "LOG_MAXSIZE" in os.environ else max_size
        backupCount_str = os.environ["LOG_BACKUP_COUNT"] if "LOG_BACKUP_COUNT" in os.environ else max_num
        loggername = os.environ["LOGGER_NAME"] if "LOGGER_NAME" in os.environ else logger
        try:
            max_filesize = int(max_filesize_str)
        except:
            max_filesize = 5242880
        try:
            backupCount = int(backupCount_str)
        except:
            backupCount = 10
        logFile = os.path.join(directory,log_file_name) if os.path.exists(directory) else log_file_name
        # self.console_handler = RichHandler(rich_tracebacks=True,show_path=False, show_time=False, markup=True)
        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(logging.DEBUG)
        console_formatter = ConsoleFormatter()
        console_formatter.set_format_str(self.format_str)
        self.console_handler.setFormatter(console_formatter)
        self.file_handler = RotatingFileHandler(logFile, mode="a", maxBytes=max_filesize,   # Max log file size: 5 MB (5242880 B) (5*1024*1024)
                                        backupCount=backupCount, encoding="utf-8", delay=0)
        self.file_handler.setFormatter(self.log_formatter)
        self.file_handler.setLevel(logging.DEBUG)

        self.get_log = logging.getLogger(loggername)
        self.get_log.setLevel(logging.DEBUG)

        self.get_log.addHandler(self.file_handler)
        self.get_log.addHandler(self.console_handler)

    def set_dbglevel_debug(self):
        self.get_log.setLevel(logging.DEBUG)
        
    def set_dbglevel_info(self):
        self.get_log.setLevel(logging.INFO)

    def set_dbglevel_warning(self):
        self.get_log.setLevel(logging.WARNING)

    def set_dbglevel_error(self):
        self.get_log.setLevel(logging.ERROR)

    def set_dbglevel_critical(self):
        self.get_log.setLevel(logging.CRITICAL)

    #set level of console logging
    def console_dbglevel_debug(self):
        self.console_handler.setLevel(logging.DEBUG)

    def console_dbglevel_info(self):
        self.console_handler.setLevel(logging.INFO)

    def console_dbglevel_warning(self):
        self.console_handler.setLevel(logging.WARNING)

    def console_dbglevel_error(self):
        self.console_handler.setLevel(logging.ERROR)

    def console_dbglevel_critical(self):
        self.console_handler.setLevel(logging.CRITICAL)

    # set level of logfile logging
    def logfile_dbglevel_debug(self):
        self.file_handler.setLevel(logging.DEBUG)

    def logfile_dbglevel_info(self):
        self.file_handler.setLevel(logging.INFO)

    def logfile_dbglevel_warning(self):
        self.file_handler.setLevel(logging.WARNING)

    def logfile_dbglevel_error(self):
        self.file_handler.setLevel(logging.ERROR)

    def logfile_dbglevel_critical(self):
        self.file_handler.setLevel(logging.CRITICAL)

    def set_maxSize(self, maxBytes):
        self.file_handler.maxBytes = maxBytes

    def set_backupCount(self, backupCount):
        self.file_handler.backupCount = backupCount

    def console_dbglevel(self, levelname):
        if levelname.lower()=="debug":
            self.console_handler.setLevel(logging.DEBUG)
        elif levelname.lower()=="info":
            self.console_handler.setLevel(logging.INFO)
        elif levelname.lower()=="warning":
            self.console_handler.setLevel(logging.WARNING)
        elif levelname.lower()=="error":
            self.console_handler.setLevel(logging.ERROR)
        elif levelname.lower()=="critical":
            self.console_handler.setLevel(logging.CRITICAL)
        else:
            print(f"Level is not defined in console_dbglevel")

    def file_dbglevel(self, levelname):
        if levelname.lower()=="debug":
            self.file_handler.setLevel(logging.DEBUG)
        elif levelname.lower()=="info":
            self.file_handler.setLevel(logging.INFO)
        elif levelname.lower()=="warning":
            self.file_handler.setLevel(logging.WARNING)
        elif levelname.lower()=="error":
            self.file_handler.setLevel(logging.ERROR)
        elif levelname.lower()=="critical":
            self.file_handler.setLevel(logging.CRITICAL)
        else:
            print(f"Level is not defined in file_dbglevel")