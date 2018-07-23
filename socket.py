import socket

class SocketSender:

    def __init__(self, host='localhost', port=9999):
        self.host=host
        self.port=port
        
        # Create a client socket
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __repr__(self):
        return f'SocketSender({self.host}, {self.port})'

    def connect(self):
        self.client.connect((self.host, self.port))
        print(f"Client connected successfully to {self.host} at port {self.port}")

    def send(self, msg):
        msgbytes = bytearray(msg, 'utf-8')
        totalsent = 0
        MSGLEN = len(msgbytes)
        while totalsent < MSGLEN:
            sent = self.client.send(msgbytes[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    
class SocketReceiver:
    def __init__(self, host='127.0.0.1', port=9999):
        self.host = host
        self.port = port

        # Create a server socket and bind it to host on port 9999
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))

    def __repr__(self):
        return f'SocketReceiver({self.host}, {self.port})'
    
    def listen(self, bufsize):
        self.server.listen(1)
        print('Server is listening at port ',self.port)

        # Establish connection with client.
        conn, addr = self.server.accept()     
        print('Connection from: ' + str(addr))

        while True:          
            data = conn.recv(bufsize).decode()
            if not data:
                break
            print ("--> " + str(data))
                  
        # Close the connection with the client
        conn.close()

