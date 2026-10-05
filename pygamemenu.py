from gpiozero import Button
from gpiozero import PWMLED
import os
import subprocess
import time
from picamera2 import Picamera2
from datetime import datetime
from PIL import Image, ImageEnhance, ImageFilter
import spotfunctions as sf
import games
import localmusic
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
        scope = scope,
        cache_path = sf.CACHE_PATH,
        open_browser = False
    )
)

import pygame
pygame.init()
up = Button(14)
down = Button(15)
left = Button(4)
right = Button(20)
action1 = Button(26)
action2 = Button(13)
action3 = Button(6)
action4 = Button(5)
select = Button(27)
back = Button(0)

clock=pygame.time.Clock()
os.makedirs("/home/cirrus/images", exist_ok=True)   # ADDED: camera crashes if this is missing

background = (30, 30, 30)
font = pygame.font.SysFont("Helvetica", 26)

screen = pygame.display.set_mode((480, 360), pygame.FULLSCREEN)
running = True
pygame.mouse.set_visible(False)

def goback():
    history.pop()

currently_playing = False
cover = None              # ADDED: was undefined until a song was started -> NameError in draw_currently_playing()
last_cover_url = None     # ADDED
song_loaded = False

visible_songs = 8
def openlikedsongs():
    global selected
    global cover
    global currentoptions   # ADDED: so drawmenugeneral() can see the song list
    global scrolloffset     # ADDED
    select.wait_for_release()   # ADDED: the press that opened this screen would otherwise start song #1
    songlist = sf.liked_songs()
    currentoptions = list(songlist.keys())
    scrolloffset = 0
    selected = 0
    while True:
        if up.is_pressed:
            if selected>0:
                selected -= 1
            time.sleep(0.15)
        if down.is_pressed:
            if selected < len(currentoptions) - 1:
                selected += 1
            time.sleep(0.15)
        if select.is_pressed:
            # CHANGED: was 1 start_playback + one add_to_queue API call per remaining song
            # (hundreds of calls -> Spotify rate-limits you and the UI freezes). One call now.
            try:
                sf.ensure_device()
                uris = [songlist[s][1] for s in currentoptions[selected:selected+50]]
                sp.start_playback(uris=uris, device_id=sf.get_device_id())
                cover = getcover()
            except Exception as err:
                print("playback failed:", err)
            select.wait_for_release()
        if back.is_pressed:
            back.wait_for_release()
            return
        # ADDED: this screen never drew anything
        if selected < scrolloffset:
            scrolloffset = selected
        if selected >= scrolloffset + visible_songs:
            scrolloffset = selected - visible_songs + 1
        drawmenugeneral(currentoptions)
        draw_currently_playing()
        pygame.display.flip()
        clock.tick(60)


def openplaylists():
    print

def opensearch():
    print

def openlocal():
    # CHANGED: was an unused stub (bare `print`). Now browses ~/music and starts playback.
    tracks = localmusic.list_tracks()
    if not tracks:
        print("no tracks in", localmusic.MUSIC_DIR)
        return
    name = choose_from(tracks.keys())
    if name is not None:
        localmusic.play_name(name)

def opengames():
    print

buttons = {"up": up, "down": down, "left": left, "right": right,
           "action1": action1, "action2": action2, "action3": action3, "action4": action4,
           "select": select, "back": back}


def run_external(cmd, keymap):
    # ADDED. The old runDOOM launched Doom while pygame still owned the screen (kmsdrm allows only
    # one owner, so Doom couldn't draw) and gave it no input. Flow now:
    # pause music -> release display -> run game with GPIO->keyboard bridge -> take display back.
    global font, clock, screen
    select.wait_for_release()
    try:
        if localmusic.is_active():
            localmusic.pause()
        else:
            sf.pause()
    except Exception:
        pass
    pygame.display.quit()
    result = games.run(cmd, buttons, keymap)
    time.sleep(0.5)
    pygame.display.init()
    screen = pygame.display.set_mode((480, 360), pygame.FULLSCREEN)
    pygame.mouse.set_visible(False)
    font = pygame.font.SysFont("Helvetica", 26)
    clock = pygame.time.Clock()
    return result


def choose_from(options):
    # ADDED: simple scrolling picker for ROM lists. Returns the chosen name or None (BACK).
    global selected, scrolloffset, currentoptions
    saved = (selected, scrolloffset, currentoptions)
    currentoptions = list(options)
    selected, scrolloffset = 0, 0
    select.wait_for_release()
    choice = None
    while True:
        if up.is_pressed and selected > 0:
            selected -= 1
            time.sleep(0.15)
        if down.is_pressed and selected < len(currentoptions) - 1:
            selected += 1
            time.sleep(0.15)
        if select.is_pressed and currentoptions:
            choice = currentoptions[selected]
            select.wait_for_release()
            break
        if back.is_pressed:
            back.wait_for_release()
            break
        if selected < scrolloffset:
            scrolloffset = selected
        if selected >= scrolloffset + visible_songs:
            scrolloffset = selected - visible_songs + 1
        drawmenugeneral(currentoptions)
        pygame.display.flip()
        clock.tick(60)
    selected, scrolloffset, currentoptions = saved
    return choice


def runDOOM():
    run_external(games.doom_command(), games.KEYMAP_DOOM)


def run_retroarch(system):
    roms = games.list_roms(system)
    if not roms:
        print("no ROMs in", games.ROM_DIRS[system])
        return
    name = choose_from(roms.keys())
    if name is not None:
        run_external(games.retroarch_command(system, roms[name]), games.KEYMAP_RETROARCH)


def runPSGAME():
    run_retroarch("ps1")

def runGAMEBOY():
    run_retroarch("gb")

def poweroff():
    subprocess.run(["sudo", "poweroff"])


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
"Local Music": openlocal,
"Back": goback,
},

"Games" : {
"Doom": runDOOM,
"PS1": runPSGAME,
"Game Boy": runGAMEBOY,
"Back": goback
},

"Settings" : {
"Volume": volume,
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

def drawmenugeneral(options):
    screen.fill(background)
    pygame.draw.rect(screen, (40, 40, 40), (2, 0, 240, 360))
    visibleoptions = currentoptions[scrolloffset: scrolloffset + visible_songs]
    for index, item in enumerate(visibleoptions):
        entryrects = pygame.Rect(2, index * 30, 240, 30)
        if index + scrolloffset == selected:
            pygame.draw.rect(screen, (80, 80, 80), entryrects)
        else:
            pygame.draw.rect(screen, (40, 40, 40), entryrects)
        text = font.render(item, False, (255, 255, 255))
        screen.blit(text, (entryrects.x + 2, entryrects.y + 2 ) )


def load_cover(url):
    # ADDED: download + shrink (raw covers are 640x640 and would swamp a 480x360 screen)
    if not url:
        return None
    try:
        response = requests.get(url, timeout=5)
        img = pygame.image.load(BytesIO(response.content))
        return pygame.transform.smoothscale(img, (120, 120))
    except Exception:
        return None


def getcover():
    # CHANGED: current_playback() is often None/stale right after start_playback(); don't crash
    try:
        cs = sp.current_playback()
        return load_cover(cs["item"]["album"]["images"][0]["url"])
    except Exception:
        return None

playimage = pygame.image.load("play.png")
pauseimage = pygame.image.load("pause.png")

def draw_currently_playing():
    global cover
    global last_cover_url
    if localmusic.is_active():           # ADDED: local playback takes over this same display area
        song = localmusic.get_current()
        if song is None:
            return
        songtext = font.render(song["name"].title(), False, (255, 255, 255))
        screen.blit(songtext, (300, 120 + 10))
        if song["duration"] > 0:
            progress = 200 * (song["progress"] / song["duration"])
            pygame.draw.rect(screen, (255, 255, 255), (300, 120, progress, 5))
        screen.blit(pauseimage if song["is_playing"] else playimage, (240, 200))
        return
    song = sf.get_current_song()
    if song is None:                     # nothing playing
        return
    if song["cover"] != last_cover_url:  # ADDED: refresh art whenever the track changes
        last_cover_url = song["cover"]
        cover = load_cover(last_cover_url)
    if cover is not None:
        screen.blit(cover, (340, 150))

    songtext = font.render(song["name"].title(), False, (255, 255, 255))
    artisttext = font.render(song["artists"].title(), False, (230, 230, 230))
    screen.blit(songtext, (300, 120 + 10))
    screen.blit(artisttext, (300, 120 + 5))

    if song["duration"] > 0:
        progress = 200*(song["progress"]/song["duration"])
        pygame.draw.rect(screen, (255, 255, 255), (300, 120, progress, 5))
    if song["is_playing"]:
        screen.blit(pauseimage, (240, 200))
    else:
        screen.blit(playimage, (240, 200))


selected = 0
scrolloffset = 0

while running:
    if selected < scrolloffset:
        scrolloffset = selected
    if selected >= scrolloffset + visible_songs:
        scrolloffset = selected - visible_songs + 1
    
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

    try:
        if action1.is_pressed:
            if localmusic.is_active():                 
                song = localmusic.get_current()
                localmusic.pause() if (song and song["is_playing"]) else localmusic.resume()
            else:
                song = sf.get_current_song()
                if song and song["is_playing"]:
                    sf.pause()
                else:
                    sf.ensure_device()
                    sf.resume()
            action1.wait_for_release()
        if action2.is_pressed:
            localmusic.next_track() if localmusic.is_active() else sf.next_song()
            action2.wait_for_release()
        if action3.is_pressed:
            localmusic.previous_track() if localmusic.is_active() else sf.previous_song()
            action3.wait_for_release()
    except Exception as err:
        print("media control failed:", err)

    pygame.display.flip()
    clock.tick(60)

