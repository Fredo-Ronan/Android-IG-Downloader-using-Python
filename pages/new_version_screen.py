# new_version_screen.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
import webbrowser
from kivy.uix.floatlayout import FloatLayout

class NewVersionScreen(Screen):
    def __init__(self, version_text, current, show_main_screen, **kwargs):
        super(NewVersionScreen, self).__init__(**kwargs)

        self.url = 'https://github.com/Fredo-Ronan/Android-IG-Downloader-using-Python/releases/latest'

        header_layout = FloatLayout(size=(0, 0), size_hint=(1, None), height=500)

        # Create widgets for the new version screen
        label1 = Label(
            text=f'New version {version_text} is available',
            pos_hint={'center_x': 0.5, 'center_y': 0.6}
        )

        label2 = Label(
            text=f'Current version is {current}',
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )

        header_layout.add_widget(label1)
        header_layout.add_widget(label2)

        button_update = Button(
            text='Update', 
            on_press=self.open_link_to_new_version,
            background_color=[0, 1, 0, 1]
        )

        button_close = Button(
            text='Close', 
            on_press=show_main_screen,
            background_color=[1, 0, 0, 1]
        )

        self.name = 'new_version'

        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Add widgets to the screen
        self.layout.add_widget(header_layout)
        self.layout.add_widget(button_update)
        self.layout.add_widget(button_close)
        
        self.add_widget(self.layout)

    def open_link_to_new_version(self, instance):
        webbrowser.open(self.url)
