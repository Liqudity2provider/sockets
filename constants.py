import pathlib

path_to_project = pathlib.Path(__file__).parent

DB_FILE_NAME = str(path_to_project) + "/db.json"
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
