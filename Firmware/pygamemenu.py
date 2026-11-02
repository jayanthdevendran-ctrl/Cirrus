import sys
import traceback
def _log_crash(exc_type, exc, tb): #claude
    # writes any startup/runtime crash to a file so we can see why the service died
    try:
        with open("/home/cirrus/cirrus_crash.log", "a") as f:
            f.write("\n--- crash ---\n")
            f.write("".join(traceback.format_exception(exc_type, exc, tb)))
    except Exception:
        pass
    sys.__excepthook__(exc_type, exc, tb)
sys.excepthook = _log_crash

from gpiozero import Button
from gpiozero import PWMLED
import os
import glob
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
select = Button(22)
back = Button(0)

clock=pygame.time.Clock()
IMAGE_DIR = "/home/cirrus/images"
os.makedirs(IMAGE_DIR, exist_ok=True)

background = (30, 30, 30)
ACCENT = (120, 200, 255)          
ACCENT_TEXT = (15, 25, 35)        
TRACK_COLOR = (65, 65, 65)        

def make_fonts():
    global font, list_font, small_font, np_font
    font = pygame.font.SysFont("Helvetica", 26)
    list_font = pygame.font.SysFont("Helvetica", 18)
    small_font = pygame.font.SysFont("Helvetica", 18)
    np_font = pygame.font.SysFont("Helvetica", 22)  
make_fonts()

screen = pygame.display.set_mode((480, 360), pygame.FULLSCREEN)
running = True
pygame.mouse.set_visible(False)

# ---------- layout ---------- Claude created variables for all the hardcoded values i placed
# The visible area of your display looks like 480x320 (the camera preview is 480x320 too),
# so everything is laid out inside SCREEN_H. If your screen really shows all 360 rows,
# change this to 360.
SCREEN_W = 480
SCREEN_H = 320

LIST_ROW_H = 24
visible_songs = SCREEN_H // LIST_ROW_H   # 13 rows
LEFT_W = 240

ICON_SIZE = 32
NP_LINE_H = np_font.get_linesize()
# right half, top to bottom: cover, progress bar, play/pause icon, song name, artist
_below_cover = 6 + 4 + 6 + ICON_SIZE + 4 + 2 * NP_LINE_H + 2
COVER_SIZE = min(230, SCREEN_H - 4 - _below_cover)       # biggest square that fits everything
COVER_X = 240 + (240 - COVER_SIZE) // 2
COVER_Y = 4
BAR_Y = COVER_Y + COVER_SIZE + 6
ICON_Y = BAR_Y + 4 + 6
NAME_Y = ICON_Y + ICON_SIZE + 4
ARTIST_Y = NAME_Y + NP_LINE_H
PANEL_CENTER_X = 360
TEXT_X = 245
TEXT_W = 230

def goback():
    history.pop()

currently_playing = False
cover = None
last_cover_url = None
song_loaded = False


# ---------- helpers ---------- claude
def draw_scroll_text(text, fnt, color, x, y, max_w, epoch, scroll=True):
    """Draw text clipped to max_w. If it's too long (and scroll=True) it marquee-scrolls."""
    surf = fnt.render(text, True, color)
    h = surf.get_height()
    prev_clip = screen.get_clip()
    screen.set_clip(pygame.Rect(x, y, max_w, h))
    if surf.get_width() <= max_w or not scroll:
        screen.blit(surf, (x, y))
    else:
        gap = 50
        period = surf.get_width() + gap
        t = pygame.time.get_ticks() - epoch
        delay = 1000
        offset = 0 if t < delay else ((t - delay) * 0.04) % period
        screen.blit(surf, (x - offset, y))
        screen.blit(surf, (x - offset + period, y))
    screen.set_clip(prev_clip)


def draw_message(text):
    screen.fill(background)
    surf = font.render(text, True, (255, 255, 255))
    screen.blit(surf, surf.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2)))
    pygame.display.flip()


def draw_divider():
    pygame.draw.rect(screen, ACCENT, (LEFT_W + 2, 0, 2, SCREEN_H))


# ---------- volume ----------claude
MIXER_CONTROL = "Master"      # change if `amixer scontrols` shows e.g. "PCM" or "Headphones"
current_volume = 50

def get_volume():
    try:
        pb = sp.current_playback()
        return int(pb["device"]["volume_percent"])
    except Exception:
        return current_volume


def apply_volume(v):
    try:
        if localmusic.is_active():
            if hasattr(localmusic, "set_volume"):
                localmusic.set_volume(v)
            else:
                subprocess.run(["amixer", "sset", MIXER_CONTROL, f"{v}%"], capture_output=True)
        else:
            try:
                sp.volume(v, device_id=sf.get_device_id())
            except Exception:
                subprocess.run(["amixer", "sset", MIXER_CONTROL, f"{v}%"], capture_output=True)
    except Exception as err:
        print("volume change failed:", err)


def volume():
    global current_volume
    select.wait_for_release()
    current_volume = get_volume()
    last_applied = current_volume
    last_apply_time = 0
    while True:
        changed = False
        if (up.is_pressed or right.is_pressed) and current_volume < 100:
            current_volume = min(100, current_volume + 5)
            changed = True
            time.sleep(0.12)
        if (down.is_pressed or left.is_pressed) and current_volume > 0:
            current_volume = max(0, current_volume - 5)
            changed = True
            time.sleep(0.12)
        now = time.time()
        if changed and now - last_apply_time > 0.3:     #prevent api spamming, this is new, claude caught this
            apply_volume(current_volume)
            last_applied = current_volume
            last_apply_time = now

        screen.fill(background)
        title = font.render("Volume", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(SCREEN_W // 2, 70)))
        bar_x, bar_w, bar_y, bar_h = 60, 360, 140, 26
        pygame.draw.rect(screen, TRACK_COLOR, (bar_x, bar_y, bar_w, bar_h))
        pygame.draw.rect(screen, ACCENT, (bar_x, bar_y, int(bar_w * current_volume / 100), bar_h))
        pct = font.render(f"{current_volume}%", True, ACCENT)
        screen.blit(pct, pct.get_rect(center=(SCREEN_W // 2, 210)))
        pygame.display.flip()

        if back.is_pressed or select.is_pressed:
            (back if back.is_pressed else select).wait_for_release()
            break
        clock.tick(60)
    if current_volume != last_applied:
        apply_volume(current_volume)


# ---------- liked songs (paged) ---------- new function that goes in the openlikedsongs() function that i wrote claude did this
LIKED_BATCH = 200

def fetch_liked(offset, count=LIKED_BATCH):
    songs = []
    total = None
    got = 0
    while got < count:
        res = sp.current_user_saved_tracks(limit=min(50, count - got), offset=offset + got)
        total = res.get("total", 0)
        items = res.get("items", [])
        if not items:
            break
        for it in items:
            t = it.get("track")
            if t:
                songs.append((t["name"], t["uri"]))
        got += len(items)
        if offset + got >= total:
            break
    return songs, total


def openlikedsongs():
    global selected
    global cover
    global currentoptions
    global scrolloffset
    select.wait_for_release()
    draw_message("Loading...")
    try:
        songs, total = fetch_liked(0)
    except Exception as err:
        print("could not load liked songs:", err)
        draw_message("Load failed")
        time.sleep(1.5)
        return
    currentoptions = [s[0] for s in songs]
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

        if total and len(songs) < total and selected >= len(songs) - 1:
            draw_message("Loading more...")
            try:
                more, total = fetch_liked(len(songs))
                songs.extend(more)
                currentoptions = [s[0] for s in songs]
            except Exception as err:
                print("could not load more:", err)
                total = len(songs)

        if select.is_pressed:
            try:
                sf.ensure_device()
                uris = [s[1] for s in songs[selected:selected+50]]
                sp.start_playback(uris=uris, device_id=sf.get_device_id())
                cover = getcover()
            except Exception as err:
                print("playback failed:", err)
            select.wait_for_release()
        if back.is_pressed:
            back.wait_for_release()
            return
        if selected < scrolloffset:
            scrolloffset = selected
        if selected >= scrolloffset + visible_songs:
            scrolloffset = selected - visible_songs + 1
        drawmenugeneral(currentoptions)
        draw_currently_playing()
        pygame.display.flip()
        clock.tick(60)


def openlocal():
    tracks = localmusic.list_tracks()
    if not tracks:
        print("no tracks in", localmusic.MUSIC_DIR)
        return
    name = choose_from(tracks.keys())
    if name is not None:
        localmusic.play_name(name)

def opengames(): #was a placeholder to see if games were being opened, now prints nothing, used to print game menu opened to troubleshoot
    print

buttons = {"up": up, "down": down, "left": left, "right": right,
           "action1": action1, "action2": action2, "action3": action3, "action4": action4,
           "select": select, "back": back}


def run_external(cmd, keymap):
    global clock, screen
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
    make_fonts()
    clock = pygame.time.Clock()
    return result


def choose_from(options):
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


def poweroff():
    select.wait_for_release()
    try:
        if localmusic.is_active():
            localmusic.pause()
        else:
            sf.pause()
    except Exception:
        pass
    draw_message("Shutting down...")
    commands = (
        ["sudo", "-n", "systemctl", "poweroff"],
        ["sudo", "-n", "poweroff"],
        ["sudo", "-n", "shutdown", "-h", "now"],
        ["systemctl", "poweroff"],
    )
    for cmd in commands:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
        except Exception as err:
            print("shutdown error:", err)
            continue
        if result.returncode == 0:
            time.sleep(60)
            return
        print("shutdown command failed:", cmd, result.stderr.strip())
    draw_message("Shutdown failed")
    time.sleep(2)


# ---------- camera ---------- again claude put my hardcoded values in neat little variables, this is very helpful
CAM_CONTROLS = {"Saturation": 1.05, "Contrast" : 1.05, "Sharpness" : 1.05,
                "NoiseReductionMode": 1, "ExposureValue": 0.7}

def take_photo(cam, picconfig):
    """Capture a full-size still, enhance it, show it briefly, then restart the preview."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{IMAGE_DIR}/{timestamp}.jpg"
    cam.stop()
    cam.configure(picconfig)
    cam.start()
    cam.capture_file(filename)
    cam.stop()

    img = Image.open(filename)
    img = ImageEnhance.Color(img).enhance(1.1)
    img = ImageEnhance.Contrast(img).enhance(1.05)
    img = ImageEnhance.Sharpness(img).enhance(1.05)
    img = img.filter(ImageFilter.GaussianBlur(0.45))
    img.save(filename, quality=82)

    pic = pygame.image.load(filename)
    pic = pygame.transform.scale(pic, (480, 320))
    screen.blit(pic, (0, 0))
    pygame.display.flip()

    # show the photo for 2 seconds (any of back / action1 skips it)
    end = pygame.time.get_ticks() + 2000
    while pygame.time.get_ticks() < end:
        if back.is_pressed or action1.is_pressed:
            (back if back.is_pressed else action1).wait_for_release()
            break
        clock.tick(30)

    cam.configure("preview")
    cam.start()
    cam.set_controls(CAM_CONTROLS)


def opencam():
    select.wait_for_release()
    cam = Picamera2()
    try:
        cam.preview_configuration.main.size = (480, 320)
        cam.preview_configuration.main.format = "RGB888"
        picconfig = cam.create_still_configuration(main = {"size": (2592, 1944)})
        cam.configure("preview")
        cam.start()
        cam.set_controls(CAM_CONTROLS)
        screen.fill((0, 0, 0))

        while True:
            array = cam.capture_array()
            # picamera2's "RGB888" is stored as B,G,R in memory -> flip channels or skin looks blue , id written it as RGB and was so confused by my skin being blue, but claude caught this
            frame = array[:, :, ::-1].copy()   # flip BGR->RGB (copy makes it contiguous)
            h, w = frame.shape[:2]
            img = pygame.image.frombuffer(frame.data, (w, h), "RGB")
            screen.blit(img, (0, 0))
            pygame.display.flip()
            if back.is_pressed:
                back.wait_for_release()
                break
            if action1.is_pressed:
                action1.wait_for_release()
                try:
                    take_photo(cam, picconfig)
                except Exception as err:
                    print("photo failed:", err)
                    try:
                        cam.stop()
                        cam.configure("preview")
                        cam.start()
                    except Exception:
                        pass
    finally:
        # releases camera from holding the canvas - again thank god for claude it caught this i was so confused why cam wouldnt open a 2nd time
        try:
            cam.stop()
        except Exception:
            pass
        try:
            cam.close()
        except Exception:
            pass


# ---------- gallery ---------- claude wrote this whole gallery part 
_gallery_cache = {}

def load_gallery_image(path):
    cached = _gallery_cache.get(path)
    if cached is not None:
        return cached
    try:
        img = Image.open(path)
        img.draft("RGB", (SCREEN_W, SCREEN_H))      # fast JPEG decode at reduced size
        img = img.convert("RGB")
        img.thumbnail((SCREEN_W, SCREEN_H))
        surf = pygame.image.fromstring(img.tobytes(), img.size, "RGB")
    except Exception as err:
        print("could not load", path, err)
        return None
    _gallery_cache[path] = surf
    if len(_gallery_cache) > 8:
        _gallery_cache.pop(next(iter(_gallery_cache)))
    return surf


def opengallery():
    # left/right = prev/next, back = exit
    select.wait_for_release()
    files = []
    for pattern in ("*.jpg", "*.jpeg", "*.png"):
        files += glob.glob(os.path.join(IMAGE_DIR, pattern))
    files = sorted(files, reverse=True)
    index = 0
    while True:
        screen.fill((0, 0, 0))
        if not files:
            msg = font.render("No photos yet", True, ACCENT)
            screen.blit(msg, msg.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2)))
        else:
            shown = load_gallery_image(files[index])
            if shown is not None:
                screen.blit(shown, shown.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2)))
            label = small_font.render(f"{index + 1} / {len(files)}", True, ACCENT)
            pygame.draw.rect(screen, (0, 0, 0), (0, SCREEN_H - 22, label.get_width() + 12, 22))
            screen.blit(label, (6, SCREEN_H - 20))
        pygame.display.flip()

        if right.is_pressed and files:
            index = (index + 1) % len(files)
            right.wait_for_release()
        if left.is_pressed and files:
            index = (index - 1) % len(files)
            left.wait_for_release()
        if back.is_pressed:
            back.wait_for_release()
            return
        clock.tick(30)


menus = { "Main":
{
"Music": "Music",
"Games" : "Games",
"Gallery" : opengallery,
"Settings" : "Settings",
"Camera" : opencam,
"Power Off" : poweroff
},
"Music" : {
"Liked Songs": openlikedsongs,
#"Playlists": openplaylists, feature intended for later, need to build first
#"Search": opensearch, feature intended for later, need to build first
"Local Music": openlocal,
"Back": goback,
},

"Games" : {
"Doom": runDOOM,
#"PS1": runPSGAME, feature intended for later, need to build first
#"Game Boy": runGAMEBOY, feature intended for later, need to build first
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
            pygame.draw.rect(screen, ACCENT, (entryrects.x, entryrects.y, 5, entryrects.height))
        else:
            pygame.draw.rect(screen, (40, 40, 40), entryrects)
        text = font.render(item, False, (255, 255, 255))
        screen.blit(text, (entryrects.x + 10, entryrects.y + 2 ) )
    draw_divider()

list_last_selected = None
list_epoch = 0

def drawmenugeneral(options):
    # selected row = light blue; only the selected row scrolls if its name is too long, claude added scrolling if name was too long
    global list_last_selected, list_epoch
    if selected != list_last_selected:
        list_last_selected = selected
        list_epoch = pygame.time.get_ticks()
    screen.fill(background)
    pygame.draw.rect(screen, (40, 40, 40), (2, 0, LEFT_W, 360))
    visibleoptions = currentoptions[scrolloffset: scrolloffset + visible_songs]
    for index, item in enumerate(visibleoptions):
        entryrects = pygame.Rect(2, index * LIST_ROW_H, LEFT_W, LIST_ROW_H)
        is_sel = (index + scrolloffset == selected)
        pygame.draw.rect(screen, ACCENT if is_sel else (40, 40, 40), entryrects)
        text_y = entryrects.y + (LIST_ROW_H - list_font.get_height()) // 2
        draw_scroll_text(str(item), list_font,
                         ACCENT_TEXT if is_sel else (255, 255, 255),
                         entryrects.x + 4, text_y, LEFT_W - 8, list_epoch, scroll=is_sel)
    draw_divider()


def load_cover(url):
    if not url:
        return None
    try:
        response = requests.get(url, timeout=5)
        img = pygame.image.load(BytesIO(response.content))
        return pygame.transform.smoothscale(img, (COVER_SIZE, COVER_SIZE))
    except Exception:
        return None


def getcover():
    try:
        cs = sp.current_playback()
        return load_cover(cs["item"]["album"]["images"][0]["url"])
    except Exception:
        return None

playimage = pygame.transform.smoothscale(pygame.image.load("play.png"), (ICON_SIZE, ICON_SIZE))
pauseimage = pygame.transform.smoothscale(pygame.image.load("pause.png"), (ICON_SIZE, ICON_SIZE))

np_last_name = None
np_epoch = 0

def draw_now_playing_panel(cover_surf, name, artist, is_playing, progress, duration):
    # right half: cover -> progress bar -> play/pause -> song name -> artist
    global np_last_name, np_epoch
    if name != np_last_name:
        np_last_name = name
        np_epoch = pygame.time.get_ticks()
    if cover_surf is not None:
        screen.blit(cover_surf, (COVER_X, COVER_Y))
    else:
        pygame.draw.rect(screen, (60, 60, 60), (COVER_X, COVER_Y, COVER_SIZE, COVER_SIZE))

    # progress bar (track + light-blue fill)
    pygame.draw.rect(screen, TRACK_COLOR, (COVER_X, BAR_Y, COVER_SIZE, 4))
    if duration and duration > 0:
        filled = int(COVER_SIZE * min(1.0, max(0.0, progress / duration)))
        pygame.draw.rect(screen, ACCENT, (COVER_X, BAR_Y, filled, 4))

    icon = pauseimage if is_playing else playimage
    screen.blit(icon, (PANEL_CENTER_X - ICON_SIZE // 2, ICON_Y))
    draw_scroll_text(name, np_font, (255, 255, 255), TEXT_X, NAME_Y, TEXT_W, np_epoch)
    if artist:
        draw_scroll_text(artist, np_font, (200, 200, 200), TEXT_X, ARTIST_Y, TEXT_W, np_epoch)


def draw_currently_playing():
    global cover
    global last_cover_url
    if localmusic.is_active():
        song = localmusic.get_current()
        if song is None:
            return
        draw_now_playing_panel(None, song["name"].title(), "", song["is_playing"],
                               song["progress"], song["duration"])
        return
    song = sf.get_current_song()
    if song is None:
        return
    if song["cover"] != last_cover_url:
        last_cover_url = song["cover"]
        cover = load_cover(last_cover_url)
    draw_now_playing_panel(cover, song["name"].title(), song["artists"].title(),
                           song["is_playing"], song["progress"], song["duration"])


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

    if back.is_pressed:
        back.wait_for_release()
        if len(history) > 1:
            history.pop()
            selected = 0

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