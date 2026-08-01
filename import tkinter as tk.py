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

pygame.init()
screen = pygame.display.set_mode((480, 360), pygame.FULLSCREEN)
running = True

main = ["music", "games", "Settings", "quit"]
history = [main]

def goback():
    history.pop()

menus = { "Main":{"Music" : {
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
}

currentmenu = history[-1]
currentoptions = menus[currentmenu].keys()
def clearscreen():
    screen.fill((240,240,240))
    pygame.draw.rect(screen, (30, 30, 30), (0,0,480,30))

def draw_menu():
    global currentmenu
    currentmenu = history[-1]
    screen.fill(background)
    pygame.draw.rect(screen, (40, 40, 40), (2, 0, 240, 320))
    for index, item in enumerate(currentoptions):
        entryrects = pygame.Rect(2, index * 30, 240, 10)
        pygame.rect(screen, (40, 40, 40), entryrects)
        text = font.render(item, True, ("255, 255, 255"))
        screen.blit(text, (entryrects.x + 2, entryrects.y + 2 ) )

selected = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    draw_menu()
    if select.is_pressed:
        choice = currentoptions[selected]
        history.append[choice]
    if down.is_pressed:
        selected += 1
    if up.is_pressed:
        selected -= 1



pygame.display.flip()
clock.tick(60)