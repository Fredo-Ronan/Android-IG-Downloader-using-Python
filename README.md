# Simple Instagram Downloader
This is a simple instagram downloader app built using python. It's currently support on Android only.

## APK file release v1.1
Here you can download the .apk file and install it on your Android phone.<br>
[Click Here to Download](https://github.com/Fredo-Ronan/Android-IG-Downloader-using-Python/releases/download/1.1/Fredo.Instagram.Downloader.apk)

## Fact about this project
This project is using Instaloader library. Actually you can install it using pip and use it on your python code like this

```Bash
pip install instaloader
```
Use it on python code
```Python
from Instaloader import Instaloader

ig = Instaloader.Instaloader() # init the object
```
But since this is an app that has GUI that built using kivy library and we are going to convert it to apk file that can be install and run on Android, the method above often doesn't run well.<br><br>

The Instaloader library was using other couple of libraries also. For example is LZMA library. That library is for data compression. LZMA as my knowledge from reading some articles on the internet is one of the powerfull data compression algorithm.
Maybe in this Instaloader library, that LZMA algorithm is use to compress the incomming data from instagram that maybe too big or for other reason.<br><br>

But that library was cause an error when the apk is installed/deployed on the Android device and run the app on that phone. That error also cause the app crashed or force closed. The error traceback is quite long, 
but there is one line error message that i think is the root problem. That error was
```Bash
No module named '_lzma'
```
That error is happen because the lzma module that included on the Instaloader library. But after i study the Instaloader library, actually if i comment that lzma library import module it should be nothing wrong.<br><br>

Then i do that. And after rebuild all, it works fine on Android.<br><br><br>
That's is a short fact about this app development process. Actually it's more than that, i can explain why that error happen other than because of Instaloader has import to it.

## What's next?
This app is still in development, it's still in very early stage release on version 1.1 that only support Android phones and very basic UI. Stay tune for the next updates :) 👍
