#!/usr/bin/python3
from pygame.locals import *
from scipy import signal
import pygame
import sys
import numpy as np
import os
import binascii



scale=24
height=8
width=8
chars=[[0 for i in range(8*8)] for k in range(256)]

def draw_grid(screen):
  screen.fill((0,0,0))
  for i in range(width):
    pygame.draw.line(screen,(0,255,0),(0,i*scale),(scale*width,i*scale),1)
  for j in range(height):
    pygame.draw.line(screen,(0,255,0),(j*scale,0),(j*scale,scale*height),1)

def set(screen,cx,cy,c):
  screen.fill((c*255,c*255,c*255),(cx*scale+1,cy*scale+1,scale-1,scale-1))

def put(F,screen):
  for i in range(len(F)):
    for j in range(len(F[1])):
       set(screen,j,i,F[i][j])

def rev(F,cx,cy):
  F[cy][cx]=int(F[cy][cx])^1
  return(F)

def clear():
    return(np.zeros((height,width)))

def input_code():
    s=input("input character or hexadecimal code w/o 0x:")
    if len(s)==2:
        ch=int(s,16)
    else:
        ch=ord(s[0])
    return ch

def load_char(screen):
    ch=input_code()
    F=[]
    a=0
    for i in range(8):
        G=[]
        for j in range(8):
            G+=[chars[ch][a]]
            a+=1
        F+=[G]
    put(F,screen)
    return(F)

def save_char(F):
    ch=input_code()
    a=0
    for i in range(8):
        for j in range(8):
             chars[ch][a]=F[i][j]
             a+=1
def eventloop(F,screen):
    global chars
    run='e'
    while run!='q':
        for event in pygame.event.get():
            if event.type == QUIT:
                run='q'
            if event.type == KEYDOWN:  # キーを押したとき
                k=pygame.key.name(event.key)
                if k== 'q':
                    run='q'
                elif k=='l':
                    F=load_char(screen)
                elif k=='w':
                    print(f"file {charsfn} wrote.")
                    print(np.savetxt(charsfn, chars, "%d"))
                elif k=='s':
                    save_char(F)
                elif k=='c':
                    F=clear()
                    put(F,screen)
            elif event.type == MOUSEBUTTONDOWN:
                    x, y = event.pos
                    F=rev(F,x//scale,y//scale)
                    put(F,screen)
            elif event.type == MOUSEMOTION:
                    x, y = event.pos
        pygame.display.update()

def main():
    global chars
    pygame.init()    # Pygameを初期化
    screen = pygame.display.set_mode((scale*width,scale*height))    # 画面を作成
    pygame.display.set_caption("pattern editor")    # タイトルを作成
    draw_grid(screen)
    charsfn=sys.argv[1] if len(sys.argv)>=2 else "chars.txt"
    if os.path.exists(charsfn):
         chars = np.loadtxt(charsfn)
    F=clear()
    put(F,screen)
    eventloop(F,screen)
    pygame.quit()
    sys.exit()

if __name__=='__main__':
    main()
