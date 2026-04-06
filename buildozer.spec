[app]
# (section) Название твоего приложения в меню телефона
title = RemoteControl
package.name = remoteclient
package.domain = org.kostya
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 0.1

# ВАЖНО: Весь список библиотек, необходимых для сетевых запросов и работы с Firebase
requirements = python3, kivy==2.2.1, requests, urllib3, charset-normalizer, idna, certifi

orientation = portrait

[app:android]
# ВАЖНО: Разрешения для выхода в сеть
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# Настройки для современных Android (Poco X8 Pro)
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 24
android.ndk_api = 21

# Архитектура процессора (arm64-v8a для Poco, armeabi-v7a для старого Lenovo)
android.archs = arm64-v8a, armeabi-v7a

# Позволяет приложению не засыпать (полезно для фоновой работы)
android.wakelock = True

[buildozer]
log_level = 2
warn_on_root = 1
