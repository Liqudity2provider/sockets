import datetime
import json
import logging
from json import JSONDecodeError

import zmq

from logger_manager import get_logger

_logger = get_logger("monitor", level=logging.ERROR, file=True)


class AbstractModule:
    """
    This module creates instances of modules and saves their last state,
    last time sent message and first message.
    Handles errors.
    """

    def __init__(self, name, time_without_message=5):
        self.name = name
        self.max_time_without_message = time_without_message
        self.__state = None
        self.__last_time_sent = None
        self.__first_time_sent = datetime.datetime.utcnow().timestamp()

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, value):
        self.last_time_sent = datetime.datetime.utcnow().timestamp()
        self.__state = value

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


class ModuleProvider:
    def __init__(self):
        self.__modules = {}
        self.__modules_by_timestamp = {}

    def all_modules(self):
        return self.__modules

    def add_module_or_return(self, module_name) -> AbstractModule:
        if module_name not in self.__modules:
            self.__modules[module_name] = AbstractModule(module_name)
        return self.__modules.get(module_name)

    def get_module(self, module_name):
        self.__modules.get(module_name)


class MonitorModules:
    def __init__(self, module_prov: ModuleProvider):
        self.module_prov = module_prov

    def process(self):
        socket = self.create_socket()

        while True:
            self.process_message(socket)

            self.check_if_module_offline()

    @staticmethod
    def create_socket():

        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.connect("tcp://localhost:5555")
        socket.setsockopt(zmq.SUBSCRIBE, b'')
        return socket

    @staticmethod
    def log_message(message):
        _logger.error(message)

    @staticmethod
    def get_message_from_socket(socket):
        message = socket.recv()

        try:
            json_message = json.loads(message)
            return json_message

        except JSONDecodeError:
            _logger.error(f"Error when trying to load json from socket")

        except socket.error as e:
            _logger.error(f"An error occurred when trying to get message "
                          f"from socket. Error: ", e)

    def process_message(self, socket):
        json_message = self.get_message_from_socket(socket)

        if not json_message:
            return

        module_name = json_message.get("module")

        module = self.module_prov.add_module_or_return(module_name)
        module.state = json_message.get("state")

        _logger.debug(json_message)

        if json_message.get("log-stream") == "stderr":
            self.log_message(json_message)
            module.handler(json_message)

    def check_if_module_offline(self):
        for m_name, module in self.module_prov.all_modules().items():
            time_now = datetime.datetime.utcnow().timestamp()
            if (time_now - module.last_time_sent) > \
                    module.max_time_without_message:
                _logger.error(
                    f"Module {m_name} is offline for more than "
                    f"{module.max_time_without_message} seconds.")


if __name__ == '__main__':
    mm = MonitorModules(
        module_prov=ModuleProvider()
    )
    mm.process()
