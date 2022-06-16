from PyQt5.QtCore import *
import youtubeDownload as yt_dl
import serial
import multitasking
import time
import json
from pathlib import Path
from demo_opts import get_device
from luma.core.virtual import viewport
from luma.core.render import canvas
from PIL import Image

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


class oledControl(QObject):
    killer = False

    @multitasking.task
    def song(self, data):
        name_song = data['song']
        if name_song == "Unknow":
            name_song = data['title']

        text = name_song+"\n"+data['album']+"\n"+data['artist']+"\n"+str(data['duration'])+"\n"+str(data['date']['year'])

        device = get_device()
        virtual = viewport(device, width=device.width, height=768)
        for _ in range(2):
            if self.killer:
                break
            with canvas(virtual) as draw:
                for i, line in enumerate(text.split("\n")):
                    draw.text((0, 40 + (i * 12)), text=line, fill="white")
        if not self.killer:
            time.sleep(1)

        for y in range(450):
            if self.killer:
                break
            virtual.set_position((0, y))
            time.sleep(0.01)
