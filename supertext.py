#!/usr/bin/python3
import pygame
import sys
import os
import time
import numpy as np
from pygame.locals import *

curx=0
cury=0
charsize=8
dotscale=2
XSIZE=40
YSIZE=25
color_=(255,255,255)
bgcolor_=(0,0,0)
vvram=[[chr(0) for _ in range(25)] for __ in range(40)]
keys={ 'space':0,'escape':0,'return':0 }
path_to_chars='/home/gar/lib/chars.txt'

screen=[]
spacechar=[ 0 for _ in range(8*8) ]
chars=[ spacechar for _ in range(0,256) ]

def loadchars():
    global chars
    chars=np.loadtxt(path_to_chars)

def bgcolor(c):
    global bgcolor_
    bgcolor_=c

def color(c):
    global color_
    color_=c

def locate(x,y):
    global curx,cury
    curx=x
    cury=y

def scrollup(sx,sy,width,height):
    global screen
    px=sx*dotscale*charsize
    py=sy*dotscale*charsize
    w=width*dotscale*charsize
    h=(height-1)*dotscale*charsize
    for i in range(h):
        for j in range(w):
            screen.set_at((px+j,py+i),screen.get_at((px+j,py+i+dotscale*charsize)))

    for i in range(height-1):
        for j in range(width):
            vvram[sx+j][sy+i]=vvram[sx+j][sy+i+1]
    locate(sx,sy+height-1)
    s=' '*width
    putstr(s)
    refresh()

def scrolldown(sx,sy,width,height):
    global screen
    w=width*dotscale*charsize
    h=height*dotscale*charsize
    px=sx*dotscale*charsize
    py=sy*dotscale*charsize
    for i in range(h-1,dotscale*charsize-1,-1):
        for j in range(w):
            screen.set_at((px+j,py+i),screen.get_at((px+j,py+i-dotscale*charsize)))

    for i in range(height-1,0,-1):
        for j in range(width):
            vvram[sx+j][sy+i]=vvram[sx+j][sy+i-1]
    locate(sx,sy)
    s=' '*width
    putstr(s)
    refresh()

def putchar(ch):
    global screen,curx,cury
    if ch=='\n':
        curx=0
        cury+=1
        if cury>=YSIZE:
            cury-=1
        return

    px=curx*dotscale*charsize
    py=cury*dotscale*charsize
    for i in range(8*8):
            c=color_ if chars[ord(ch)][i] else bgcolor_
            screen.fill(c,(px+i%8*dotscale,py+i//8*dotscale,dotscale,dotscale))
    if ch==' ':
        vvram[curx][cury]=chr(0)
    else:
        vvram[curx][cury]=ch
    move_curpos()

def move_curpos():
    global curx,cury
    curx+=1
    if curx>=XSIZE:
        curx=0
        cury+=1
        if cury>=YSIZE:
            cury-=1
            curx=XSIZE-1

def putstr(s):
    for ch in s:
        putchar(ch)

def peek(x,y):
    ch=vvram[x][y]
    return ch

def poke(x,y,c):
    global curx,cury
    sx=curx
    sy=cury
    locate(x,y)
    putchar(c)
    curx=sx
    cury=sy
    return

def clearscreen():
    global vvram,screen
    screen.fill((0,0,0)) # clear screen
    vvram=[[chr(0) for _ in range(25)] for __ in range(40)]
    return

def getkeys():
    getkeyboard()
    return keys

def getkey(k):
    if getkeys()[k]:
        return 1
    return 0

def getkeyboard():
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit(0)
        if event.type == KEYDOWN:  # キーを押したとき
            k=pygame.key.name(event.key)
            if len(k)==3 and k[1] in "0123456789.+-*/":
                k=k[1]
            keys[k]=1
            return k
        if event.type == KEYUP:    # キーを離したとき
            k=pygame.key.name(event.key)
            if len(k)==3 and k[1] in "0123456789.+-*/":
                k=k[1]
            keys[k]=0
            return ''
    return ''

def setscreen(title):
    global screen,keys
    pygame.init()    # Pygameを初期化
    screen = pygame.display.set_mode((XSIZE*charsize*dotscale,YSIZE*charsize*dotscale))    # 画面を作成
    pygame.display.set_caption(title)    # タイトルを作成
    loadchars()
    clearscreen()
    color((255,255,255))
    bgcolor((0,0,0))
    for _ in range(256):
        keys[chr(_)]=0
    return

def sleep(t):
    if (t<0.0001):
        getkeyboard()
        time.sleep(0.0001)
        return
    y=int(t/0.005)
    for i in range(y):
        time.sleep(0.0001)
        getkeyboard()

def quitsupertext():
    pygame.quit()

def refresh():
    pygame.display.update()

def main():
    setscreen("Supertext")
    color((0,255,0))
    putstr(" 0123456789ABCDEF\n")
    for i in range(0,16):
        color((0,255,0))
        locate(0,i+1)
        putchar(chr(0x30+i if i<10 else 0x41+i-10))
        color((255,255,255))
        for j in range(0,16):
            c=i*16+j
            locate(j+1,i+1)
            putchar(chr(c))

    locate(5,20)
    color((0,255,255))
    putstr("SUPERTEXT CODE and CHARACTERS")
    locate(5,21)
    color((0,0,255))
    putstr("Press 'q' key to quit.")
        
    refresh()

    while 1:
        if getkey('8'):
            scrollup(0,0,40,25)
        if getkey('2'):
            scrolldown(0,0,40,25)
        k=getkey('q')
        if k==1:
            quitsupertext()
            sys.exit()

if __name__=='__main__':
    main()
