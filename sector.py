import pygame, sys, os, math, random
from collections import namedtuple

Vec2 = namedtuple('Vec2', 'x y')

radDeg = 180 / math.pi

# Vec2's
def angleTo(a, b):
    ang = math.atan2(b.x - a.x, b.y - a.y) * radDeg
    if(ang < 0): ang += 360
    return ang

def dst(a, b):
    x_d = b.x - a.x
    y_d = b.y - a.y
    return math.sqrt(x_d ** 2 + y_d ** 2)

def shadow(a, b):
    return round(angleTo(a, b), 2)


# example: angle = shadow(a, b)


#Sector by Txar
#big thanks to Xelo and ThePythonGuy3 as they helped me with some of the code <3
devMode = False
width = 800
height = 576
gameOver = False
wholeLevel = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
gameMode = 0 #0 is menu, 1 is level, 2 is level select
playerSprite = pygame.image.load("sprites/player.png")
playerRightSprite = pygame.image.load("sprites/playerRight.png")
playerLeftSprite = pygame.image.load("sprites/playerLeft.png")
playerBackSprite = pygame.image.load("sprites/playerBack.png")
shadowSprite = pygame.image.load("sprites/shadow.png")
pushblockSprite = pygame.image.load("sprites/pushblock.png")
floorSprite = pygame.image.load("sprites/floorTile.png")
blockSprite = pygame.image.load("sprites/block.png")
holeSprite = pygame.image.load("sprites/hole.png")
sectorIcon = pygame.image.load("sprites/icon.png")
restartButtonSprite = pygame.image.load("sprites/restartButton.png")
playButtonSprite = pygame.image.load("sprites/playButton.png")
editorButtonSprite = pygame.image.load("sprites/pencil.png")
exitButtonSprite = pygame.image.load("sprites/exitButton.png")
rightArrowSprite = pygame.image.load("sprites/arrowRight.png")
leftArrowSprite = pygame.image.load("sprites/arrowLeft.png")
tilesSprites = pygame.image.load("sprites/tiles.png")
railSprite = pygame.image.load("sprites/rail.png")
wallsSprite = pygame.Surface((width, height))

true = True #this made me laugh so hard that i will just leave it here
playerFacing = 0
x = 400 #player x
y = 300 #player y
upG = False #up go (for player)
leftG = False #left go (for player)
downG = False #down go (for player)
rightG = False #right go (for player)
mouseKeyPressed = False #do i need to explain this?
levelsCompleted = [0] # *useful comment*
pbX = [] #pushblocks x
pbY = [] #pushblocks y
bX = [] #blocks x
bY = [] #blocks y
hX = [] #holes x
hY = [] #holes y
hrX = [] #horizontal rails x
hrY = [] #horizontal rails y

restartButton = [768, 0] #restart button coordinates
playButton = [304, 256] #play button coordinates
editorButton = [368, 256] #level editor coordinates
exitButton = [432, 256] #exit button coordinates
rightButton = [768, 256] #right arrow button coordinates
leftButton = [0, 256] #left arrow button coordinates  

levelExit = [0, 0] #exit coordinates
rightPushable = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2] #list of pushblocks 1 = pushable to right, 0 = unpushable to right
leftPushable = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2] #same goes for those 3
upPushable = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2] #btw, pushblocks limit is 15 for a level because im stupid
downPushable = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
DrightG, DleftG, DupG, DdownG = False, False, False, False #dont go right/left/up/down
levelsLoaded = 1
lC = 1 #levels checked
while True:
    filename = "levels/level" + str(lC) + ".srlv"
    if not os.path.exists(filename):
        progressSave = open("data/progress.srgd", "r")
        levelsCompleted = progressSave.readlines(1)
        levelsLoaded = int(levelsCompleted[0]) + 1
        progressSave.close()
        existingLevels = lC
        break
    lC = lC + 1

def generateWalls():
    if levelsLoaded >= int(levelsCompleted[0]) + 2 or levelsLoaded >= existingLevels:
        return
    global wallsSprite, bX, bY, wholeLevel
    columnPixel = -32
    rowPixel = -32
    for rD in range(0, 18):
        for cD in range(0, 25):
            variant = random.randint(0, 7)
            wallsSprite.blit(tilesSprites, (columnPixel + 32, rowPixel + 32), (0, variant * 32, 32, variant * 32 + 32)) 
            columnPixel = columnPixel + 32
        columnPixel = -32
        rowPixel = rowPixel + 32

    for rD in range(0, 18):
        for cD in range(0, 25):
            mask = 0
            x = cD * 32
            y = rD * 32
            if wholeLevel[rD][cD] == "06":
                if cD + 1 < 25:
                    if wholeLevel[rD][cD + 1] == "06":
                        mask = mask + 1
                if cD - 1 < 25:
                    if wholeLevel[rD][cD - 1] == "06":
                        mask = mask + 2
                wallsSprite.blit(railSprite, (x, y), (mask * 32, 0, 32, 32))


    for columnsGenerated in range(0, 25):
        for rowsGenerated in range(0, 18):
            mask = 0
            x = columnsGenerated * 32
            y = rowsGenerated * 32
            if wholeLevel[rowsGenerated][columnsGenerated] == "01":
                if rowsGenerated + 1 < 18:
                    if wholeLevel[rowsGenerated + 1][columnsGenerated] == "01":
                        mask = mask + 8
                if wholeLevel[rowsGenerated][columnsGenerated - 1] == "01":
                    mask = mask + 4
                if wholeLevel[rowsGenerated - 1][columnsGenerated] == "01":
                    mask = mask + 2
                if columnsGenerated + 1 < 25:
                    if wholeLevel[rowsGenerated][columnsGenerated + 1] == "01":
                        mask = mask + 1
                variant = random.randint(0, 0)
                wallsSprite.blit(blockSprite, (x, y), (mask * 32, variant * 32, 32, variant * 32 + 32))

def saveProgress():
    progressData = open("data/progress.srgd", "w")
    pds = int(levelsCompleted[0])
    progressData.writelines(str(pds))
    progressData.close()

def loadLevel():
    global levelsLoaded, x, y, pbX, pbY, bX, bY, hX, hY, hrX, hrY, existingLevels, gameMode, levelsCompleted, wholeLevel
    wholeLevel = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
    pbX = [] #pushblocks x
    pbY = [] #pushblocks y
    bX = [] #blocks x
    bY = [] #blocks y
    hX = [] #holes x
    hY = [] #holes y
    hrX = [] #horizontal rails x
    hrY = [] #horizontal rails y
    #pygame.mixer.music.play()
    if levelsLoaded >= int(levelsCompleted[0]) + 2 or levelsLoaded >= existingLevels:
        gameMode = 0
        return
    filename = "levels/level" + str(levelsLoaded) + ".srlv"
    levelFile = open(filename, "r")
    linesPlaced = 0

    loadedLevel = open(filename)
    for rowsLoaded in range(0, 18):
        wholeLevel[rowsLoaded].append(loadedLevel.readlines(rowsLoaded + 1))
        wholeLevel[rowsLoaded] = str(wholeLevel[rowsLoaded]).replace("\\n", "")
        wholeLevel[rowsLoaded] = str(wholeLevel[rowsLoaded]).replace("[['", "") #yes, what the fuck?
        wholeLevel[rowsLoaded] = str(wholeLevel[rowsLoaded]).replace("']]", "") #i actually dont know ;-;
        wholeLevel[rowsLoaded] = wholeLevel[rowsLoaded].split(" ")
    loadedLevel.close()

    while linesPlaced < 18:
        blocksPlaced = 0
        for albl in levelFile.readlines(linesPlaced + 1): #almost level blocks lines, basically a thing for levelBlocksLines
            albl = albl.replace("\n", "")
            levelBlocksLines = albl.split(" ")
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

                elif levelBlocksLines[blocksPlaced] == "04":
                    hX.append(blocksPlaced*32)
                    hY.append(linesPlaced*32)

                elif levelBlocksLines[blocksPlaced] == "05":
                    levelExit[0] = blocksPlaced*32
                    levelExit[1] = linesPlaced*32

                elif levelBlocksLines[blocksPlaced] == "06":
                    hrX.append(blocksPlaced*32)
                    hrY.append(linesPlaced*32)

                blocksPlaced = blocksPlaced + 1
            linesPlaced = linesPlaced + 1
    levelFile.close()

#bugi ono (buggy ohno)

def getLights():
    lights = []
    if(len(pbX) > 0):
        for i in range(len(pbX)):
            lights.append(Vec2(pbX[i], pbY[i]))
    return lights

def drawShadows(a):
    b = Vec2(a.x+16, a.y+16)
    a = b
    lights = getLights()
    if(len(lights) <= 0):
        dis.blit(shadowSprite, (a.x, a.y))
    else:
        for i in lights:
            angle = shadow(a, i)
            shadow_rect = shadowSprite.get_rect(center = (a.x, a.y))
            shadowScale = pygame.transform.scale(shadowSprite, (int(128 - max(0, min(dst(a, i), 64))/2), 32))
            shadowRot = pygame.transform.rotozoom(shadowScale, angle+90, 1)
            shadowDraw = shadowRot.get_rect(center = (a.x, a.y))
            dis.blit(shadowRot, shadowDraw)
        
def drawPlayer(x, y):
    drawShadows(Vec2(x, y))
    if playerFacing == 0:
        dis.blit(playerSprite, (x, y))
    elif playerFacing == 1:
        dis.blit(playerLeftSprite, (x, y))
    elif playerFacing == 2:
        dis.blit(playerBackSprite, (x, y))
    elif playerFacing == 3:
        dis.blit(playerRightSprite, (x, y))
    

def drawAllBlocks(): #draws blocks and pushblocks
    dis.blit(wallsSprite, (0, 0))
    hD = 0 #holes drawn
    while hD != len(hX):
        dis.blit(holeSprite, (hX[hD], hY[hD]))
        hD = hD + 1
    pD = 0 #pushblocks drawn
    while pD != len(pbX):
        dis.blit(pushblockSprite, (pbX[pD], pbY[pD]))
        pD = pD + 1

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

        if pbX[pM] < x + 32 and pbX[pM] > x and pbY[pM] < y + 24 and pbY[pM] > y - 24:
            pm2 = 0
            mr = True
            cipbcm = 0
            while cipbcm != len(bX):
                if bX[cipbcm] < pbX[pM] + 32 and bX[cipbcm] > pbX[pM] and bY[cipbcm] < pbY[pM] + 24 and bY[cipbcm] > pbY[pM] - 24:
                    mr = False
                    rightPushable[pM] = 0
                cipbcm = cipbcm + 1
            while pm2 != len(pbX):
                if pm2 != pM:
                    if pbX[pM] > pbX[pm2] - 32 and pbX[pM] < pbX[pm2] and pbY[pM] < pbY[pm2] + 24 and pbY[pM] > pbY[pm2] - 24:
                        rightPushable[pM] = 0
                        mr = False
                pm2 = pm2 + 1
            if mr:
                pbX[pM] = pbX[pM] + 4

        elif pbX[pM] > x - 32 and pbX[pM] < x and pbY[pM] < y + 24 and pbY[pM] > y - 24:
            pm2 = 0
            ml = True
            cipbcm = 0
            while cipbcm != len(bX):
                if bX[cipbcm] > pbX[pM] - 32 and bX[cipbcm] < pbX[pM] and bY[cipbcm] < pbY[pM] + 24 and bY[cipbcm] > pbY[pM] - 24:
                    ml = False
                    leftPushable[pM] = 0
                cipbcm = cipbcm + 1
            while pm2 != len(pbX):
                if pm2 != pM:
                    if pbX[pM] < pbX[pm2] + 32 and pbX[pM] > pbX[pm2] and pbY[pM] < pbY[pm2] + 24 and pbY[pM] > pbY[pm2] - 24:
                        leftPushable[pM] = 0
                        ml = False
                pm2 = pm2 + 1
            if ml:
                pbX[pM] = pbX[pM] - 4

        elif pbY[pM] > y - 32 and pbY[pM] < y and pbX[pM] < x + 24 and pbX[pM] > x - 24: 
            pm2 = 0
            mu = True
            cipbcm = 0
            while cipbcm != len(bY):
                if bY[cipbcm] > pbY[pM] - 32 and bY[cipbcm] < pbY[pM] and bX[cipbcm] < pbX[pM] + 24 and bX[cipbcm] > pbX[pM] - 24:
                    mu = False
                    upPushable[pM] = 0
                cipbcm = cipbcm + 1
            while pm2 != len(pbX):
                if pm2 != pM:
                    if pbY[pM] < pbY[pm2] + 32 and pbY[pM] > pbY[pm2] and pbX[pM] < pbX[pm2] + 24 and pbX[pM] > pbX[pm2] - 24:
                        upPushable[pM] = 0
                        mu = False
                pm2 = pm2 + 1
            cipbcm = 0
            while cipbcm != len(hrY):
                if hrY[cipbcm] > pbY[pM] - 32 and hrY[cipbcm] < pbY[pM] and hrX[cipbcm] < pbX[pM] + 24 and hrX[cipbcm] > pbX[pM] - 24:
                    mu = False
                    upPushable[pM] = 0
                cipbcm = cipbcm + 1
            if mu:
                pbY[pM] = pbY[pM] - 4

        elif pbY[pM] < y + 32 and pbY[pM] > y and pbX[pM] < x + 24 and pbX[pM] > x - 24:
            pm2 = 0
            md = True
            cipbcm = 0
            while cipbcm != len(bY):
                if bY[cipbcm] < pbY[pM] + 32 and bY[cipbcm] > pbY[pM] and bX[cipbcm] < pbX[pM] + 24 and bX[cipbcm] > pbX[pM] - 24:
                    md = False
                    downPushable[pM] = 0
                cipbcm = cipbcm + 1
            while pm2 != len(pbX):
                if pm2 != pM:
                    if pbY[pM] > pbY[pm2] - 32 and pbY[pM] < pbY[pm2] and pbX[pM] < pbX[pm2] + 24 and pbX[pM] > pbX[pm2] - 24:
                        downPushable[pM] = 0
                        md = False
                pm2 = pm2 + 1
            cipbcm = 0
            while cipbcm != len(hrY):
                if hrY[cipbcm] < pbY[pM] + 32 and hrY[cipbcm] > pbY[pM] and hrX[cipbcm] < pbX[pM] + 24 and hrX[cipbcm] > pbX[pM] - 24:
                    md = False
                    downPushable[pM] = 0
                cipbcm = cipbcm + 1
            if md:
                pbY[pM] = pbY[pM] + 4
        pM = pM + 1
    #if mu or mr or ml or md:
        #pushblockSound.play()

def roundTo32(x, base = 32):
    return int(base * math.ceil(float(x) / base) - 32)

def cheat():
    if summonBox:
        if playerFacing == 0:
            pbX.append(x)
            pbY.append(y + 32)
        if playerFacing == 1:
            pbX.append(x - 32)
            pbY.append(y)
        if playerFacing == 2:
            pbX.append(x)
            pbY.append(y - 32)
        if playerFacing == 3:
            pbX.append(x + 32)
            pbY.append(y)
    if summonWall:
        if playerFacing == 0:
            bX.append(x)
            bY.append(y + 32)
        if playerFacing == 1:
            bX.append(x - 32)
            bY.append(y)
        if playerFacing == 2:
            bX.append(x)
            bY.append(y - 32)
        if playerFacing == 3:
            bX.append(x + 32)
            bY.append(y)

def checkInteractiveBlocks():
    hC = 0 #holess checked
    while hC != len(hY):
        pC = 0 #pushblocks checked
        while pC != len(pbY):
            if pbX[pC] + 31 >= hX[hC] and pbX[pC] <= hX[hC] + 31 and pbY[pC] + 31 >= hY[hC] and pbY[pC] <= hY[hC] + 31:
                #drawFallingBlock(hX[hC], hY[hC]) 
                pbX.pop(pC)
                pbY.pop(pC)
                hX.pop(hC)
                hY.pop(hC)
                hC = hC - 1
                break
            pC = pC + 1
        hC = hC + 1

def checkPlayerCollisions(): #this checks for blocks collisions with player
    global levelsCompleted, levelsLoaded
    if levelExit[0] >= x - 8 and levelExit[0] <= x + 40 and levelExit[1] >= y - 8 and levelExit[1] <= y + 40:
        if levelsLoaded > int(levelsCompleted[0]):
            levelsCompleted[0] = int(levelsCompleted[0]) + 1
            levelsLoaded = levelsLoaded + 1
        else:
            levelsLoaded = levelsLoaded + 1
        saveProgress()
        loadLevel()
        generateWalls()
    bC = 0 #blocks checked
    pC = 0 #pushblocks checked
    global rightG, leftG, upG, downG, DrightG, DleftG, DupG, DdownG
    DrightG, DleftG, DupG, DdownG = False, False, False, False
    while bC != len(bX):
        if rightG or leftG or upG or downG:
            if bX[bC] < x + 32 and bX[bC] > x and bY[bC] < y + 24 and bY[bC] > y - 24:
                DrightG = True
            elif bX[bC] > x - 32 and bX[bC] < x and bY[bC] < y + 24 and bY[bC] > y - 24:
                DleftG = True
            elif bY[bC] > y - 32 and bY[bC] < y and bX[bC] < x + 24 and bX[bC] > x - 24: 
                DupG = True
            elif bY[bC] < y + 32 and bY[bC] > y and bX[bC] < x + 24 and bX[bC] > x - 24: 
                DdownG = True
        bC = bC + 1

    while pC != len(pbX):
        if rightG or leftG or upG or downG:
            if pbX[pC] < x + 32 and pbX[pC] > x and pbY[pC] < y + 24 and pbY[pC] > y - 24:
                if rightPushable[pC] == 0:
                    DrightG = True
            elif pbX[pC] > x - 32 and pbX[pC] < x and pbY[pC] < y + 24 and pbY[pC] > y - 24:
                if leftPushable[pC] == 0:
                    DleftG = True
            elif pbY[pC] > y - 32 and pbY[pC] < y and pbX[pC] < x + 24 and pbX[pC] > x - 24: 
                if upPushable[pC] == 0:
                    DupG = True
            elif pbY[pC] < y + 32 and pbY[pC] > y and pbX[pC] < x + 24 and pbX[pC] > x - 24: 
                if downPushable[pC] == 0:
                    DdownG = True
        pC = pC + 1
    hC = 0
    while hC != len(hX):
        if rightG or leftG or upG or downG:
            if hX[hC] < x + 32 and hX[hC] > x and hY[hC] < y + 24 and hY[hC] > y - 24:
                DrightG = True
            elif hX[hC] > x - 32 and hX[hC] < x and hY[hC] < y + 24 and hY[hC] > y - 24:
                DleftG = True
            elif hY[hC] > y - 32 and hY[hC] < y and hX[hC] < x + 24 and hX[hC] > x - 24: 
                DupG = True
            elif hY[hC] < y + 32 and hY[hC] > y and hX[hC] < x + 24 and hX[hC] > x - 24: 
                DdownG = True
        hC = hC + 1
    for hrC in range(0, len(hrX)):
        if upG or downG:
            if hrY[hrC] > y - 32 and hrY[hrC] < y and hrX[hrC] < x + 24 and hrX[hrC] > x - 24: 
                DupG = True
            elif hrY[hrC] < y + 32 and hrY[hrC] > y and hrX[hrC] < x + 24 and hrX[hrC] > x - 24: 
                DdownG = True

def checkMouseButtons():
    global levelsLoaded, gameMode, levelsCompleted, levelsLoaded, mouseKeyPressed, existingLevels
    mousePos = pygame.mouse.get_pos()
    if gameMode == 1:
        if mousePos[0] < restartButton[0] + 32 and mousePos[0] > restartButton[0] and mousePos[1] > restartButton[1] and mousePos[1] < restartButton[1] + 32:
            loadLevel()
            generateWalls()

    elif gameMode == 0:
        if mousePos[0] < playButton[0] + 32 and mousePos[0] > playButton[0] and mousePos[1] > playButton[1] and mousePos[1] < playButton[1] + 32:
            if levelsLoaded >= int(levelsCompleted[0]) + 2 or levelsLoaded >= existingLevels:
                levelsLoaded = levelsLoaded - 1
            gameMode = 2
            loadLevel()
            generateWalls()
        elif mousePos[0] < editorButton[0] + 32 and mousePos[0] > editorButton[0] and mousePos[1] > editorButton[1] and mousePos[1] < editorButton[1] + 32:
            pygame.quit()
            os.system("python " + "levelEditor.py")
            sys.exit()
        elif mousePos[0] < exitButton[0] + 32 and mousePos[0] > exitButton[0] and mousePos[1] > exitButton[1] and mousePos[1] < exitButton[1] + 32:
            pygame.quit()
            sys.exit()

    elif gameMode == 2:
        if mousePos[0] < rightButton[0] + 32 and mousePos[0] > rightButton[0] and mousePos[1] > rightButton[1] and mousePos[1] < rightButton[1] + 32:
            if levelsLoaded < int(levelsCompleted[0]) + 1:
                levelsLoaded = levelsLoaded + 1
                loadLevel()
                generateWalls()
        if mousePos[0] < leftButton[0] + 32 and mousePos[0] > leftButton[0] and mousePos[1] > leftButton[1] and mousePos[1] < leftButton[1] + 32:
            if levelsLoaded > 1:
                levelsLoaded = levelsLoaded - 1
                loadLevel()
                generateWalls()
        if mousePos[0] < playButton[0] + 32 and mousePos[0] > playButton[0] and mousePos[1] > playButton[1] and mousePos[1] < playButton[1] + 32:
            generateWalls()
            gameMode = 1
        if mousePos[0] < exitButton[0] + 32 and mousePos[0] > exitButton[0] and mousePos[1] > exitButton[1] and mousePos[1] < exitButton[1] + 32:
            gameMode = 0

def drawUi():
    global gameMode, playButton, exitButton
    if gameMode == 1:
        dis.blit(restartButtonSprite, (restartButton[0], restartButton[1]))
    if gameMode == 0:
        playButton = [304, 256]
        exitButton = [432, 256]
        dis.blit(playButtonSprite, (playButton[0], playButton[1]))
        dis.blit(editorButtonSprite, (editorButton[0], editorButton[1]))
        dis.blit(exitButtonSprite, (exitButton[0], exitButton[1]))
    if gameMode == 2:
        playButton = [704, 0]
        exitButton = [768, 0]
        dis.blit(playButtonSprite, (playButton[0], playButton[1]))
        dis.blit(exitButtonSprite, (exitButton[0], exitButton[1]))
        dis.blit(rightArrowSprite, (rightButton[0], rightButton[1]))
        dis.blit(leftArrowSprite, (leftButton[0], leftButton[1]))

pygame.init()
dis = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sector")
clock = pygame.time.Clock()
pygame.mixer.music.load("sounds/theme1.mp3")
pygame.display.set_icon(sectorIcon)
pushblockSound = pygame.mixer.Sound("sounds/pbs.wav")

while not gameOver:
    summonBox, summonWall, destroyWall = False, False, False
    mouseKeyPressed = False
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
            if event.key == pygame.K_r:
                loadLevel()
                generateWalls()
            if event.key == pygame.K_p:
                summonBox = True
            if event.key == pygame.K_i:
                summonWall = True
        if gameMode == 0:
            x = 0
            y = 0
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseKeyPressed = True
    if gameMode == 1:
        checkPlayerCollisions()
    if gameMode != 1:
        DupG, DleftG, DdownG, DrightG = True, True, True, True
    if upG and not DupG:
        playerFacing = 2
        y = y - 4
    if leftG and not DleftG:
        playerFacing = 1
        x = x - 4
    if downG and not DdownG:
        playerFacing = 0
        y = y + 4
    if rightG and not DrightG:
        playerFacing = 3
        x = x + 4
    checkInteractiveBlocks()
    movePushblocks()
    drawAllBlocks()
    drawPlayer(x, y)
    if mouseKeyPressed:
        checkMouseButtons()
    if devMode: #i find these 2 lines so funny
        cheat()
    drawUi()
    pygame.display.update()
    clock.tick(30)

pygame.quit()
sys.exit()
