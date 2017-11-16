import kivy
from kivy.lang import Builder

kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivymd.theming import ThemeManager


class Menu(FloatLayout):
    pass

presentation = Builder.load_file("kivy.kv")

if __name__ == '__main__':
    class MenuApp(App):
        theme_cls = ThemeManager()

        def build(self):
            self.theme_cls.theme_style = 'Dark'
            return Menu()
    MenuApp().run()
