import socket
import random
import string
import json
import threading
import time

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.parties = []
        self.conn = None
        self.addr = None
        self.init = None

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen()

    def run(self):
        while True:
            print("Server Starting...")
            conn, addr = self.socket.accept()
            thread = threading.Thread(target=self.listen, args=(conn, addr))
            print(f'Connected to  {addr}')
            thread.start()
            self.init = True

    
    def listen(self, clientsocket, addr):
        while True:
            data = clientsocket.recv(2048)
            if not data:
                clientsocket.close()
                self.remove_party(clientsocket)
                
            # decode data
            if data:
                print(data.decode())
                json_data = json.loads(data.decode())
                if json_data['endpoint'] == 'create-party':
                    self.create_party(json_data['song'], addr[0], clientsocket)
                elif json_data['endpoint'] == 'join-party':
                    print("joined party")
                    self.join_party(json_data['code'], clientsocket)
                elif json_data['endpoint'] == 'update-song':
                    new_song = json_data['song']
                    code = json_data['code']
                    # find party
                    for party in self.parties:
                        print("reached")
                        if party.get_code() == code:
                            party.set_song(new_song)
                elif json_data['endpoint'] == 'leave-party':
                    self.leave_or_remove_party(clientsocket)
                    clientsocket.send('{"type": "left-party", "message": "C"}'.replace("C", "Left party").encode())
                elif json_data['endpoint'] == 'start-game':
                    print("starting game...")
                    for party in self.parties:  
                        if party.get_leader_str() == clientsocket.getpeername()[0]:
                            # only start game if leader called it
                            party.start_game()
                elif json_data['endpoint'] == "update-spawn-rate":
                    new_spawn_rate = json_data['value']
                    for party in self.parties:
                        if party.get_leader_str() == clientsocket.getpeername()[0]:
                            # if leader sending updates, transmit back to client
                            self.update_spawn_rate(party, True, new_spawn_rate)
                        elif party.get_player_str() == clientsocket.getsockname()[0]:
                             self.update_spawn_rate(party, False, new_spawn_rate)

    def update_spawn_rate(self, party, leader: bool, value):
        message = '{"type" : "update-spawn-rate", "value": "C"}'.replace("C", value).encode()
        if leader:
            # leader to player
            party.player.send(message)
        else:
            # player to leader
            party.leader.send(message)
            
    def leave_or_remove_party(self, conn):
        for party in self.parties:
            if party.get_leader_str() == conn.getpeername()[0]:
                self.parties.remove(party)
            elif party.get_player_str() == conn.getpeername()[0]:
                party.reset_player()
 
    def create_party(self, song: str, leader: str, clientsocket):
        # check if leader not in party
        for party in self.parties:
            if party.get_leader_str() == leader:
                clientsocket.send("Leader already in party".encode())
                return
            
        self.parties.append(Party(clientsocket, song))
        clientsocket.send(
            '{"type" : "code", "code": "C"}'.replace("C", str(self.parties[-1].get_code())).encode()
        )

    def join_party(self, code: str, player):
        for party in self.parties:
            if party.get_code() == code:
                party.join_party(player)
                print("Code: " + party.get_code())
                print("Party Leader: " + party.get_leader_str())
                print("Member: " + party.get_player_str())
                print("Song" + party.get_song())
                return
        self.conn.send("Party doesn't exist".encode())

class Party():
    def __init__(self, leader, song, player = None):
        self.leader = leader # conn of leader
        self.song = song
        self.code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        self.player = player
        self.wager_folder_path = ""

    def set_wager_folder_path(self, new_path: str):
        self.wager_folder_path = new_path
    
    def get_wager_folder_path(self):
        return self.wager_folder_path

    def get_song(self):
        return self.song
    
    def set_song(self, new_song: str):
        self.song = new_song

    def test_send_leader(self, data):
        self.leader.send(f"Hello from {data}".encode())
        print("Im being sent")

    def test_send_client(self, data):
        self.player.send(f"Hello from {data}".encode())

    def get_player(self):
        if not self.is_empty():
            return self.player
        else:
            return ""

    def reset_player(self):
        self.player = None

    def get_leader_str(self):
        return str(self.leader.getpeername()[0])
    
    def get_player_str(self):
        return str(self.player.getpeername()[0])

    def get_code(self):
        """
        Returns party code
        """
        return self.code

    def is_empty(self):
        """
        Checks if the party is empty
        """
        if self.player == None:
            return True
        else:
            return False
    
    def join_party(self, player):
        """
        checks if party is empty, and allows player to join
        """
        if self.is_empty():
            self.player = player

    def start_game(self):
        # send ready message
        # if both ready, send run game()
        offset = 5
        if self.player == None:
            print("Could not start game, not enough players")
            return
        message = '{"type": "start", C}'.replace("C", f'"timestamp": "{str(time.time() + offset)}", "song" : "{self.get_song()}"').encode()
        self.leader.send(message)
        self.player.send(message)

    def game(self):
        return
    
server = Server('0.0.0.0', 3000)
server.run()
