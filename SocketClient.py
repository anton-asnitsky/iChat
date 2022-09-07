import socket
from threading import Thread


class SocketClient:
    def __init__(self):
        self.HEADER_LENGTH = 10
        self.client_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, ip, port, my_username, error_callback):
        try:
            self.client_socket.connect((ip, port))
        except Exception as e:
            error_callback(f"Connection error: {str(e)}")
            return False

        username = my_username.encode('utf-8')
        username_header = f"{len(username):<{self.HEADER_LENGTH}}".encode('utf-8')
        self.client_socket.send(username_header + username)

        return True

    def send(self, message):
        message = message.encode('utf-8')
        message_header = f"{len(message):<{self.HEADER_LENGTH}}".encode('utf-8')
        self.client_socket.send(message_header + message)

    def start_listening(self, incoming_message_callback, error_callback):
        Thread(target=self.listen, args=(incoming_message_callback, error_callback), daemon=True).start()

    def listen(self, incoming_message_callback, error_callback):
        while True:
            try:
                while True:
                    username_header = self.client_socket.recv(self.HEADER_LENGTH)

                    if not len(username_header):
                        error_callback('Connection closed by the server')

                    username_length = int(username_header.decode('utf-8').strip())
                    username = self.client_socket.recv(username_length).decode('utf-8')
                    message_header = self.client_socket.recv(self.HEADER_LENGTH)
                    message_length = int(message_header.decode('utf-8').strip())
                    message = self.client_socket.recv(message_length).decode('utf-8')
                    incoming_message_callback(username, message)

            except Exception as e:
                error_callback('Reading error: {}'.format(str(e)))
