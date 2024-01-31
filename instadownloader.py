from kivy.clock import Clock
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout  # Import FloatLayout

import instaloader
import requests
import re


class InstaDownloaderApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # FloatLayout for the header section
        header_layout = FloatLayout(size=(0, 0), size_hint=(1, None), height=100)

        # Header Labels
        header_label1 = Label(
            text='Instagram Downloader',
            font_size=40,
            bold=True,
            color=[1, 1, 1, 1],  # White color
            halign='center',  # Center align the text
            valign='middle',  # Vertically align the text in the middle
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
        )

        header_label2 = Label(
            text='by Fredo Ronan',
            font_size=24,
            color=[1, 1, 1, 1],  # White color
            halign='center',  # Center align the text
            valign='middle',  # Vertically align the text in the middle
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.1},  # Adjust position
        )

        header_layout.add_widget(header_label1)
        header_layout.add_widget(header_label2)

        # Input Box and Download Button
        self.link_input = TextInput(
            hint_text='Enter Instagram Link',
            multiline=False,
            write_tab=False,
        )
        download_button = Button(
            text='Download',
            font_size=40,
            on_press=self.show_download_popup,
            background_color=[0, 1, 1, 1],  # Blue color
        )

        # Progress Bar
        self.progress_bar = ProgressBar(max=1000, size_hint_y=None, height=30)

        # Add widgets to the layout
        self.layout.add_widget(header_layout)
        self.layout.add_widget(self.link_input)
        self.layout.add_widget(download_button)
        self.layout.add_widget(self.progress_bar)

        return self.layout

    def parse_link(self, link):
        clean_up_pattern = re.compile(r'https://www\.instagram\.com/([^/]+)/([^/?]+)/\?.*')
        match = re.search(clean_up_pattern, link)

        if match:
            type = match.group(1)
            short_code = match.group(2)
            print(type)
            print(short_code)
            return {"type": type, "short_code": short_code}
        else:
            return None

    def show_download_popup(self, instance):
        link = self.link_input.text
        parsed_code = self.parse_link(link)

        if parsed_code:
            download_popup = self.create_download_popup()
            download_popup.open()

            def download_callback(dt):
                self.download_instagram_media(parsed_code['short_code'])
                download_popup.dismiss()

            Clock.schedule_once(download_callback, 0.1)
        else:
            self.show_error_popup("Invalid Instagram link")

    def create_download_popup(self):
        download_popup = Popup(
            title='Downloading...',
            content=Label(text='Please wait while the download is in progress.'),
            size_hint=(None, None),
            size=(300, 150),
        )
        return download_popup

    def download_instagram_media(self, short_code):
        loader = instaloader.Instaloader()
        post = instaloader.Post.from_shortcode(loader.context, short_code)

        if post.is_video:
            video_url = post.video_url
            response = requests.get(video_url, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            chunk_size = 1024
            bytes_downloaded = 0

            with open(f"{post.owner_username}_{post.shortcode}.mp4", 'wb') as f:
                for data in response.iter_content(chunk_size=chunk_size):
                    f.write(data)
                    bytes_downloaded += len(data)
                    self.update_progress(bytes_downloaded, total_size)

            self.show_success_popup(f"Video downloaded: {post.owner_username}_{post.shortcode}.mp4")
        else:
            loader.download_post(post, target=f"{post.owner_username}_{post.shortcode}")

    def update_progress(self, value, max_value):
        # Update the progress bar value
        progress_percent = (value / max_value) * 1000
        self.progress_bar.value = progress_percent

    def show_error_popup(self, message):
        error_popup = Popup(
            title='Error',
            content=Label(text=message),
            size_hint=(None, None),
            size=(300, 150),
        )
        error_popup.open()

    def show_success_popup(self, message):
        success_popup = Popup(
            title='Success',
            content=Label(text=message),
            size_hint=(None, None),
            size=(300, 150),
        )
        success_popup.open()
        # Schedule a reset function after success popup disappears
        Clock.schedule_once(self.reset_layout, 3.0)

    def reset_layout(self, dt):
        # Reset text input and progress bar
        self.link_input.text = ''
        self.progress_bar.value = 0


if __name__ == "__main__":
    InstaDownloaderApp().run()
