---
title: "Cirrus"
author: "goosegt"
description: "A mp3 player that streams music from spotify, as well as a retro video game console, play classics like DOOM, GranTurismo and other PS1 titles; all the while listening to your favourite beats."
created_at: "2026-08-22"
---

# 2026-11-02: Readme

**Total time spent: 4 hours**

Spent 2 hours writing my readme, used a lot of inspiration (copied all his subheadings) from a friend at : https://github.com/Diamond0608/Little-Helper/tree/main
he submitted for beest and got approved so I thought itd give me an idea.
took screen shots of everything, took photos of the screen couldnt really minimize glare though, updated my BOM with screws, wrote the actual readme, part of it is incomplete since I need to build this thing to fill in the rest besides that its all been completed mainly took so long since I ran into some bugs while working on it, fixed an issue with doom not launching due to an incompatibility with multiple versions of DOOM, since ive currently got Freedoom, chocolatedoom, and ive linked a doom.wad, I've been working for around 4 hours most of that was debugging doom, and uploading all my files, and recollecting all the work I've done before, especially since I needed to track down old commands that I'd run
![image.png](https://cdn.hackclub.com/01a19db9-7192-74cd-9e5a-82984dbfaa6d/image.png)

# 2026-11-02: Finished wiring diagram

**Total time spent: 130 minutes**

Finished rest of the code didnt lapse it though cuz i took some ai help.
Used kicad to finish my wiring diagram formally. Since there was no available symbol for any of the breakout boards nor the pi, because obviously kicad is for pcbs and not wiring diagrams, I made custom symbols 
![image.png](https://cdn.hackclub.com/01a19db0-d423-702b-ace1-b7cbd6b5e128/image.png)
for example this for the pi
then i just routed it best i could to keep it clean while preserving all my connections
![image.png](https://cdn.hackclub.com/01a19db1-8aca-78b8-a363-a9f39cbb7275/image.png)
i copied all my connections from this rough diagram i did here 
![connection.png](https://cdn.hackclub.com/01a19db1-e185-7cff-8256-f458f5e1cdbb/connection.png) 
and it worked out

# 2026-10-10: LAST OF FIRMWARE

**Total time spent: 20 minutes**

So, had some remaining stuff left over, as well as some impulse adds, my now playing half of the screen was all messed up
![image.png](https://cdn.hackclub.com/01a12641-1cbf-7369-ab8c-a19594b36cd6/image.png)
here it is, so had to change a lot of pixel values to make it look right. 
Added some accent colours cuz it looked so boring earlier, im using lightblue because the project is called cirrus so cirrus = cloud = sky = blue. The last parts I had claude do it, ive commented wherever claude did the work in my menu file, cuz i have JEE Mains (college entrance exam) mock test tomorrow and I havent studied.
Im itching to build cirrus, i predict lots of issues during the build stage, but yeah lets hope.
Added features :
Gallery
1. song names scroll if theyre too long to fit on screen

2. placement of different things fixed
3. crash log
4. fixed a bug where camera wouldnt hand over the screen claude caught this
5. some other small bugs

# 2026-10-10: Code Log

**Total time spent: 20 hours 50 minutes**

A lot of my code was explained in logs that are now deleted, so I thought I'll put a quick write up with some notes about it.
Additionally since I wasnt aware about hackatime hours needing to be logged, all my vsc hours are gonna be logged in this dev log

1. Initial stage : I used a few different drivers, and change between display libraries aswell, currently using pygame, but I started with TKinter and something called luma.LCD, most of this early work is logged, it involved creating the first skeleton of my menu code, essentially a continuously running loop that would print a list of options. The options are taken from a dictionary that shows the menu "tree" i guess id say, 
![image.png](https://cdn.hackclub.com/01a125d4-f946-7398-8cb2-d37d6f06620d/image.png)
since its a dictionary, each submenu corresponds to a function that performs that give capability, allowing some amount of modularity. Originally, this was a list, but when you print <listvariable> the things within the list are printed not the name of the list itself, hence the switch to dictionaries.

2. Second stage, biggest one. So this was the bulk of my work, it involved most of my coding, all done manually btw. So heres where i implemented stacks to keep a history of which menus cirrus is in, and when you leave a menu, id just pop the stack, and throughout all this, the menu function is drawing whichever the highest element in the stack is. so when you leave the menu, the last element is popped, hence the highest element is now 1 menu before. little confusing over text but its like a file path e.g : C:/Downloads/Games/Sims/Warthunder
so when i leave a menu, the element "Warthunder" is popped, so now the highest is "Sims"
, now the menu function sees this and is like OH i gotta write whatever is given in "Sims", now you leave again, "Sims" is removed and the highest is "Games", so now the menu sees its Games and is like i gotta print whatever is in Gaames, which could be : 'Sims', "RPGS", "FPS", "Racing", etc.
After this I was just building the separate functions, the camera one was quite easy, most of that is available online, had to read through some docs, then adjust some values to get the kind of aesthetic i wanted. The part I've decided right now thats a little weird is that I dont want a gallery, i want this to be a kinda live in the moment device, so once you take a picture, the whole system is paused to let you see it for a second, and after that you cant see it again until you export.
Besides this I put in all the music functions, this was a matter of choosing which features i wanted from spotify, then checking the docs, and seeing how to return the data i required, also easy, just long boring work.
The hardest part was making the Liked songs menu, i built a scrolling menu for this since the original menu wasnt, additionally, it runs within its own menu, since now i need the individual song texts to scroll, besides this it was a repeat of the original menu code

3. Final stage, clean up mostly plus some claude assistance
now we come to the last part, its cleaning up some errors, for example earlier, once the screen was taken control of by the camera loop, once the camera exits, the original pygame canvas that held the menu didnt start back up, so i had to go add that line, a lot of small issues like this need fixing, for example the spacing on my album cover display is horrendous, the text is laid over the cover for some reason, and it above when it should be below, ill be fixing that now.
additionally I need the songs to load in slowly when opening liked songs, currently all my 800 songs load in at once, hence the device pauses until all are loaded
used claude to find a lot of the errors in this one, plus it cleaned up my spotify functions that had a lot of redundant code, plus some looping errors in my main code, e.g I would continuously call the album cover function, since it was in the loop that would display the currently playing song, so the image would be downloaded a hundred time per second, and my api continuously checks which song is playing. Thats most of my ai use, I also used it to troubleshoot my driver issues are the beginning of the project.
4. Once these are done, I need to write my readme plus create my circuit diagram on kicad, plus upload all my files to github
then we're ready to ship yay
![image.png](https://cdn.hackclub.com/01a125e2-bcd7-7a82-b620-20fb9406b169/image.png)

# 2026-09-18: Adding missed hours

**Total time spent: 1 hour 40 minutes**

since ive moved from macondo ive had to copy paste all my entries which was a pain I seem to have missed logging some hours here and there since currently it says 58.4 hours even though my lapse time on hackatime is tracked to be 60 hours 4 minutes, so Im going to manually add the missing time to ensure its the same, ill also include the rest 20 hours of coding in the devlog after this since I didnt know vsc/hackatime tracked time needed to be logged too so thats my bad
![image.png](https://cdn.hackclub.com/01a0b47d-fba8-7202-a7a6-473a2dfee220/image.png)
![image.png](https://cdn.hackclub.com/01a0b47e-d9a7-75ef-b803-5f70f1c494bf/image.png)

# 2026-09-18: Circuit Diagram

**Total time spent: 49 minutes**

wasted 40 minutes on this, but I made a wiring diagram using paint, only to realize i should probably make it on kicad instead of it being a mess of lines on paint, nothing much to say about this its just wasted work :(
![image.png](https://cdn.hackclub.com/01a0b47a-222d-7735-a6f7-072342d9745a/image.png) 
already made it though so ill just copy the connection on a kicad page

# 2026-09-18: Searching for audio board

**Total time spent: 1 hour 16 minutes**

content got deleted -
short form of what happened - I was searching for a replacement audio board, landed on this -
TLV320DAC3100 it has speaker out and headphone out, has a build in amp, so no line level adio that i need to worry about, i discussed line level audio in previous log, lost the lapse link for this actually. most of this lapse was browsing forums to see if i was right about the dac
![image.png](https://cdn.hackclub.com/01a12659-4c29-71fd-b9d1-2ab1bcfd2344/image.png)
the dac i landed on

# 2026-08-28: MORE CAD + BOM + AUDIO

**Total time spent: 78 minutes**

So, Im near finishing my design, so ive started writing my BOM, half of these I already have, but would like to upgrade, e.g my picam is a 1.3 but id much rather buy the picam 3, for wayy better quality, I kinda also broke the camera slot clip on my pi so that needs replacing too. I've added mounting everywhere, and tried to keep it accessibly since I predict ill be opening and closing this several times.

I also found a good I2S dac the adafruit PCM5100, unfortunately this gives line level output. From what I understand, line level output is a low fidelity analog signal, technically strong enough to overcome the load/impedence of the earphones  My main audio device is a pair of KZ Castor Pro IEMS which have a low load of around 16 ohms from their website. DACs are really weird, audio in general is really weird.

So essentially the dac is strong enough, but not built to power earphones, forums and websites and gemini tell me that Id get good midend, but spotty bass and highend sounds. 

Using like 11th grade or probably 9th grade physics (I = V/R) if resistance is low, you get high current for some voltage, but if resistance is high, you get lower current. So essentially, PCM5100 cant give out high enough current for the low resistance/impedence IEMS.

anyway wrapping that up I actually didnt lapse any of that research so there goes the hour i spent on that :(.

I did some cad stuff, added more screws, added a 3d model of the DAC forgetting that I need an amp too. The build is kinda cramped the battery takes up like 50% of my space, so i dont really know where im going to fit everything, especially an amp board. Hence, the research continues tomorrow.
So yeah, did audio research, modeled the board, added screws wherever necessary.
BOM so far

![image.png](https://cdn.hackclub.com/01a0d8f2-69a7-75ef-b986-e527b24f3530/image.png)

the board i was planning on using
![image.png](https://cdn.hackclub.com/01a0499c-8506-7caf-9364-c367c4eabcc0/image.png)

lapse link :
https://lapse.hackclub.com/timelapse/vB4Y-UXvmmx2

# 2026-08-27: Finishing/beautifying CAD model

**Total time spent: 735 minutes**

So by now the basic design was struck down, so now I just needed to make the design look a bit better so that I could get a nice render image to use as the banner, I also needed to finalize some design choices.
1.test fit the screen, print it out and see if the dimensions match
2.decide on the placement of the screen, offsetting it a little bit, or widening the handheld so the screen was deadcenter
3.add decals of the actual boards, e.g a png of the pizero2w, of the charging board, and a little doom png to look nice for the render.
4.add screw holes, and decide how to mount.
mounting was the hardest part I decided on a framing/bracket type design, since the inside was so cramped i didnt think I could include put the screws plus the nuts inside and still make it easily removable, still not sure if the current plan would work, ill print it out then test after submitting for design approval.
![image.png](https://cdn.hackclub.com/01a043b7-4fdb-71bc-9154-24341b2f8699/image.png)
this was the final render, not the best, and not the most accurate since I want the final product to have a transclucent plastic body.

https://lapse.hackclub.com/timelapse/kWrqMAY2Z0ix

https://lapse.hackclub.com/timelapse/Hfa6SdB1_1lD

https://lapse.hackclub.com/timelapse/fghbvYQu7Y0F

https://lapse.hackclub.com/timelapse/QQ8Aa-NBWccV

https://lapse.hackclub.com/timelapse/qDXh-jfPKI6N

https://lapse.hackclub.com/timelapse/D-QN2E1qZfYQ

https://lapse.hackclub.com/timelapse/OeBpeLTwyQ0m

https://lapse.hackclub.com/timelapse/TGdq2tbScegc

https://lapse.hackclub.com/timelapse/Ms0he7BTcqnL

https://lapse.hackclub.com/timelapse/0OgNzmTMXMRq

https://lapse.hackclub.com/timelapse/KtGPH7tahxCf

https://lapse.hackclub.com/timelapse/7j41Nzsqq4Yc

https://lapse.hackclub.com/timelapse/WNLnoq2Hd_St

https://lapse.hackclub.com/timelapse/oBfC5JPmcv-f

https://lapse.hackclub.com/timelapse/2ngbh0oyL0tV

https://lapse.hackclub.com/timelapse/NPfJMUKbqkYa

https://lapse.hackclub.com/timelapse/N_VPuhrVtKB7

https://lapse.hackclub.com/timelapse/y0yyvSdczzuz

# 2026-08-27: Backlight

**Total time spent: 8 minutes**

[content missing due to database mishap]
all of the time logged on vsc, 8 minutes for research.
so i decided to try a backlight via pwm, so i could change the frequency that the screen was on/off to adjust how bright it looked
unfortunately the board seemed to emit noises when i used pwm, it created this whining sound like a siren that changed with frequency, so i assumed its from the backlight.
anyway i decided a backlight isnt that important and removed this feature, but i got it to work, just with the buzzing sound. The image for this is lost, nor can it be recovered, since this code has been deleted so heres an image of a pwm wave
![image.png](https://cdn.hackclub.com/01a12658-43f2-732e-8c58-a3be7df2cdda/image.png)

# 2026-08-27: Menu testing + camera tweaking to get desired look

**Total time spent: 216 minutes**

[content missing due to database mishap]
tweaked with camera more, everything is blue for some reason like reds and blues are swapped, tested my menu code, had some bugs, for example camera would open once but when trying to reopen again, pi would crash. This is fixed in my last log, additionally got camera looking natural-ish and noise free with the exception of me being blue, most of this time was spend fixing the pygame menu.
Did this on the pi, as troubleshooting, with some code, so the time spent troubleshooting and working from the terminal has been logged here, while the code is logged on hackatime via extension.
![image.png](https://cdn.hackclub.com/01a12654-d963-7c02-99a0-c1c70596ddd9/image.png)
camera values to make it look more natural

# 2026-08-27: drivers + buttons

**Total time spent: 106 minutes**

Had to do more display driver work, the new display uses yet new drivers, I had to learn about wayland and x11, and kms and soo many different confusing things
in the end i lucked out, see kms needs a configuration file so that the driver knows what display youre using, this is where my luck kept running out, i couldnt find a config suitable for my older screens not for my newer one, however while scouring the forums i found that someone had made exactly what i needed, and posted it.
so in the end i only needed to extract a zip file and that was enough

after that i made the button faces, im using these clicky push buttons, but i didnt want an exposed pcb so im creating big button faces, especially because the push buttons have a really small surface area so you need something big to press on

https://lapse.hackclub.com/timelapse/P_7iC9Ysl47w

https://lapse.hackclub.com/timelapse/LvDYWEiO5nxd

![image.png](https://cdn.hackclub.com/01a04366-8594-7d78-8e83-7b397ced7e5c/image.png)

# 2026-08-27: Finishing up base model, getting the camera working, and making it look nicer

**Total time spent: 2 hours 5 minutes 31 seconds**

[content missing due to database mishap]
![image.png](https://cdn.hackclub.com/01a1264e-c6a0-75b1-a7f2-ff4cdbccc6d5/image.png) 
did a test print that turned out like this i think
initialized the camera using picam2 library, it has low resolution but its good enough i feel
took test pictures, messed around with the camera values to look nicer
in regards to making to look nicer, added some design work to the case, made it look much better, since i had no space inside, went for brackets that would be mounted externally, we'll see how the tolerance is once i print it, this was where i finalize lots of design elements that you can see in the upcoming logs where i created the render for the banner image


# 2026-08-27: More CAD work

added some mounting hardware, spent time moving the pi around trying to find where it fits 
![image.png](https://cdn.hackclub.com/01a04355-4ddd-7847-8df7-d2707d73b098/image.png)
 creating the pi mounting hardware yesterday, mainly tried to fit all the components today, changed the diameter an dimensions of some items that were previously incorrect, and tried to adjust tolerances, increased every screw hole by about 0.2mm to make sure the screw goes in there. found a lot of m3 and m2.5 screws at home, so wont need to buy those I think also bought a pi camera 1.3 and modeled it 
![image.png](https://cdn.hackclub.com/01a04355-9f21-79dc-9bca-3ee0a120188c/image.png)
 not sure if ill use it, i dont want to add too many features and make it too gimicky, its not a dumb phone, its an mp3 player/ retro game machine. Im getting too ambitious I also have a sim card module, so i could technically add voice call functionality, but again i think it would be too gimicky so best to keep to the basics
the lapse for this is actually in the previous devlog, i decided to go with the camera, cuz i carry a digicam everywhere, so this could replace that, especially since that has horrible battery life.
The test pics i took were mostly of my face, but here are few of the pics i took that don thave my face
![2026-08-06_23-41-45.jpg](https://cdn.hackclub.com/01a04357-521e-7673-85ea-089303372a99/2026-08-06_23-41-45.jpg)
![2026-08-06_23-47-11.jpg](https://cdn.hackclub.com/01a04357-7f21-73aa-9c15-704d8cc9333f/2026-08-06_23-47-11.jpg)

https://lapse.hackclub.com/timelapse/F7YJgzOrExC8

# 2026-08-27: Day UNKNOWN 

**Total time spent: 308 minutes**

Have actually done a lot of cad work in the past week, most of it is on lapse besides some stuff i forgot to record and todays work, because i accidentally recorded 3 hours without pausing. Anyway, so im getting a new screen, since the last one broke obviously. Instead of buying the same thing however, im gambling with drivers and buying a new one 
![image.png](https://cdn.hackclub.com/01a125d1-cd58-7970-b6b8-c9dbd0d81abf/image.png)
 this is the one i chose, reasons being : its 3.5 inches, its spi, and unlike the previous one it has no header, meaning its much more flat and easier to stick in my case. So i designed a new front to accomodate 
![image.png](https://cdn.hackclub.com/01a125d2-0549-73ae-b14f-326f8ceaa758/image.png)
 much uglier now, so lots of design work to be done I also found a 30x10x30 fan to cool the pi, since i was a bit worried about heat, but when testing it only reached 44 degrees celsius which is still hot to the touch. 
![image.png](https://cdn.hackclub.com/01a125d2-3f97-7049-9d19-45832ea5b25f/image.png)
 this is the most recent mockup, after the 1 hour worth of work i did today, I added the fan , shifted the i2s dac and the usb c charger, found some space and measured tolerances to reduce thickness by 3 to 4mm. 
![image.png](https://cdn.hackclub.com/01a125d2-7d11-7fc4-953f-236228db555b/image.png)
 this is the i2s dac, its i2s so i dont need much gpio.

# 2026-08-27: First CAD work

**Total time spent: 363 minutes**

[content missing due to database mishap]

# 2026-08-27: ALL THE DRIVER/DOOM LAPSE LINKS

**Total time spent: 684 minutes**

https://lapse.hackclub.com/timelapse/AY-Yt1Ps9Z02
https://lapse.hackclub.com/timelapse/keWMGi3Uo978
https://lapse.hackclub.com/timelapse/GmLnyF5Qe2bI
https://lapse.hackclub.com/timelapse/taZrfdB8wV1V
https://lapse.hackclub.com/timelapse/dVrX3Kw9zI0F
https://lapse.hackclub.com/timelapse/0biXCHS8Vedz
https://lapse.hackclub.com/timelapse/nWEDscTkeGt4
https://lapse.hackclub.com/timelapse/wUR-ss82tI4V
https://lapse.hackclub.com/timelapse/drjttrt5CANK
https://lapse.hackclub.com/timelapse/sCLb-_z7WeJk
https://lapse.hackclub.com/timelapse/WAr5hzCM6g5i
https://lapse.hackclub.com/timelapse/Pq41xFA9IWWJ
https://lapse.hackclub.com/timelapse/k69EYTy4OEle
https://lapse.hackclub.com/timelapse/sHK2hCCwWFSI
https://lapse.hackclub.com/timelapse/sYLjdMrwpyK2
https://lapse.hackclub.com/timelapse/L8VgyhjbVMN1
![image.png](https://cdn.hackclub.com/01a04321-7ffb-7cd6-9338-4b3b33c01d6f/image.png)
all the lapses

# 2026-08-27: Day 11-16 : part 3 

so now that my display worked, I needed to test that it worked with something, so I downloaded chocolate-doom, moved the .wad files over to my pi with scp, then ran the command, it booted perfectly (or so it seemed) until it reached this message Error creating window for video startup: Could not initialize EGL so doom worked fine but i ran into another issue where the EGL backend couldnt find a display to initialize to, anyway that was just me being stupid turned out I forgot to do startx again and so X11 wasnt connected to my display so once that was fixed 
![image.png](https://cdn.hackclub.com/01a125d0-acfe-7072-9449-0a28b33b6c50/image.png
 I GOT THIS, which meant doom was running just that it was on the bottom 1/20th of my screen, this was an easy fix, just turned out that i had to declare my display dimensions in a .cfg file for x11, so i fixed that and entered 430x320 (my display pixel dimensions) and got THISS 
![image.png](https://cdn.hackclub.com/01a125d0-dbe2-7ef9-b939-b0b1ffd3c8f5/image.png)
 the display worked, i got doom to start on it, and now this is where we are. actually we've regressed, i dropped my display today and broke a connection :( 
![image.png](https://cdn.hackclub.com/01a125d1-132e-75bc-8c86-7bb4606533a5/image.png)
 not sure how visible it is here, but yeah the contact came off, so gotta order a new one, and im gonna work on cad until thats here

# 2026-08-27: Day 11-16 : part 2 

so starting this with a picture of my new display 
![image.png](https://cdn.hackclub.com/01a125cf-c528-7fea-a12f-171817ff44f7/image.png)
 this doesnt show the screen but dont worry because i have good news and that will come in good time so firstly this is an office raspberry pi display clone, meaning the support was SOOOOO MUCH BETTER a google search and a link on lcd-wiki led me directly to GoodTFT drivers that were genuinely a god send, so instead of a framebuffer like fbcpi-ili9341 GoodTFT communicated with the pi so that its directly listed as an active display, and not the pi thinking it has a hdmi display and having the drivers copy that over to an spi display so apparently that alone has a lot of benefits skipping over that because i never really googled the benefits, the drivers worked, they took some elbow grease, ducttape and time but it worked so firstly Goodtft actually replaced a few kernel overlays that caused me issues, it also changed how X11, a display protocol, interacted with my pi. So i had to change some settings, modify X11 and stop fbcp from booting because that was auto enabled for some reaosn. so first to find out that i needed X11, i ran *xrandr this printed cant open display which meant that there wasnt any session that xrandr could communicate to so i googled how to start a session and that required xstartx so this actually worked, it got me this screen 
![image.png](https://cdn.hackclub.com/01a125d0-0035-76b5-a326-5ee8df6c11f6/image.png)
 a little _ showing that the driver properly started and its expecting me to type soemthing this meant x11 was starting fine, but it didnt show my console so it still wasnt receiving any output, this involved me changing config files, and manually using DISPLAY = :0 to manually set my display and have x11 identify it under the banner :0, so this worked and i got 
![image.png](https://cdn.hackclub.com/01a125d0-338f-7890-a694-6d85ba0246c7/image.png)
 some very good news that meant my display was receiving output, since it showed my terminal just with inverted colors for some reason

# 2026-08-27: Day 11-16 part 1 

okay firstly, ive split this into a few logs cuz i forgot to write logs and did a lot of things in these last 5 days first ill detail using the 2.4 inch display so as i mentioned in past logs i started with a 2.4 inch spi display that used a fbcp ili9341 chip, that did NOT gel well with the current raspberry pi os version, the framebuffer/drivers it used are archaic and depracated by now. I tried using fbcp-ili9341 drivers by juj that copies the frame buffer onto an imaginary hdmi output that the pi thinks it has. this is a pretty common approach, but the drivers just had 0 support with raspbian bookworm, which is what I am using, and I'd have to change sooo many things to make it work, this was a solid 2 3 hours of work of just trying and retrying and googling and regoogling error messages, chatgpt was a life saver here, it would go through like 400 lines of errors and tell me which one mattered. fbcpi-ili9341 was built around old deprecated stacks/kernels/graphics libraries, it was around this time that I thought i should ask my brother, hes learning embedded systems at pennstate in the US, and he made his own like retro phone, as well as an esp32 based watch, hes pretty handy. So i called him up, and he mentioned he had an old 3.5 inch rpi display somewhere at home that ran on a different chip and had newer display drivers. so since the errors i faced -
raspbian bookworm lite compatibility
legacy graphics components
mismatched dependencies
REPEATED BUILD ERRORS FROM CMAKE LIKE SO MANY
config mismatch, like the drivers would look for a .config file in /boot/config, but bookworm would have it in /boot/firmware/config and making the driver read the new file just didnt work.
updating my system broke my working output, so it was obviously unstable those were the issues, so without really thinking of it just hoping the new display would be a hail mary i shifted to the 3.5 inch 
![image.png](https://cdn.hackclub.com/01a125cd-d750-7ca3-8573-1f38713057dc/image.png)
![image.png](https://cdn.hackclub.com/01a125cd-f5fd-7bca-9af0-c3ae6169b747/image.png)ld

# 2026-08-27: Day-10 part 2 Reimaging 

**Total time spent: 1 hour**

So, I've decided to proceed with option 3 actually, which is fbcp-ili9341 by juj. First part of that is reimaging to an older version, because fbcp has old path names and I kept running into an issue where it expected config file at /boot/config.txt but on bookworm it was at /boot/firmware/config.txt

this is what it was: cirrus@cirrus:~/fbcp-ili9341/build $ sudo nano /boot/config.txt cirrus@cirrus:~/fbcp-ili9341/build $ sudo ln -sf /boot/firmware/config.txt /boot/config.txt cirrus@cirrus:~/fbcp-ili9341/build $ ls -l /boot/config.txt lrwxrwxrwx 1 root root 25 Jul 3 21:39 /boot/config.txt -> /boot/firmware/config.txt cirrus@cirrus:~/fbcp-ili9341/build $ sudo ./fbcp-ili9341 bcm_host_get_peripheral_address: 0x3f000000, bcm_host_get_peripheral_size: 16777216, bcm_host_get_sdram_address: 0xc0000000 BCM core speed: current: 250000000hz, max turbo: 400000000hz. SPI CDIV: 6, SPI max frequency: 66666667hz Allocated DMA channel 7 Allocated DMA channel 1 Enabling DMA channels Tx:7 and Rx:1 DMA hardware register file is at ptr: 0x75d96000, using DMA TX channel: 7 and DMA RX channel: 1 DMA hardware TX channel register file is at ptr: 0x75d96700, DMA RX channel register file is at ptr: 0x75d96100 Resetting DMA channels for use DMA all set up Initializing display Creating SPI task thread InitSPI done vc_dispmanx_display_open failed! Make sure to have hdmi_force_hotplug=1 setting in /boot/config.txt

anyway, so i flashed with bullseye lite 32bit, which now involves creating a seperate file with ssh, wifi details and user details, which was a hastle, however before that i ran into a few issues. my computer wasnt detecting my sd card after flashing, so i put it in my phone and checked there, there it read perfectly fine, so i thought my sd card must be on the wrong file system, so i formatted it with a really annoying software that made you watch an ad each time you wanted to do something 
![image.png](https://cdn.hackclub.com/01a125cc-0ea6-7450-a6ee-91b3bc736e60/image.png)
after this, went this also proved fruitless I googled it and realized i had to assign a letter to the drive so did that and continued, then went through the process of creating wpa_supplicant, ssh and user files, yet to test it but im hoping it worked

# 2026-08-27: Day-10 Project reset 

Through the entire project so far, ive been using luma.lcd shaders, this is good enough for my menu or music but not so much for the actual games or videos i want to play. I dont really have a good assortment of drivers to pick from, from my research we have fbtft, luma.lcd, fbcp, and modern kms/drm. So lets go through why all of this hasnt worked so far.

    fbtft - hella old, doesnt work right with my current kernel, im using raspbian bookworm aswell which is the 2nd most recent one, and thats holding me back. This could work with an older version of rasbian like bullseye, (my current plan c)
    luma.lcd - too basic, retroarch cant work with this
    fbcp - similar to fbtft, would work with older version of raspbian, also require 32bit, current im on 64 bit though, so another option or my plan b is using this, with a 32 bit version of raspbian lite os
    modern kms/drm drivers, the most up-to-date, but thats its major draw back, seems that it might not be fully tested, and it requires some verification and specific config files that I cant find anywhere, so i attempted this but didnt work Alright, so moving forward with fbcp plus reimaging to 32bit, wish my luck bosses. 
![image.png](https://cdn.hackclub.com/01a125ca-f36f-7ff2-8297-bc247f6e937e/image.png)
 drivers installed, check the readme file, but no change to my static screen 
![image.png](https://cdn.hackclub.com/01a125cb-8b56-7a3c-b23c-37bd225aa48c/image.png)

# 2026-08-27: Day-9 ; Menu Code ACTUALLY finished 

**Total time spent: 3 hours 38 minutes**

yeah so the stuff i wrote last time did not actually work, I kinda just assumed it would and posted a log but it DOES NOT, or atleast not the way I wanted. I can navigate, and I can see the menus, the only thing is, since I was using lists, print (listvariablename) just prints the contents of the list which obviously we dont want. 
![image.png](https://cdn.hackclub.com/01a125c8-604b-7865-9cc6-c0228dff5337/image.png)
 So, decided I gotta somehow link the name of the menu to its actual contents while somehow making the name separate, first attempt was the hare-brained idea of two lists with same indexing and stuff, it was possible, but wayy too confusing and complicated. Hence I landed on dictionaries, which is the obvious solution but im not the smartest 
![image.png](https://cdn.hackclub.com/01a125c8-9ae7-7e25-a8d1-52ab9703c5a8/image.png)
 so this was my dictionary structure, after this i changed all the function calls, the navigation and stuff and that took me a good hour or 2. next, decided to text, first try WOO it works, YAY, lets just navigate, I open music submenu, woah it works, i try the functions, yeah theyre working, i try to go back, pi crashes. uh oh 
![image.png](https://cdn.hackclub.com/01a125c8-dae9-7aa1-b084-d69378fd56a7/image.png)
![image.png](https://cdn.hackclub.com/01a125c8-f184-7b9c-8938-c2449309c2ae/image.png)
 so I get this error, and i kid you not it took me a bloody hour, I tried so many things, and NOTHING worked, essentially this is what was happening: I would enter some sub menu, e.g : music, then I would click <Go back>, the pi would process go back, but then instantly select music again, then try to go back AGAIN, however within the stack it hasnt updated that its entered music. So the stack basically becomes: Main>Music then Main> after go back happens, then < > (empty stack) after it processes go back AGAIN. SO I ended up with out of bounds errors again and again. I thought this was obviously, classic button bouncing, the go back was being triggered multiple times, OBVIOUSLY. So tried : software debouncing using gpiozero, debouncing using sooo many convoluted if and elses, hardware debouncing (switching to more accurate switches, and so many other small random tweaks, until I realized what a fool I'd been. 
![image.png](https://cdn.hackclub.com/01a125ca-110a-7c7d-a4dd-77d4b1f432fb/image.png)
 this part of my code used to be IF and IF, not IF and ELIF. that was the mistake, I'd click to go back, and two functions would run simultaneously. 2 hours of work because I put if and not elif. what a pain anyway its over now, that change fixed everything, and now its all A-OKAY. See y'all next post.

# 2026-08-27: Day-7+8 : Menu Code finished 

**Total time spent: 1 hour 17 minutes**

If you would refer to my previous logs, i've been through a few iterations of my menu code now. First came a looong list of if-statements if ___ is pressed do ___, something which i quickly realized was really unfeasible, especially with how many submenus and functions I'd eventually have, here each menu had its own index variable, and all in all it was really confusing, this is what it looked like : 
![image.png](https://cdn.hackclub.com/01a125c7-003d-72b3-b164-9ed3452db816/image.png)
 imagine each submenu (music, games, mp3s, local files), etc ALLL having their own index variables and other things, it was just a PROPER headache. A variation of this I thought of was to use dictionaries, here each key (a header) would call a function (that actually did the work, however, this was too confusing and i js dont know dictionaries nor do I trust myself to do it right. So i got fed up and googled ways to make menus for systems like this, and coincidentally, a recommended option was the "stack" data structure, a list where I would call the top most variable. thats what this is: 
![image.png](https://cdn.hackclub.com/01a125c7-305b-7752-a26c-432c70b3aef3/image.png)
 each menu is appended to the list, so thats its really easy to know which path im in, and which path my file is. I believe I've found the best menu format moving forward, so this is what ill stick to, now its time for spotify functions, to actually write the code to play music, or actually cuz im lazy i might do the games instead, but that would require buttons, lets see what pans out.

# 2026-08-27: Day-6 : Hardware and UI Design 

**Total time spent: 2 hours 6 minutes**

Decided I've had too much of software, and since this is technically a hard-ware project I should really begin work on that. Started with sketching what I want retroport/cirrus to look like (havent decided on a name), one inspiration is the classic old-school cool Ipod especially the 5th, 6th and 7th generations. 
![image.png](https://cdn.hackclub.com/01a125c5-d5b4-7167-b15e-337e5c399c54/image.png)
 as far as software goes these are my biggest influences, as is fairly apparent in my first draft 
![image.png](https://cdn.hackclub.com/01a125c6-1178-7307-bf21-6c6f31570572/image.png)
 color selection was HARD, decided two neutral + one pop-out color works, and cirrus is a candidate name, hence skyblue was the pop-out. Hardware was far harder to decide for than software, I took HEAVY inspiration from other handhelds like the OG Gameboy 
![image.png](https://cdn.hackclub.com/01a125c6-4750-768f-8ddb-3e3a582b3de5/image.png)
![image.png](https://cdn.hackclub.com/01a125c6-5c52-7159-bfad-b1b6a35d036e/image.png)
 and then just mated that with a PS1 non joystick controller, since I dont think I have the gpio for joysticks. This matrimony led to my first hardware draft - 
![image.png](https://cdn.hackclub.com/01a125c6-875d-7efb-a7e7-2d5baa2fc269/image.png)
 Hope the handwriting is legible, but I feel I've covered all the functionalities, and should STILL BE within my gpio limit. Taxing day today, see y'all next time.

# 2026-08-27: Day-5 : Leaning Menus 

**Total time spent: 38 minutes**

I've built a menu system that consists of a huge set of if statements, which I feel is most likely not the best way to do this, it is however the only way I know with my limited python knowledge, HOWEVER, fret not actual coders, this week we've learnt about data structures at school, at this leads me to believe I DONT need a huge list of if functions to go between menus, the following are the if loop JUST for the main menu and ONE of like 12 bazillion submenus. 
![image.png](https://cdn.hackclub.com/01a125c5-4faa-7868-9804-fb3e9baddc31/image.png)
 Hence, from data structures I intend to use stacks, the reason the if statements are so cumbersome is that I need soooo many variables and thingamjigs to track which menu im currently in, each submenu needs its own index variable, its own list, its just too much. Hence, I've decided stacks are the best way to track my path, instead of a bunch of index variables signaling which menu I am in, I am going to use a menu stack that consists of the path, eg ["main", "MP3", "Liked Songs", "Other Side - Brent Faiyaz"] In theory this should simplify my work flow by a LOT so lets see. See y'all once I test this

# 2026-08-27: Day-2 : Soldering pins to pi 

**Total time spent: 47 minutes**

[content missing due to database mishap]

# 2026-08-27: Day-3+4 : Set up display, Learning code 

**Total time spent: 1 hour 33 minutes**

Installed all my libraries and packages, and set up my display today. Today was my longest stretch of work so far, around 2 to 3 hours I think not really sure, I needed to test the display out and get some concrete results so today really felt like a victory. Printed some text to the screen as an example, and then wrote some basic code, no particular goal for that besides learning the software/firmware side of things. Anyway, GOODNEWS it WORKS : 
![image.png](https://cdn.hackclub.com/01a125c2-970c-791c-a894-b415d1bac6ff/image.png)
![image.png](https://cdn.hackclub.com/01a125c2-b53f-78e6-b94f-b33a70cf1aab/image.png)
![image.png](https://cdn.hackclub.com/01a125c2-e566-7e46-ba42-e65d58eae702/image.png)
 Set up a quick menu as well, with two buttons to test input and learn how to move through menus. Today was more learning oriented than progress oriented, in the way that I spent time learning what I need to instead of making big decisions.
quick note : 

# 2026-08-27: THE BEGINNING

This journal contains work from a week ago, as well as my new thoughts. Okay first of all, first 2 lapses were a waste of time. My understanding of my pi is very low, and this is quickly becoming more and more apparent. The first hour of attempts involved attempting to install juj's fbcpi-ili9341, after some research however, it seems my usecase, a handheld that doubles as an mp3 player as well as a ps1 emulator, a driver system like fbcp, which uses framebuffers to copy hdmi output onto the screen, are completely UNNECCESARY,doubly it seems fbcp has issues with 64 bit systems like mine, atleast thats what reddit says (as does gemini, didnt use it specifically btw, just gave its response when i googled the error).
![image.png](https://cdn.hackclub.com/01a042e6-d494-7bce-ba9f-92a039847b65/image.png)
![image.png](https://cdn.hackclub.com/01a042e7-1ac8-7bb4-99c2-fe0075dd74e8/image.png)
Anyway, this concludes an hour of work, and so now its time to switch gears. I've found a lightweight simple driver called luma.lcd, I hope it is sufficient. These are first steps though, so lets see what happens.
Lets review my timeline of work -

    gather courage
    lock TF in
    waste time on the wrong thing
    understand my incompetence
    lots of googling
    next steps decided
    created to do list.

**TO-DO list (tasks to complete in this session):

    update and install pip
    add all libraries (list after todolist)
    run some sanity checks** 
![image.png](https://cdn.hackclub.com/01a042e7-81ec-7469-afcf-d3da180817d3/image.png)
![image.png](https://cdn.hackclub.com/01a042e7-b2ed-7b2c-9296-33889d2deb81/image.png)
Fairly useless work today, didnt pan out how I expected it to. I know very little about what im working it, it seems i need to study before I post my next log. Excited but frustrated, errors you know nothing about really bring the vibes down. Peace out, I think im heading in the right direction, luma.lcd seems a good fit for me, and I think my other libraries work well together. See y'all next time, how this for a first post? Lapse links :
https://lapse.hackclub.com/timelapse/znqaEBvbwskL
https://lapse.hackclub.com/timelapse/vwL9kOPGjzrk
https://lapse.hackclub.com/timelapse/vgn-oSMu0bpm
https://lapse.hackclub.com/timelapse/737Athk4Cmmg

# 2026-08-22: First Log

**Total time spent: 1 hour**

[content missing due to database mishap]

