import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import json
import glob

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
        self.refreshDataSheet()

        app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.MainWindow.resize(1200, 800)
        self.window_1()
        self.MainWindow.show()
        app.exec_()


    def window_1(self):
        widgets_1 = QtWidgets.QWidget(self.MainWindow)

        self.back = QtWidgets.QLabel(widgets_1)
        self.back.setGeometry(QtCore.QRect(0, 0, 1200, 800))
        self.back.setText("")
        self.back.setPixmap(QtGui.QPixmap("data/gato_piano.jpg"))

        canciones_secc_1 = QtWidgets.QPushButton(widgets_1)
        canciones_secc_1.setGeometry(QtCore.QRect(20, 40, 150, 40))
        canciones_secc_1.setText("Canciones")
        canciones_secc_1.clicked.connect(self.window_2)
        #canciones_secc_1.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        #canciones_secc_1.setTransform(QtGui.QTransform().rotate(-90),QtCore.Qt.SmoothTransformation)

        canciones_secc_1 = QtWidgets.QPushButton(widgets_1)
        canciones_secc_1.setGeometry(QtCore.QRect(20, 240, 150, 40))
        canciones_secc_1.setText("Siguiente")
        canciones_secc_1.clicked.connect(self.nextSong)

        canciones_secc_1 = QtWidgets.QPushButton(widgets_1)
        canciones_secc_1.setGeometry(QtCore.QRect(20, 440, 150, 40))
        canciones_secc_1.setText("Antes")
        canciones_secc_1.clicked.connect(self.prevSong)

        canciones_secc_1 = QtWidgets.QPushButton(widgets_1)
        canciones_secc_1.setGeometry(QtCore.QRect(20, 640, 150, 40))
        canciones_secc_1.setText("Play/Pause")
        canciones_secc_1.clicked.connect(self.playPause)

        self.title = QtWidgets.QLabel(widgets_1)
        self.title.setGeometry(QtCore.QRect(300, 40, 150, 40))
        self.title.setText("Kacerrolas")

        self.artist = QtWidgets.QLabel(widgets_1)
        self.artist.setGeometry(QtCore.QRect(300, 240, 150, 40))
        self.artist.setText("By Antonio, Frida & Jhonny")

        self.progress = QtWidgets.QSlider(widgets_1)
        self.progress.setGeometry(QtCore.QRect(300, 440, 150, 40))

        canciones_secc_1 = QtWidgets.QPushButton(widgets_1)
        canciones_secc_1.setGeometry(QtCore.QRect(300, 640, 150, 40))
        canciones_secc_1.setText("random")
        canciones_secc_1.clicked.connect(self.shuffle)

        canciones_secc_1 = QtWidgets.QPushButton(widgets_1)
        canciones_secc_1.setGeometry(QtCore.QRect(500, 40, 150, 40))
        canciones_secc_1.setText("repeat")
        canciones_secc_1.clicked.connect(self.loop)

        self.progress.setOrientation(1)
        self.progress.setMaximum(60)
        self.progress.setMinimum(0)
        self.progress.setValue(0)

        self.MainWindow.setCentralWidget(widgets_1)

    def window_2(self):
        widgets_2 = QtWidgets.QWidget(self.MainWindow)

        canciones_secc_2 = QtWidgets.QPushButton(widgets_2)
        canciones_secc_2.setGeometry(QtCore.QRect(225, 360, 150, 32))
        canciones_secc_2.setText("reproductor")
        canciones_secc_2.clicked.connect(self.window_1)

        #box = QtWidgets.QTextBrowser(widgets_2)
        #box.setGeometry(QtCore.QRect(550, 60, 450, 630))

        data = []

        for song in self.songs:

            title = song["song"]
            if title == "Unknow":
                title = song["title"]
                
            time = '{0}:{1}'.format(song["duration"]//60, (str(song["duration"]%60-10)).zfill(2))

            data.append([
                title,
                song["artist"],
                song["album"],
                song["date"]["year"],
                time
            ])

        self.model = TableModel(data)

        self.table = QtWidgets.QTableView(widgets_2)
        self.table.setGeometry(QtCore.QRect(500, 60, 650, 630))
        self.table.setModel(self.model)

        self.MainWindow.setCentralWidget(widgets_2)

    def refreshDataSheet(self):
        self.songs = json.load(open("database.json", "r"))["songs"]
        self.sizeSongs = len(self.songs)
        self.selected = 0

    def nextSong(self):
        print("next")
        self.selected = (self.selected + 1) % self.sizeSongs
        self.setPlayer(self.selected)
        print("listening to: ", self.songs[self.selected]["title"])

    def prevSong(self):
        print("previous")
        self.selected = (self.selected or (self.sizeSongs)) -1
        self.setPlayer(self.selected)
        print("listening to: ", self.songs[self.selected]["title"])

    def playPause(self):
        self.controlPP = not self.controlPP
        if self.controlPP:
            print("play")
        else:
            print("pause")

    def setPlayer(self, number):
        if self.songs[self.selected]["song"] != "Unknow":
            self.title.setText(self.songs[self.selected]["song"])
        else:
            self.title.setText(self.songs[self.selected]["title"])

        self.artist.setText(self.songs[self.selected]["artist"])

        self.progress.setMaximum(self.songs[self.selected]["duration"])

        self.back.setPixmap(QtGui.QPixmap(glob.glob("data/music/"+str(self.songs[self.selected]["song_number"]) + "_thumbnail*")[0]))

    def loop(self):
        print("loop active")
        print("loop inactive")

    def shuffle(self):
        print("shuffled")



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Ui_MainWindow()
    sys.exit(app.exec_())
