import json
from json import JSONDecodeError

from constants import DB_FILE_NAME
from logger_manager import get_logger

_logger = get_logger("DBManager")


class DBManager:
    """
    Provides simple api for DB (as file)
    """

    def __init__(self):
        self.file_name = DB_FILE_NAME
        with open(self.file_name, "w") as f:
            f.write("{}")

    def get_dict_from_db(self):
        try:
            with open(self.file_name, "r") as f:
                json_f = json.load(f)
            return json_f
        except FileNotFoundError:
            _logger.error(f"File {self.file_name} does not exists")
            return {}
        except JSONDecodeError:
            _logger.error(
                f"Error when trying to load json object from file")
            return {}

    def save_dict_to_db(self, json_file):
        try:
            with open(self.file_name, "w") as f:
                json.dump(json_file, f)
        except FileNotFoundError:
            _logger.error(f"File {self.file_name} does not exists")
