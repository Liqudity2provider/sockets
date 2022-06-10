import datetime
import time

from logger_manager import get_logger
from db_manager import DBManager

_logger = get_logger("check_offline_module")


class CheckOfflineModule:
    """
    Provides functionality to get objects from DB and check if they are
    sending logs more often then specified
    """
    def __init__(self, db_manager: DBManager):
        self.db_manager = db_manager

    def check_if_module_offline(self):
        while True:
            for m_name, v in self.db_manager.get_dict_from_db().items():
                time_now = datetime.datetime.utcnow().timestamp()
                _logger.debug("scanning...")
                try:
                    if (time_now - v.get("last_activity")) > \
                            v.get("max_time_offline"):
                        _logger.error(
                            f"Module {m_name} is offline for more than "
                            f"{v.get('max_time_offline')} seconds.")
                except TypeError:
                    continue
                time.sleep(1)


if __name__ == '__main__':
    com = CheckOfflineModule(db_manager=DBManager())
    com.check_if_module_offline()
