import time
import serial

con = serial.Serial(port='/dev/ttyACM0', baudrate = 19200, timeout=1)
functions = {
                "A" : lambda _: print("A"),
                "B" : lambda _: print("B"),
                "C" : lambda _: print("C"),
                "D" : lambda _: print("D"),
                "#" : lambda _: print("#"),
                "*" : lambda _: print("*")
            }

data = ""
num = -1

while 1:
    x = con.read().decode('utf-8')
    if functions.get(x) != None:
        functions[x](True)
        data = ""
    elif x != "":
        data += x
    elif data != "":
        num = int(data)
        print(num)
        data = ""
