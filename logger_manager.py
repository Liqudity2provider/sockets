import logging

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(level=logging.DEBUG)


def get_logger(log_name,
               level=logging.DEBUG,
               file=False,
               file_level=logging.ERROR):
    """
    :param file_level: NOTSET, DEBUG, INFO, WARNING, ERROR
    :param file: bool
    :param level: NOTSET, DEBUG, INFO, WARNING, ERROR
    :type log_name: str
    :type level: int
    """

    _logger = logging.getLogger(log_name)

    if file:
        fh = logging.FileHandler(f"monitor_logfile.log")
        fh.setLevel(file_level)
        _logger.addHandler(fh)

    return _logger
