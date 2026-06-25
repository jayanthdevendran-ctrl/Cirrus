import subprocess
import time
from PIL import ImageFont
from gpiozero import Button
from luma.core.interface.serial import spi
from luma.lcd.device import ili9341
from luma.core.render import canvas
serial = spi(port=0, device=0, gpio_DC=25, gpio_RST=27)
device = ili9341(serial, width=160, height=240)

menu = {
    "Music" : {"Liked songs" : likedsongsfunction,
               "Playlists" : displayplaylists,
               "Search" : opensearch,
               "Local" : downloadedmusic},

    "Games" : { "PS1" : {"Castlevania" : Launch castlevania,
                        "Doom" : Launch Doom},
                "Gameboy": Launchgameboy}
        }        

menustack = [menu]
top = menustack(len) - 1
topmenu = menustack[top]
def drawmenu (topmenu, selected_index):
    with canvas(device) as draw:
        for index, item in enumerate(topmenu):
            if index == selected_index:
                draw.text((10, 15*(index+1)), item, fill = "yellow")
            else:
                draw.text((10, 15*(index+1)), item, fill = "white")

down = Button(26)
up = Button(24)
select = Button(19)

while True:
    downtrue = down.is_pressed
    uptrue = up.is_pressed
    selecttrue = select.is_pressed
    if downtrue == True:
        if x<4:
            x = x+1
    if uptrue == True:
        if x>0:
            x = x-1
    if selecttrue == True:
        menu.append{}
        x = 0
        drawmenu(current_menu, x)

    drawmenu(current_menu, x)
    time.sleep(0.2)
    
