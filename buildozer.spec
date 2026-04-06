[app]
title = MyApp
package.name = myapp
package.domain = org.example
source.dir = .
source.include_exts = py
version = 0.1
requirements = python3,kivy
orientation = portrait
osx.python_version = 3
osx.kivy_version = 1.9.1

[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
android.permissions = INTERNET
android.api = 31
android.minapi = 21
android.ndk = 25b
android.sdk = 24
android.ndk_api = 21
android.arch = arm64-v8a
