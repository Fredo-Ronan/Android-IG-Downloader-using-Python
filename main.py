# insta_downloader_app.py
from kivy.config import Config
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from pages.main_screen import MainScreen
from pages.new_version_screen import NewVersionScreen
import requests
import sys
import os

Config.set('kivy', 'window_title', 'Fredo Instagram Downloader')

# https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

Config.set('kivy', 'window_icon', resource_path('assets\\icon.ico'))
Window.set_icon(resource_path('assets\\icon.ico'))
Window.set_title('Fredo Instagram Downloader')

class Fredo_Instagram_DownloaderApp(App):
    def build(self):
        # Check for a new version
        version_url = "https://api.github.com/repos/Fredo-Ronan/Android-IG-Downloader-using-Python/releases/latest"
        current_version = "1.2.5"
        latest_version = self.get_latest_version(version_url)
        
        if latest_version and latest_version != current_version:
            return self.create_new_version_app(current_version, latest_version)

        # If no new version, show the main screen
        return self.create_main_app(current_version)

    def get_latest_version(self, version_url):
        try:
            response = requests.get(version_url)
            response.raise_for_status()
            release_info = response.json()
            latest_version = release_info['tag_name']
            return latest_version
        except Exception as e:
            print(f"Error fetching latest version: {e}")
            return None

    def create_main_app(self, version_text):
        # Create the Screen Manager
        sm = ScreenManager()

        # Create screens
        main_screen = MainScreen(version_text=version_text)
        sm.add_widget(main_screen)

        # Set the current screen to 'main'
        sm.current = 'main'

        return sm

    def create_new_version_app(self, current_version, latest_version):
        # Create the Screen Manager
        sm = ScreenManager()

        # Create screens
        main_screen = MainScreen(version_text=current_version)
        new_version_screen = NewVersionScreen(version_text=latest_version, current=current_version, show_main_screen=self.show_main_screen)
        sm.add_widget(main_screen)
        sm.add_widget(new_version_screen)

        # Set the current screen to 'new_version'
        sm.current = 'new_version'

        return sm

    def show_new_version_screen(self):
        self.root.current = 'new_version'

    def show_main_screen(self, instance):
        self.root.current = 'main'

if __name__ == "__main__":
    Fredo_Instagram_DownloaderApp().run()
