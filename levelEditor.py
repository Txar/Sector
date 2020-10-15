import pygame, sys, os

mouseKeyPressed, gameOver = False, False

lastUsedLevelFile = open("data/lastUsedLevel.srgd", "r")
lastUsedLevel = str(lastUsedLevelFile.readlines(1))
lastUsedLevelFile.close()
loadLastUsedFile = os.path.exists("levels/" + str(lastUsedLevelFile))
wholeLevel = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]

width = 800
height = 640
playerSprite = pygame.image.load("sprites/pushblock.png")
pushblockSprite = pygame.image.load("sprites/pushblock.png")
floorSprite = pygame.image.load("sprites/floort.png")
blockSprite = pygame.image.load("sprites/testicon.png")
holeSprite = pygame.image.load("sprites/hole.png")
sectorIcon = pygame.image.load("sprites/testicon.png")

def loadLevelFile(levelName):
	global lastUsedLevel, wholeLevel
	if loadLastUsedFile:
		levelName = lastUsedLevel
	loadedLevel = open("levels/" + levelName)
	for rowsLoaded in range(0, 18):
		wholeLevel[rowsLoaded].append(loadedLevel.readlines(rowsLoaded + 1))
		wholeLevel[rowsLoaded] = str(wholeLevel[rowsLoaded]).replace("\\n", "")
		wholeLevel[rowsLoaded] = str(wholeLevel[rowsLoaded]).replace("[['", "")
		wholeLevel[rowsLoaded] = str(wholeLevel[rowsLoaded]).replace("']]", "")
		wholeLevel[rowsLoaded] = wholeLevel[rowsLoaded].split(" ")

def drawLevel():
	global wholeLevel
	for rowsDrawn in range(0, 18):
		for columnsDrawn in range(0, 25):
			x = int(columnsDrawn) * 32
			y = int(rowsDrawn) * 32
			if wholeLevel[rowsDrawn][columnsDrawn] == "01":
				dis.blit(blockSprite, (int(x), int(y)))



loadLevelFile("level1.srlv")
print(wholeLevel[0][0])

pygame.init()
dis = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sector - level editor")
clock = pygame.time.Clock()

while not gameOver:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			gameOver = True
		if event.type == pygame.MOUSEBUTTONDOWN:
			mouseKeyPressed = True
		if event.type == pygame.MOUSEBUTTONUP:
			mouseKeyPressed = False

	drawLevel()
	pygame.display.update()
	clock.tick(15)

pygame.quit()
sys.exit()