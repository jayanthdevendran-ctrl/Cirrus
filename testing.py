from luma.core.interface.serial import spi
from luma.lcd.device import ili9341
from luma.core.render import canvas
serial = spi(port=0, device=0, gpio_DC=25, gpio_RST=27)
device = ili9341(serial, width=320, height=240)

items = ["MP3", "PS1", "DOOM", "Settings", "Power OFF"]
def draw_menu(items, selected_index):
    with canvas(device) as draw:
        for index, item in enumerate(items):
            if index == selected_index:
                draw.text((10, 15*(index+1)), item, fill = "yellow")
            else:
                draw.text((10, 15*(index+1)), item, fill = "white")
draw_menu(items, 1)
input ("type smth")


