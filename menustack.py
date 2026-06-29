import subprocess
import time
from gpiozero import Button
from luma.core.interface.serial import spi
from luma.lcd.device import ili9341
from luma.core.render import canvas
serial = spi(port=0, device=0, gpio_DC=25, gpio_RST=27)
device = ili9341(serial, width=320, height=240)

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
def poweroff():
    subprocess.run(["sudo", "poweroff"])
def goback():
    x = 0
    stack.pop()
def backlight():
    print
def volume():
    print


menus = {"Menu" : {
         "Music": {"Liked Songs" : openlikedsongs, "Playlists" : openplaylists, "Search": opensearch, "Go Back": goback}, 
         "Games": {"Doom": runDoom, "PS1": runPSGAME, "Go Back": goback},
         "Settings": {"Backlight": backlight, "Volume": volume} ,
         "PowerOff": poweroff
        }}

stack = [menus["Menu"]] 
currentmenu = stack[-1]

down = Button(26)
up = Button(24)
select = Button(19, bounce_time=0.05)

def draw_menus(menu, selected_index):
    keys = menu.keys()
    with canvas(device) as draw:
        for index, item in enumerate(keys):
            if index == selected_index:
                draw.text((10, 15*(index+1)), str(item), fill = "green")
            else:
                draw.text((10, 15*(index+1)), str(item), fill = "gray")

x = 0
while True:
    keys = list(currentmenu.keys())
    selected = currentmenu[keys[x]]
    downtrue = down.is_pressed
    uptrue = up.is_pressed
    selecttrue = select.is_pressed
    
    if downtrue == True and x < len(currentmenu) - 1:
        x = x+1
        selected = currentmenu[keys[x]]

    if uptrue == True and x > 0:
        x = x-1
        selected = currentmenu[keys[x]]
    
    if selecttrue == True and keys[x] == "Go Back":
        x = 0
        print(stack)
        print("WENTBACK")
        stack.pop()
        time.sleep(1.5)
        while select.is_pressed:
            time.sleep(0.01)
        
    elif selecttrue == True and keys[x] != "Go Back":
        print("ENTEREDMENU/RANFUNCTION")
        if isinstance(selected, dict): 
            stack.append(selected)
            x = 0
        else:
            selected()
            time.sleep(2)
        while select.is_pressed:
            time.sleep(0.01)

    currentmenu = stack[-1]
    draw_menus(currentmenu, x)
    time.sleep(0.2)

