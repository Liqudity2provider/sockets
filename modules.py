import datetime

from db_manager import DBManager


class AbstractModule:
    """
    This module creates instances of modules and saves their last state,
    last time sent message and first message.
    Handles errors.
    Writes to db last activity of module.
    """

    def __init__(self, name, time_without_message=5):
        self.name = name
        self.max_time_without_message = time_without_message
        self.__state = None
        self.__last_time_sent = None
        self.__first_time_sent = datetime.datetime.utcnow().timestamp()
        self.db_service = DBManager()

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, value):
        """
        1. Saves last time when module send its state.
        2. Changes state
        3. Writes to DB layer last activity of module
        :param value: new value of state
        """
        self.last_time_sent = datetime.datetime.utcnow().timestamp()
        self.__state = value
        self.write_to_db_last_activity()

    @staticmethod
    def handler(message):
        """
        This method should handle errors based on message
        """

    @property
    def last_time_sent(self):
        return self.__last_time_sent

    @last_time_sent.setter
    def last_time_sent(self, value):
        self.__last_time_sent = value

    @property
    def first_time_sent(self):
        return self.__first_time_sent

    @first_time_sent.setter
    def first_time_sent(self, value):
        self.__first_time_sent = value

    def write_to_db_last_activity(self):
        """
        1. Get DB data
        2. Creates first activity of module if not yet.
        3. Update last activity of object
        4. Saves object to DB
        """
        json_f = self.db_service.get_dict_from_db()
        if not json_f.get(self.name):
            self.write_to_db_first_activity()
            json_f = self.db_service.get_dict_from_db()

        json_f[self.name].update({
            "last_activity": self.last_time_sent
        })
        self.db_service.save_dict_to_db(json_f)

    def write_to_db_first_activity(self):
        """
        When first write to db, need to be specified next fields:
        * first_activity
        * max_time_offline
        """
        json_f = self.db_service.get_dict_from_db()
        json_f[self.name] = {
            "first_activity": self.first_time_sent,
            "max_time_offline": self.max_time_without_message
        }
        self.db_service.save_dict_to_db(json_f)


class ModuleProvider:
    """
    This class provides simple storage for all modules, and manages them.
    """

    def __init__(self):
        self.__modules = {}

    def all_modules(self):
        return self.__modules

    def add_module_or_return(self, module_name) -> AbstractModule:
        if module_name not in self.__modules:
            self.__modules[module_name] = AbstractModule(module_name)
        return self.__modules.get(module_name)

    def get_module(self, module_name):
        self.__modules.get(module_name)
