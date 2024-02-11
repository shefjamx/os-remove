import socket
import json
import time
import threading
#from misc.logger import log
#from misc.settings import ADDRESS, PORT

def log(string, type="DEBUG"):
    allowed_types = ["DEBUG", "INFO", "WARNING", "ERROR"]
    print(f"{type.upper() if type.upper() in allowed_types else 'OTHER'} \t> {string}")

# NETWORK
ADDRESS = '192.168.0.109' 
PORT = 3000

class Client():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.is_connected = False
        self.is_listening = True # listens by default
        self.party_code = ""

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # attempt connection
        try:
            self.socket.connect((self.host, self.port))
            self.is_connected = True
            log("Connected to server.", type="INFO")
            # start listening thread
            thread = threading.Thread(target=self.run)
            thread.start()
        except Exception as e:
            log(f"Failed to connect to socket. Traceback:\n {str(e)}", type="ERROR")
        
    def disconect(self):
        try:
            self.socket.close()
            self.is_connected = False
            log("Disconnected from server.", type="INFO")
        except Exception as e:
            log(f"Failed to disconnect from socket. Traceback:\n {str(e)}", type="ERROR")
        
    def run(self):   
        log("Listening for server pings...", type="INFO")
        while True:
            # as soon as connection is estanlished and sockets 
            data = self.socket.recv(1024)
            if data:
                json_data = json.loads(data.decode())
                if json_data['type'] == "start":
                   epoch_start_time = json_data['timestamp']
                   print(epoch_start_time)
                elif json_data['type'] == "code":
                   party_code = json_data['code']
                   print(party_code)
                   self.party_code = party_code

    def get_party_code(self):
        return str(self.party_code)

    def join_party(self, party_code: str):
        try:
            self.socket.send(
                '{"endpoint": "join-party, "code" : "C" }'.replace("C", party_code).encode()
            )  
            log("Connected to server.", type="INFO")
        except Exception as e:
            log(f"Failed to join party. Traceback:\n {str(e)}", type="ERROR")

    def create_party(self):
        try:
            self.socket.send(
                '{"endpoint" : "create-party"}'.encode()
            )
        except Exception as e:
            log(f"Failed to create party. Traceback: \n {str(e)}", type="ERROR")

    def start_game(self):
        try:
            self.socket.send(
                '{"endpoint" : "start-game"}'.encode()
            )
        except Exception as e:
            log(f"Failed to start game. Might be caused by sudden disconnection.")

    def set_is_listening(self, val: bool):
        self.is_listening = val
