from PyQt5.QtCore import QTimer
from Cope import Signal

class Animation:
    def __init__(self, subject, laps, fps, frames, name=None):
        self.subject = subject
        self.frames = frames
        self.len = len(self.frames)
        self.curFrame = 0
        self.playing = False
        self.laps = laps
        self.lap = 0
        self.done = False
        self.finished = Signal()
        self.lapped = Signal()
        self.increment = Signal()
        self.fps = fps
        self.name = name

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.setInterval(self.fps)

    def update(self):
        self.curFrame += 1
        if self.curFrame >= self.len:
            self.lap += 1
            if self.lap >= self.laps and self.laps > 0:
                self.done = True
                self.stop()
                self.finished()
                return
            else:
                self.lapped()
                self.curFrame = 0

        self.increment()
        self.subject.setPixmap(self.frames[self.curFrame])

    def play(self):
        self.timer.start()
        self.playing = True
        self.lap = 0
        self.curFrame = 0

    def pause(self):
        self.timer.stop()
        self.playing = False

    def stop(self):
        self.pause()

    def resume(self):
        self.timer.start()
        self.playing = True
