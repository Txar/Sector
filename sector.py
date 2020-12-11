import pygame, sys, os, math, random
from collections import namedtuple

#Sector by Txar
#big thanks to Xeloboyo and ThePythonGuy3 as they helped me with some of the code <3

version = "pre-alpha 0.1"
sys.stderr = open("log.txt", "r+")
sys.stdout = sys.stderr
command = ""
console = ""
firstTime = False
if not os.path.exists("data/progress.srgd"):
    firstTime = True
    progressData = open("data/progress.srgd", "w")
    progressData.writelines("0")
    progressData.close()
consoleOn = False
pygame.font.init()
consolas = pygame.font.SysFont("consolas", 23)
consoleFont = pygame.font.SysFont("consolas", 16)
fpsSettingTitle = consolas.render("FPS", False, (70, 185, 35))
commandRender = consoleFont.render("> ", False, (255, 255, 255))
versionRender = consoleFont.render(version, False, (255, 255, 255))
brightnessSettingTitle = consolas.render("brightness", False, (70, 185, 35))
levelToLoad = "backgroundLevel"
bgx = 0 #background x
Vec2 = namedtuple('Vec2', 'x y')
radDeg = 180 / math.pi
devMode = True #allows to place walls and pushblocks (by pressing i and p) when True, you can change it in console (which is accesed by pressing F1)
width = 800
height = 576
gameOver = False
wholeLevel = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
lightMap = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
gameMode = 0 #0 is menu, 1 is level, 2 is level select
sectorTitleSprite = pygame.image.load("sprites/sectorTitle.png")
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
settingsButtonSprite = pygame.image.load("sprites/settingsButton.png")
plusButtonSprite = pygame.image.load("sprites/plusButton.png")
settingsDisplay = pygame.image.load("sprites/settingsDisplay1.png")
settingsDisplayWide = pygame.image.load("sprites/settingsDisplay2.png")
minusButtonSprite = pygame.image.load("sprites/minusButton.png")
rightArrowSprite = pygame.image.load("sprites/arrowRight.png")
leftArrowSprite = pygame.image.load("sprites/arrowLeft.png")
tilesSprites = pygame.image.load("sprites/tiles.png")
railSprite = pygame.image.load("sprites/rail.png")
lampSprite = pygame.image.load("sprites/lamp.png")
lightLevelsSprite = pygame.image.load("sprites/lightLevels.png")
wallsSprite = pygame.Surface((width, height), pygame.SRCALPHA)
floorSprite = pygame.Surface((width, height))
dis = pygame.Surface((width, height))
lightSprite = pygame.Surface((width, height), pygame.SRCALPHA)
menuBackground = pygame.Surface((width, height))
playerFacing = 0
backGroundPos = 0
x = 400 #player x
y = 300 #player y
cy = 0 #console y
upG = False #up go (for player)
leftG = False #left go (for player)
downG = False #down go (for player)
rightG = False #right go (for player)
mouseKeyPressed = False #do i need to explain this?
levelsCompleted = [0] # *useful comment*
fpsLimit = 30
brightness = 0
playerSpeed = 4
settingSelected = 2 #0 is brightness, 2 is fps
pbX = [] #pushblocks x
pbY = [] #pushblocks y
bX = [] #blocks x
bY = [] #blocks y
hX = [] #holes x
hY = [] #holes y
hrX = [] #horizontal rails x
hrY = [] #horizontal rails y
lX = [] #lamps x
lY = [] #lamps y
fpsLimitSettingRender = consolas.render(str(fpsLimit), False, (70, 185, 35))
brightnessSettingRender = consolas.render(str(brightness), False, (70, 185, 35))
sectorTitle = [232, 128] #menu title coordinates
restartButton = [736, 0] #restart button coordinates
playButton = [320, 256] #play button coordinates
editorButton = [416, 256] #level editor button coordinates
settingsButton = [352, 256] #settings button coordinates
exitButton = [448, 256] #exit button coordinates
plusButton = [448, 256] #plus button coordinates
minusButton = [320, 256] #minus button coordinates
rightButton = [768, 256] #right arrow button coordinates
leftButton = [0, 256] #left arrow button coordinates

levelExit = [0, 0] #exit coordinates
rightPushable = [] #list of pushblocks 1 = pushable to right, 0 = unpushable to right
leftPushable = [] #same goes for those 3
upPushable = []
downPushable = []
for i in range(0, 30):
    rightPushable.append("2")
    leftPushable.append("2")
    upPushable.append("2")
    downPushable.append("2")

lightMap = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
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

def generateLightMap(lightSprite, wholeLevel): #this is mostly made by Xelo
    global lightMap
    lightMap = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
    neighbours = []
    b = False
    for rows in range(0, 18):
        for columns in range(0, 25): 
            mindarkfound = 5
            for lookx in range(-8, 9):
                for looky in range(-8, 9):
                    if mindarkfound == 0:
                    #we found the brightest it can be, 
                    # don look for more
                        break
                    searchx = columns + lookx
                    searchy = rows + looky
                    if searchx > 24 or searchx < 0 or searchy > 17 or searchy < 0:
                        #dont look outside the level -> skip
                        continue
                    if  wholeLevel[searchy][searchx] != "08":
                        #its not a light -> skip
                        continue
                    #known as the chebeshev distance
                    distance = abs(lookx) + abs(looky)
                    dist = math.sqrt(lookx*lookx+looky*looky)
                    if dist == 0:
                        mindarkfound = min(mindarkfound, distance)
                        continue
                    ablx = lookx/dist
                    ably = looky/dist 
                    mag = 0
                    pscanx = columns
                    pscany = rows
                    while mag<dist:
                        scanx = math.floor(ablx*mag+columns)
                        scany = math.floor(ably*mag+rows)
                        if scanx != pscanx or scanx != pscany:
                            if wholeLevel[scany][scanx]== "01":
                                distance+=1
                        pscanx = scanx 
                        pscany = scany
                        mag += 0.2
                    mindarkfound = min(mindarkfound, distance)
            lightMap[rows].append(mindarkfound)
    for rows in range(0, 18):
        for columns in range(0, 25):
            if not wholeLevel[rows][columns] == "01":
                continue
            neighbours = []
            for looky in range(-1, 2):
                for lookx in range(-1, 2):
                    if lookx == 0 and looky == 0:
                        continue
                    searchy = rows + looky
                    searchx = columns + lookx
                    if searchy > 17 or searchx > 24 or searchy < 0 or searchx < 0:
                        continue
                    if wholeLevel[searchy][searchx] == "01":
                        continue
                    neighbours.append(lightMap[searchy][searchx])
            if len(neighbours) > 0:
                lightMap[rows][columns] = min(neighbours)
            else:
                lightMap[rows][columns] = 5

def drawLight():
    lightSprite.fill((0, 0, 0, 0))
    global wholeLevel, lightMap
    for rows in range(0, 18):
        for columns in range(0, 25):
            if wholeLevel[rows][columns] == "08":
                continue
            lightSprite.blit(lightLevelsSprite, (columns*32, rows*32), (lightMap[rows][columns]*32, 0, 32, 32))

def glowPlayer():
    pygame.draw.rect(lightSprite, (0, 0, 0, 0), (roundTo32(x+16), roundTo32(y+16), 32, 32))
    lightSprite.blit(lightLevelsSprite, (roundTo32(x+16), roundTo32(y+16)), (lightMap[int(roundTo32(y+16)/32)][int(roundTo32(x+16)/32)]*32-32, 0, 32, 32))

def generateFloor():
    columnPixel = -32
    rowPixel = -32
    for rD in range(0, 18):
        for cD in range(0, 25):
            variant = random.randint(0, 7)
            cfs = pygame.Surface((32, 32))
            cfs.blit(tilesSprites, (0, 0), (0, variant * 32, 32, variant * 32 + 32))
            rotation = random.randint(0, 360)
            floorSprite.blit(pygame.transform.rotate(cfs, int(90 * math.ceil(float(rotation) / 90) - 90)), (columnPixel + 32, rowPixel + 32)) 
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
                floorSprite.blit(railSprite, (x, y), (mask * 32, 0, 32, 32))

def generateWalls():
    global gameMode
    if levelsLoaded >= int(levelsCompleted[0]) + 2 or levelsLoaded >= existingLevels:
        if gameMode != 0:
            return
    generateFloor()
    global wallsSprite, bX, bY, wholeLevel
    wallsSprite.fill((0, 0, 0, 0))
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
    global levelsLoaded, x, y, pbX, pbY, bX, bY, hX, hY, hrX, hrY, lX, lY, existingLevels, gameMode, levelsCompleted, wholeLevel, levelToLoad
    wholeLevel = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
    pbX = [] #pushblocks x
    pbY = [] #pushblocks y
    bX = [] #blocks x
    bY = [] #blocks y
    hX = [] #holes x
    hY = [] #holes y
    hrX = [] #horizontal rails x
    hrY = [] #horizontal rails y
    lX = []
    lY = []
    #pygame.mixer.music.play()
    if levelsLoaded >= int(levelsCompleted[0]) + 2 or levelsLoaded >= existingLevels:
        if not gameMode == 0:
            gameMode = 3
            return
    filename = "levels/level" + str(levelsLoaded) + ".srlv"
    if levelToLoad != "none":
        filename = "levels/" + levelToLoad + ".srlv"
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

                elif levelBlocksLines[blocksPlaced] == "08":
                    lX.append(blocksPlaced*32)
                    lY.append(linesPlaced*32)
                    bX.append(blocksPlaced*32)
                    bY.append(linesPlaced*32)

                blocksPlaced = blocksPlaced + 1
            linesPlaced = linesPlaced + 1
    generateLightMap(lightSprite, wholeLevel)
    if levelFile.readline(19).replace("\n", "") == "1":
        levelScript = levelFile.readlines()
        print(levelScript)
        for i in range(0, len(levelScript)):
            levelScript[i] = levelScript[i].replace("\n", "")
            levelScript[i] = levelScript[i].replace("['", "")
            levelScript[i] = levelScript[i].replace("']", "")
            exec(levelScript[i])
    levelFile.close()

def generateBackground():
    global gbg #generating background
    menuBackground.blit(floorSprite, (0, 0))
    #if len(getLights()) > 0:
    #    drawShadows(Vec2(x, y))
    menuBackground.blit(wallsSprite, (0, 0))
    for hD in range(0, len(hX)):
        menuBackground.blit(holeSprite, (hX[hD], hY[hD]))
    for pD in range(0, len(pbX)):
        menuBackground.blit(pushblockSprite, (pbX[pD], pbY[pD]))
    for lD in range(0, len(lX)):
        menuBackground.blit(lampSprite, (lX[lD], lY[lD]))
    menuBackground.blit(lightSprite, (0, 0))
    menuBackground.blit(blurSurf(menuBackground, 5), (0, 0))

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

#bugi ono (buggy ohno)
def getLights():
    lights = []
    if(len(lX) > 0):
        for i in range(len(lX)):
            lights.append(Vec2(lX[i], lY[i]))
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
            shadow_rect = shadowSprite.get_rect(center = (a.x, a.y + 10))
            shadowScale = pygame.transform.scale(shadowSprite, (int(128 - max(0, min(dst(a, i), 64))/2), 32))
            shadowRot = pygame.transform.rotozoom(shadowScale, angle+90, 1)
            shadowDraw = shadowRot.get_rect(center = (a.x, a.y + 10))
            dis.blit(shadowRot, shadowDraw)
        
def drawPlayer(x, y):
    if playerFacing == 0:
        dis.blit(playerSprite, (x, y))
    elif playerFacing == 1:
        dis.blit(playerLeftSprite, (x, y))
    elif playerFacing == 2:
        dis.blit(playerBackSprite, (x, y))
    elif playerFacing == 3:
        dis.blit(playerRightSprite, (x, y))
    

def drawAllBlocks(): #draws blocks and pushblocks
    dis.blit(floorSprite, (0, 0))
    #if len(getLights()) > 0:
    #    drawShadows(Vec2(x, y))
    dis.blit(wallsSprite, (0, 0))
    for hD in range(0, len(hX)):
        dis.blit(holeSprite, (hX[hD], hY[hD]))
    for pD in range(0, len(pbX)):
        dis.blit(pushblockSprite, (pbX[pD], pbY[pD]))
    for lD in range(0, len(lX)):
        dis.blit(lampSprite, (lX[lD], lY[lD]))

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
                pbX[pM] = pbX[pM] + playerSpeed

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
                pbX[pM] = pbX[pM] - playerSpeed

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
                pbY[pM] = pbY[pM] - playerSpeed

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
                pbY[pM] = pbY[pM] + playerSpeed
        pM = pM + 1
    #if mu or mr or ml or md:
        #pushblockSound.play()

def roundTo32(x, base = 32):
    return int(base * math.ceil(float(x) / base) - 32)

def blurSurf(surface, amt):
    """
    Blur the given surface by the given 'amount'.  Only values 1 and greater
    are valid.  Value 1 = no blur.
    """
    if amt < 1.0:
        raise ValueError("Arg 'amt' must be greater than 1.0, passed in value is %s"%amt)
    scale = 1.0/float(amt)
    surf_size = surface.get_size()
    scale_size = (int(surf_size[0]*scale), int(surf_size[1]*scale))
    surf = pygame.transform.smoothscale(surface, scale_size)
    surf = pygame.transform.smoothscale(surf, surf_size)
    return surf

def cheat():
    if summonBox:
        if playerFacing == 0:
            pbX.append(roundTo32(x + 16))
            pbY.append(roundTo32(y + 48))
        if playerFacing == 1:
            pbX.append(roundTo32(x - 16))
            pbY.append(roundTo32(y + 16))
        if playerFacing == 2:
            pbX.append(roundTo32(x + 16))
            pbY.append(roundTo32(y - 16))
        if playerFacing == 3:
            pbX.append(roundTo32(x + 48))
            pbY.append(roundTo32(y + 16))
    if summonWall:
        if playerFacing == 0:
            bX.append(roundTo32(x + 16))
            bY.append(roundTo32(y + 48))
            lx = roundTo32(x + 16)
            ly = roundTo32(y + 48)
            wholeLevel[int(ly/32)][int(lx/32)] = "01"
        if playerFacing == 1:
            bX.append(roundTo32(x - 16))
            bY.append(roundTo32(y + 16))
            lx = roundTo32(x - 16)
            ly = roundTo32(y + 16)
            wholeLevel[int(ly/32)][int(lx/32)] = "01"
        if playerFacing == 2:
            bX.append(roundTo32(x + 16))
            bY.append(roundTo32(y - 16))
            ly = roundTo32(y - 16)
            lx = roundTo32(x + 16)
            wholeLevel[int(ly/32)][int(lx/32)] = "01"
        if playerFacing == 3:
            bX.append(roundTo32(x + 48))
            bY.append(roundTo32(y + 16))
            ly = roundTo32(y + 16)
            lx = roundTo32(x + 48)
            wholeLevel[int(ly/32)][int(lx/32)] = "01"
        generateWalls()

def checkInteractiveBlocks():
    hC = 0 #holess checked
    while hC != len(hY):
        pC = 0 #pushblocks checked
        while pC != len(pbY):
            if pbX[pC] + 26 >= hX[hC] and pbX[pC] <= hX[hC] + 26 and pbY[pC] + 26 >= hY[hC] and pbY[pC] <= hY[hC] + 26:
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
            d, u = False, False
            if hrY[hrC] > y - 24 and hrY[hrC] < y and hrX[hrC] < x + 24 and hrX[hrC] > x - 24: 
                DupG = True
                u = True
            elif hrY[hrC] < y + 24 and hrY[hrC] > y and hrX[hrC] < x + 24 and hrX[hrC] > x - 24: 
                DdownG = True
                d = True
            if x + 16 > hrX[hrC] - 4 and x + 16 < hrX[hrC] + 36 and y + 16 > hrY[hrC] - 4 and y + 16 < hrY[hrC] + 36:
                if d:
                    DdownG = False
                if u:
                    DupG = False

def checkMouseButtons():
    global levelsLoaded, gameMode, levelsCompleted, levelsLoaded, mouseKeyPressed, existingLevels, bgx, levelToLoad, wholeLevel, settingsButton, settingSelected, fpsLimit, scaling, sx, sy, width, height
    mousePos = list(pygame.mouse.get_pos())
    mousePos[0] = math.floor(abs(sx-mousePos[0])/scaling)
    mousePos[1] = math.floor(abs(sy-mousePos[1])/scaling)
    if gameMode == 1:
        if mousePos[0] < restartButton[0] + 32 and mousePos[0] > restartButton[0] and mousePos[1] > restartButton[1] and mousePos[1] < restartButton[1] + 32:
            loadLevel()
            generateWalls()
        if mousePos[0] < exitButton[0] + 32 and mousePos[0] > exitButton[0] and mousePos[1] > exitButton[1] and mousePos[1] < exitButton[1] + 32:
            gameMode = 2
    elif gameMode == 0:
        if mousePos[0] < playButton[0] + 32 and mousePos[0] > playButton[0] and mousePos[1] > playButton[1] and mousePos[1] < playButton[1] + 32:
            if levelsLoaded >= int(levelsCompleted[0]) + 2 or levelsLoaded >= existingLevels:
                levelsLoaded = levelsLoaded - 1
            gameMode = 2
            levelToLoad = "none"
            loadLevel()
            generateWalls()
        elif mousePos[0] < editorButton[0] + 32 and mousePos[0] > editorButton[0] and mousePos[1] > editorButton[1] and mousePos[1] < editorButton[1] + 32:
            pygame.quit()
            os.system("python levelEditor.py")
            sys.exit()
        elif mousePos[0] < exitButton[0] + 32 and mousePos[0] > exitButton[0] and mousePos[1] > exitButton[1] and mousePos[1] < exitButton[1] + 32:
            pygame.quit()
            sys.exit()
        elif mousePos[0] < settingsButton[0] + 32 and mousePos[0] > settingsButton[0] and mousePos[1] > settingsButton[1] and mousePos[1] < settingsButton[1] + 32:
            gameMode = 4

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
    elif gameMode == 4:
        if mousePos[0] < exitButton[0] + 32 and mousePos[0] > exitButton[0] and mousePos[1] > exitButton[1] and mousePos[1] < exitButton[1] + 32:
            gameMode = 0
        elif mousePos[0] < plusButton[0] + 32 and mousePos[0] > plusButton[0] and mousePos[1] > plusButton[1] and mousePos[1] < plusButton[1] + 32:
            if settingSelected == 2:
                if fpsLimit < 99:
                    fpsLimit = fpsLimit + 1
        elif mousePos[0] < minusButton[0] + 32 and mousePos[0] > minusButton[0] and mousePos[1] > minusButton[1] and mousePos[1] < minusButton[1] + 32:
            if settingSelected == 2:
                if fpsLimit > 16:
                    fpsLimit = fpsLimit - 1

def renderConsole():
    global console
    consoleWhole = pygame.Surface((width, height), pygame.SRCALPHA)
    sys.stderr.seek(0)
    acl = sys.stderr.readlines()
    console = ""
    for cr in range(0, len(acl)):
        console = acl[cr].replace("\n", "")
        consoleLine = consoleFont.render(str(console), False, (255, 255, 255))
        consoleWhole.blit(consoleLine, (5, cr*20))
    return consoleWhole

def drawUi():
    global gameMode, playButton, exitButton, rightButton, leftButton
    if gameMode == 1:
        dis.blit(restartButtonSprite, (restartButton[0], restartButton[1]))
        dis.blit(exitButtonSprite, (exitButton[0], exitButton[1]))
    if gameMode == 0:
        #for cd in range(0, 25):
        #    for rd in range(0,18):
        #        dis.blit(floorSprite, (cd*32, rd*32))
        dis.blit(menuBackground, (bgx, 0))
        playButton = [288, 256]
        exitButton = [480, 256]
        dis.blit(playButtonSprite, (playButton[0], playButton[1]))
        dis.blit(editorButtonSprite, (editorButton[0], editorButton[1]))
        dis.blit(exitButtonSprite, (exitButton[0], exitButton[1]))
        dis.blit(sectorTitleSprite, (sectorTitle[0], sectorTitle[1]))
        dis.blit(versionRender, (sectorTitle[0] + 108, sectorTitle[1] + 100))
        dis.blit(settingsButtonSprite, (settingsButton[0], settingsButton[1]))
    if gameMode == 2:
        rightButton = [768, 256]
        leftButton = [0, 256]
        playButton = [704, 0]
        exitButton = [768, 0]
        dis.blit(playButtonSprite, (playButton[0], playButton[1]))
        dis.blit(exitButtonSprite, (exitButton[0], exitButton[1]))
        dis.blit(rightArrowSprite, (rightButton[0], rightButton[1]))
        dis.blit(leftArrowSprite, (leftButton[0], leftButton[1]))

    if gameMode == 4:
        dis.blit(menuBackground, (bgx, 0))
        exitButton = [768, 0]
        plusButton = [448, 256]
        minusButton = [320, 256]
        rightButton = [448, 192]
        leftButton = [320, 192]
        dis.blit(exitButtonSprite, (exitButton[0], exitButton[1]))
        dis.blit(plusButtonSprite, (plusButton[0], plusButton[1]))
        dis.blit(minusButtonSprite, (minusButton[0], minusButton[1]))
        dis.blit(rightArrowSprite, (rightButton[0], rightButton[1]))
        dis.blit(leftArrowSprite, (leftButton[0], leftButton[1]))
        dis.blit(settingsDisplayWide, (368, 192))
        dis.blit(settingsDisplay, (384, 256))
        if settingSelected == 2:
            dis.blit(fpsLimitSettingRender, (387, 261))
            dis.blit(fpsSettingTitle, (381, 197))
        if settingSelected == 1:
            dis.blit(brightnessSettingRender)
            dis.blit(brightnessSettingTitle)


pygame.init()
display = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Sector")
clock = pygame.time.Clock()
pygame.display.set_icon(sectorIcon)
loadLevel()
generateWalls()
drawAllBlocks()
generateLightMap(lightSprite, wholeLevel)
drawLight()
generateBackground()



while not gameOver:
    summonBox, summonWall, destroyWall = False, False, False
    mouseKeyPressed = False
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if not consoleOn:
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
            if event.key == pygame.K_DOWN:
                cy = cy + 20
            if event.key == pygame.K_UP:
                cy = cy - 20
            if not consoleOn:
                continue
            command = command + event.unicode
            if event.key == pygame.K_RETURN:
                print("> " + str(command))
                try:
                    exec(str(command))
                except Exception as err:
                    print("An error has occured: " + str(err))
                command = ""
            if event.key == pygame.K_BACKSPACE:
                command = command[:-1]
            commandRender = consoleFont.render("> " + command, False, (255, 255, 255))
        if gameMode == 0:
            x = 0
            y = 0
        w, h = pygame.display.get_surface().get_size()
        scaling = min(w/width, h/height)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                upG = False
            if event.key == pygame.K_a:
                leftG = False
            if event.key == pygame.K_s:
                downG = False
            if event.key == pygame.K_d:
                rightG = False
            if event.key == pygame.K_h:
                pygame.image.save(dis, "screenshot.png")
            if event.key == pygame.K_F1:
                if consoleOn:
                    consoleOn = False
                else:
                    consoleOn = True
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
        y = y - playerSpeed
    if leftG and not DleftG:
        playerFacing = 1
        x = x - playerSpeed
    if downG and not DdownG:
        playerFacing = 0
        y = y + playerSpeed
    if rightG and not DrightG:
        playerFacing = 3
        x = x + playerSpeed
    if gameMode == 4:
        fpsLimitSettingRender = consolas.render(str(fpsLimit), False, (70, 185, 35))
    checkInteractiveBlocks()
    movePushblocks()
    drawAllBlocks()
    drawPlayer(x, y)
    if gameMode == 2:
        drawLight()
    if gameMode == 1:
        drawLight()
        glowPlayer()
    if mouseKeyPressed:
        checkMouseButtons()
    if devMode:
        cheat()
    if gameMode == 3:
        gameMode = 0
    playerSpeed = 30/fpsLimit*4
    dis.blit(lightSprite, (0, 0))
    drawUi()
    if consoleOn:
        dis.blit(commandRender, (5, 548))
        dis.blit(renderConsole(), (0, cy))
    sx = abs(w-width*scaling)/2
    sy = abs(h-height*scaling)/2
    dis.fill((10*brightness, 10*brightness, 10*brightness), special_flags=pygame.BLEND_RGB_ADD)
    display.blit(pygame.transform.scale(dis, (math.floor(width*scaling), math.floor(height*scaling))), (sx, sy))
    pygame.display.update()
    clock.tick(fpsLimit)

pygame.quit()
sys.exit()
