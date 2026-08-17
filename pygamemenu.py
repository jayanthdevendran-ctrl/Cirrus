from gpiozero import Button
from gpiozero import PWMLED
import os
import subprocess
import time
from picamera2 import Picamera2
from datetime import datetime
from PIL import Image, ImageEnhance, ImageFilter
import spotfunctions as sf
import requests
from io import BytesIO
import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = (
    "user-read-playback-state "
    "user-modify-playback-state "
    "user-read-playback-state "
    "playlist-read-private "
    "user-library-modify "
    "user-library-read "
)

sp = spotipy.Spotify(
    auth_manager = SpotifyOAuth(
        scope = scope
    )
)

import pygame
pygame.init()
up = Button(26)
down = Button(6)
left = Button(1)
right = Button(2)
action1 = Button(3)
action2 = Button(4)
action3 = Button (9)
action4 = Button(7)
select = Button(5)
back = Button(8)

clock=pygame.time.Clock()

background = (30, 30, 30)
font = pygame.font.SysFont("Helvetica", 26)

screen = pygame.display.set_mode((480, 360), pygame.FULLSCREEN)
running = True
pygame.mouse.set_visible(False)

def goback():
    history.pop()

currently_playing = False
song_loaded = False

visible_songs = 8
def openlikedsongs():
    global songlist
    songlist = sf.liked_songs()
    currentoptions = list(songlist.keys())
    scrolloffset = 0
    selected = 0
    while True:
        if selected< scrolloffset:
            scrolloffset = selected
        if selected >= scrolloffset + visible_songs:
            scrolloffset = selected - visible_songs + 1
        screen.fill(background)
        pygame.draw.rect(screen, (40,40,40), (2,0,300,360))
        for item in range(scrolloffset, min(scrolloffset + visible_songs, len(currentoptions))):
            song = currentoptions[item]
            y = (item - scrolloffset) * 40
            if item == selected:
                pygame.draw.rect(screen, (80,80,80), (5, y, 290, 38))
            text = font.render(song, True, (255, 255, 255))
            screen.blit(text, (15, y+5))
        pygame.display.flip()

        if up.is_pressed:
            if selected>0:
                selected -= 1
            time.sleep(0.15)
        if down.is_pressed:
            if selected < len(currentoptions) - 1:
                selected += 1
            time.sleep(0.15)
        if select.is_pressed:
            song = currentoptions[selected]
            global coverurl
            global response
            global queue
            uri = songlist[song][1]
            sp.start_playback(uris=[uri])
            queue = songlist[song, len(songlist)]
            coverurl = cs["item"]["album"]["images"][0]["url"]
            response = requests.get(coverurl)
            select.wait_for_release()
        if back.is_pressed:
            back.wait_for_release()
            return
        clock.tick(60)

for song in queue:
    if position>= length-500:
        uri = songlist[song][1]
        sp.start_playback(uris = [uri])

def openplaylists():
    global currently_playing
    global song_loaded 
    playlists = sf.playlists() 
    selected = 0
    currentoptions = list(playlists.keys())
    while True:
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
            draw_menu()

            if select.wait_for_press(timeout=0):
                playlist_name = currentoptions[selected]
                playlist_id = playlists[playlist_name]
                select.wait_for_release()
                sf.openplaylist(playlist_id)
    
            if down.wait_for_press(timeout=0) and selected < len(currentoptions)-1:
                selected += 1
                down.wait_for_release()
    
            if up.wait_for_press(timeout=0) and selected > 0:
                selected -= 1
                up.wait_for_release()
                
            if back.wait_for_press(timeout = 0):
                back.wait_for_release()
                return
    
            if action4.wait_for_press(timeout = 0):
                sp.pause_playback()
                currently_playing = False
                action4.wait_for_release()
    
            if action2.wait_for_press(timeout = 0):
                playback = sp.current_playback()
                if playback:
                    current_position = playback["progress_ms"]
                    new_position = max(0, current_position - 15000)
                    sp.seek_track(new_position)
                action2.wait_for_release()
    
            if action3.wait_for_press(timeout = 0):
                playback = sp.current_playback()
                if playback:
                    current_position = playback["progress_ms"]
                    new_position = playback["progress_ms"] + 15000
                    sp.seek_track(new_position)
                action3.wait_for_release()
    
            pygame.display.flip

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
    select.wait_for_release()
    doomrunning = subprocess.Popen(["chocolate-doom"])
    pygame.mouse.set_visible(False)
    select.wait_for_press()

    doomrunning.terminate()
    doomrunning.wait()
    time.sleep(0.5)

    pygame.display.quit()
    pygame.display.init()

    screen = pygame.display.set_mode((480, 360), pygame.FULLSCREEN)
    pygame.mouse.set_visible(False)
    font = pygame.font.SysFont("Helvetica", 26)
    clock = pygame.time.Clock()


def runPSGAME():
    print ("running psgame")

def runGAMEBOY():
    print

def poweroff():
    subprocess.run(["sudo", "poweroff"])


def backlight():
    global backlightvalue
    select.wait_for_release()
    pygame.draw.rect(screen, (40, 40, 40), (2, 0, 240, 360))

    text = font.render("Brightness", False, (255, 255, 255))
    screen.blit(text, (2, 2))

    while True:

        if down.wait_for_press(timeout=0):
            backlightvalue = max(0, backlightvalue - 0.1)
            down.wait_for_release()

        if up.wait_for_press(timeout=0):
            backlightvalue = min(1, backlightvalue + 0.1)
            up.wait_for_release()

        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (2, 40, 220, 16)
        )

        pygame.draw.rect(
            screen,
            (60, 60, 60),
            (3, 42, int(220 * backlightvalue), 12)
        )


        pygame.display.flip()

        if select.is_pressed:
            select.wait_for_release()
            return

        clock.tick(60)


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
    cam.set_controls({"Saturation": 1.05, "Contrast" : 1.05, "Sharpness" : 1.05, "NoiseReductionMode":1, "ExposureValue": 0.7})

    while True:
        array = cam.capture_array()
        img = pygame.image.frombuffer(array.data, (480, 320), "BGR")
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

            img = Image.open(filename)
            img = ImageEnhance.Color(img).enhance(1.1)
            img = ImageEnhance.Contrast(img).enhance(1.05)
            img = ImageEnhance.Sharpness(img).enhance(1.05)
            img = img.filter(ImageFilter.GaussianBlur(0.45))
            img.save(filename, quality=82)

            pic = pygame.image.load(filename)
            pic = pygame.transform.scale(pic, (480, 320))
            screen.blit(pic, (0,0))
            pygame.display.flip()
            pygame.time.wait(5000)
            clock.tick(60)
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

def draw_currently_playing():
    global cs
    cs = sp.current_playback()
    global position
    global length
    if cs:
        track = cs["item"]["name"]
        artist = cs["item"]["artists"][0]["name"]
        position = cs["progress_ms"]
        length = cs["item"]["duration_ms"]
        cp = cs["is_playing"]
        cover = pygame.image.load(BytesIO(response.content))
        covertf = pygame.transform.scale(cover, (120, 120))
        screen.blit(covertf, (340, 150))
        songtext = font.render(track.title(), False, (255, 255, 255))
        artisttext = font.render(artist.title(), False, (230, 230, 230))
        bar = pygame.Rect(300, 120, 200*(position/length), 5)
        pygame.draw.rect(screen, (255, 255, 255), bar)
        screen.blit(songtext, (bar.x, bar.y + 10))
        screen.blit(artisttext, (bar.x, bar.y + 5))
        playimage = pygame.image.load("play.png")
        pauseimage = pygame.image.load("pause.png")
        if cp:
            screen.blit(pauseimage, (340, 200))
        else:
            screen.blit(playimage, (240, 200))

selected = 0

while running:

    draw_menu()
    draw_currently_playing()

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

