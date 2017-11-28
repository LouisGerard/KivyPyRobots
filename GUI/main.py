from collections import namedtuple

import kivy
from kivy.lang import Builder

kivy.require('1.9.1')
import sqlite3
from kivy.app import App

from suggestion import Suggestion

from kivy.uix.floatlayout import FloatLayout
from kivymd.theming import ThemeManager
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.window import WindowBase, Window
from editor import Editor
from fight import Field

Window.fullscreen = False


class Menu(FloatLayout):
    pass


class Acceuil(Screen):
    pass


presentation = Builder.load_file("kivy.kv")

if __name__ == '__main__':
    class MenuApp(App):
        theme_cls = ThemeManager()

        def build(self):
            return Menu()


    MenuApp().run()
