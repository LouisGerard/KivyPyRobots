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
class jeu(object):
    cptTour = 0
    layout = FloatLayout()
    caseWidth = Window.width / 32
    caseHeight = Window.height / 32
    game = 0
    @staticmethod
    def init(t1, t2, ia1, ia2):
        jeu.game = Game.Game(Tank(t1), Tank(t2), IA(ia1), IA(ia2))

    @staticmethod
    def incrCptTour():
        jeu.cptTour+=1


class field(App):
    # def __init__(self, t1, t2, ia1, ia2, **kwargs):
    #     super().__init__(**kwargs)
    #     print("init")
    #     self.cptTour = 0
    #
    #     self.layout = FloatLayout()
    #     self.caseWidth = Window.width / 32
    #     self.caseHeight = Window.height / 32
    #     #tank1 = Game.Robot(Tank(t1), 0)
    #     #tank2 = Game.Robot(Tank(t2), 1)
    #     self.game = Game.Game(Tank(t1), Tank(t2), IA(ia1), IA(ia2))

    def build(self):
        field = InstructionGroup()
        field.add(Color(0.9294, 0.7882, 0.6863))

        i = 0
        while i < 32 * 32:
            field.add(Rectangle(pos=(i % 32 * jeu.caseWidth, math.floor(i / 32) * jeu.caseHeight),
                                size=(jeu.caseWidth - 1, jeu.caseHeight - 1)))
            i += 1
        [jeu.layout.canvas.add(group) for group in [field]]
        return jeu.layout

    def update(self):
        lifeTank1 = jeu.game.getLife(0)
        lifeTank2 = jeu.game.getLife(1)
        posTank1 = jeu.game.getPosition(0)
        posTank2 = jeu.game.getPosition(1)
        print("tour numéro : %d" % (jeu.cptTour,))
        print("vie tank 1 : %d" % (lifeTank1,))
        print("vie tank 2 : %d \n" % (lifeTank2,))
        if (lifeTank1 <= 0 or lifeTank2 <= 0):
            print("fin de la partie")
            difLife = lifeTank2 - lifeTank1
            if difLife < 0:
                print("victoire de tank1")
            elif difLife > 0:
                print("victoire de tank2")
            else:
                print("égalité")
            App.get_running_app().stop()
        field = InstructionGroup()
        i = 0
        while i < 32 * 32:
            if i == posTank1:  # tank1
                field.add(Color(0, 0, 1))
            elif i == posTank2:  # tank2
                field.add(Color(0, 1, 0))
            else:  # reste de la map
                field.add(Color(0.9294, 0.7882, 0.6863))
            field.add(Rectangle(pos=(i % 32 * jeu.caseWidth,
                                     math.floor(i / 32) * jeu.caseHeight),
                                size=(jeu.caseWidth - 1,
                                      jeu.caseHeight - 1)))
            i += 1
        jeu.game.run(jeu.cptTour + 1)
        jeu.incrCptTour()
        [jeu.layout.canvas.add(group) for group in [field]]
        return jeu.layout


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
        self.weapon = weap(4, 1, 5)

if __name__ == '__main__':
    jeu.init(0,0,0,0)
    Clock.schedule_interval(field.update, 0.5)
    field().run()