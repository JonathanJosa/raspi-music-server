import time
import json
from pathlib import Path
from demo_opts import get_device
from luma.core.virtual import viewport
from luma.core.render import canvas
from PIL import Image

def main(num):
    song = json.load(open('cancion.json'))['songs'][num]

    name_song = song['song']
    if name_song == "Unknow":
        name_song = song['title']

    text = name_song+"\n"+song['album']+"\n"+song['artist']+"\n"+str(song['duration'])+"\n"+str(song['date']['year'])

    device = get_device()
    virtual = viewport(device, width=device.width, height=768)
    for _ in range(2):
        with canvas(virtual) as draw:
            for i, line in enumerate(text.split("\n")):
                draw.text((0, 40 + (i * 12)), text=line, fill="white")
    time.sleep(1)

    for y in range(450):
        virtual.set_position((0, y))
        time.sleep(0.01)

if __name__ == "__main__":
    main()
