import subprocess
import time
from PIL import ImageFont
from gpiozero import Button
from luma.core.interface.serial import spi
from luma.lcd.device import ili9341
from luma.core.render import canvas
serial = spi(port=0, device=0, gpio_DC=25, gpio_RST=27)
device = ili9341(serial, width=160, height=240)

menus = { "Menu" : {
    "Music" : {"Liked songs" : print("open liked songs"),
               "Playlists" : print("opened playlists"),
               "Search" : print("opened searc"),
               "Local" : print("opened dl")},

    "Games" : { "PS1" : {"Castlevania" : print("Launch castlevania"),
                        "Doom" : print("Launch Doom")},
                "Gameboy": ("Launchgameboy")}}
        }        
menustack = [menus]
top = menustack(len) - 1
topmenu = menustack[top]
def drawmenu (topmenu, selectedindex):
    with canvas(device) as draw:
        indexes = topmenu.getkeys
        global current_item
        indexcurrent = indexes.index()
        for sub in menus[topmenu]:
            if sub == selectedindex:
                draw.text((10, 15*()), item, fill = "yellow")



down = Button(26)
up = Button(24)
select = Button(19)

while True:
    downtrue = down.is_pressed
    uptrue = up.is_pressed
    selecttrue = select.is_pressed
    if downtrue == True:
        if x<len():
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

"""so we want a dictionary 
main > MP3 > Playlists
             liked songs
             search
    > Games > PS1 > MGS
                    Granturismo 
            > Doom
            > Wolfenstein
    > Settings > Volume
                 brightness
                 wifi
                 etc

so, we have a draw with canvas
a dictionary each time, so i want to iterate through a dictionary                 
            """
for element in dict of current menu:
    draw wtv is in the dictionary
dict has to change for each menu
dict = dict under each thing

for ele in 