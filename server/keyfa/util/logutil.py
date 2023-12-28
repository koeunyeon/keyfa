import os
import logging
import logging.handlers

from keyfa.config import Config


# LOG_FMT = '{"timestamp" : "%(asctime)s", "level" : "%(levelname)s", "message": "%(message)s"}'

loggers = {}

def get_logger(logger_name:str = Config.log.name, log_dir:str = Config.log.path, log_level=logging.DEBUG):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    global loggers
    
    if logger_name in loggers:
        return loggers[logger_name]
    
    LOG_FMT = '{"timestamp" : "%(asctime)s", "level" : "%(levelname)s", "message": "%(message)s"}'

    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)
    formatter = logging.Formatter(LOG_FMT)

    stream_hander = logging.StreamHandler()
    stream_hander.setFormatter(formatter)
    logger.addHandler(stream_hander)
    
    log_file = f"{logger_name}.log"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_path = os.path.join(log_dir, log_file)
    file_handler = logging.handlers.TimedRotatingFileHandler(
        filename=log_path,
        when="midnight",
        interval=1,
        encoding="utf8"
    )
    
    # file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    file_handler.suffix = "%Y%m%d"
    logger.addHandler(file_handler)    

    loggers[logger_name] = logger
    return logger

    


