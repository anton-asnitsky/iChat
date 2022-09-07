import os
import sys

from SocketClient import SocketClient
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout  # one of many layout structures
from kivy.uix.textinput import TextInput  # allow for ...text input.
from kivy.uix.button import Button
from kivy.clock import Clock


class ConnectPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app = None
        self.cols = 2

        self.socket = SocketClient()

        if os.path.isfile("prev_details.txt"):
            with open("prev_details.txt", "r") as f:
                d = f.read().split(",")
                prev_ip = d[0]
                prev_port = d[1]
                prev_username = d[2]
        else:
            prev_ip = ''
            prev_port = ''
            prev_username = ''

        self.add_widget(Label(text='IP:'))
        self.ip = TextInput(text=prev_ip, multiline=False)
        self.add_widget(self.ip)

        self.add_widget(Label(text='Port:'))
        self.port = TextInput(text=prev_port, multiline=False)
        self.add_widget(self.port)

        self.add_widget(Label(text='Username:'))
        self.username = TextInput(text=prev_username, multiline=False)
        self.add_widget(self.username)

        self.join = Button(text="Join")
        self.join.bind(on_press=self.join_button)
        self.add_widget(Label())
        self.add_widget(self.join)

    def join_button(self, instance):
        port = self.port.text
        ip = self.ip.text
        username = self.username.text
        with open("prev_details.txt", "w") as f:
            f.write(f"{ip},{port},{username}")

        info = f"Joining {ip}:{port} as {username}"
        self.app.info_page.update_info(info)
        self.app.screen_manager.current = 'Info'

        self.connect()

    def connect(self):
        port = int(self.port.text)
        ip = self.ip.text
        username = self.username.text

        if not self.socket.connect(ip, port, username, self.show_error):
            return

        self.app.screen_manager.current = 'Chat'
        self.app.chat_page.setup_socket(self.socket)

    def show_error(self, message):
        self.app.info_page.update_info(message)
        self.app.screen_manager.current = 'Info'
        Clock.schedule_once(sys.exit, 10)
