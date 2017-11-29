import unittest
import sqlite3

from editor import Editor
import sqlite3
import unittest

from editor import Editor


class TestGame(unittest.TestCase):
    def test_save(self):
        conn = sqlite3.connect('Date/kivy.db')

        c = conn.cursor()
        c.execute('INSERT INTO IA VALUES (2, 1, "aze"')
        codeToSave = "Code = \"Un code quelconque\""

        editor = Editor(2)
        editor.code_input = codeToSave

        editor.save()

        c = conn.cursor()
        c.execute('SELECT code FROM IA WHERE id = 2')
        result = c.fetchone()

        self.assertEqual(result, editor.code_input)

        c.execute('DELETE FROM IA WHERE id = 2')


def test_load(self):
    conn = sqlite3.connect('Date/kivy.db')
    c = conn.cursor()
    c.execute('INSERT INTO IA VALUES (2, 1, "test"')
    codeToMatchWithDB = "test"

    editor = Editor(2)
    editor.load()

    self.assertEqual(editor.code_input, codeToMatchWithDB)
    c.execute('DELETE FROM IA WHERE id = 2')


if __name__ == '__main__':
    unittest.main()
