#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-2020 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

import time
import json

from pathlib import Path
from demo_opts import get_device
from luma.core.virtual import viewport
from luma.core.render import canvas
from PIL import Image


with open('cancion.json') as file:
    songs = json.load(file)['songs']
    i = 0

    song = songs[0]
    blurb =song['title']+"\n"+song['album']+"\n"+song['artist']+"\n"+str(song['duration'])+"\n"+str(song['date']['year'])

def main():
    virtual = viewport(device, width=device.width, height=768)
    for _ in range(2):
        with canvas(virtual) as draw:
            for i, line in enumerate(blurb.split("\n")):
                draw.text((0, 40 + (i * 12)), text=line, fill="white")

    time.sleep(2)

    # update the viewport one position below, causing a refresh,
    # giving a rolling up scroll effect when done repeatedly
    for y in range(450):
        virtual.set_position((0, y))
        time.sleep(0.01)


if __name__ == "__main__":
    try:
        i=0
        device = get_device()
        main()
    except KeyboardInterrupt:
        pass
