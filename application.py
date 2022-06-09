import logging  # pip install pyzmq
import random
from datetime import datetime
from time import sleep

import zmq
from faker import Faker
from faker.providers import BaseProvider

from logger_manager import get_logger

random.seed = 0
Faker.seed = 0
_logger = get_logger("test")


class ModuleProvider(BaseProvider):

    @staticmethod
    def module_name():
        return random.choice(['evse', 'ocpp', 'slac'])

    @staticmethod
    def module_state():
        """
        Random states are not really reasonable, but this is just for testing
        """

        return random.choice(
            ['initializing', 'idle', 'charging', 'finalizing'])

    @staticmethod
    def module_output():
        stream = random.choice(['stdout', 'stdout', 'stderr'])

        message = 'Something happened.'
        return stream, message


class PostFakeLogs:
    def __init__(self):
        self.fake = Faker()
        self.fake.add_provider(ModuleProvider)

    def process(self):
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.bind("tcp://*:5555")
        try:
            while True:
                log_output = self.fake.module_output()
                msg = {'module': self.fake.module_name(),
                       'timestamp': datetime.now().isoformat(),
                       'state': self.fake.module_state(),
                       'log-stream': log_output[0],
                       'logmessage': log_output[1]
                       }
                _logger.debug(msg)
                socket.send_json(msg)
                sleep(1)
        except KeyboardInterrupt:
            print("Program has finished")


if __name__ == '__main__':
    pfl = PostFakeLogs()
    pfl.process()
