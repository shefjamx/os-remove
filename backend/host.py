import socket
import random
import string
import json
import threading

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
                self.remove_party(addr[0])
                
            # decode data
            if data:
                print(data.decode())
                json_data = json.loads(data.decode())
                if json_data['endpoint'] == 'create-party':
                    self.create_party(addr[0], clientsocket)
                elif json_data['endpoint'] == 'join-party':
                    print("joined party")
                    self.join_party(json_data['code'], clientsocket)
            
    def remove_party(self, leader: str):
        for party in self.parties:
            if party.get_leader() == leader:
                self.parties.remove(party)

    def create_party(self, leader: str, clientsocket):
        # check if leader not in party
        for party in self.parties:
            if party.get_leader() == leader:
                self.conn.send("Leader already in party".encode())
                return
            
        self.parties.append(Party(clientsocket))
        clientsocket.send(f"Party code is: {self.parties[-1].get_code()}".encode())

    def join_party(self, code: str, player):
        for party in self.parties:
            if party.get_code() == code:
                party.join_party(player)
                print("Code: " + party.get_code())
                print("Party Leader: " + party.get_leader())
                print("Member: " + party.get_player())
                party.test_send_leader("from client")
                party.test_send_client("from leader")
                return
        self.conn.send("Party doesn't exist".encode())

class Party():
    def __init__(self, leader, player = None):
        self.leader = leader # ip of leader
        self.code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        self.player = player

    def test_send_leader(self, data):
        self.leader.send(f"Hello from {data}".encode())
        print("Im being sent")

    def test_send_client(self, data):
        self.player.send(f"Hello from {data}".encode())

    def get_player(self):#
        if not self.is_empty():
            return self.player
        else:
            return ""

    def get_leader(self):
        return str(self.leader.getsockname()[0])
    
    def get_player(self):
        return str(self.player.getsockname()[0])

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
    
server = Server('0.0.0.0', 3000)
server.run()
