from kivy.uix.button import Button


class Suggestion(Button):
    def __init__(self, op, **kwargs):
        super().__init__(**kwargs)
        self.font_name = "code.ttf"
        self.text = op.display
        self.insert = op.text
        self.shift = op.shift
        self.select_size = op.select_size
