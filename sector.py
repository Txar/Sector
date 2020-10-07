import pygame
import sys

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
pbX = [64, 640, 96] #pushblocks x
pbY = [64, 128, 64] #pushblocks y
bX = [] #blocks x
bY = [] #blocks y
rightPushable = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2] #list of pushblocks 1 = pushable to right, 0 = unpushable to right
leftPushable = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2] #same goes for those 3
upPushable = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2] #btw, pushblocks limit is 15 for a level
downPushable = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
DrightG, DleftG, DupG, DdownG = False, False, False, False #dont go right/left/up/down
levelsLoaded = 1

pygame.init()
dis = pygame.display.set_mode((width, height))
pygame.display.update()
pygame.display.set_caption("Sector")
clock = pygame.time.Clock()
pygame.mixer.music.load("theme1.mp3")
pygame.mixer.music.play(0)

def loadLevel():
    pygame.mixer.music.play()
    global levelsLoaded
    levelFile = open("levels/level" + str(levelsLoaded), "r")
    linesPlaced = 0
    while linesPlaced < 18:
        blocksPlaced = 0
        for albl in levelFile.readlines(linesPlaced + 1): #almost level blocks lines, basically a thing for levelBlocksLines
            albl = albl.replace("\n", "")
            levelBlocksLines = albl.split(" ")
            print(levelBlocksLines)
            while blocksPlaced < 25:
                if levelBlocksLines[blocksPlaced] == "01":
                    bX.append(blocksPlaced*32)
                    bY.append(linesPlaced*32)

                elif levelBlocksLines[blocksPlaced] == "02":
                    pbX.append(blocksPlaced*32)
                    pbY.append(linesPlaced*32)

                elif levelBlocksLines[blocksPlaced] == "03":
                    x = blocksPlaced*32
                    y = linesPlaced*32

                blocksPlaced = blocksPlaced + 1
            linesPlaced = linesPlaced + 1
    levelsLoaded = levelsLoaded + 1


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
        dis.blit(pushblockSprite, (pbX[pD], pbY[pD]))
        pD = pD + 1
    bD = 0 #blocks drawn
    while bD != len(bY):
        dis.blit(blockSprite, (bX[bD], bY[bD]))
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
    global rightG, leftG, upG, downG, DrightG, DleftG, DupG, DdownG
    DrightG, DleftG, DupG, DdownG = False, False, False, False
    while bC != len(bX):
        if rightG or leftG or upG or downG:
            if bX[bC] < x + 32 and bX[bC] > x - 8 and bY[bC] < y + 24 and bY[bC] > y - 24:
                DrightG = True
            elif bX[bC] > x - 32 and bX[bC] < x + 8 and bY[bC] < y + 24 and bY[bC] > y - 24:
                DleftG = True
            elif bY[bC] > y - 32 and bY[bC] < y - 8 and bX[bC] < x + 24 and bX[bC] > x - 24: 
                DupG = True
            elif bY[bC] < y + 32 and bY[bC] > y + 8 and bX[bC] < x + 24 and bX[bC] > x - 24: 
                DdownG = True
        bC = bC + 1

    while pC != len(pbX):
        if rightG or leftG or upG or downG:
            if pbX[pC] < x + 32 and pbX[pC] > x - 8 and pbY[pC] < y + 24 and pbY[pC] > y - 24:
                if rightPushable[pC] == 0:
                    DrightG = True
            elif pbX[pC] > x - 32 and pbX[pC] < x + 8 and pbY[pC] < y + 24 and pbY[pC] > y - 24:
                if leftPushable[pC] == 0:
                    DleftG = True
            elif pbY[pC] > y - 32 and pbY[pC] < y - 8 and pbX[pC] < x + 24 and pbX[pC] > x - 24: 
                if upPushable[pC] == 0:
                    DupG = True
            elif pbY[pC] < y + 32 and pbY[pC] > y + 8 and pbX[pC] < x + 24 and pbX[pC] > x - 24: 
                if downPushable[pC] == 0:
                    DdownG = True
        pC = pC + 1
loadLevel()

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
    if upG and not DupG:
        y = y - 3
    if leftG and not DleftG:
        x = x - 3
    if downG and not DdownG:
        y = y + 3
    if rightG and not DrightG:
        x = x + 3
    movePushblocks()
    drawFloor()
    drawPlayer(x, y)
    drawAllBlocks()
    pygame.display.update()
    clock.tick(30)

pygame.quit()
sys.exit()