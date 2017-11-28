import kivy
import sqlite3

from kivy.uix.screenmanager import Screen

from suggestion import Suggestion

from collections import namedtuple

from kivy.core.window import WindowBase
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock, mainthread

kivy.require('1.9.0')


class Editor(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.sublayout = BoxLayout(orientation='horizontal', size_hint=(1, .1))

    @mainthread
    def on_enter(self):
        WindowBase.on_key_up = self.autoindent

        op = namedtuple('op', 'display text shift select_size')
        ops = (
            op('if', 'if condition', 9, 9),
            op('while', 'while condition', 9, 9),
            op('self', 'self.', 0, 0),
            op('for', 'for i in range(0, len(collection))', 12, 10)
        )

        for i in range(0, len(ops)):
            b = Suggestion(ops[i])
            b.bind(on_press=self.autocomplete)
            self.sublayout.add_widget(b)

        self.ids.box.add_widget(self.sublayout)

    @mainthread
    def on_leave(self):
        self.ids.box.remove_widget(self.sublayout)

    def save(self, value=""):
        conn = sqlite3.connect('../Data/kivy.db')
        c = conn.cursor()
        c.execute('UPDATE IA SET code=? WHERE id=?', (self.ids.code_input.text, 1))
        conn.commit()
        conn.close()

    def load(self):
        conn = sqlite3.connect('../Data/kivy.db')
        c = conn.cursor()
        c.execute('SELECT code FROM IA WHERE id=?', (1,))
        result = c.fetchone()
        conn.close()
        return result[0]

    def autoindent(self, key, scancode=None, codepoint=None, modifier=None):
        if self.ids.code_input.focused:
            if key == 13:
                indent = self.get_indent(1)

                text = str(self.ids.code_input.text)
                if len(text)-2 >= 0 and text[len(text)-2] == ':':
                    indent += ' ' * 4

                self.ids.code_input.insert_text(indent)

    def get_indent(self, end_offset=0):
        text = str(self.ids.code_input.text)
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
        self.ids.code_input.insert_text(instance.insert)
        textsize = len(str(self.ids.code_input.text))
        self.ids.code_input.select_text(textsize - instance.shift, textsize - instance.shift + instance.select_size)
        self.focus()

    def focus(self):
        Clock.schedule_once(self.__focus__)  # Kivy Bug with textinput focus

    def __focus__(self, dt):
        self.ids.code_input.focus = True


if __name__ == '__main__':
    editor = Editor()
    editor.run()
