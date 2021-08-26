from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QMainWindow, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QEvent, QSize
from PyQt5.QtGui import QPixmap, QMouseEvent, QIcon
from Neko import Neko
from Cope import *
from globals import *
from NekoInteractionObj import *
import pyautogui as ag
import ctypes as C


class HomeObj(QPushButton):
    def __init__(self, parent, img, size, spawnItem, neko):
        QPushButton.__init__(self)
        self.setMinimumWidth(size[0])
        self.setMaximumWidth(size[0])
        self.setMinimumHeight(size[1])
        self.setMaximumHeight(size[1])
        self.neko = neko
        self.img = img
        self.spawnItem = spawnItem
        self.setFlat(True)
        self.setIcon(QIcon(self.img))
        self.setIconSize(QSize(*size))
        self.pressed.connect(self.handle_pressed)
        self.itm = None

    def handle_pressed(self):
        if self.spawnItem is not None:
            # debug(showFunc=True)
            self.itm = self.spawnItem(self.neko)
            # self.itm.setGeometry(self.x(), self.y(), self.itm.width(), self.itm.height())
            self.itm.show()

    # def dragMoveEvent(self, event):
        # self.setGeometry(event.ax, event.ay)


class Home(QWidget):
    def __init__(self):
        # self.setOverrideCursor(PyQt5.QtCore.Qt.BlankCursor)

        self.size = (100, 100)
        QMainWindow.__init__(self)
        setBorderless(self)
        # BorderlessWidget.__init__(self)

        self.neko = Neko()
        self.neko.show()

        # self.grid = QGridLayout(self)
        self.vert = QVBoxLayout(self)
        self.horz = QHBoxLayout(self)
        # self.setCentralWidget(self.grid)

        self.sprayBottle =    HomeObj(self, QPixmap(DIR + '/objs/sprayBottle.png'),    SPRAY_BOTTLE_SIZE, SprayBottle, self.neko)
        self.gun =            HomeObj(self, QPixmap(DIR + '/objs/gun.png'),            GUN_SIZE, Gun, self.neko)
        self.snackDispenser = HomeObj(self, QPixmap(DIR + '/objs/snackDispenser.png'), SNACK_DISPENSER_SIZE, Snack, self.neko)
        self.litterBox =      HomeObj(self, QPixmap(DIR + '/objs/litterBox.png'),      LITTER_BOX_SIZE, None, self.neko)

        self.horz.addWidget(self.sprayBottle)
        self.horz.addWidget(self.gun)
        self.horz.addWidget(self.snackDispenser)
        hack = QWidget(self)
        hack.setLayout(self.horz)
        self.vert.addWidget(hack)
        self.vert.addWidget(self.litterBox)

        self.setLayout(self.vert)

    def closeEvent(self, event):
        debug('destroying', color=5)
        self.neko.destroy()
        super().closeEvent(event)

    def event(self, event):
        if type(event) is QMouseEvent and (event.buttons() & Qt.LeftButton) and event.button() != 1:
            try:
                self.setGeometry(event.screenPos().x(), event.screenPos().y(), self.width(), self.height())
            except OverflowError:
                pass

        return super().event(event)
