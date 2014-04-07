#!/usr/bin/python 
from wand.image import Image

with Image(filename="./static/upload/3/3.pdf",resolution=70) as img:
        img.format="png"
        img.alpha_channel=False
        img.save(filename="/tmp/t.png")
