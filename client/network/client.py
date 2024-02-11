import socket
import json
import time
import threading
from misc.logger import log
from scenes.play import PlayScene

class Client():
    def __init__(self, host, port, main_loop):
        self.host = host
        self.port = port
        self.main_loop = main_loop
        self.is_connected = False
        self.is_listening = True # listens by default
        self.party_code = ""
        self.is_in_party = False
        self.song = "ascension-to-heaven"
        self.start_epoch = 0

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
                   self.start_epoch = json_data['timestamp']
                   self.song = json_data['song']
                   self.main_loop.change_scene(PlayScene, self.song, float(self.start_epoch), False)
                   print(self.start_epoch)
                elif json_data['type'] == "code":
                   party_code = json_data['code']
                   print(party_code)
                   self.party_code = party_code
                elif json_data['type'] == "left-party":
                    self.is_in_party = False
                    log("Left party")
                elif json_data['type'] == "update-spawn-rate":
                    value = float(json_data['value'])
                    print(json_data['value'])
                    self.main_loop.current_scene.enemyHandler.updateSpawnRate(value)

    def get_party_code(self):
        return str(self.party_code)
    
    def get_epoch_start(self):
        return self.start_epoch
    
    def update_song(self, new_song: str):
        try:
            self.socket.send(
                '{"endpoint": "update-song", C}'.replace("C", f'"song" : "{new_song}", "code": "{self.get_party_code}"').encode()
            )
        except Exception as e:
            log(f"Failed to update song. Traceback:\n {str(e)}", type="ERROR")

    def join_party(self, party_code: str):
        try:
            self.socket.send(
                '{"endpoint": "join-party", "code" : "C"}'.replace("C", party_code).encode()
            )  
            log("JOINED PARTY.", type="INFO") 
            self.is_in_party = True
        except Exception as e:
            log(f"Failed to join party. Traceback:\n {str(e)}", type="ERROR")

    def create_party(self):
        try:
            self.socket.send(
                '{"endpoint" : "create-party", "song": "C"}'.replace("C", self.song).encode()
            )
            self.is_in_party = True
        except Exception as e:
            log(f"Failed to create party. Traceback: \n {str(e)}", type="ERROR")

    def leave_party(self):
        try:
            self.socket.send(
                '{"endpoint" : "leave-party"}'.encode()
            )
            self.is_in_party = True
        except Exception as e:
            log(f"Failed to leave party. Traceback: \n {str(e)}", type="ERROR")

    def start_game(self):
        try:
            self.socket.send(
                '{"endpoint" : "start-game"}'.encode()
            )
        except Exception as e:
            log(f"Failed to start game. Might be caused by sudden disconnection.")

    def send_spawn_rate(self, new_spawn_rate):
        try:
            self.socket.send(
                '{"endpoint" : "update-spawn-rate", "value": "C"}'.replace("C", str(new_spawn_rate)).encode()
            )
        except Exception as e:
            log(f"Failed to update spawn rate\n {str(e)}")


    def set_is_listening(self, val: bool):
        self.is_listening = val
