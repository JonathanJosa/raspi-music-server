from PyQt5.QtCore import *
import youtubeDownload as yt_dl
import serial

class Keyboard(QObject):

    finished = pyqtSignal()
    instruction = pyqtSignal(str)
    number = pyqtSignal(int)
    functions = {"A" : 1, "B" : 1, "C" : 1, "D" : 1, "#" : 1, "*" : 1}

    def readData(self):
        con = serial.Serial(port='/dev/ttyACM0', baudrate = 19200, timeout=1)
        data = ""
        while 1:
            x = con.read().decode('utf-8')
            if self.functions.get(x) != None:
                self.instruction.emit(x)
                data = ""
            elif x != "":
                data += x
            elif data != "":
                self.number.emit(int(data))
                data = ""

        self.finished.emit()

class Downloader(QObject):

    finished = pyqtSignal()
    progress = pyqtSignal(str)

    def set(self, songName):
        self.song = songName

    def dwn(self):
        for msg in yt_dl.busqueda(self.song):
            self.progress.emit(msg)
        self.finished.emit()
