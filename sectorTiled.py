import pygame
import sys
from math import *

#Sector by Txar

width = 800
height = 576
gameOver = False
playerSprite = pygame.image.load("pushblock.png")
pushblockSprite = pygame.image.load("pushblock.png")
floorSprite = pygame.image.load("floortile.png")
blockSprite = pygame.image.load("block.png")

x = 400 #player x
y = 300 #player y
upG = False #up go (for player)
leftG = False #left go (for player)
downG = False #down go (for player)
rightG = False #right go (for player)
pbX = [64, 640] #pushblocks x
pbY = [64, 128] #pushblocks y
bX = [128, 160, 192] #blocks x
bY = [64, 64, 64] #blocks y
rightPushable = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2] #list of pushblocks 1 = pushable to right, 0 = unpushable to right
leftPushable = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2] #same goes for those 3
upPushable = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2] #btw, pushblocks limit is 15 for a level
downPushable = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]

pygame.init()
dis = pygame.display.set_mode((width, height))
pygame.display.update()
pygame.display.set_caption("Sector")
clock = pygame.time.Clock()

def drawPlayer(x, y):
    dis.blit(playerSprite, (x, y))
    
def drawFloor():
    cD = 0 #columns drawn
    rD = 0 #rows drawn
    columnPixel = -32
    rowPixel = -32
    while rD < 18:
        while cD < 25:
            dis.blit(floorSprite, (columnPixel + 32, rowPixel + 32)) 
            columnPixel = columnPixel + 32
            cD = cD + 1
        cD = 0
        columnPixel = -32
        rowPixel = rowPixel + 32
        rD = rD + 1

def drawAllBlocks(): #draws blocks and pushblocks
    pD = 0 #pushblocks drawn
    while pD != len(pbX):
        dis.blit(pushblockSprite, (round(pbX[pD]/32)*32, round(pbY[pD]/32)*32))
        pD = pD + 1
    bD = 0 #blocks drawn
    while bD != len(bX):
        dis.blit(blockSprite, (round(bX[pD]/32)*32, round(bY[pD]/32)*32))
        bD = bD + 1

def movePushblocks(): #moves pushblocks (how unexpected, huh?)
    pM = 0 #pushblocks moved
    cipbcm = 0 #checked if pushblock can move, yes im good at naming
    
    global downPushable, upPushable, leftPushable, rightPushable, md, mr, ml, mu
    mu = False
    ml = False
    md = False
    mr = False
    while pM != len(pbX): #this loop checks if theyre blocks next to pushblocks
        downPushable[pM] = 1
        upPushable[pM] = 1
        leftPushable[pM] = 1
        rightPushable[pM] = 1

        if pbX[pM] < x + 32 and pbX[pM] > x - 8 and pbY[pM] < y + 24 and pbY[pM] > y - 24:
            pm2 = 0
            mr = True
            cipbcm = 0
            while cipbcm != len(bX):
                if bX[cipbcm] < pbX[pM] + 32 and bX[cipbcm] > pbX[pM] - 8 and bY[cipbcm] < pbY[pM] + 24 and bY[cipbcm] > pbY[pM] - 24:
                    mr = False
                    rightPushable[pM] = 0
                cipbcm = cipbcm + 1
            while pm2 != len(pbX):
                if pm2 != pM:
                    if pbX[pM] > pbX[pm2] - 32 and pbX[pM] < pbX[pm2] + 8 and pbY[pM] < pbY[pm2] + 24 and pbY[pM] > pbY[pm2] - 24:
                        rightPushable[pM] = 0
                        mr = False
                pm2 = pm2 + 1
            if mr:
                pbX[pM] = pbX[pM] + 3

        elif pbX[pM] > x - 32 and pbX[pM] < x + 8 and pbY[pM] < y + 24 and pbY[pM] > y - 24:
            pm2 = 0
            ml = True
            cipbcm = 0
            while cipbcm != len(bX):
                if bX[cipbcm] > pbX[pM] - 32 and bX[cipbcm] < pbX[pM] + 8 and bY[cipbcm] < pbY[pM] + 24 and bY[cipbcm] > pbY[pM] - 24:
                    ml = False
                    leftPushable[pM] = 0
                cipbcm = cipbcm + 1
            while pm2 != len(pbX):
                if pm2 != pM:
                    if pbX[pM] < pbX[pm2] + 32 and pbX[pM] > pbX[pm2] - 8 and pbY[pM] < pbY[pm2] + 24 and pbY[pM] > pbY[pm2] - 24:
                        leftPushable[pM] = 0
                        ml = False
                pm2 = pm2 + 1
            if ml:
                pbX[pM] = pbX[pM] - 3

        elif pbY[pM] > y - 32 and pbY[pM] < y - 8 and pbX[pM] < x + 24 and pbX[pM] > x - 24: 
            pm2 = 0
            mu = True
            cipbcm = 0
            while cipbcm != len(bY):
                if bY[cipbcm] > pbY[pM] - 32 and bY[cipbcm] < pbY[pM] + 8 and bX[cipbcm] < pbX[pM] + 24 and bX[cipbcm] > pbX[pM] - 24:
                    mu = False
                    upPushable[pM] = 0
                cipbcm = cipbcm + 1
            while pm2 != len(pbX):
                if pm2 != pM:
                    if pbY[pM] < pbY[pm2] + 32 and pbY[pM] > pbY[pm2] - 8 and pbX[pM] < pbX[pm2] + 24 and pbX[pM] > pbX[pm2] - 24:
                        upPushable[pM] = 0
                        mu = False
                pm2 = pm2 + 1
            if mu:
                pbY[pM] = pbY[pM] - 3

        elif pbY[pM] < y + 32 and pbY[pM] > y + 8 and pbX[pM] < x + 24 and pbX[pM] > x - 24:
            pm2 = 0
            md = True
            cipbcm = 0
            while cipbcm != len(bY):
                if bY[cipbcm] < pbY[pM] + 32 and bY[cipbcm] > pbY[pM] - 8 and bX[cipbcm] < pbX[pM] + 24 and bX[cipbcm] > pbX[pM] - 24:
                    md = False
                    downPushable[pM] = 0
                cipbcm = cipbcm + 1
            while pm2 != len(pbX):
                if pm2 != pM:
                    if pbY[pM] > pbY[pm2] - 32 and pbY[pM] < pbY[pm2] + 8 and pbX[pM] < pbX[pm2] + 24 and pbX[pM] > pbX[pm2] - 24:
                        downPushable[pM] = 0
                        md = False
                pm2 = pm2 + 1
            if md:
                pbY[pM] = pbY[pM] + 3
        pM = pM + 1

def checkPlayerCollisions(): #this checks for blocks collisions with player
    bC = 0 #blocks checked
    pC = 0 #pushblocks checked
    global rightG, leftG, upG, downG
    while bC != len(bX):
        if rightG or leftG or upG or downG:
            if bX[bC] < x + 32 and bX[bC] > x - 8 and bY[bC] < y + 24 and bY[bC] > y - 24:
                rightG = False
            elif bX[bC] > x - 32 and bX[bC] < x + 8 and bY[bC] < y + 24 and bY[bC] > y - 24:
                leftG = False
            elif bY[bC] > y - 32 and bY[bC] < y - 8 and bX[bC] < x + 24 and bX[bC] > x - 24: 
                upG = False
            elif bY[bC] < y + 32 and bY[bC] > y + 8 and bX[bC] < x + 24 and bX[bC] > x - 24: 
                downG = False
        bC = bC + 1

    while pC != len(pbX):
        if rightG or leftG or upG or downG:
            if pbX[pC] < x + 32 and pbX[pC] > x - 8 and pbY[pC] < y + 24 and pbY[pC] > y - 24:
                if rightPushable[pC] == 0:
                    rightG = False
            elif pbX[pC] > x - 32 and pbX[pC] < x + 8 and pbY[pC] < y + 24 and pbY[pC] > y - 24:
                if leftPushable[pC] == 0:
                    leftG = False
            elif pbY[pC] > y - 32 and pbY[pC] < y - 8 and pbX[pC] < x + 24 and pbX[pC] > x - 24: 
                if upPushable[pC] == 0:
                    upG = False
            elif pbY[pC] < y + 32 and pbY[pC] > y + 8 and pbX[pC] < x + 24 and pbX[pC] > x - 24: 
                if downPushable[pC] == 0:
                    downG = False
        pC = pC + 1


while not gameOver:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                upG = True
            if event.key == pygame.K_a:
                leftG = True
            if event.key == pygame.K_s:
                downG = True
            if event.key == pygame.K_d:
                rightG = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                upG = False
            if event.key == pygame.K_a:
                leftG = False
            if event.key == pygame.K_s:
                downG = False
            if event.key == pygame.K_d:
                rightG = False
        if event.type == pygame.QUIT:
            gameOver = True
    checkPlayerCollisions()
    if upG:
        y = y - 3
    if leftG:
        x = x - 3
    if downG:
        y = y + 3
    if rightG:
        x = x + 3
    movePushblocks()
    drawFloor()
    drawPlayer(round(x/32)*32, round(y/32)*32)
    drawAllBlocks()
    pygame.display.update()
    clock.tick(30)

pygame.quit()
sys.exit()