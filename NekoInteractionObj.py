from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QSizePolicy
from PyQt5.QtCore import Qt, QEvent, QTimer
from PyQt5.QtGui import QPixmap, QMouseEvent, QIcon, QCursor
from Cope import *
from globals import *
import pyautogui as ag

class NekoInteractionObj(QLabel):
    def __init__(self, img, size, neko):
        self.neko = neko
        self.img = img
        self.size = size
        self.size = (20, 20)

        QLabel.__init__(self)

        setBorderless(self, false)

        # self.setPixmap(self.img)
        # self.setCursor(Qt.BlankCursor)

        self.setGeometry(*ag.position(), *self.size)
        self.c = QCursor(self.img)
        self.setCursor(self.c)

        self.active = True

        self.update()
        self.show()

        self.updateTimer = QTimer()
        self.updateTimer.timeout.connect(self.updateLoc)
        self.updateTimer.setInterval(5)
        self.updateTimer.start()


    def updateLoc(self):
        pos = ag.position()
        self.setGeometry(pos[0] - 10, pos[1] - 10, self.width(), self.height())


    def mousePressEvent(self, event):
        if event.button() == 1:
            self._clicked()

        if event.button() == 2:
            self.active = False
            self.destroy()

            # debug()
            # self.setGeometry(event.globalX(), event.globalY(), self.width(), self.height())
        return super().mousePressEvent(event)


    def _clicked(self):
        debug('mouse clicked...')
        debug(self.neko.geometry(), name='neko rect')
        debug(ag.position(), name='mouse pos')
        if self.active and self.neko.geometry().contains(*ag.position()):
            self.nekoClicked()


    def nekoClicked(self):
        raise NotImplementedError


class SprayBottle(NekoInteractionObj):
    def __init__(self, neko):
        super().__init__(QPixmap(DIR + '/objs/sprayBottle.png'), SPRAY_BOTTLE_SIZE, neko)

    def nekoClicked(self):
        self.neko.sprayed()


class Gun(NekoInteractionObj):
    def __init__(self, neko):
        super().__init__(QPixmap(DIR + '/objs/gun.png'), GUN_SIZE, neko)

    def nekoClicked(self):
        exit(0)


class Snack(NekoInteractionObj):
    def __init__(self, neko):
        super().__init__(QPixmap(DIR + '/objs/snack.png'), SNACK_SIZE, neko)

    def nekoClicked(self):
        self.neko.eat()
        self.destroy()
        self.active = False
