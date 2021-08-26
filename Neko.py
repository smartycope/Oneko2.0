# This Python file uses the following encoding: utf-8
import sys, os, time, random, math
from PyQt5.QtWidgets import QApplication, QMainWindow
from Animation import Animation
from PyQt5 import *
# from PyQt5 import QtCore, QtGui, QtMultimedia, QtWidgets, uic
from PyQt5.QtCore import *
from PyQt5.QtCore import QEvent, Qt, QTimer
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
# from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QWidget
import numpy as np
from copy import deepcopy

import Cope
from Cope import *
import pyautogui as ag

# DIR = os.path.dirname(__file__)
from globals import *


class Neko(QLabel):
    def __init__(self):
        self.size = (35, 35)
        QLabel.__init__(self)
        setBorderless(self)
        # BorderlessWidget.__init__(self)

        self.frameSpeed = 400 # In milliseconds
        self.moveSpeed = 20   # In pixels - sorta

        # Load all the frames
        self.pixmaps = {}
        for frame in os.listdir(DIR + '/frames/'):
            self.pixmaps[frame[:-4]] = QPixmap(DIR + f'/frames/{frame}')

        self.animations = {
            'sit':           Animation(self, -1, self.frameSpeed,       [self.pixmaps['sit']], name='sit'),
            'walkUp':        Animation(self, -1, self.frameSpeed,       [self.pixmaps['up1'],        self.pixmaps['up2']], name='walkUp'),
            'walkDown':      Animation(self, -1, self.frameSpeed,       [self.pixmaps['down1'],      self.pixmaps['down2']], name='walkDown'),
            'walkLeft':      Animation(self, -1, self.frameSpeed,       [self.pixmaps['left1'],      self.pixmaps['left2']], name='walkLeft'),
            'walkRight':     Animation(self, -1, self.frameSpeed,       [self.pixmaps['right1'],     self.pixmaps['right2']], name='walkRight'),
            'walkUpLeft':    Animation(self, -1, self.frameSpeed,       [self.pixmaps['upLeft1'],    self.pixmaps['upLeft2']], name='walkUpLeft'),
            'walkUpRight':   Animation(self, -1, self.frameSpeed,       [self.pixmaps['upRight1'],   self.pixmaps['upRight2']], name='walkUpRight'),
            'walkDownLeft':  Animation(self, -1, self.frameSpeed,       [self.pixmaps['downLeft1'],  self.pixmaps['downLeft2']], name='walkDownLeft'),
            'walkDownRight': Animation(self, -1, self.frameSpeed,       [self.pixmaps['downRight1'], self.pixmaps['downRight2']], name='walkDownRight'),
            'pawUp':         Animation(self,  3, self.frameSpeed / 1.5, [self.pixmaps['pawUp1'],     self.pixmaps['pawUp2']], name='pawUp'),
            'pawDown':       Animation(self,  3, self.frameSpeed / 1.5, [self.pixmaps['pawDown1'],  self.pixmaps['pawDown2']], name='pawDown'),
            'pawLeft':       Animation(self,  3, self.frameSpeed / 1.5, [self.pixmaps['pawLeft1'],   self.pixmaps['pawLeft2']], name='pawLeft'),
            'pawRight':      Animation(self,  3, self.frameSpeed / 1.5, [self.pixmaps['pawRight1'],  self.pixmaps['pawRight2']], name='pawRight'),
            'pawCenter':     Animation(self,  3, self.frameSpeed / 1.5, [self.pixmaps['pawCenter'],  self.pixmaps['sit']], name='pawCenter'),
            'yawn':          Animation(self,  4, self.frameSpeed,       [self.pixmaps['yawn'],       self.pixmaps['sit']], name='yawn'),
            'sleep':         Animation(self, -1, self.frameSpeed / 1.5, [self.pixmaps['sleep1'],     self.pixmaps['sleep2']], name='sleep'),
            'scratch':       Animation(self,  2, self.frameSpeed / 1.5, [self.pixmaps['scratch1'],   self.pixmaps['scratch2']], name='scratch'),
            'wakeUp':        Animation(self,  1, self.frameSpeed,       [self.pixmaps['awake']], name='wakeUp'),
            'fallAsleep':    Animation(self,  1, self.frameSpeed,       [self.pixmaps['sit'],        self.pixmaps['scratch1'], self.pixmaps['scratch2'], self.pixmaps['scratch1'], self.pixmaps['scratch2'], self.pixmaps['yawn']], name='fallAsleep'),
            'sprayed':       Animation(self,  3, self.frameSpeed,       [self.pixmaps['awake']], name='sprayed'),
            'eat':           Animation(self,  3, self.frameSpeed / 2,   [self.pixmaps['yawn'], self.pixmaps['sit']], name='eat'),
        }

        self._runningAnim = self.animations['sit']
        self._runningAnim.play()

        self.mission = Mission.FOLLOW_MOUSE

        self.minSleepCycles = 5
        self.maxSleepCycles = 100

        self.minYawnTimeSec = 20
        self.maxYawnTimeSec = 360

        self.closeEnoughTolerance = 20

        self.sleep_timer = None

        self.prevMouseLoc = ag.position()

        self.chase(self.genNextDest())


    def setAnim(self, anim):
        self._runningAnim.stop()
        self._runningAnim = self.animations[anim]
        self._runningAnim.play()


    def move(self, dx, dy):
        self.setGeometry(self.x() + dx, self.y() + dy, self.width(), self.height())


    def dirFromAngle(self, ang):
        ang = absrad(ang)
        if Cope.isBetween(ang, 0, np.deg2rad(45), True, True) or Cope.isBetween(ang, np.deg2rad(315), np.deg2rad(360)):
            return Dir.UP
        elif Cope.isBetween(ang, np.deg2rad(45), np.deg2rad(135), True, False):
            return Dir.RIGHT
        elif Cope.isBetween(ang, np.deg2rad(135), np.deg2rad(225), True, False):
            return Dir.DOWN
        elif Cope.isBetween(ang, np.deg2rad(225), np.deg2rad(315), True, False):
            return Dir.LEFT
        else:
            debug(ang, color=5)
            assert(False)


    def genNextDest(self):
        if self.mission == Mission.WANDER:
            return (random.randint(0, self.screenSize.width()), random.randint(0, self.screenSize.height()))
        if self.mission == Mission.FOLLOW_MOUSE:
            return ag.position()
        else:
            todo('all the other missions')


    def chase(self, dest=None):
        if dest is None:
            assert(self._runningAnim.name == 'sleep')
            self.setAnim('wakeUp')
            self._runningAnim.finished.connect(self.chase, self.genNextDest())

        assert(dest)

        opp = self.y() - dest[1]
        adj = self.x() - dest[0]
        angle = math.atan2(adj, opp)  #Cope.normalize2rad(abs(math.atan2(self.y() - self.to[1], self.x() - self.to[0])))

        #  self.move(-math.sin(self.angle) / self.moveSpeed, -math.cos(self.angle) / self.moveSpeed)
        dx, dy = (math.cos(angle) * self.moveSpeed, math.sin(angle) * self.moveSpeed)

        debug(opp, adj, merge=True, showFunc=True)

        _dir = self.dirFromAngle(angle)
        if _dir == Dir.UP:
            self.setAnim('walkUp')
        elif _dir == Dir.DOWN:
            self.setAnim('walkDown')
        elif _dir == Dir.LEFT:
            self.setAnim('walkLeft')
        elif _dir == Dir.RIGHT:
            self.setAnim('walkRight')

        def checkDest(tolerance):
            if self.mission is Mission.FOLLOW_MOUSE:
                dest = ag.position()
                if getDist(self.x(), self.y(), dest[0], dest[1]) < tolerance:
                    self.setAnim('pawCenter')
                    self._runningAnim.finished.connect(self.fallAsleep, -1)
            elif getDist(self.x(), self.y(), dest[0], dest[1]) < tolerance:
                self.fallAsleep(randint(self.minSleepCycles, self.maxSleepCycles))

            debug(getDist(self.x(), self.y(), dest[0], dest[1]), name='dist')
            debug(dest, self.geometry(), name=('mouse loc', 'my pos'), color=2)

        self._runningAnim.increment.connect(self.move, dx, dy)
        self._runningAnim.increment.connect(checkDest, self.closeEnoughTolerance)


    def fallAsleep(self, sleepAmount):
        self.setAnim('fallAsleep')
        self._runningAnim.finished.connect(self.setAnim, 'sleep')

        def checkForMovement():
            if ag.position() != self.prevMouseLoc:
                self.chase()

        def setSleepTime(time):
            assert(self._runningAnim.name == 'sleep')
            if time < 0:
                assert(self.mission in (Mission.FOLLOW_MOUSE, Mission.FOLLOW_MOUSE_CLICKS))
                self._runningAnim.increment.connect(checkForMovement)

            self._runningAnim.laps = time
            self._runningAnim.finished.connect(self.chase)

        self._runningAnim.finished.connect(setSleepTime, sleepAmount)


    def paw(self, _dir):
        if _dir == Dir.UP:
            self.setAnim('pawUp')
        elif _dir == Dir.DOWN:
            self.setAnim('pawDown')
        elif _dir == Dir.LEFT:
            self.setAnim('pawLeft')
        elif _dir == Dir.RIGHT:
            self.setAnim('pawRight')
        else:
            self.setAnim('sit')
            debug('Cannot paw in that direction!', color=5)


    def sit(self):
        self.setAnim('sit')

        self.yawnTimer = QTimer()
        self.yawnTimer.timeout.connect(lambda: self.setAnim('yawn'))
        self.yawnTimer.start(randint(self.minYawnTime * 1000, self.maxYawnTime * 1000))


    def eat(self):
        tmp = deepcopy(self._runningAnim.name)
        debug(self._runningAnim.name)
        debug(tmp)
        self.setAnim('eat')
        self._runningAnim.finished.connect(self.setAnim, tmp)


    def sprayed(self):
        tmp = deepcopy(self._runningAnim.name)
        self.setAnim('sprayed')
        self._runningAnim.finished.connect(self.setAnim, tmp)
