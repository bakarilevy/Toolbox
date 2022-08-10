import socket
import select
import threading


# Can I make this more devious with Scapy?
SOCKS_VERSION = 5

class Proxy:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_available_methods(self, nmethods, connection):
        methods = []
        for i in range(nmethods):
            methods.append(ord(connection.recv(1)))
        return methods

    def verify_credentials(connection):
        version = ord(connection.recv(1)) # should be 1

        username_len = ord(connection.recv(1))
        username = connection.recv(username_len).decode('utf-8')

        password_len = ord(connection.recv(1))
        password = connection.recv(password_len).decode('utf-8')

        if username == self.username and password == self.password:
            # Success status code 0
            response = bytes([version, 0])
            connection.sendall(response)
            return True
        
        # Failure to login status != 0
        response = bytes([version, 0xff])
        connection.sendall(response)
        connection.close()
        return False


    def generate_failed_reply(self, address_type, error_number):
        return b''.join([
            SOCKS_VERSION.to_bytes(1, 'big'),
            error_number.to_bytes(1, 'big'),
            int(0).to_bytes(1, 'big'),
            address_type.to_bytes(1, 'big'),
            int(0).to_bytes(4, 'big'),
            int(0).to_bytes(4, 'big'),
        ])

    def exchange_loop(self, connection, remote):
        while True:
            # Wait for client or remote socket is available for read
            r, w, e = select.select([connection, remote], [], [])

            if connection in r:
                data = connection.recv(4096)
                if remote.send(data) <= 0:
                    break
            
            if remote in r:
                data = remote.recv(4096)
                if client.send(data) <= 0:
                    break

    def handle_client(self, connection):
        # Read and unpack 2 bytes from the client
        version, nmethods = connection.recv(2)
        # Get available methods [0, 1, 2]
        methods = self.get_available_methods(nmethods, connection)
        # Accept only USERNAME/PASSWORD auth
        if 2 not in set(methods):
            connection.close()
            return
        # Send welcome message
        connection.sendall(bytes([SOCKS_VERSION, 2]))

        if not self.verify_credentials(connection):
            return
        
        # Request (version=5)
        version, cmd, _, address_type = connection.recv(4)

        if address_type == 1: # IPv4
            address = socket.inet_ntoa(connection.recv(4))
        elif address_type == 3: # Domain name
            domain_length = connection.recv(1)[0]
            address = connection.recv(domain_length)
            socket.gethostbyname(address)
        # Convert bytes to unsigned short array
        port = int.from_bytes(connection.recv(2), 'big', signed=False)
        
        try:
            if cmd == 1: # Connect
                remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                remote.connect((address, port))
                bind_address = remote.getsockname()
                print(f"[*] Connected to: {address} on port: {port}")
            else:
                connection.close()
            addr = int.from_bytes(socket.inet_aton(bind_address[0]), 'big', signed=False)
            port = bind_address[1]

            reply = b''.join([
                SOCKS_VERSION.to_bytes(1, 'big'),
                int(0).to_bytes(1, 'big'),
                int(0).to_bytes(1, 'big'),
                int(1).to_bytes(1, 'big'),
                addr.to_bytes(4, 'big'),
                port.to_bytes(2, 'big')
            ])

        except Exception as e:
            # Return connection refused on exception
            reply = self.generate_failed_reply(address_type, 5)
            connection.sendall(reply)

        # Establish data exchange
        if reply[1] == 0 and cmd == 1:
            self.exchange_loop(connection, remote)
        
        connection.close()

    def run(self, host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.listen()
        print(f"[*] SOCKS5 proxy server running on port {port}")

        while True:
            connection, address = s.accept()
            print(f"[+] New connection received from: {address}")
            t = threading.Thread(self.handle_client, args=(connection,))
            t.start()

if __name__=='__main__':
    proxy = Proxy("username", "password")
    proxy.run("127.0.0.1", 3000)