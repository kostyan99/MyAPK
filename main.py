import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class MainApp(App):
    def build(self):
        self.target = random.randint(1, 100)
        self.counter = 0

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.label = Label(text='Угадай число от 1 до 100', font_size='20sp')
        self.input = TextInput(hint_text='Введи число', multiline=False,
                               font_size='20sp', size_hint=(1, 0.2))
        self.btn = Button(text='Проверить', size_hint=(1, 0.2), font_size='18sp')
        self.btn.bind(on_press=self.check)

        self.layout.add_widget(self.label)
        self.layout.add_widget(self.input)
        self.layout.add_widget(self.btn)
        return self.layout

    def check(self, instance):
        try:
            choice = int(self.input.text)
            if choice < 1 or choice > 100:
                self.label.text = 'Вне диапазона! Только 1-100'
                return
            self.counter += 1
            if choice == self.target:
                self.label.text = f'Угадал за {self.counter} попыток!\nЧисло было {self.target}\nНажми ещё раз для новой игры'
                self.target = random.randint(1, 100)
                self.counter = 0
            elif choice > self.target:
                self.label.text = f'Меньше! Попытка {self.counter}'
            else:
                self.label.text = f'Больше! Попытка {self.counter}'
            self.input.text = ''
        except ValueError:
            self.label.text = 'Введи только цифры!'

MainApp().run()
