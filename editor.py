import kivy
import sqlite3

from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

kivy.require('1.9.0')


class Editor(App):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)

        self.save_button = Button(text="Sauvegarder", size_hint=(1, .1))
        self.save_button.bind(on_press=self.save)

        self.code_input = TextInput(text=text, size_hint=(1, .9))
        self.code_input.font_name = "code.ttf"

    def build(self):
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.save_button)
        layout.add_widget(self.code_input)
        return layout

    def save(self, value):
        conn = sqlite3.connect('Data/kivy.db')
        c = conn.cursor()
        aze = (self.code_input.text,) # todo change db
        c.execute('update IA set code=?', aze)
        conn.commit()
        conn.close()


editor = Editor(text="Let's code !")
editor.run()
