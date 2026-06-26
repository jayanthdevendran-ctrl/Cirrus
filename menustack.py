import subprocess
import time
from PIL import ImageFont
from gpiozero import Button
from luma.core.interface.serial import spi
from luma.lcd.device import ili9341
from luma.core.render import canvas
serial = spi(port=0, device=0, gpio_DC=25, gpio_RST=27)
device = ili9341(serial, width=160, height=240)

def openlikedsongs():
    print
def openplaylists():
    print
def opensearch():
    print
def openlocal():
    print
def opengames():
    print
def runDoom():
    print
def runPSGAME():
    print
def runGAMEBOY():
    print

Doom = runDoom
ps1 = runPSGAME
Gameboy = runGAMEBOY
LikedSongs = openlikedsongs
Playlists = openplaylists
Search = opensearch
Local = openlocal

Settings = ["Backlight", "Voume", "Go Back"]
Games = [Doom, ps1, Gameboy, "Go Back"]
Music = [LikedSongs, Playlists, Search, Local, "Go Back"]
menus = [ Music, Games, Settings]

stack = [menus] 
currentmenu = stack[-1]

down = Button(26)
up = Button(24)
select = Button(19)

def draw_main(menu, selected_index):
    with canvas(device) as draw:
        for index, item in enumerate(menu):
            if index == selected_index:
                draw.text((10, 15*(index+1)), item, fill = "yellow")
            else:
                draw.text((10, 15*(index+1)), item, fill = "white")

x = 0
while True:
    downtrue = down.is_pressed
    uptrue = up.is_pressed
    selecttrue = select.is_pressed
    if downtrue == True and x < len(currentmenu) - 1:
        x = x+1

    if uptrue == True and x > 0:
        x = x-1

    if selecttrue == True and currentmenu[x] == "Go Back":
        x = 0
        stack.pop()
        
    if selecttrue == True and currentmenu[x] != "Go Back":
        if type(currentmenu[x]) == list:
            stack.append(currentmenu[x])
            x = 0
        else:
            currentmenu[x]()        

    currentmenu = stack[-1]
    draw_main(currentmenu, x)
    time.sleep(0.2)

