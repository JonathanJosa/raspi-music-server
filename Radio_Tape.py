#!/usr/bin/env python3
import json, glob, time, random, sys
from audioplayer import AudioPlayer
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *

import taskQCorePython
import modelsPyQt5

class Ui_MainWindow(object):

    def __init__(self):
        self.controlPP = False
        self.loopSong = False
        self.refreshDataSheet()
        self.playerMaster = AudioPlayer("data/music/1.mp3")
        self.keyboardControl()
        self.downloadingSong = True

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
        self.widgets_0 = QtWidgets.QWidget(self.MainWindow)

        fondo = QtWidgets.QLabel(self.widgets_0)
        fondo.setGeometry(QtCore.QRect(0, 0, 1200, 800))
        fondo.setPixmap(QtGui.QPixmap("data/line.jpg"))

        self.back = QtWidgets.QLabel(self.widgets_0)
        self.back.setGeometry(QtCore.QRect(120, 130, 960, 540))
        self.back.setPixmap(QtGui.QPixmap("data/casette.png"))

        self.MainWindow.setCentralWidget(self.widgets_0)

    def window_1(self):
        widgets_1 = QtWidgets.QWidget(self.MainWindow)

        fondo = QtWidgets.QLabel(widgets_1)
        fondo.setGeometry(QtCore.QRect(0, 0, 1200, 800))
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
                                        "border-radius : 15px;"
                                        "font: 500 10pt 'Bahnschrift'"
                                        "}"
                                        "QPushButton:pressed""{background-color:white;"
                                        "color:black;"
                                        "}")
        canciones.clicked.connect(self.window_2)
        canciones.clicked.connect(self.setPlayer)

        siguiente = QtWidgets.QPushButton(widgets_1)
        siguiente.setGeometry(QtCore.QRect(630, 655, 140, 50))
        siguiente.setStyleSheet("QPushButton"
                                        "{"
                                        "background-color: white;"
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
                                        "border-radius : 20px;"
                                        "image: url(data/prev.png);"
                                        "}"
                                        "QPushButton:pressed""{background-color:black;"
                                        "image: url(data/prev_.png);}")
        antes.clicked.connect(self.prevSong)

        playPauseBtn = QtWidgets.QPushButton(widgets_1)
        playPauseBtn.setGeometry(QtCore.QRect(560, 630, 100, 100))
        playPauseBtn.setStyleSheet("QPushButton"
                                        "{"
                                        "background-color: black;"
                                        "border-radius : 50px;"
                                         "image: url(data/play-pause1_.png);"
                                        "}"
                                        "QPushButton:pressed""{background-color:white;"
                                        "image: url(data/play-pause1.png);"
                                        "}")
        playPauseBtn.clicked.connect(self.playPause)

        self.title = QtWidgets.QLabel(widgets_1)
        self.title.setGeometry(QtCore.QRect(400, 505, 250, 50))
        self.title.setStyleSheet("font: 5000 12pt 'Bahnschrift'")
        self.title.setText("Radio Tape")

        self.artist = QtWidgets.QLabel(widgets_1)
        self.artist.setGeometry(QtCore.QRect(400, 540, 250, 50))
        self.artist.setStyleSheet("font: 5000 12pt 'Bahnschrift'")
        self.artist.setText("By Antonio, Frida & Jhonny")

        self.progress = QtWidgets.QSlider(widgets_1)
        self.progress.setGeometry(QtCore.QRect(400, 590, 400, 30))
        self.progress.setOrientation(1)
        self.progress.setValue(0)

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

        self.repeat = QtWidgets.QPushButton(widgets_1)
        self.repeat.setGeometry(QtCore.QRect(380, 665, 30, 30))
        self.repeat.setStyleSheet("QPushButton"
                                        "{"
                                        "background-color: black;"

                                        "border-radius : 15px;"
                                        "image: url(data/repeat.png);"
                                        "}"
                                        "QPushButton:pressed""{border : 3px solid black;"
                                        "}"
                                        )
        self.repeat.clicked.connect(self.loop)

        self.time1 = QtWidgets.QLabel(widgets_1)
        self.time1.setGeometry(QtCore.QRect(400, 600, 100, 50))
        self.time1.setStyleSheet("font: 50 10pt 'Bahnschrift'")
        self.time1.setText("0:00")

        #Duración total
        self.time2 = QtWidgets.QLabel(widgets_1)
        self.time2.setGeometry(QtCore.QRect(775, 600, 100, 50))
        self.time2.setStyleSheet("font: 50 10pt 'Bahnschrift'")
        self.time2.setText("0:00")

        self.MainWindow.setCentralWidget(widgets_1)

        self.loopSong = not self.loopSong
        self.loop()

    def window_2(self):
        widgets_2 = QtWidgets.QWidget(self.MainWindow)

        self.fondo = QtWidgets.QLabel(widgets_2)
        self.fondo.setGeometry(QtCore.QRect(0, 0, 1200, 800))
        self.fondo.setText("")
        self.fondo.setPixmap(QtGui.QPixmap("data/im.png"))

        self.back = QtWidgets.QLabel(widgets_2)
        self.back.setGeometry(QtCore.QRect(700, 515, 100, 100))
        imagen = QtGui.QPixmap('data/cover.jpg')
        imag_red = imagen.scaled(100, 100)
        self.back.setPixmap(QtGui.QPixmap(imag_red))

        reproductor = QtWidgets.QPushButton(widgets_2)
        reproductor.setGeometry(QtCore.QRect(530, 30, 150, 30))
        reproductor.setText("Reproductor")
        reproductor.setStyleSheet("QPushButton"
                                        "{"
                                        "background-color: black;"
                                        "color:white;"
                                        "border-radius : 15px;"
                                        "font: 500 10pt 'Bahnschrift'"
                                        "}"
                                        )
        reproductor.clicked.connect(self.window_1)
        reproductor.clicked.connect(self.setPlayer)

        self.download_in = QtWidgets.QLineEdit(widgets_2)
        self.download_in.setGeometry(QtCore.QRect(550, 160, 150, 32))

        self.download_btn = QtWidgets.QPushButton(widgets_2)
        self.download_btn.setGeometry(QtCore.QRect(725, 160, 150, 32))
        self.download_btn.setText("Download Song")
        self.download_btn.setStyleSheet("QPushButton"
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
        self.download_btn.clicked.connect(self.download)
        self.download_btn.setEnabled(self.downloadingSong)

        data = []
        for song in self.songs:
            title = song["song"]
            if title == "Unknow":
                title = song["title"]

            time = '{0}:{1}'.format(song["duration"]//60, (str(song["duration"]%60)).zfill(2))
            data.append([title, song["artist"], song["album"], song["date"]["year"], time])

        self.model = modelsPyQt5.TableModel(data)

        self.table = QtWidgets.QTableView(widgets_2)
        self.table.setGeometry(QtCore.QRect(261, 140, 677, 350))
        self.table.setModel(self.model)

        nextSongBtn = QtWidgets.QPushButton(widgets_2)
        nextSongBtn.setGeometry(QtCore.QRect(630, 675, 140, 50))
        nextSongBtn.setStyleSheet("QPushButton"
                                        "{"
                                        "background-color: white;"
                                        "border-radius : 20px;"
                                        "image: url(data/next.png);"
                                        "}"
                                        "QPushButton:pressed""{background-color:black;"
                                        "image: url(data/next_.png);}")
        nextSongBtn.clicked.connect(self.nextSong)

        prevSongBtn = QtWidgets.QPushButton(widgets_2)
        prevSongBtn.setGeometry(QtCore.QRect(440, 675, 140, 50))
        prevSongBtn.setStyleSheet("QPushButton"
                                        "{"
                                        "background-color: white;"
                                        "border-radius : 20px;"
                                        "image: url(data/prev.png);"
                                        "}"
                                        "QPushButton:pressed""{background-color:black;"
                                        "image: url(data/prev_.png);}")
        prevSongBtn.clicked.connect(self.prevSong)

        playPauseBtn = QtWidgets.QPushButton(widgets_2)
        playPauseBtn.setGeometry(QtCore.QRect(560, 650, 100, 100))
        playPauseBtn.setStyleSheet("QPushButton"
                                        "{"
                                        "background-color: black;"
                                        "border-radius : 50px;"
                                         "image: url(data/play-pause1_.png);"
                                        "}"
                                        "QPushButton:pressed""{background-color:white;"
                                        "image: url(data/play-pause1.png);"
                                        "}")
        playPauseBtn.clicked.connect(self.playPause)

        self.title = QtWidgets.QLabel(widgets_2)
        self.title.setGeometry(QtCore.QRect(400, 515, 250, 50))
        self.title.setStyleSheet("font: 5000 12pt 'Bahnschrift'")
        self.title.setText("Kacerrolas")

        self.artist = QtWidgets.QLabel(widgets_2)
        self.artist.setGeometry(QtCore.QRect(400, 550, 250, 50))
        self.artist.setStyleSheet("font: 5000 12pt 'Bahnschrift'")
        self.artist.setText("By Antonio, Frida & Jhonny")

        self.progress = QtWidgets.QSlider(widgets_2)
        self.progress.setGeometry(QtCore.QRect(400, 610, 400, 30))
        self.progress.setOrientation(1)

        randomBtn = QtWidgets.QPushButton(widgets_2)
        randomBtn.setGeometry(QtCore.QRect(800, 685, 30, 30))
        randomBtn.setStyleSheet("QPushButton"
                                        "{"
                                        "background-color: black;"
                                        "border-radius : 15px;"
                                        "image: url(data/random.png);"
                                        "}"
                                        "QPushButton:pressed""{background-color:white;"
                                        "image: url(data/random_.png);"
                                        "}")
        randomBtn.clicked.connect(self.shuffle)

        self.repeat = QtWidgets.QPushButton(widgets_2)
        self.repeat.setGeometry(QtCore.QRect(380, 685, 30, 30))

        self.repeat.setStyleSheet("QPushButton"
                                        "{"
                                        "background-color: black;"
                                        "border-radius : 15px;"
                                        "image: url(data/repeat.png);"
                                        "}"
                                        "QPushButton:pressed""{background-color:white;"
                                        "image: url(data/repeat_.png);"
                                        "}")
        self.repeat.clicked.connect(self.loop)

        self.time1 = QtWidgets.QLabel(widgets_2)
        self.time1.setGeometry(QtCore.QRect(400, 610, 100, 50))
        self.time1.setStyleSheet("font: 50 10pt 'Bahnschrift'")
        self.time1.setText("0:00")

        #Duración total
        self.time2 = QtWidgets.QLabel(widgets_2)
        self.time2.setGeometry(QtCore.QRect(775, 620, 100, 50))
        self.time2.setStyleSheet("font: 50 10pt 'Bahnschrift'")
        self.time2.setText("0:00")

        self.MainWindow.setCentralWidget(widgets_2)
        self.loopSong = not self.loopSong
        self.loop()


    def keybordInstruction(self, ins):
        ({
                        "A" : lambda _: self.playPause(),
                        "B" : lambda _: self.nextSong(),
                        "C" : lambda _: self.prevSong(),
                        "D" : lambda _: print("D"),
                        "#" : lambda _: print(self.playerMaster.volume),
                        "*" : lambda _: self.playerMaster._do_setvolume
        })[ins](True)

    def keybordSelectSong(self, num):
        num -= 1
        self.selected = num % self.sizeSongs
        self.setPlayer(self.selected)
        self.playSong()

    def keyboardControl(self):
        self.thread_key = QThread()
        self.keyboardClass = taskQCorePython.Keyboard()
        self.keyboardClass.moveToThread(self.thread_key)

        self.keyboardClass.finished.connect(self.thread_key.quit)
        self.keyboardClass.finished.connect(self.keyboardClass.deleteLater)
        self.keyboardClass.instruction.connect(self.keybordInstruction)
        self.keyboardClass.number.connect(self.keybordSelectSong)

        self.thread_key.started.connect(self.keyboardClass.readData)
        self.thread_key.finished.connect(self.thread_key.deleteLater)

        self.thread_key.start()

    def download(self):
        if self.download_in.text() == "":
            return
        self.download_in.setText("")
        self.download_btn.setEnabled(False)
        self.downloadingSong = False
        self.thread = QThread()
        self.Downloader = taskQCorePython.Downloader()
        self.Downloader.set(self.download_in.text())
        self.Downloader.moveToThread(self.thread)

        self.Downloader.finished.connect(self.thread.quit)
        self.Downloader.finished.connect(self.Downloader.deleteLater)

        self.thread.started.connect(self.Downloader.dwn)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()
        self.thread.finished.connect(self.refreshDataSheet)
        self.thread.finished.connect(self.endDownload)

    def endDownload(self):
        try:
            self.downloadingSong = True
            self.download_in.setText("")
            self.download_btn.setEnabled(True)
        except:
            pass

    def refreshDataSheet(self):
        self.songs = json.load(open("database.json", "r"))["songs"]
        self.sizeSongs = len(self.songs)
        self.selected = 0

    def setValueTime(self):
        self.timestampSong += 1
        try:
            self.progress.setValue(self.timestampSong)
            self.time1.setText(str(self.timestampSong//60)+":"+(str(self.timestampSong%60)).zfill(2))
        except:
            pass
        if self.timestampSong >= self.maxSongDuration:
            self.endSong()

    def playSong(self):
        self.setPlayer(self.selected)
        self.timestampSong = 0
        self.playerMaster = AudioPlayer("./data/music/" + str(self.songs[self.selected]["song_number"]) + ".mp3")
        self.playerMaster.play()

        self.timerSong.start()
        self.maxSongDuration = self.songs[self.selected]["duration"]

    def nextSong(self):
        self.selected = (self.selected + 1) % self.sizeSongs
        self.playSong()

    def prevSong(self):
        self.selected = (self.selected or (self.sizeSongs)) -1
        self.playSong()

    def playPause(self):
        self.controlPP = not self.controlPP
        if self.controlPP:
            if self.playerMaster._player == None:
                self.playSong()
                self.controlPP = not self.controlPP
            else:
                print(dir(self.playerMaster))
                self.playerMaster.pause()
                self.timerSong.stop()
        else:
            self.playerMaster.resume()
            self.timerSong.start()

    def setPlayer(self, number=-1):
        if number == -1:
            number = self.selected

        self.loopSong = not self.loopSong
        self.loop()
        if self.songs[self.selected]["song"] != "Unknow":
            self.title.setText(self.songs[self.selected]["song"])
        else:
            self.title.setText(self.songs[self.selected]["title"])

        self.artist.setText(self.songs[self.selected]["artist"])
        self.progress.setMaximum(self.songs[self.selected]["duration"])
        self.back.setPixmap(QtGui.QPixmap(glob.glob("data/music/"+str(self.songs[self.selected]["song_number"]) + "_thumbnail*")[0]))
        self.time2.setText(str(self.songs[self.selected]["duration"]//60) + ":" + (str(self.songs[self.selected]["duration"]%60)).zfill(2))

    def loop(self):
        self.loopSong = not self.loopSong
        if self.loopSong:
            self.repeat.setStyleSheet("QPushButton"
                                        "{"
                                        "background-color: white;"
                                        "border-radius : 15px;"
                                        "image: url(data/repeat_.png);"
                                        "}"
                                        )
        else:
            self.repeat.setStyleSheet("QPushButton"
                                        "{"
                                        "background-color: black;"
                                        "border-radius : 15px;"
                                        "image: url(data/repeat.png);"
                                        "}"
                                        )

    def endSong(self):
        if not self.loopSong:
            self.selected = (self.selected + 1) % self.sizeSongs
        self.setPlayer(self.selected)
        self.playSong()

    def shuffle(self):
        random.shuffle(self.songs)
        data = []
        for song in self.songs:
            title = song["song"]
            if title == "Unknow":
                title = song["title"]

            time = '{0}:{1}'.format(song["duration"]//60, (str(song["duration"]%60)).zfill(2))
            data.append([title, song["artist"], song["album"], song["date"]["year"], time])
        self.model = modelsPyQt5.TableModel(data)
        self.table.setModel(self.model)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Ui_MainWindow()
    sys.exit(app.exec_())
