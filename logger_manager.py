import logging

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"


def get_logger(log_name, level=logging.DEBUG, file=False):
    """
    :param file: bool
    :param level: NOTSET, DEBUG, INFO, WARNING, ERROR
    :type log_name: str
    :type level: int
    """

    if file:
        logging.basicConfig(filename=f"{log_name}_logfile.log",
                            filemode="a",
                            format=LOG_FORMAT,
                            level=logging.ERROR)
    else:
        logging.basicConfig()

    module_logger = logging.getLogger(log_name)
    if level:
        module_logger.setLevel(level)
    return module_logger
