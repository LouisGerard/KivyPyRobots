import kivy
import sqlite3
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics.context_instructions import Color
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics.vertex_instructions import Rectangle
from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from collections import namedtuple

import math
import Game

kivy.require('1.9.0')

# Set window size or not with your screen resolution

Window.fullscreen = False


class field(App):
    def __init__(self, t1, t2, ia1, ia2, **kwargs):
        super().__init__(**kwargs)
        print("init")
        self.cptTour = 0

        self.layout = FloatLayout()
        self.caseWidth = Window.width / 32
        self.caseHeight = Window.height / 32
        #tank1 = Game.Robot(Tank(t1), 0)
        #tank2 = Game.Robot(Tank(t2), 1)
        self.game = Game.Game(Tank(t1), Tank(t2), IA(ia1), IA(ia2))

    def build(self):
        print("build")
        field = InstructionGroup()
        field.add(Color(0.9294, 0.7882, 0.6863))

        i = 0
        while i < 32 * 32:
            field.add(Rectangle(pos=(i % 32 * self.caseWidth, math.floor(i / 32) * self.caseHeight),
                                size=(self.caseWidth - 1, self.caseHeight - 1)))
            i += 1
        [self.layout.canvas.add(group) for group in [field]]
        return self.layout

    def update(self):
        print("update")

        posTank1 = self.game.getPosition(0)
        posTank2 = self.game.getPosition(1)
        field = InstructionGroup()
        i = 0
        while i < 32 * 32:
            if i == posTank1:  # tank1
                field.add(Color(0, 0, 1))
            elif i == posTank2:  # tank2
                field.add(Color(0, 1, 0))
            else:  # reste de la map
                field.add(Color(0.9294, 0.7882, 0.6863))
            field.add(Rectangle(pos=(i % 32 * self.caseWidth,
                                     math.floor(i / 32) * self.caseHeight),
                                size=(self.caseWidth - 1,
                                      self.caseHeight - 1)))
            i += 1
        self.game.run(self.cptTour + 1)
        self.cptTout += 1
        [self.layout.canvas.add(group) for group in [field]]
        return self.layout


class IA:
    def __init__(self, id):
        self.id = id

        conn = sqlite3.connect('Data/kivy.db')
        c = conn.cursor()
        c.execute('SELECT code '
                  'FROM IA '
                  'WHERE id = ?', (id,))
        result = c.fetchone()
        conn.close()

        #self.text = result[0]
        self.text = "enemy = self.getEnemyTankId()\nenemypos = self.getPosition(enemy)\nself.moveTank(enemypos)\nself.shoot()"


class Tank:
    def __init__(self, id):
        self.id = id

        conn = sqlite3.connect('Data/kivy.db')
        c = conn.cursor()
        c.execute('SELECT moveValue, actionValue, range, attackcost, attackValue '
                  'FROM tank t '
                  'JOIN caterpillar c ON t.caterpillar_id = c.id '
                  'JOIN navSystem n ON t.navSystem_id = n.id '
                  'JOIN weapon w ON t.weapon_id = w.id '
                  'WHERE t.id = ?', (id,))
        result = c.fetchone()
        conn.close()

        cat = namedtuple('cat', 'moveValue')
        #self.caterpillar = cat(result[0])
        self.caterpillar = cat(2)

        nav = namedtuple('nav', 'actionValue')
        #self.navSystem = nav(result[1])
        self.navSystem = nav(2)

        weap = namedtuple('weap', 'range attackCost attackValue')
        #self.weapon = weap(result[2], result[3], result[4])
        self.weapon = weap(4, 1, 1)

if __name__ == '__main__':
    Clock.schedule_interval(field.update, 1)
    field(0, 0, 0, 0).run()