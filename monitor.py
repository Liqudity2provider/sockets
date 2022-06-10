from logger_manager import get_logger
from modules import ModuleProvider
from socket_manager import SocketManager

_logger = get_logger("monitor", file=True)


class MonitorModules:
    """
    This class provides functionality to process messages from sockets.
    """

    def __init__(self,
                 module_prov: ModuleProvider,
                 socket_manager: SocketManager):
        self.module_prov = module_prov
        self.socket_manager = socket_manager

    def process(self):
        while True:
            self.process_message()

    @staticmethod
    def log_message(message):
        _logger.error(message)

    def process_message(self):
        """
        Method provides functionality of getting messages from socket,
        then change state of module and proceed error message if received one
        """
        json_message = self.socket_manager.get_message_from_socket()

        if not json_message:
            return

        module_name = json_message.get("module")
        if not module_name:
            _logger.debug(f"Can't monitor module with name - {module_name}")

        module = self.module_prov.add_module_or_return(module_name)

        # changing last state of module
        module.state = json_message.get("state")

        _logger.debug(json_message)

        if json_message.get("log-stream") == "stderr":
            self.log_message(json_message)
            module.handler(json_message)


if __name__ == '__main__':
    mm = MonitorModules(
        module_prov=ModuleProvider(),
        socket_manager=SocketManager()
    )
    mm.process()
