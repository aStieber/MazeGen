import sys, random, math, time, pygame
from noise import pnoise3
pygame.init()

class BaseMaze(object):
	"""M A Z E B O Y S"""
	def __init__(self, arg):
		self.side = arg
		self.board = [[1 for x in range(arg)] for x in range(arg)] #maze initializer, self attaches board to the instance variable
		self.marker = (0,0)
		self.screen =  pygame.display.set_mode(((self.side * 20) + 80,(self.side *20) + 80))
		self.screen.fill((150,150,150))

	def findBlocked(self, marker, boardArray):
		dTracker = {'up': 1, 'down': 1,'left': 1,'right': 1}
		if marker[0] != 0: 
			if boardArray[marker[0] - 1][marker[1]] == 0: dTracker['left'] = 0
		else: dTracker['left'] = 0
		if marker[0] != self.side - 1:
			if boardArray[marker[0] + 1][marker[1]] == self.side:
				dTracker['right'] = 0
		else: dTracker['right'] = 0 
		if marker[1] != 0:
			if boardArray[marker[0]][marker[1] - 1] == 0: dTracker['up'] = 0
		else:
			dTracker['up'] = 0
		if marker[1] != self.side - 1:
			if boardArray[marker[0]][marker[1] + 1] == self.side: dTracker['down'] = 0
		else: dTracker['down'] = 0
		return(dTracker)

	def generatePerlin(self):
		pArray = [[1 for x in range(self.side)] for x in range(self.side)]
		freq = 16.0
		randZ = random.random() * self.side
		for y in range(self.side):
			for x in range(self.side):
				pArray[x][y] = int(pnoise3(x / freq, y / freq, randZ) * 128.0)#max: 87 min: -92
		# for x in range(self.side):
		# 	print(pArray[x])
		return(pArray)

	def generateBoard(self):
		dTracker = {'up': 1, 'down': 1,'left': 1,'right': 1}
		newBoard = [[0 for x in range(self.side)] for x in range(self.side)] #generate fully walled board
		newPerlin = self.generatePerlin()
		z = 0.47
		for y in range(self.side):
			for x in range(self.side):
				sideCounter = 4
				if x == 0:
					dTracker['left'] = 0
					sideCounter -= 1
				else: dTracker['left'] = newPerlin[x - 1][y]
				if x == self.side - 1:
					dTracker['right'] = 0
					sideCounter -= 1
				else: dTracker['right'] = newPerlin[x + 1][y] 
				if y == 0:
					dTracker['up'] = 0
					sideCounter -= 1
				else: dTracker['up'] = newPerlin[x][y - 1]
				if y == self.side - 1:
					dTracker['down'] = 0
					sideCounter -= 1
				else: dTracker['down'] = newPerlin[x][y + 1]
				#print("x: ", x, "y: ", y, "dTracker: ",dTracker)
				cellAverage = (dTracker['left'] + dTracker['right'] + dTracker['up'] + dTracker['down']) / sideCounter

				if cellAverage >= newPerlin[x][y] - z and cellAverage <= newPerlin[x][y] + z:
					newBoard[x][y] = 0
				else:
					newBoard[x][y] = 1

		return(newBoard)

	def displayMaze(self, boardArray):
		for y in range(self.side):
			for x in range(self.side):
				blocked = self.findBlocked((x, y), boardArray)
				newCell = self.generateCell(blocked, (x,y), boardArray)
				newSpot = (40 +(20 * x), 40 + (20 * y))
				self.screen.blit(newCell, newSpot)
		pygame.display.update()
		
	def generateCell(self, dTracker, checkCoords, boardArray):
		black = (0, 0, 0)
		white = (255, 255, 255)
		tempCell = pygame.Surface((20,20))
		if boardArray[checkCoords[0]][checkCoords[1]] == 1:
			tempCell.fill(black)
			return(tempCell)
		#generate base surface (4x4 black squares in every corner of a 20x20 image)
		tempCell.fill(white)
		pygame.draw.rect(tempCell, black, (0, 0, 4, 4)) #top left  #x,y,width,height
		pygame.draw.rect(tempCell, black, (0, 16, 4, 4))#bottom left
		pygame.draw.rect(tempCell, black, (16, 0, 4, 4)) #top right
		pygame.draw.rect(tempCell, black, (16, 16, 4, 4)) #bottom right
		#directional conditionals
		if dTracker['up'] == 1:
			if (checkCoords[0], checkCoords[1]) == (0,0):#ensures top of (0,0) is open
				pygame.draw.rect(tempCell, white, (4, 0, 12, 4))
			else:
				pygame.draw.rect(tempCell, black, (4, 0, 12, 4))
		if dTracker['left'] == 1: pygame.draw.rect(tempCell, black, (0, 4, 4, 12))
		if dTracker['right'] == 1: pygame.draw.rect(tempCell, black, (16, 4, 4, 12))
		if dTracker['down'] == 1: pygame.draw.rect(tempCell, black, (4, 16, 12, 4))
		return(tempCell)


	def solutionGen(self, iterations):
		masterNewBoard = [0 for x in range(iterations)]
		for x in range(iterations):
			masterNewBoard[x] = self.generateBoard()
			self.displayMaze(masterNewBoard[x])
			pygame.image.save(self.screen,"%s.png" % x)
			pygame.time.wait(200)




		
main_board = BaseMaze(12)
# greatest = 0
# least = 0
# for x in range(1000):
# 	myArray = main_board.generatePerlin(16)
# 	for y in range(16):
# 		for x2 in range(16):
# 			if myArray[x2][y] > greatest:
# 				greatest = myArray[x2][y]
# 			if myArray[x2][y] < least:
# 				least = myArray[x2][y]
# 	print(x, "\r", end="") #moves cursor back to beginning of line, allows console overwriting
# print(greatest, least)
main_board.solutionGen(10)
# main_board.solutionGen('v')
