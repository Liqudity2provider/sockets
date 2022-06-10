## This is project about receiving messages from socket and then processing them

There are 3 file that you can run:
1. application.py - sending fake messages to socket connection

![image](https://user-images.githubusercontent.com/56783638/173069236-a8f82487-c080-4109-ae58-adf8cdc7a984.png)


2. monitor.py - monitors and receives messages from socket connection. Logging if only stderr


![image](https://user-images.githubusercontent.com/56783638/173069384-a3246485-8773-407b-95e5-46b4b5c7af93.png)


3. check_offilne_module.py - checks if there is any module that is offline for specific time

![image](https://user-images.githubusercontent.com/56783638/173069461-10993341-1ddd-4054-ac57-0cbf21921fea.png)

There're also some modules:

- db_manager.py - Provides simple api for DB (as file)
- logger_manager.py - creates specific logger for every module
- modules.py - creates AbstractModule (each module) and ModuleProvider (to save all modules here)
- socket_manager.py - manages connection to socket and receiving messages from socket.
