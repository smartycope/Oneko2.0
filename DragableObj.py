from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QPixmap, QMouseEvent
from Cope import *
from globals import *

class DragableObj(QLabel):
    def __init__(self, img, size):
        debug('initializing dragable')
        self.size = size
        # self.size = (img.size().width(), img.size().height())
        QLabel.__init__(self)
        setBorderless(self)

        self.setMinimumWidth(size[0])
        self.setMaximumWidth(size[0])
        self.setMinimumHeight(size[1])
        self.setMaximumHeight(size[1])

        self.img = img
        self.setPixmap(self.img)

        self.show()

    def event(self, event):
        if type(event) is QMouseEvent and (event.buttons() & Qt.LeftButton) and event.button() != 1:
            self.setGeometry(event.screenPos().x(), event.screenPos().y(), self.width(), self.height())

        return super().event(event)

class Poop(DragableObj):
    def __init__(self):
        super().__init__(QPixmap(DIR + '/objs/poop.png'), POOP_SIZE)
