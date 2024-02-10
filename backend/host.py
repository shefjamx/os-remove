import socket
import random
import string
import json

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
        print("Server Starting...")
        while True:
            conn, addr = self.socket.accept()
            print(f'Connected to  {addr}')
            self.conn = conn
            self.addr = addr
            self.init = True
            self.listen() # listen for pings

    
    def listen(self):
        while self.conn:
            data = self.conn.recv(2048)
            if not data:
                self.socket.close()
                self.remove_party(self.addr[0])
                
            for party in self.parties:
                print("Code: " + party.get_code())
                print("Party Leader: " + party.get_leader())
                print("Member: " + party.get_player())
                    
            # decode data
            if data:
                json_data = json.loads(data.decode())
                if json_data['endpoint'] == 'create-party':
                    self.create_party(self.addr[0])
                elif json_data['endpoint'] == 'join-party':
                    self.join_party(json_data['code'], self.addr[0])
            
    def remove_party(self, leader: str):
        for party in self.parties:
            if party.get_leader() == leader:
                self.parties.remove(party)

    def create_party(self, leader: str):
        # check if leader not in party
        for party in self.parties:
            if party.get_leader() == leader:
                self.conn.send("Leader already in party".encode())
                return
            
        self.parties.append(Party(leader))
        print("party created: " + self.parties[-1].get_code())

    def join_party(self, code: str, player: str):
        for party in self.parties:
            if party.get_code() == code:
                party.join_party(player)
                print("Code: " + party.get_code())
                print("Party Leader: " + party.get_leader())
                print("Member: " + party.get_player())
                return
        self.conn.send("Party doesn't exist".encode())

class Party():
    def __init__(self, leader, player = None):
        self.leader = leader # ip of leader
        self.code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        self.player = player

    def get_player(self):#
        if not self.is_empty():
            return self.player
        else:
            return ""

    def get_leader(self):
        return self.leader

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
            player = player
    
server = Server('0.0.0.0', 3000)
server.run()
