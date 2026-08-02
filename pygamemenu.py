from gpiozero import Button
import pygame
pygame.init()

up = Button(5)
down = Button(17)
left = Button(23)
right = Button(25)
select = Button(21)
clock=pygame.time.Clock()

background = (30, 30, 30)
font = pygame.font.SysFont("Helvetica", 26)

screen = pygame.display.set_mode((480, 360), pygame.FULLSCREEN)
running = True

def goback():
    history.pop()

menus = { "Main": 
    {
    "Music": "Music",
    "Games" : "Games",
    "Settings" : "Settings"
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
        text = font.render(item, True, (255, 255, 255))
        screen.blit(text, (entryrects.x + 2, entryrects.y + 2 ) )

selected = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    draw_menu()
    if select.wait_for_press(timeout=0):
        selected = 0
        choice = currentoptions[selected]
        action = menus[currentmenu][choice]
        if isinstance (action, str):
            history.append(choice)
        else:
            action()
        select.wait_for_release()
    if down.wait_for_press(timeout=0) and selected < len(currentoptions)-1:
        selected += 1
        down.wait_for_release()
    if up.wait_for_press(timeout=0) and selected > 0:
        selected -= 1
        up.wait_for_release()
    pygame.display.flip()
    clock.tick(60)


