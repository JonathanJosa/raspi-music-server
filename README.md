# raspi-music-server
using python3 with pyqt5, i2c and bluetooth protocol, serial connection to arduino threads for keyboard and volume control with interrumpts, telegram bot for shell commands control and utilities for api rest and ftp music database

## Mp3
Este es un codigo programado en python y C# con FreeRtos en el microcontrolador 328p, para el funcionamiento de un reproductor mp3. Se integraron dos componentes que funcionaron como dispositivos de entrada y salida, un teclado matricial para el control y manejo de las canciones y una pantalla oled donde se muestra la información de la canción en reproducción. 

## Instalación 
Instalación de pyqt5
```sh
pip3 install PyQt5
```
Instalación de luma.core
```sh
pip3 install luma.core
```
Instalación de multitasking
```sh
pip3 install multitasking
```
Instalación de audioplayer
```sh
pip3 install audioplayer
```
Instalación de youtube_dl
```sh
pip3 install youtube_dl
```

## Construcción del código
### Codigo principal
Se importan las siguientes librerías:
```Py
import json, glob, time, random, sys, signal, multitasking
from audioplayer import AudioPlayer
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *

import taskQCorePython
import modelsPyQt5
```
Se crea la clase de la interfaz(Ui_MainWindow), se definien algunos estados de las funciones y se definen algunas detalles como lo son el tamaño de la interfaz gráfica
```PY
class Ui_MainWindow(object):

    def init(self):
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
```
Se crean la primera ventana de inicio en donde se carga una imagen para poder dar la bienvenida a la aplicación 
```Py
    def window_0(self):
        self.widgets_0 = QtWidgets.QWidget(self.MainWindow)

        fondo = QtWidgets.QLabel(self.widgets_0)
        fondo.setGeometry(QtCore.QRect(0, 0, 1200, 800))
        fondo.setPixmap(QtGui.QPixmap("data/line.jpg"))

        self.back = QtWidgets.QLabel(self.widgets_0)
        self.back.setGeometry(QtCore.QRect(120, 130, 960, 540))
        self.back.setPixmap(QtGui.QPixmap("data/casette.png"))

        self.MainWindow.setCentralWidget(self.widgets_0)
```
Se crea la segunda ventana del reproductor de música en donde se muestran los botones de pause, play, next previous, rewind y shuffle, tambien se muestran datos de la cancion como lo son el nombre, tiempo de duración, autor de la canción album, etc.
A su vez se asignan las acciones de cada boton correspóndiendo al icono con el que este cuenta
```Py
    def window_1(self):
        widgets_1 = QtWidgets.QWidget(self.MainWindow)
        self.widthScaled = 400

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

```
Dentro de la siguiente funcion al igual que la anterior se crea la segunda ventana la cual cuenta con funcionalidades parecidas sin embargo se le agrega la funcionalidad de poder descargar canciones directamente desde internet en timpo real y se puede observar en forma de lista todos los elementos con los que cuenta el reproductor mp3
```Py
    def window_2(self):
        widgets_2 = QtWidgets.QWidget(self.MainWindow)
        self.widthScaled = 100

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
        self.download_in.setGeometry(QtCore.QRect(300, 85, 400, 32))

        self.download_btn = QtWidgets.QPushButton(widgets_2)
        self.download_btn.setGeometry(QtCore.QRect(725, 85, 200, 32))
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
        self.table.setGeometry(QtCore.QRect(311, 140, 577, 350))
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
```
Las siguientes funciones se encargan de la lectura del teclado matricial así como de la comprobación de los datos enviados y realizar las acciones que cada boton cuenta para poder manipularlo directamente desde el arduino a la raspberry
```Py
    def keybordInstruction(self, ins):
        ({
                        "A" : lambda _: self.playPause(),
                        "B" : lambda _: self.nextSong(),
                        "C" : lambda _: self.prevSong(),
                        "D" : lambda _: print("D"),
                        "#" : lambda _: self.shuffle(),
                        "*" : lambda _: self.loop()
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
```
Esta funcion es la encargada de poder descargar directamente desde youtube las canciones, siendo que esta guarda los datos como lo son artista, album, duración, etc. Por otra parte tambien se encarga de descargar la imagen en la mejor calidad posible para posteriormente poder mostrarla en la interfaz
```Py
    def download(self):
        if self.download_in.text() == "":
            return
        self.download_btn.setEnabled(False)
        self.downloadingSong = False
        self.thread = QThread()
        self.Downloader = taskQCorePython.Downloader()
        self.Downloader.set(self.download_in.text())
        self.Downloader.moveToThread(self.thread)

        self.download_in.setText("")

        self.Downloader.finished.connect(self.thread.quit)
        self.Downloader.finished.connect(self.Downloader.deleteLater)

        self.thread.started.connect(self.Downloader.dwn)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()
        self.thread.finished.connect(self.refreshDataSheet)
        self.thread.finished.connect(self.endDownload)
```
Esta función se encarga de controlar las acciones que indicamos al programa desde telegram, ya que con este podemos realizar acciones como lo son pausar la musica, siguiente, anterior, seleccionar la canción o ponerla en loop
```Py
    def telegramInterpreter(self, opt):
        ({
            "Next": lambda _ : self.nextSong(),
            "Prev": lambda _ : self.prevSong(),
            "PlPa": lambda _ : self.playPause(),
            "PlPa": lambda _ : self.playPause(),
            "Sele": lambda n : self.keybordSelectSong(n),
            "Loop": lambda _ : self.loop(),
            "Shuf": lambda _ : self.shuffle()
        }[opt[0:4]])(int(opt[4:]))
```
Gracias a esta función podemos ver la información de las canciones en la Oled
```Py
    def oledShow(self):
        try:
            self.disp.killer = True
        except:
            pass
        self.disp = taskQCorePython.oledControl()
        self.disp.song(self.songs[self.selected])
```
Se comprueba que las canciones se hayan descargado correctamente para posteriormente enviarla a una base de datos para su almacenamiento tanto de la multimedia como de la información de la canción
```Py

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
```
Se asignan las funcionalidades con las que contarán los botones que se muestran en la interfaz gráfica y las acciones son programadas en las siguientes funciones
```Py
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

        imagen = QtGui.QPixmap(glob.glob("data/music/"+str(self.songs[self.selected]["song_number"]) + "_thumbnail*")[0])
        imag_red = imagen.scaled(self.widthScaled, self.widthScaled)
        self.back.setPixmap(imag_red)

        self.time2.setText(str(self.songs[self.selected]["duration"]//60) + ":" + (str(self.songs[self.selected]["duration"]%60)).zfill(2))
        self.oledShow()

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
        try:
            self.table.setModel(self.model)
        except:
            pass
```

### Codigo arduino
Codigo arduino para el control de las acciones que se enviarán por medio de un teclado matricial.

Se declaran las librerías y se configura el uso y manejo de pines para los macros
```arduino
//demostración del uso de queues con FreeRTOS
#include <Arduino_FreeRTOS.h>
#include "queue.h"

//macros para la configuración y manejo de pines
#define MakeInputPin(REG, PIN)       (REG &= (~(1 << PIN)))
#define MakeOutputPin(REG, PIN)      (REG |= (1 << PIN))
#define EnablePullUp(REG, PIN)       (REG |= (1 << PIN))
#define ReadInputPin(REG, PIN)       (REG & (1 << PIN))
#define WriteOutputPinLow(REG, PIN)  (REG &= ~(1 << PIN))
#define WriteOutputPinHigh(REG, PIN) (REG |= (1 << PIN))
#define ToggleOutputPin(REG, PIN)    (REG ^= (1 << PIN))
```
Se declara el valor de la tasa de comunicación, se crea el handle para una cola y se crea un buffer para el uart
```arduino
//declaraciones de la tasa de comunicación serial
#define F_CPU 16000000UL
#define USART_BAUDRATE 19200
#define UBRR_VALUE (((F_CPU / (USART_BAUDRATE * 16UL))) - 1)

const TickType_t xTicksToWait = pdMS_TO_TICKS(100);

//handle para un queue
QueueHandle_t myQueue;

//buffer para el UART
unsigned char mybuffer[25];
```
Se declara el tamaño de la cola y se crean las tareas del programa
```Arduino
//Tecla presionada
//Modificada por el isr
int row = 0;
char* teclas[] = {"*0#D", "789C", "456B", "123A"};

void setup()
{
  //Forzar para crear queue, debe ser creada antes de usarla por xTask
  while(true){
    //Tamaño de queue pequeño para limitar datos en caso de un rebote
    myQueue = xQueueCreate(3, sizeof(int32_t));
    //revisa si la queue ha sido creada
    if(myQueue != NULL)
    {
      break;
    }
  }

  //creación de tareas
  xTaskCreate(vSenderRows,       "ROWS SENDER",   100, NULL, 1, NULL);
  xTaskCreate(vReceiverTask,     "RECEIVER TASK", 100, NULL, 1, NULL);

```
Declaramos los pines como entradas y salidas así como se habilitan los pull up.
```arduino
  // Renglones en alta impedancia
  MakeInputPin(DDRB, PB3); WriteOutputPinHigh(PORTB, PB3);
  MakeInputPin(DDRB, PB2); WriteOutputPinHigh(PORTB, PB2);
  MakeInputPin(DDRB, PB1); WriteOutputPinHigh(PORTB, PB1);
  MakeInputPin(DDRB, PB0); WriteOutputPinHigh(PORTB, PB0);

  // Columnas en pullup
  MakeInputPin(DDRD, PD7); EnablePullUp(PORTD, PD7);
  MakeInputPin(DDRD, PD6); EnablePullUp(PORTD, PD6);
  MakeInputPin(DDRD, PD5); EnablePullUp(PORTD, PD5);
  MakeInputPin(DDRD, PD4); EnablePullUp(PORTD, PD4);
```
Se habilitan las interrupciones por el cambio de estado en el puerto D y se configura el puerto serial
```arduino
  //interrupciones para DDRD
  //se habilita interrupción por cambio de estado en PORTD
  PCICR |= (1 << PCIE2);
  PCMSK2 |= (1<<7)|(1<<6)|(1<<5)|(1<<4);
  sei();

  //configuración del puerto serial
  UBRR0H = (uint8_t)(UBRR_VALUE >> 8);
  UBRR0L = (uint8_t)UBRR_VALUE;
  UCSR0C = 0x06;       // Set frame format: 8data, 1stop bit
  UCSR0B |= (1 << RXEN0) | (1 << TXEN0);   // TX y RX habilitados
}
```
Acciones de las tareas vSenderRows y vReceiverTask en donde se lee el estado del teclado matricial y en caso de que se encuentre una acción esta se reviará por medio del UART
```arduino
void vSenderRows(void * pvParameters){
  while(true){
    MakeOutputPin(DDRB, row);
    WriteOutputPinLow(PORTB, row);
    //Delay de 60ms, debido a la lectura de posibles rebotes en teclado que duren hasta 50 ms, el doble de un rebote normal
    _delay_ms(60);
    WriteOutputPinHigh(PORTB, row);
    MakeInputPin(DDRB, row);
    row = (row + 1) % 4;
  }
}

void vReceiverTask(void * pvParameters)
{
  char valueReceived;
  BaseType_t qStatus;
  while(1)
  {
    qStatus = xQueueReceiveFromISR(myQueue, &valueReceived, xTicksToWait);
    if(qStatus == pdPASS)
    {
      sprintf(mybuffer, "%c", valueReceived);
      USART_Transmit_String((unsigned char *)mybuffer);
    }
    vTaskDelay(pdMS_TO_TICKS(250));
  }
}
```
Transmición de información por medio del UART
```arduino
//////////funciones de transmisión del UART///////////////

void USART_Transmit(unsigned char data)
{
  while(!(UCSR0A & (1 << UDRE0)));
  UDR0 = data;
}

void USART_Transmit_String(unsigned char * pdata)
{
  unsigned char i;
  unsigned char len = strlen(pdata);
  for(i=0; i < len; i++)
  {
    while(!(UCSR0A & (1 << UDRE0)));
    UDR0 = pdata[i];
  }
}

//////////////////////////////////////////////////////////////
```
Creación del ISR para la transmición de datos hacia la cola
```arduino
ISR(PCINT2_vect){
  int pin_interrupt[4] = {7, 6, 5, 4};
  int row_interrupt = row;
  for(int i=0; i<4; i++){
    if(ReadInputPin(PIND, pin_interrupt[i]) == 0)
    {
      _delay_ms(25);
      while(ReadInputPin(PIND, pin_interrupt[i]) == 0);
      char key = teclas[row_interrupt][i];
      xQueueSendToBackFromISR(myQueue, &key, xTicksToWait);
      return;
    }
  }
}


void loop() {

}
```

## Ejecución de código
```sh
python3 Radio_Tape.py
```
# Conexiones
Conexión del teclado matricial al arduino uno por medio del puerto b y d
![cover](https://github.com/JonathanJosa/raspi-music-server/blob/main/Conexiones/Matricial.PNG)

Conexión de la oled a la raspberry 3b+ por medio del protocolo i2c

![cover](https://github.com/JonathanJosa/raspi-music-server/blob/main/Conexiones/oled.png)

# Video demo de la aplicación
https://youtu.be/2BXIbfJhkOk

## Conclusiones
Este reto fue algo que nos impulso a dar más de nosotros mismos implementando cosas que no se marcaban como tal dentro del reto haciendo que este contara con un valor agregado y así poder mejorar la funcionalidad con la que cuenta nuestro reproductor.
A su vez pudimos implementar las diferentes tecnologías que vimos a lo largo del semestre y pudimos desarrollar más cosas de las esperadas resultando en un proyecto con un punto de vista muy fresco e inovador.
