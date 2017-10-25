import kivy

from kivy.app import App
from kivy.uix.textinput import TextInput

kivy.require('1.9.0')


class Editor(App):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.text = text

    def build(self):
        code_input = TextInput(text=self.text)
        code_input.font_name = "code.ttf"
        return code_input


editor = Editor(text="Let's code !")
editor.run()
