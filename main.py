from kivy.app import App  # required base class for your app.
from kivy.uix.screenmanager import ScreenManager, Screen

from ConnectPage import ConnectPage
from InfoPage import InfoPage
from ChatPage import ChatPage


class ChatApp(App):
    def __init__(self):
        super().__init__()
        self.info_page: InfoPage = InfoPage()
        self.connect_page: ConnectPage = ConnectPage()
        self.screen_manager: ScreenManager = ScreenManager()
        self.chat_page: ChatPage = ChatPage()

    def build(self):
        self.setup_widget('Connect', self.connect_page)
        self.setup_widget('Info', self.info_page)
        self.setup_widget('Chat', self.chat_page)

        return self.screen_manager

    def setup_widget(self, screen_name, widget):
        screen = Screen(name=screen_name)
        screen.add_widget(widget)
        self.screen_manager.add_widget(screen)
        widget.app = self


if __name__ == "__main__":
    chat_app = ChatApp()
    chat_app.run()
