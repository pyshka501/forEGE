import time
import os
import math
import keyboard
import threading
import random
from playsound import playsound
import pygame
from pygame.locals import *

pygame.init()

wall = 'upali-dengi-na-igrovoy-schet.wav'
frame = 'upali-dengi-na-igrovoy-schet.wav'
def wally():
    playsound(wall)
    return
def framy():
    playsound(frame)
    return

g = 9.81
#bounce
b = 0.95
#v1 and v2
v1 = 100
v2 = 0.001

v0 = math.sqrt(v1**2+v2**2)

v0m = 1000
v3 = v1/v0
v4 = v2/v0
vx = 1

if v1 == 0.001 and v2 == 0.001:
    v0 = 0
    v3 = 0
    v4 = -1

t = 0
tmax = 100

#fps
tstep = 1/60

bounces=10**6
maxbounces = bounces + 1
counter = 1


x0 = round((0.5*v3*t*t) - (t*v3*v0))
y0 = round((0.5*(v4-g)*t*t) - (t*v4*v0))

#starting position
x = 10
y = 2

yresolution = 20
xresolution = 20
resmult = 12

sizemult = 1.01
size = 1

#enable air resistance
ar = False
tail = " "

select = False
if select == True:
    v1 = float(input("X velocity: "))
    v2 = float( input( "Y velocity: " ))
    b = float( input( "Bounciness: " ))
    x = int( input( "X start pos: " ))
    y = int( input( "Y start pos: " ))
    tstep = 1/(int(input("FPS: ")))
    bounces = int(input('Bounces: '))
    maxbounces = bounces + 1
    if input("Enable Trail (Y/N)? ") == 'Y':
        tail = "."
    else:
        tail = " "
    if input("Enable Air Resistance (Y/N)? ") == 'Y':
        ar = True
    else:
        ar = False

m = 1
C = 1
r = 1
p = 1
A = 1
k = 1
e = 1

if ar == True:

    #mass
    m = 0.625

    #coeff
    C= 0.47

    # radius
    r = 0.2426/2

    #fluid density
    p = 1.293

    # cross sectional area
    A = math.pi*r*r

    k = 0.5*p*v0*C*A
    e = math.e

a = 1

tandb = "::::"
A45 = [1,1]

if x >= xresolution:
    x = xresolution - 1

if y >= yresolution:
    y = yresolution - 1

for tb in range(xresolution):
    tandb += "::"
row = 0
column = 0
grid = []
grid2 = []
grid_display = []
grid_display2 = ""
grid_value = ""
gridvaldispaly = []
while row != yresolution:
    globals()['column'+str(row)] = []
    grid.append(globals()['column'+str(row)])

    globals()['column2' + str( row )] = []
    grid2.append( globals()['column2' + str( row )] )
    grid_display.append("")
    gridvaldispaly.append("")
    while column != xresolution:
        globals()['column'+str(row)].append(0)
        globals()['column2' + str(row)].append( 0 )
        column += 1
    globals()['column'+str(row)].append(str(row))
    globals()['column2' + str( row )].append( str( row ) )
    column =  0
    row += 1

x1 = round((0.5*v3*t*t)+(t*v3*v0)) +x
y1 = round((0.5*(v4-g)*t*t) + (t*v4*v0)) + y
x2 = round((0.5*v3*t*t)+(t*v3*v0)) +x
y2 = round((0.5*(v4-g)*t*t) + (t*v4*v0)) + y
x3 = round((0.5*v3*t*t)+(t*v3*v0)) +x
y3 = round((0.5*(v4-g)*t*t) + (t*v4*v0)) + y

bounces = 0
for r in range(yresolution):
    for c in range(xresolution):
        rh = (r - (yresolution/2) + 0.5)
        ch = (c - (xresolution/2) + 0.5)
        if (rh**2+ch**2) >= (yresolution/2)**2: #change 174
            grid[r][c] == -1

engle = 0.00000

window = pygame.display.set_mode((1920, 1080))

# yresolution*4*resmult

window.fill((255, 255, 255))
xdis = (1920- yresolution * 4 * resmult) / 2
ydis = (1080 - yresolution * 4 * resmult) / 2

pygame.draw.circle(window,
                   (0,0,0),
                   [(yresolution*2*resmult)+xdis, (yresolution*2*resmult) + ydis],
                   yresolution*2*resmult,
                   4
                   )

pygame.display.update()

red = 255
grn = 0
blu = 0
col = 0

while bounces != maxbounces and size <= yresolution+ 0.5:
    while ((y - yresolution/2)**2 + (x-xresolution/2)**2 ) > (yresolution/2 - (0.5*size))**2:
        x -=(x - yresolution/2)*tstep*0.1
        y -=(y- yresolution/2)*tstep*0.1
    xy = math.sqrt((x - yresolution/2)**2 + (y - yresolution/2)**2)
    xengle = (x - yresolution/2)/(xy) # 201
    yengle = (y - yresolution/2)/(xy)
    t = 0
    v1 = -v1
    v2 = -v2
    mm = 1
    if x > yresolution/2 and y < yresolution/2:
        mm = 1
    if x < yresolution/2 and y > yresolution/2:
        mm = 1

    v0 = math.sqrt((v1**2 + v2**2))
    v3 = math.cos(math.radians(-math.degrees(math.acos(v1/ math.sqrt(v1**2+v2**2))) - 2 *(mm*math.degrees(math.acos(yengle)) - 90) - (x-yresolution/2)))
    v4 = math.sin(math.radians(-math.degrees(math.asin(v2/ math.sqrt(v1**2+v2**2))) - 2 *(mm*math.degrees(math.asin(xengle)) - 90) - (y-yresolution/2)))


    v0  *= vx
    v0m *= vx
    if v0>v0m:
        v0 = v0m

    if v1 == 0.001 and v2 == 0.001:
        v0 = 0
        v3 = 0
        v4 = -1
        while t <= tmax:
            col += 1/255
            if (col - (col%1)) % 6 == 0:
                grn +=1
            elif (col - (col%1)) % 6 == 1:
                red -= 1
            elif (col - (col%1)) % 6 == 2:
                blu  +=1
            elif (col - (col%1)) % 6 == 3:
                grn -=1
            elif (col - (col%1)) % 6 == 4:
                red +=1
            elif (col - (col%1)) % 6 == 5:
                blu -=1

            # window.fill(0, 0, 0)
            pygame.draw.circle( window,
                                (255, 255, 255),
                                [(yresolution * 2 * resmult) + xdis, (yresolution * 2 * resmult) + ydis],
                                yresolution * 2 * resmult + yresolution,
                                4 + yresolution
                                )

            if ar == True:
                a = (-k/m)*math.pow(e, ((-k*t)/m))*v0
            te = t - 0.000981
            x0 = round((0.5*v3*t*t)+(t*v3*v0) + x)
            y0 = round((0.5*(v4 - g)*t*t) + (t*v4*v0) +y) #251
            xh = (0.5*v3*t*t)+(t*v3*v0) + x
            yh = (0.5*(v4-g)*t*t) + (t*v4*v0) +y

            if x0 >=0 and x0 <= xresolution - 1 and y0 >= 0 and y0 <= yresolution - 1 and ((yh-yresolution/2)**2 + (xh - xresolution/2)**2) < (yresolution/2 - (0.5*size))**2 :
                if grid[y0][x0] == -1:
                    grid[y0][x0] = -1
                else:
                    grid[y0][x0] == counter

                x1 = ( (0.5 * v3 * t * t) + (t * v3 * v0) ) + x
                y1 = ( (0.5 * (v4 - g) * t * t) + (t * v4 * v0) ) + y
                x2 = ( (0.5 * v3 * t * t) + (t * v3 * v0) ) + x
                y2 = ( (0.5 * (v4 - g) * te * te) + (te * v4 * v0) ) + y
                x3 = ( (0.5 * v3 * t * t) + (t * v3 * v0) ) + x
                y3 = ( (0.5 * (v4 - g) * t * t) + (t * v4 * v0) ) + y

                if size > yresolution -2/resmult:
                    size = yresolution -2/resmult

                pygame.draw.circle(window, (red, grn, blu),
                                   [round(xh*4*resmult)+xdis, round((yresolution-yh)*4*resmult)+ydis], 2*resmult*size, 0)
                pygame.draw.circle( window, (0, 0, 0),
                                    [round( xh * 4 * resmult ) + xdis, round( (yresolution - yh) * 4 * resmult ) + ydis], 2 * resmult * size, 3 )
                pygame.draw.circle( window, (0, 0, 0),
                                    [(yresolution*2*resmult)+xdis, (yresolution*2*resmult)+ydis], yresolution*2*resmult, 8 )

                pygame.display.update() #274

                globals()['fram'+str(t)+str(bounces)] = threading.Thread(target=framy)

                time.sleep(tstep/5)
                row = 0
                column = 0
            else:
                t = tmax
                x = x1
                y = y1
                v1 = ((x3-x2)/0.001)
                v2 = ((y3-y2)/ 0.001)
                while ((y-(yresolution/2))**2+(x-(xresolution/2))**2) < ((yresolution/2) - (0.5*size))**2:
                    x+=(v1)*tstep*0.2
                    y+=v2*tstep*0.2
                while ((y-(yresolution/2))**2+(x-(xresolution/2))**2) > ((yresolution/2) - (0.5*size))**2:
                    x -= (v1) * tstep * 0.2
                    y -= v2 * tstep * 0.2

            t+=tstep
            counter+=1
        bounces += 1
        globals()["wall"+str(bounces)] = threading.Thread(target=wally)
        globals()["wall" + str( bounces )].start()
        vx  = 1* (math.pow(b, bounces))
        vx = b
        size = size*sizemult
    counter = 0
    while True:
        grid_display2 += ("\n"+tandb) # 303

        for ree in range(yresolution):
            re = yresolution - ree - 1
            for c in range(xresolution):
                if str(grid[re][c]) == str(counter):
                    grid_display[re] = grid_display[re] + "##"
                elif str(grid[re][c]) == "0":
                    grid_display[re] = grid_display[re]+ " "
                    #314
                else:
                    grid_display[re] = grid_display[re] + "."
            grid_display[re] += '::'
            grid_display2 += '\n' + ('::'+grid_display[re])

        grid_display2 += ("\n" + tandb)

        os.system('cls')

        print(grid_display)
        time.sleep(tstep/10)
        grid_display2 = ""
        row = 0
        column = 0

        while row != yresolution:
            grid_display[row] = ""
            row += 1
        counter+=1






