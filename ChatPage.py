import sys

from kivy.uix.gridlayout import GridLayout  # one of many layout structures
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from ScrollableLabel import ScrollableLabel
from kivy.clock import Clock

from SocketClient import SocketClient


class ChatPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.socketClient = None
        self.app = None

        self.cols = 1
        self.rows = 2

        self.history = ScrollableLabel(height=Window.size[1] * 0.9, size_hint_y=None)
        self.add_widget(self.history)

        self.new_message = TextInput(width=Window.size[0] * 0.8, size_hint_x=None, multiline=False)
        self.send = Button(text="Send")
        self.send.bind(on_press=self.send_message)

        bottom_line = GridLayout(cols=2)
        bottom_line.add_widget(self.new_message)
        bottom_line.add_widget(self.send)
        self.add_widget(bottom_line)

        Window.bind(on_key_down=self.on_key_down)

        Clock.schedule_once(self.focus_text_input, 1)

    def setup_socket(self, socket):
        self.socketClient = socket
        self.socketClient.start_listening(self.incoming_message, self.show_error)

    def incoming_message(self, username, message):
        self.history.update_chat_history(f'[color=20dd20]{username}[/color] > {message}')

    def focus_text_input(self, _):
        self.new_message.focus = True

    def on_key_down(self, instance, keyboard, keycode, text, modifiers):
        if keycode == 40:
            self.send_message(None)

    def show_error(self, message):
        self.app.info_page.update_info(message)
        self.app.screen_manager.current = 'Info'
        Clock.schedule_once(sys.exit, 10)

    def send_message(self, _):
        message = self.new_message.text
        self.new_message.text = ''

        if message:
            self.history.update_chat_history(
                f'[color=dd2020]{self.app.connect_page.username.text}[/color] > {message}')
            self.socketClient.send(message)

        Clock.schedule_once(self.focus_text_input, 0.1)
