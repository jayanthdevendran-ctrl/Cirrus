# CIRRUS
<img width="1856" height="770" alt="cirrus v41" src="https://github.com/user-attachments/assets/44a49cf2-a787-4612-947a-dd029395485c" />
Cirrus, the handheld that manages my boredom (and maybe yours too!)

## Basic overview and questions:

### Why does one need a Cirrus?

So, while I cant speak to every single person on this planet, I can speak for myself. Reels is a big distraction for me, who doesnt get sucked into a bit of doomscrolling after all, and along with that, im a massive fan of analog tech, I use an old samsung digicam that my dad worked on while at samsung, I semi-use a fiio mp3 player my brother left behind at home, and I really wish I had a nintendo DS.
The short of it is that, I want an analog device that can occupy my love for videogames (im a big fan of doom64 ever since I got it for free on epicgames), my love for music, and keep me occupied without turning to my phone, since appreciating music is more productive than scrolling, and everything else is less addictive than reels. Besides that its a question of whether I can, this is my first foray into a fully, completed, self contained project, and I want to test my capabilities in design. 

### How long would I take to build this myself?

Right now, as i write this before building it, as part of project review, I can guestimate around 5 hours? Building is not very complicated, besides wiring being a possible issue, but with some creative harnesses and management, 5 for troubleshooting, debugging, assembling, and not counting printing seems pretty fair

### What future updated can I expect to this?

One thing I can see myself doing for sure, is making it a pcb instead, currently the wiring is my most iffy part of the build, plus a pcb would cut down on space massively, removing wiring and breakout boards and help me give it a much smaller profile. Secondly, I'd want to switch to another battery, the current 10k mah battery is massive, and likely overkill.

### Can I build this myself?

Yes! Im a big fan of open-source, everything here is available for anyone to do with as they please, only just give me a share of the profits if this is ever profitable ;)
It isn't very difficult to build, and I support others improving upon my design. It currently does cost around 6432 INR or 68 USD, a pcb can cut this a lot, since a major chunk comes from the display and adafruit DAC which isnt avaiable locally in India and thus is fairly overpriced.

## Functionality:

This is what the main menu currently looks like:
<img width="1600" height="870" alt="image" src="https://github.com/user-attachments/assets/ec99ed3d-d013-46ae-a02e-787f110c39d6" />

It currently has 3 main menus and 1 game with more planned (PS1 hopefully, with MAYBE 007 GOLDENEYE)

1. Music (Obviously)
So, as seen in the main menu, your currently playing is displayed on the right of the screen at all times, which I stole from the ipod gui design. Cirrus currently supports spotify and local playback, spotify playback required you to set authentication details in a .env file, mine are kinda hardcoded onto my device. to do so follow this:
```
SPOTIPY_CLIENT_ID=your_client_id_here
SPOTIPY_CLIENT_SECRET=your_client_secret_here
SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback
```
To get this info set up a spotify developer account and accordingly set the details
The music path:

<img width="1599" height="965" alt="image" src="https://github.com/user-attachments/assets/7b209003-8ebb-4abf-9963-d8a3a27efd32" />
<img width="1600" height="936" alt="image" src="https://github.com/user-attachments/assets/6f6c5e64-7ce0-4bcf-95dd-bb17488eefd7" />


2. Games
Currently I've only got Doom installed on this, currently DOOM 2, before this Chocolate DOOM. The retroarch function is written in firmware, however due to issues with the cores needed (PCSX ReARMed) installation I've halted that and decided to ship the current working Cirrus.

<img width="1600" height="906" alt="image" src="https://github.com/user-attachments/assets/0ce82156-e4bd-4ef2-92bb-477ef0cc94d2" />
<img width="1079" height="630" alt="image" src="https://github.com/user-attachments/assets/c82362e1-4800-4957-91cc-29ad5a9fcf7f" />


3. Camera
Im using a picam 1.3, its not the greatest, so I've done my best to simulate the kind of pictures I get on my samsung vluu i100, it hasnt worked amazingly, all these values can be changed by you, to your liking. Exporting the photos involves removing the sd card from the pi and inserting it into your laptop/desktop as needed, or using SCP via SSH.

<img width="1600" height="823" alt="image" src="https://github.com/user-attachments/assets/a5da2baa-32e9-4d1e-b216-12f8a48147d7" />
<img width="1600" height="911" alt="image" src="https://github.com/user-attachments/assets/65f15513-e54d-4bf5-bed7-32fe81aec6d5" />

## Building the project:
(as not built majority is to be done after initial ship, then filled in during build time)

1. Flash your pi zero 2w using bookworm 32 bit over raspberry pi imager

2. Enable SSH 

3. Add the following in '/boot/firmware/config.txt':
```
dtparam=spi=on

dtoverlay=mipi-dbi-spi-format-parameter,spi0-0,speed=60000000

dtparam=compatible=4in\0panel-mipi-dbi-spi
dtparam=width=480,height=320,width-mm=35,height-mm=28
dtparam=reset-gpio=25,dc-gpio=24

dtparam=write-only,cpha,cpol

dtparam=format=b6x2g6x2r6x2

dtoverlay=ads7846,cs=1,penirq=17,speed=1000000,keep_vref_on=1,swapxy=1,xohms=60
```

4. Install the dependencies and make the required directories:
```
sudo apt update
sudo apt install python3-evdev python3-gpiozero python3-pygame python3-picamera2 \
                 python3-pil chocolate-doom retroarch
pip3 install spotipy requests --break-system-packages
mkdir -p ~/music ~/roms/ps1 ~/roms/gb ~/wads ~/images
```

5. Upload the firmware in the firmware folder in pyscripts
   
6. Set the following in pygamemenu.service:
```
Environment=SDL_VIDEODRIVER=kmsdrm
Environment=SDL_KMSDRM_DEVICE_INDEX=1
```

7. Create an app at the spotify developer dashboard, and set your env as I'd mentioned before like this:
```
SPOTIPY_CLIENT_ID=your_client_id_here
SPOTIPY_CLIENT_SECRET=your_client_secret_here
SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback
```
after putting this in your spotify.env file do
```
chmod 600 spotify.env
```

8. Set `LIBRESPOT_NAME="cirrus"` in `/etc/raspotify/conf`, then `sudo systemctl restart raspotify`.

9. Log in then follow the instructions

10. Run these at boot to set up the menu to autostart 
```
sudo cp ~/pyscripts/pygamemenu.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now pygamemenu
```

11. // to be filled after physical build

## 3d MODEL:
A step, stl and f3d file can all be found in the 3d models folder (f3d since I work on fusion 360)

front:
<img width="1031" height="696" alt="image" src="https://github.com/user-attachments/assets/157c9c89-2c04-4ca7-9411-c66119e25885" />
<img width="902" height="661" alt="image" src="https://github.com/user-attachments/assets/3413bb7c-90f4-480e-8d98-637e00026b4d" />
<img width="937" height="670" alt="image" src="https://github.com/user-attachments/assets/93698f19-4d88-4535-9c85-6b49f3fb468e" />
<img width="906" height="686" alt="image" src="https://github.com/user-attachments/assets/c210b842-33e6-4b82-8dab-c8d40615fc4c" />

back:
<img width="1224" height="793" alt="image" src="https://github.com/user-attachments/assets/30287471-e85b-4c55-aa53-62daacdbe00d" />
<img width="1205" height="789" alt="image" src="https://github.com/user-attachments/assets/a1ffbe5b-1506-4b06-9ca2-f134c0e27d28" />
<img width="1271" height="773" alt="image" src="https://github.com/user-attachments/assets/b05a1970-550d-4bca-92c3-c1edfdcd19d4" />
<img width="1139" height="768" alt="image" src="https://github.com/user-attachments/assets/11746c63-22bd-48b7-b438-77c91a959f5e" />

## Wiring Schematic:
Since ive got no pcb right now this is just a kicad representation of the physical wiring that will be done using jumper cables, I'll use thicker cables for the 5v power.

<img width="914" height="794" alt="image" src="https://github.com/user-attachments/assets/8c02abd8-04ba-46a2-b1a8-4aad9a95947a" />

## Bill Of Materials:
This is the BOM as it stands, it assumes I print everything myself with my ender3, include pricing based on your 3d printer availability. Since forge can avail printing legion I might use that to get around the ender 3's quality bottle necks.

| Item | Quantity | Description | Link | Price (INR) |
|---|---:|---|---|---:|
| NOVA 125785 Battery | 1 | 10,000 mAh 3.7V LiPo Battery | [Robu.in](https://robu.in/product/nova-125785-10000mah-3-7v-lipo-battery-pack/) | 1,132 |
| IP5310 Charge Module | 1 | 5V 3A Type C Boost Converter + Step Up Charging Board | [Robu.in](https://robu.in/product/ip5310-5v-3a-type-c-boost-power-module/) | 106.80 |
| Raspberry Pi 02w | 1 | Dev Board | [Robu.in](https://robu.in/product/raspberry-pi-zero-2-w/) | 1,647 |
| Pi Zero V1.3 Camera Cable | 1 | 0.5mm to 1mm Pi Zero form factor camera cable | [Robu.in](https://robu.in/product/raspberry-pi-zero-v1-3-camera-cable/) | 74 |
| ILI 9488 3.5 inch SPI Display | 1 | 480x320 colour SPI TFT display | [Robu.in](https://robu.in/product/3-5-inch-spi-50pin-tft-lcd-touch-moduleili9488-driver-480x320-color-screen/) | 1,029 |
| Cooling Fan | 1 | 5V mini fan for a Pi | [Robocraze](https://robocraze.com/products/5v-mini-fan-for-raspberry-pi) | 149 |
| Camera Module | 1 | V1.3 5MP Pi Camera Module | [Robocraze](https://robocraze.com/products/raspberry-pi-5mp-camera-module) | 449 |
| Push Buttons | 20 | 2 × 10-piece packs of 6x6x5mm tactile push buttons | [Robocraze](https://robocraze.com/products/4-pins-dip-momentary-square-tactile-push-button-switch-10-pieces-6x6x5mm) | 32 |
| Vero Board | 1 | 4x3 inch prototyping board | [Robocraze](https://robocraze.com/products/vero-board-3-x4) | 28 |
| 3D Print | 1 | ABS 3D print of the frame + buttons | [Robu.in](https://robu.in/product/3d-printing-service1/) | 708 |
| Adafruit TLV320DAC3100 | 1 | I2S DAC with built-in amplifier and direct headphone stereo output | [Robu.in](https://robu.in/product/adafruit-tlv320dac3100-i2s-dac-with-headphone-and-speaker-out/) | 1,109 |
| M3 Screws | 20 | Screws to mount everything else, plus extras | [OnlyScrews](https://onlyscrews.in/products/phillips-pan-head-m3-x-12mm-pack-of-20) | 40 |
| M2 Screws | 10 | Screws for Pi, charging board and amp | [OnlyScrews](https://onlyscrews.in/products/m2-x-6mm-phillips-pan-head-ss-304-screw) | 20 |
| **TOTAL** | **40** | | | **6,523.80** |

<img width="1127" height="454" alt="image" src="https://github.com/user-attachments/assets/c977bc31-a5ad-4d9f-b447-aa36d3bd640b" />

# C'est Fini
and thats it I guess, you can ofcourse make any changes as you wish and adapt my design as you wish, the code is around 60 percent me 40 percent claude, feel free to email me at : jayanthdevendran@gmail.com
Its been a blast working on this project, my first hackclub submission hopefully the first of many, since I will be turning 18 soon. Best wishes to anyone reading this, hope you live long fulfilling lives. 










