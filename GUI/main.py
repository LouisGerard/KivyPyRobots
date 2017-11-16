import kivy
from kivy.lang import Builder

kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivymd.theming import ThemeManager


class RootWidget(FloatLayout):
    pass

presentation = Builder.load_file("kivy.kv")

if __name__ == '__main__':
    class TestApp(App):
        theme_cls = ThemeManager()

        def build(self):
            self.theme_cls.theme_style = 'Dark'
            return RootWidget()
    TestApp().run()
