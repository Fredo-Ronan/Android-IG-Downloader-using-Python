
"""
    WARNING!

    This code is very unstable hence it is not imported to anything

    This code actually in purpose to make this app can self update according to
    the latest github release
"""


from plyer import filechooser
from jnius import autoclass
import urllib.request as getFile
from kivy.utils import platform
from kivy.logger import Logger
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import requests
import os

class UpdateApp():
    def __init__(self) -> None:
        pass

    def create_update_popup(self):
        update_popup = Popup(
            title='Updating...',
            content=Label(text='Please wait while the update is in progress.'),
            size_hint=(None, None),
            size=(400, 250),
        )
        return update_popup

    def show_update_done(self):
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

            print('SEBELUM REQUEST!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            # Interact with github api to get the latest version from repository
            apk_url = f'https://github.com/Fredo-Ronan/Android-IG-Downloader-using-Python/releases/latest/download/Fredo.Instagram.Downloader.apk'
            response = requests.get(apk_url)
            response.raise_for_status()
            
            print('OYYYY SEBELUM LINK!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            download_apk_path = os.path.join('/storage/emulated/0/Download/', 'Fredo_Instagram_Downloader.apk')

            # Save the new APK file
            # new_apk_path = 'Fredo_Instagram_Downloader.apk'
            with open(download_apk_path, 'wb') as apk_file:
                apk_file.write(response.content)

            # getFile.urlretrieve(apk_url, download_apk_path)

            # Install the new APK
            self.install_apk(download_apk_path)
            # update_status_popup.dismiss()
            self.show_update_done()
        except Exception as e:
            print(f"Error updating app: {e}")


    def install_apk(self, apk_path):
        if platform == 'android':
            # noinspection PyUnresolvedReferences
            from android.os import Build
            from java.io import File

            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            PackageManager = autoclass('android.content.pm.PackageManager')
            Build.VERSION = autoclass('android.os.Build$VERSION')

            # Check if the app has the REQUEST_INSTALL_PACKAGES permission
            if check_permission("android.permission.REQUEST_INSTALL_PACKAGES"):
                Intent = autoclass('android.content.Intent')
                Uri = autoclass('android.net.Uri')

                # Install APK
                intent = Intent(Intent.ACTION_VIEW)
                file_uri = Uri.fromFile(File(apk_path))
                intent.setDataAndType(file_uri, "application/vnd.android.package-archive")
                intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                PythonActivity.mActivity.startActivity(intent)
                print("APK installation started.")
            else:
                print("App does not have REQUEST_INSTALL_PACKAGES permission.")

            def check_permission(self, permission):
                context = get_context()
                package_manager = context.getPackageManager()
                return package_manager.checkPermission(permission, context.getPackageName()) == PackageManager.PERMISSION_GRANTED

            def get_context(self):
                from jnius import autoclass
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                return PythonActivity.mActivity
        else:
            Logger.error("Update not supported on this platform.")