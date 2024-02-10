import socket

test_message_join_party = '{"endpoint" : "join-party", "code" : "X8HT" }'

class Client():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.is_connected = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.is_connected = True

        # once connected a
        # attempt to join party using code
        self.socket.send(test_message_join_party.encode())
        self.ping_num = 0 

    def run(self):
        while True:
            data = self.socket.recv(1024)
            if data:
                print(data.decode())

client = Client('192.168.0.109', 3000)
client.run()