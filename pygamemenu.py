from gpiozero import Button
import os
import subprocess
import time
from picamera2 import Picamera2
from datetime import datetime

import pygame
pygame.init()
up = Button(26)
down = Button(6)
select = Button(5)
clock=pygame.time.Clock()

background = (30, 30, 30)
font = pygame.font.SysFont("Helvetica", 26)

screen = pygame.display.set_mode((480, 360), pygame.FULLSCREEN)
running = True
pygame.mouse.set_visible(False)

def goback():
    history.pop()
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
def runDOOM():
    global font
    global clock
    global screen
    global running
    doomrunning = subprocess.Popen(["chocolate-doom"])
    pygame.mouse.set_visible(False)
    select.wait_for_release()
    select.wait_for_press()

    doomrunning.kill()
    doomrunning.wait()
    time.sleep(0.5)

    select.wait_for_release()

    pygame.mouse.set_visible(False)

def runPSGAME():
    print ("running psgame")
def runGAMEBOY():
    print 
def poweroff():
    subprocess.run(["sudo", "poweroff"])
def backlight():
    print
def volume():
    print

def opencam():
    print("opened camera")
    select.wait_for_release()
    cam = Picamera2()
    cam.preview_configuration.main.size = (480, 320)
    cam.preview_configuration.main.format = "BGR888"
    picconfig = cam.create_still_configuration(main = {"size": (2592, 1944)})
    cam.configure("preview")
    cam.start()
    cam.set_controls({"Saturation": 1.3, "Contrast" : 1.2, "Sharpness" : 1.4, "NoiseReductionMode":0, "ExposureValue": 0.5})

    while True:
        array = cam.capture_array()
        img = pygame.image.frombuffer(array.data, (480, 320), "RGB")
        screen.blit(img, (0,0))
        pygame.display.flip()
        if select.is_pressed:
            select.wait_for_release()
            break
        if down.is_pressed:
            down.wait_for_release()
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"/home/cirrus/images/{timestamp}.jpg" 
            cam.stop()
        
            cam.configure(picconfig) 
            cam.start()          
            cam.capture_file(filename)
            pic = pygame.image.load(filename)
            pic = pygame.transform.scale(pic, (480, 320))
            screen.blit(pic, (0,0))
            pygame.display.flip()
            pygame.time.wait(5000)
            clock.tick(30)
            cam.stop()
            
            cam.configure("preview")
            cam.start()
    cam.stop()


menus = { "Main": 
    {
    "Music": "Music",
    "Games" : "Games",
    "Settings" : "Settings",
    "Camera" : opencam,
    "Power Off" : poweroff
    },
    "Music" : {
    "Liked Songs": openlikedsongs,
    "Playlists": openplaylists,
    "Search": opensearch,
    "Back": goback,
    },

"Games" : {
    "Doom": runDOOM,
    "PS1": runPSGAME,
    "Back": goback
},

"Settings" : {
    "Volume": volume,
    "Backlight": backlight,
    "Back": goback
}}

history = ["Main"]
currentmenu = history[-1]
currentoptions = list(menus[currentmenu].keys())

def clearscreen():
    screen.fill((240,240,240))
    pygame.draw.rect(screen, (30, 30, 30), (0,0,480,30))

def draw_menu():
    global currentmenu
    global currentoptions
    currentmenu = history[-1]
    currentoptions = list(menus[currentmenu].keys())
    screen.fill(background)
    pygame.draw.rect(screen, (40, 40, 40), (2, 0, 240, 360))
    for index, item in enumerate(currentoptions):
        entryrects = pygame.Rect(2, index * 30, 240, 30)
        if index == selected:
            pygame.draw.rect(screen, (80, 80, 80), entryrects)
        else:
            pygame.draw.rect(screen, (40, 40, 40), entryrects)
        text = font.render(item, False, (255, 255, 255))
        screen.blit(text, (entryrects.x + 2, entryrects.y + 2 ) )

selected = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    draw_menu()
    if select.wait_for_press(timeout=0):
        choice = currentoptions[selected]
        action = menus[currentmenu][choice]
        if isinstance (action, str):
            history.append(choice)
        else:
            action()
        selected = 0
        select.wait_for_release()
    if down.wait_for_press(timeout=0) and selected < len(currentoptions)-1:
        selected += 1
        down.wait_for_release()
    if up.wait_for_press(timeout=0) and selected > 0:
        selected -= 1
        up.wait_for_release()
    pygame.display.flip()
    clock.tick(60)


