import kivy
import sqlite3
from kivy.graphics.context_instructions import Color
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics.vertex_instructions import Rectangle
from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock, mainthread
from collections import namedtuple

import math

from kivy.uix.screenmanager import Screen

import Game

kivy.require('1.9.0')


class Jeu(object):
    cptTour = 0
    caseWidth = Window.width/ 32
    caseHeight = (Window.height - 75)/ 32
    game = None

    @staticmethod
    def init(t1, t2, ia1, ia2):
        Jeu.game = Game.Game(Tank(t1), Tank(t2), IA(ia1), IA(ia2))

    @staticmethod
    def incr_cpt_tour():
        Jeu.cptTour += 1


class Field(Screen):

    @mainthread
    def on_enter(self):
        Jeu.init(0, 0, 0, 0)
        field = InstructionGroup()
        field.add(Color(0.9294, 0.7882, 0.6863))

        i = 0
        while i < 32 * 32:
            field.add(Rectangle(pos=(i % 32 * Jeu.caseWidth, math.floor(i / 32) * Jeu.caseHeight),
                                size=(Jeu.caseWidth - 1, Jeu.caseHeight - 1)))
            i += 1
        [self.ids.layout.canvas.add(group) for group in [field]]
        Clock.schedule_interval(self.update, 0.5)
        return self.ids.layout

    def update(self, dt):
        life_tank1 = Jeu.game.getLife(0)
        life_tank2 = Jeu.game.getLife(1)
        pos_tank1 = Jeu.game.getPosition(0)
        pos_tank2 = Jeu.game.getPosition(1)
        print("tour numéro : %d" % (Jeu.cptTour,))
        print("vie tank 1 : %d" % (life_tank1,))
        print("vie tank 2 : %d \n" % (life_tank2,))
        if life_tank1 <= 0 or life_tank2 <= 0:
            print("fin de la partie")
            dif_life = life_tank2 - life_tank1
            if dif_life < 0:
                print("victoire de tank1")
            elif dif_life > 0:
                print("victoire de tank2")
            else:
                print("égalité")
            App.get_running_app().stop()
        field = InstructionGroup()
        i = 0
        while i < 32 * 32:
            if i == pos_tank1:  # tank1
                field.add(Color(0, 0, 1))
            elif i == pos_tank2:  # tank2
                field.add(Color(0, 1, 0))
            else:  # reste de la map
                field.add(Color(0.9294, 0.7882, 0.6863))
            field.add(Rectangle(pos=(i % 32 * Jeu.caseWidth,
                                     math.floor(i / 32) * Jeu.caseHeight),
                                size=(Jeu.caseWidth - 1,
                                      Jeu.caseHeight - 1)))
            i += 1
        Jeu.game.run(Jeu.cptTour + 1)
        Jeu.incr_cpt_tour()
        [self.ids.layout.canvas.add(group) for group in [field]]
        return self.ids.layout


class IA:
    def __init__(self, id):
        self.id = id

        conn = sqlite3.connect('../Data/kivy.db')
        c = conn.cursor()
        c.execute('SELECT code '
                  'FROM IA '
                  'WHERE id = ?', (id,))
        result = c.fetchone()
        conn.close()

        # todo self.text = result[0]
        self.text = "enemy = self.getEnemyTankId()\n" \
                    "enemypos = self.getPosition(enemy)\n" \
                    "self.moveTank(enemypos)\n" \
                    "self.shoot() "


class Tank:
    def __init__(self, id):
        self.id = id

        conn = sqlite3.connect('../Data/kivy.db')
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
        # todo self.caterpillar = cat(result[0])
        self.caterpillar = cat(2)

        nav = namedtuple('nav', 'actionValue')
        # todo self.navSystem = nav(result[1])
        self.navSystem = nav(2)

        weap = namedtuple('weap', 'range attackCost attackValue')
        # todo self.weapon = weap(result[2], result[3], result[4])
        self.weapon = weap(4, 1, 5)


if __name__ == '__main__':
    Jeu.init(0, 0, 0, 0)
    Field().run()
