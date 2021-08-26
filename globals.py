from enum import Enum, auto
from PyQt5.QtWidgets import QWidget, QDesktopWidget
from PyQt5.QtCore import Qt

SPRAY_BOTTLE_SIZE = (18, 33)
GUN_SIZE = (25, 25)
SNACK_DISPENSER_SIZE = (25, 40)
LITTER_BOX_SIZE = (70, 40)
POOP_SIZE = (15, 15)
SNACK_SIZE = (15, 15)

class Dir(Enum):
    UP    = 0
    DOWN  = 1
    LEFT  = 2
    RIGHT = 3
    UP_RIGHT   = 4
    UP_LEFT    = 5
    DOWN_RIGHT = 6
    DOWN_LEFT  = 7
    NORTH = UP
    SOUTH = DOWN
    EAST  = RIGHT
    WEST  = LEFT
    NORTH_WEST = UP_LEFT
    NORTH_EAST = UP_RIGHT
    SOUTH_WEST = DOWN_LEFT
    SOUTH_EAST = DOWN_RIGHT


class State(Enum):
    WALKING = auto()
    PAWING  = auto()
    YAWNING = auto()
    POOPING = auto()
    SITTING = auto()
    SLEEPING = auto()
    WAKING_UP = auto()
    FALLING_ASLEEP = auto()


class Mission(Enum):
    WANDER = auto()
    FOLLOW_MOUSE = auto()
    FOLLOW_MOUSE_CLICKS = auto()
    WANDER_EDGE = auto()
    WANDER_EDGE_VAUGE = auto()
    WANDER_WINDOW = auto()


#! Depricated
class BorderlessWidget(QWidget):
    def __init__(self):
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowFlag(Qt.BypassGraphicsProxyWidget)
        self.setWindowFlag(Qt.WindowDoesNotAcceptFocus)
        # Qt.NoDropShadowWindowHint
        # Qt.BypassWindowManagerHint
        # Qt.X11BypassWindowManagerHint
        # Qt.CustomizeWindowHint

        # Center it
        geo = QDesktopWidget().availableGeometry()
        self.screenSize = geo.size()
        self.screenCenter = geo.center()
        self.setGeometry(self.screenCenter.x() - (self.size[0] / 2), self.screenCenter.y() - (self.size[1] / 2), self.size[0], self.size[1])


def setBorderless(widget: QWidget, center=True):
    widget.setAttribute(Qt.WA_TranslucentBackground)
    widget.setWindowFlag(Qt.FramelessWindowHint)
    widget.setWindowFlag(Qt.WindowStaysOnTopHint)
    widget.setWindowFlag(Qt.BypassGraphicsProxyWidget)
    widget.setWindowFlag(Qt.WindowDoesNotAcceptFocus)
    # Qt.NoDropShadowWindowHint
    # Qt.BypassWindowManagerHint
    # Qt.X11BypassWindowManagerHint
    # Qt.CustomizeWindowHint

    # Center it
    if center:
        geo = QDesktopWidget().availableGeometry()
        widget.screenSize = geo.size()
        widget.screenCenter = geo.center()
        widget.setGeometry(widget.screenCenter.x() - (widget.size[0] / 2), widget.screenCenter.y() - (widget.size[1] / 2), widget.size[0], widget.size[1])
