import kivy

from kivy.app import App
from kivy.uix.button import Label
from kivy.uix.widget import Widget

kivy.require('1.9.0')


class Editor(Widget):
    def build(self):
        return Label(text="Let's code !")


editor = Editor()
editor.run()
