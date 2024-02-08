from kivy.clock import Clock
from kivy.utils import platform
from kivy.logger import Logger
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout  # Import FloatLayout

from instaloader2 import instaloader
import requests
import re
import os

class InstaDownloaderApp(App):
    def build(self):
        # Check version function
        self.version_url = "https://api.github.com/repos/Fredo-Ronan/Android-IG-Downloader-using-Python/releases/latest"
        self.current_version = "1.2.2"
        self.check_updates()

        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # FloatLayout for the header section
        header_layout = FloatLayout(size=(0, 0), size_hint=(1, None), height=100)

        # Header Labels
        header_label1 = Label(
            text='Instagram Downloader',
            font_size=50,
            bold=True,
            color=[1, 1, 1, 1],  # White color
            halign='center',  # Center align the text
            valign='middle',  # Vertically align the text in the middle
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
        )

        header_label2 = Label(
            text='by Fredo Ronan',
            font_size=30,
            color=[1, 1, 1, 1],  # White color
            halign='center',  # Center align the text
            valign='middle',  # Vertically align the text in the middle
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.1},  # Adjust position
        )

        header_label3 = Label(
            text=f'version {self.current_version}',
            font_size=18,
            color=[1, 1, 1, 1],  # White color
            halign='center',  # Center align the text
            valign='middle',  # Vertically align the text in the middle
            size_hint=(1, 1),
            pos_hint={'center_x': 0.94, 'center_y': 0.01},  # Adjust position
        )

        header_layout.add_widget(header_label1)
        header_layout.add_widget(header_label2)
        header_layout.add_widget(header_label3)

        # Input Box and Download Button
        self.link_input = TextInput(
            hint_text='Enter Instagram Link',
            multiline=True,
            write_tab=False,
        )
        download_button = Button(
            text='Download',
            font_size=50,
            on_press=self.show_download_popup,
            background_color=[0, 1, 1, 1],  # Green ish color
        )
        update_app_btn = Button(
            text=f'Update to latest version {self.latest_version}',
            font_size=30,
            on_press=self.update_app,
            background_color=[0, 1, 0.5, 1],
        )

        # Progress Bar
        self.progress_bar = ProgressBar(max=1000, size_hint_y=None, height=30)

        # Add widgets to the layout
        self.layout.add_widget(header_layout)
        self.layout.add_widget(self.link_input)
        self.layout.add_widget(download_button)

        if self.latest_version != self.current_version:
            self.layout.add_widget(update_app_btn)
        
        self.layout.add_widget(self.progress_bar)

        return self.layout
    
    # Update Functions
    def check_updates(self):
        self.latest_version = self.get_latest_version()

    def get_latest_version(self):
        try:
            response = requests.get(self.version_url)
            response.raise_for_status()
            release_info = response.json()
            latest_version = release_info['tag_name']
            return latest_version
        except Exception as e:
            print(f"Error fetching latest version: {e}")
            return None
    
    def create_update_popup():
        update_popup = Popup(
            title='Updating...',
            content=Label(text='Please wait while the update is in progress.'),
            size_hint=(None, None),
            size=(400, 250),
        )
        return update_popup
    
    def show_update_done():
        update_done = Popup(
            title='Update Done!',
            content=Label(text='You may restart the app to enjoy the new version'),
            size_hint=(None, None),
            size=(400, 250),
        )
        update_done.open()

    def update_app(self, instance):
        try:
            update_status_popup = self.create_download_popup()
            update_status_popup.open()
            # Interact with github api to get the latest version from repository
            apk_url = f'https://github.com/Fredo-Ronan/Android-IG-Downloader-using-Python/releases/latest/download/Fredo.Instagram.Downloader.apk'
            response = requests.get(apk_url)
            response.raise_for_status()

            # Save the new APK file
            new_apk_path = 'Fredo_Instagram_Downloader.apk'
            with open(new_apk_path, 'wb') as apk_file:
                apk_file.write(response.content)

            # Install the new APK
            self.install_apk(new_apk_path)
            update_status_popup.dismiss()
            self.show_update_done()
        except Exception as e:
            print(f"Error updating app: {e}")
    

    def install_apk(self, apk_path):
        if platform == 'android':
            try:
                from jnius import autoclass

                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                Intent = autoclass('android.content.Intent')
                Uri = autoclass('android.net.Uri')

                intent = Intent(Intent.ACTION_VIEW)
                intent.setDataAndType(Uri.parse(f'file://{apk_path}'), 'application/vnd.android.package-archive')
                intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                PythonActivity.mActivity.startActivity(intent)

            except Exception as e:
                Logger.error(f"Error installing APK: {e}")
        else:
            Logger.error("Update not supported on this platform.")


    # Main App Functions
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
            size=(400, 250),
        )
        return download_popup

    def download_instagram_media(self, short_code):
        loader = instaloader.Instaloader()
        post = instaloader.Post.from_shortcode(loader.context, short_code)

        # Set the custom directory name
        custom_directory = 'Download'

        # Construct the target directory path
        internal_storage_download_path = os.path.join('/storage/emulated/0', custom_directory)

        # Create the custom directory if it doesn't exist
        os.makedirs(internal_storage_download_path, exist_ok=True)

        if post.is_video:
            video_url = post.video_url
            response = requests.get(video_url, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            chunk_size = 1024
            bytes_downloaded = 0

            # Set the download path in the custom directory
            download_path = os.path.join(internal_storage_download_path, f"{post.owner_username}_{post.shortcode}.mp4")

            with open(download_path, 'wb') as f:
                for data in response.iter_content(chunk_size=chunk_size):
                    f.write(data)
                    bytes_downloaded += len(data)
                    self.update_progress(bytes_downloaded, total_size)

            self.show_success_popup(f"Video downloaded: {download_path}")
        else:
            # Set the download path in the custom directory
            download_path = os.path.join(internal_storage_download_path, f"{post.owner_username}_{post.shortcode}")

            loader.download_post(post, target=download_path)

    def update_progress(self, value, max_value):
        # Update the progress bar value
        progress_percent = (value / max_value) * 1000
        self.progress_bar.value = progress_percent

    def show_error_popup(self, message):
        error_popup = Popup(
            title='Error',
            content=Label(text=message),
            size_hint=(None, None),
            size=(400, 250),
        )
        error_popup.open()

    def show_success_popup(self, message):
        success_popup = Popup(
            title='Success',
            content=Label(text=message),
            size_hint=(None, None),
            size=(400, 250),
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
