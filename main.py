import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QCursor, QPixmap, QBitmap
import PyQt5
from Home import Home
from Cope import DIR, debugged

if __name__ == "__main__":
    app = QApplication([])
    window = Home()
    window.show()
    # app.setOverrideCursor(PyQt5.QtCore.Qt.BlankCursor)
    sys.exit(app.exec_())