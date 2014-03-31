#!/usr/bin/python 
from wand.image import Image

with Image(filename="./static/upload/demo.pdf",resolution=70) as img:
        img.save(filename="./static/upload/pic.png")
