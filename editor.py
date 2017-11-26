import kivy
import sqlite3
from suggestion import Suggestion

from collections import namedtuple

from kivy.app import App
from kivy.core.window import WindowBase
from kivy.uix.codeinput import CodeInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

kivy.require('1.9.0')


class Editor(App):
    def __init__(self, id, **kwargs):
        super().__init__(**kwargs)

        self.id = id

        self.save_button = Button(text="Sauvegarder", size_hint=(1, .05))
        self.save_button.bind(on_press=self.save)

        text = self.load()
        self.code_input = CodeInput(text=text, size_hint=(1, .9))
        self.code_input.font_name = "code.ttf"
        WindowBase.on_key_up = self.autoindent

    def build(self):
        self.focus()

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.save_button)
        layout.add_widget(self.code_input)

        op = namedtuple('op', 'display text shift select_size')
        ops = (
            op('if', 'if condition', 9, 9),
            op('while', 'while condition', 9, 9),
            op('self', 'self.', 0, 0),
            op('for', 'for i in range(0, len(collection))', 12, 10)
        )

        sublayout = BoxLayout(orientation='horizontal', size_hint=(1, .05))

        for i in range(0, len(ops)):
            b = Suggestion(ops[i])
            b.bind(on_press=self.autocomplete)
            sublayout.add_widget(b)

        layout.add_widget(sublayout)
        return layout

    def save(self, value=""):
        conn = sqlite3.connect('Data/kivy.db')
        c = conn.cursor()
        c.execute('UPDATE IA SET code=? WHERE id=?', (self.code_input.text, self.id))
        conn.commit()
        conn.close()

    def load(self):
        conn = sqlite3.connect('Data/kivy.db')
        c = conn.cursor()
        c.execute('SELECT code FROM IA WHERE id=?', (self.id,))
        result = c.fetchone()
        conn.close()
        return result[0]

    def autoindent(self, key, scancode=None, codepoint=None, modifier=None):
        if self.code_input.focused:
            if key == 13:
                indent = self.get_indent(1)

                text = str(self.code_input.text)
                if len(text)-2 >= 0 and text[len(text)-2] == ':':
                    indent += ' ' * 4

                self.code_input.insert_text(indent)

    def get_indent(self, end_offset=0):
        text = str(self.code_input.text)
        last_line = text[text.rfind('\n', 0, len(text) - end_offset) + 1:]
        i = 0
        level = 0
        while i < len(last_line):
            if last_line[i] == ' ':
                level += 1
            elif last_line[i] == '\t':
                level += 4
            else:
                break
            i += 1

        indent = ' ' * level
        return indent

    def autocomplete(self, instance):
        self.code_input.insert_text(instance.insert)
        textsize = len(str(self.code_input.text))
        self.code_input.select_text(textsize - instance.shift, textsize - instance.shift + instance.select_size)
        self.focus()

    def focus(self):
        Clock.schedule_once(self.__focus__)  # Kivy Bug with textinput focus

    def __focus__(self, dt):
        self.code_input.focus = True


if __name__ == '__main__':
    editor = Editor(1)
    editor.run()
