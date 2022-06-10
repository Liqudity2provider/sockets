import json
from json import JSONDecodeError

import zmq

from logger_manager import get_logger

_logger = get_logger("SocketManager")


class SocketManager:
    """
    This class manages connection to socket and receiving messages from socket.
    """

    def __init__(self):
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.connect("tcp://localhost:5555")
        socket.setsockopt(zmq.SUBSCRIBE, b'')
        self.socket = socket

    def get_message_from_socket(self):
        message = self.socket.recv()

        try:
            json_message = json.loads(message)
            return json_message

        except JSONDecodeError:
            _logger.error(f"Error when trying to load json from socket")

        except self.socket.error as e:
            _logger.error(f"An error occurred when trying to get message "
                          f"from socket. Error: ", e)
