import kivy
import sqlite3

from kivy.app import App
from kivy.uix.codeinput import CodeInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

kivy.require('1.9.0')


class Editor(App):
    def __init__(self, id, **kwargs):
        super().__init__(**kwargs)

        self.id = id

        self.save_button = Button(text="Sauvegarder", size_hint=(1, .1))
        self.save_button.bind(on_press=self.save)

        text = self.load()
        self.code_input = CodeInput(text=text, size_hint=(1, .9))
        self.code_input.font_name = "code.ttf"

    def build(self):
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.save_button)
        layout.add_widget(self.code_input)
        return layout

    def save(self, value):
        conn = sqlite3.connect('Data/kivy.db')
        c = conn.cursor()
        aze = (self.code_input.text, self.id) # todo change db
        c.execute('update IA set code=? where id=?', aze)
        conn.commit()
        conn.close()

    def load(self):
        conn = sqlite3.connect('Data/kivy.db')
        c = conn.cursor()
        c.execute('select code from IA where id=?', (self.id,))
        result = c.fetchone()
        conn.close()
        return result[0]


editor = Editor(1)
editor.run()
