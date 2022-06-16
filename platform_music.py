#!/usr/bin/env python3
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from audioplayer import AudioPlayer
import json
import glob
import time
import random
import serial
import youtubeDownload as yt_dl

class Downloader(QObject):

    finished = pyqtSignal()
    progress = pyqtSignal(str)

    def set(self, songName):
        self.song = songName

    def dwn(self):
        for msg in yt_dl.busqueda(self.song):
            self.progress.emit(msg)
        self.finished.emit()

class Keyboard(QObject):

    finished = pyqtSignal()
    instruction = pyqtSignal(str)
    number = pyqtSignal(int)
    functions = {
                    "A" : lambda _: print("A"),
                    "B" : lambda _: print("B"),
                    "C" : lambda _: print("C"),
                    "D" : lambda _: print("D"),
                    "#" : lambda _: print("#"),
                    "*" : lambda _: print("*")
                }

    def readData(self):
        con = serial.Serial(port='/dev/ttyACM0', baudrate = 19200, timeout=1)
        data = ""
        num = -1
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

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])

class Ui_MainWindow(object):

    def __init__(self):
        self.controlPP = False
        self.loopSong = False
        self.refreshDataSheet()
        self.playerMaster = AudioPlayer("data/music/1.mp3")
        self.keyboardControl()

        self.timestampSong = 0

        self.timerSong = QtCore.QTimer()
        self.timerSong.setInterval(1000)
        self.timerSong.timeout.connect(self.setValueTime)
        self.maxSongDuration = 30000

        app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.MainWindow.resize(1200, 800)
        self.window_0()
        self.MainWindow.show()
        QtCore.QTimer.singleShot(3000, self.window_1)
        app.exec_()
        exit()

    def window_0(self):
        widgets_0 = QtWidgets.QWidget(self.MainWindow)

        fondo = QtWidgets.QLabel(widgets_0)
        fondo.setGeometry(QtCore.QRect(0, 0, 1200, 800))
        fondo.setText("")
        fondo.setPixmap(QtGui.QPixmap("data/line.jpg"))

        self.back = QtWidgets.QLabel(widgets_0)
        self.back.setGeometry(QtCore.QRect(120, 130, 960, 540))
        self.back.setText("")
        self.back.setPixmap(QtGui.QPixmap("data/casette.png"))

        self.MainWindow.setCentralWidget(widgets_0)

    def window_1(self):
        widgets_1 = QtWidgets.QWidget(self.MainWindow)

        fondo = QtWidgets.QLabel(widgets_1)
        fondo.setGeometry(QtCore.QRect(0, 0, 1200, 800))
        fondo.setText("")
        fondo.setPixmap(QtGui.QPixmap("data/im.png"))

        self.back = QtWidgets.QLabel(widgets_1)
        self.back.setGeometry(QtCore.QRect(400, 95, 400, 400))
        imagen = QtGui.QPixmap('data/cover.jpg')
        imag_red = imagen.scaled(400, 400)
        self.back.setPixmap(QtGui.QPixmap(imag_red))

        canciones = QtWidgets.QPushButton(widgets_1)
        canciones.setGeometry(QtCore.QRect(530, 30, 150, 30))
        canciones.setText("Canciones")
        canciones.setStyleSheet("QPushButton"
                                        "{"
                                        "background-color: black;"
                                        "color:white;"
                                        #"border : 3px solid black;"
                                        "border-radius : 15px;"
                                        "font: 500 10pt 'Bahnschrift'"
                                        "}"
                                        "QPushButton:pressed""{background-color:white;"
                                        "color:black;"
                                        "}")
        canciones.clicked.connect(self.window_2)

        siguiente = QtWidgets.QPushButton(widgets_1)
        siguiente.setGeometry(QtCore.QRect(630, 655, 140, 50))
        siguiente.setStyleSheet("QPushButton"
                                        "{"
                                        "background-color: white;"
                                        #"border : 3px solid black;"
                                        "border-radius : 20px;"
                                        "image: url(data/next.png);"
                                        "}"
                                        "QPushButton:pressed""{background-color:black;"
                                        "image: url(data/next_.png);}")
        siguiente.clicked.connect(self.nextSong)

        antes = QtWidgets.QPushButton(widgets_1)
        antes.setGeometry(QtCore.QRect(440, 655, 140, 50))
        antes.setStyleSheet("QPushButton"
                                        "{"
                                        "background-color: white;"
                                        #"border : 3px solid black;"
                                        "border-radius : 20px;"
                                        "image: url(data/prev.png);"
                                        "}"
                                        "QPushButton:pressed""{background-color:black;"
                                        "image: url(data/prev_.png);}")
        antes.clicked.connect(self.prevSong)

        playPause = QtWidgets.QPushButton(widgets_1)
        playPause.setGeometry(QtCore.QRect(560, 630, 100, 100))
        playPause.setStyleSheet("QPushButton"
                                        "{"
                                        "background-color: black;"
                                        #"border : 3px solid black;"
                                        "border-radius : 50px;"
                                         "image: url(data/play-pause1_.png);"
                                        "}"
                                        "QPushButton:pressed""{background-color:white;"
                                        "image: url(data/play-pause1.png);"
                                        "}")
        playPause.clicked.connect(self.playPause)

        self.title = QtWidgets.QLabel(widgets_1)
        self.title.setGeometry(QtCore.QRect(400, 505, 250, 50))
        self.title.setStyleSheet("font: 5000 12pt 'Bahnschrift'")
        self.title.setText("Kacerrolas")

        self.artist = QtWidgets.QLabel(widgets_1)
        self.artist.setGeometry(QtCore.QRect(400, 540, 250, 50))
        self.artist.setStyleSheet("font: 5000 12pt 'Bahnschrift'")
        self.artist.setText("By Antonio, Frida & Jhonny")

        self.progress = QtWidgets.QSlider(widgets_1)
        self.progress.setGeometry(QtCore.QRect(400, 590, 400, 30))

        random = QtWidgets.QPushButton(widgets_1)
        random.setGeometry(QtCore.QRect(800, 665, 30, 30))
        random.setStyleSheet("QPushButton"
                                        "{"
                                        "background-color: black;"
                                        #"border : 3px solid black;"
                                        "border-radius : 15px;"
                                        "image: url(data/random.png);"
                                        "}"
                                        "QPushButton:pressed""{background-color:white;"
                                        "image: url(data/random_.png);"
                                        "}")
        random.clicked.connect(self.shuffle)

        repeat = QtWidgets.QPushButton(widgets_1)
        repeat.setGeometry(QtCore.QRect(380, 665, 30, 30))
        repeat.setStyleSheet("QPushButton"
                                        "{"
                                        "background-color: black;"
                                        #"border : 3px solid black;"
                                        "border-radius : 15px;"
                                        "image: url(data/repeat.png);"
                                        "}"
                                        "QPushButton:pressed""{background-color:white;"
                                        "image: url(data/repeat_.png);"
                                        "}")
        repeat.clicked.connect(self.loop)

        self.progress.setOrientation(1)
        self.progress.setValue(0)

        self.MainWindow.setCentralWidget(widgets_1)

    def window_2(self):
        widgets_2 = QtWidgets.QWidget(self.MainWindow)

        self.fondo = QtWidgets.QLabel(widgets_2)
        self.fondo.setGeometry(QtCore.QRect(0, 0, 1200, 800))
        self.fondo.setText("")
        self.fondo.setPixmap(QtGui.QPixmap("data/im.png"))

        reproductor = QtWidgets.QPushButton(widgets_2)
        reproductor.setGeometry(QtCore.QRect(530, 30, 150, 30))
        reproductor.setText("Reproductor")
        reproductor.setStyleSheet("QPushButton"
                                        "{"
                                        "background-color: black;"
                                        "color:white;"
                                        #"border : 3px solid black;"
                                        "border-radius : 15px;"
                                        "font: 500 10pt 'Bahnschrift'"
                                        "}"
                                        "QPushButton:pressed""{background-color:white;"
                                        "color:black;"
                                        "}")
        reproductor.clicked.connect(self.window_1)

        self.download_in = QtWidgets.QLineEdit(widgets_2)
        self.download_in.setGeometry(QtCore.QRect(550, 160, 150, 32))

        download = QtWidgets.QPushButton(widgets_2)
        download.setGeometry(QtCore.QRect(725, 160, 150, 32))
        download.setText("Download Song")
        download.setStyleSheet("border-radius : 15px;")
        download.clicked.connect(self.download)

        self.label_res = QtWidgets.QLabel(widgets_2)
        self.label_res.setGeometry(QtCore.QRect(900, 160, 150, 32))
        self.label_res.setText("Download songs")
        self.label_res.setStyleSheet("font: 500 10pt 'Bahnschrift'")

        data = []
        for song in self.songs:
            title = song["song"]
            if title == "Unknow":
                title = song["title"]

            time = '{0}:{1}'.format(song["duration"]//60, (str(song["duration"]%60)).zfill(2))
            data.append([title, song["artist"], song["album"], song["date"]["year"], time])

        self.model = TableModel(data)

        self.table = QtWidgets.QTableView(widgets_2)
        self.table.setGeometry(QtCore.QRect(275, 260, 650, 430))
        self.table.setModel(self.model)

        self.MainWindow.setCentralWidget(widgets_2)

    def setLabelYt(self, msg):
        self.label_res.setText(msg)

    def keybordInstruction(self, ins):
        ({
                        "A" : lambda _: self.playPause(),
                        "B" : lambda _: self.nextSong(),
                        "C" : lambda _: self.prevSong(),
                        "D" : lambda _: print("D"),
                        "#" : lambda _: print("#"),
                        "*" : lambda _: print("*")
        })[ins](True)

    def keybordSelectSong(self, num):
        num -= 1
        self.selected = num % self.sizeSongs
        self.setPlayer(self.selected)
        self.playSong()

    def keyboardControl(self):
        self.thread_key = QThread()
        self.keyboardClass = Keyboard()
        self.keyboardClass.moveToThread(self.thread_key)

        self.keyboardClass.finished.connect(self.thread_key.quit)
        self.keyboardClass.finished.connect(self.keyboardClass.deleteLater)
        self.keyboardClass.instruction.connect(self.keybordInstruction)
        self.keyboardClass.number.connect(self.keybordSelectSong)

        self.thread_key.started.connect(self.keyboardClass.readData)
        self.thread_key.finished.connect(self.thread_key.deleteLater)

        self.thread_key.start()

    def download(self):
        self.thread = QThread()
        self.Downloader = Downloader()
        self.Downloader.set(self.download_in.text())
        self.Downloader.moveToThread(self.thread)

        self.Downloader.finished.connect(self.thread.quit)
        self.Downloader.finished.connect(self.Downloader.deleteLater)
        self.Downloader.progress.connect(self.setLabelYt)

        self.thread.started.connect(self.Downloader.dwn)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()
        self.thread.finished.connect(self.refreshDataSheet)

    def refreshDataSheet(self):
        self.songs = json.load(open("database.json", "r"))["songs"]
        self.sizeSongs = len(self.songs)
        self.selected = 0

    def setValueTime(self):
        self.timestampSong += 1
        try:
            self.progress.setValue(self.timestampSong)
        except:
            pass
        if self.timestampSong >= self.maxSongDuration:
            self.endSong()

    def playSong(self):
        self.timestampSong = 0
        self.playerMaster = AudioPlayer("./data/music/" + str(self.songs[self.selected]["song_number"]) + ".mp3")
        self.playerMaster.play()

        self.timerSong.start()
        self.maxSongDuration = self.songs[self.selected]["duration"]

    def nextSong(self):
        self.selected = (self.selected + 1) % self.sizeSongs
        self.setPlayer(self.selected)
        self.playSong()

    def prevSong(self):
        self.selected = (self.selected or (self.sizeSongs)) -1
        self.setPlayer(self.selected)
        self.playSong()

    def playPause(self):
        self.controlPP = not self.controlPP
        if self.controlPP:
            self.playerMaster.pause()
            self.timerSong.stop()
        else:
            self.playerMaster.resume()
            self.timerSong.start()

    def setPlayer(self, number):
        if self.songs[self.selected]["song"] != "Unknow":
            self.title.setText(self.songs[self.selected]["song"])
        else:
            self.title.setText(self.songs[self.selected]["title"])

        self.artist.setText(self.songs[self.selected]["artist"])
        self.progress.setMaximum(self.songs[self.selected]["duration"])
        self.back.setPixmap(QtGui.QPixmap(glob.glob("data/music/"+str(self.songs[self.selected]["song_number"]) + "_thumbnail*")[0]))

    def loop(self):
        self.loopSong = not self.loopSong

    def endSong(self):
        if not self.loopSong:
            self.selected = (self.selected + 1) % self.sizeSongs
        self.setPlayer(self.selected)
        self.playSong()

    def shuffle(self):
        random.shuffle(self.songs)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Ui_MainWindow()
    sys.exit(app.exec_())
