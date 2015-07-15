import sys, random, time, pygame, json
pygame.init()
#Maze generator. Will comment soon.

class SolTree(object):
	def __init__(self, iparent, ix, iy, ivisit):
		self.parent = iparent
		self.x = ix
		self.y = iy
		self.isVisited = ivisit

class BaseMaze(object):
	"""M A Z E B O Y S"""
	def __init__(self, arg):
		self.side = arg
		self.board = [[1 for x in range(arg)] for x in range(arg)]#maze initializer, self attaches board to the instance variable
		self.screen =  pygame.display.set_mode(((self.side * 20) + 80,(self.side *20) + 80))
		self.screen.fill((150,150,150))

	def displayMaze(self, boardArray):
		font = pygame.font.SysFont("arialblack", 20)
		eCell = font.render("E", True, (0, 0, 0), (255,241,38))
		sCell = font.render("S", True, (0, 0, 0), (255,241,38))
		self.screen.blit(sCell, (40, 10))
		self.screen.blit(eCell, ((self.side * 20) + 26, (self.side * 20) + 40)) #26 is right

		for y in range(self.side):
			for x in range(self.side):
				newCell = self.generateCell(boardArray, x, y)
				newSpot = (40 +(20 * x), 40 + (20 * y))
				self.screen.blit(newCell, newSpot)
		pygame.display.update()
		
	def generateCell(self, board, x, y):
		BLACK = (0, 0, 0)
		WHITE = (255, 255, 255)
		tempCell = pygame.Surface((20,20))
		#generate base surface (4x4 BLACK squares in every corner of a 20x20 image)
		tempCell.fill(WHITE)
		pygame.draw.rect(tempCell, BLACK, (0, 0, 4, 4)) #top left  #x,y,width,height
		pygame.draw.rect(tempCell, BLACK, (0, 16, 4, 4))#bottom left
		pygame.draw.rect(tempCell, BLACK, (16, 0, 4, 4)) #top right
		pygame.draw.rect(tempCell, BLACK, (16, 16, 4, 4)) #bottom right

		if board[x][y][0] and board[x][y][1] and board[x][y][2] and board[x][y][3] is True:
			pygame.draw.rect(tempCell, BLACK, (0, 0, 20, 20))
		else:
			if board[x][y][0] is True:#top
				pygame.draw.rect(tempCell, BLACK, (4, 0, 12, 4))

			if board[x][y][1] is True:#right
				pygame.draw.rect(tempCell, BLACK, (16, 4, 4, 12))

			if board[x][y][2] is True:#bottom
				pygame.draw.rect(tempCell, BLACK, (4, 16, 12, 4))

			if board[x][y][3] is True:#left
				pygame.draw.rect(tempCell, BLACK, (0, 4, 4, 12))

		return(tempCell)

	def boardInit(self, inBoard):
		board = inBoard
		sideMax = self.side - 1
		for x in range(self.side):
			for y in range(self.side):
				board[x][y] = [False, False, False, False]
		for x in range(self.side):
			board[x][0][0] = True#top
			board[x][sideMax][2] = True#bottom
			board[0][x][3] = True#left
			board[sideMax][x][1] = True#right
		
		board[0][0][1] = False
		board[0][0][2] = False
		
		return(board)

	def contentGen(self, inBoard):
		board = inBoard

		for x in range(self.side):
			for y in range(self.side):
				walls = board[x][y] #0:top|1:right|2:down|3:left
				for z in range(4):
					if walls[z] is False:
						if random.random() >= 0.68: #adjust this to tweak boards
							walls[z] = True
							#fix walls, think this is the right spot for it.
							try:
								if z == 0: board[x][y-1][2] = True
								if z == 1: board[x+1][y][3] = True
								if z == 2: board[x][y+1][0] = True
								if z == 3: board[x-1][y][1] = True
							except IndexError:
								pass
				board[x][y] = walls
		
		#board[0][0][0] = False
		#board[self.side-1][self.side-1][2] = False

		return board
	
	def parentTrap(self, finalCell, tBoard):
		treeArray = tBoard
		finalRoute = []
		tempCell = finalCell
		active = True
		while active is True:
			try:
				finalRoute.insert(0,(tempCell.x, tempCell.y))

				tempParent = tBoard[tempCell.x][tempCell.y].parent

				tempCell = treeArray[tempParent[0]][tempParent[1]]
			except TypeError:
				active = False

			
		return(finalRoute)


	def solutionGen(self, inBoard): #http://pastebin.com/i7JHa2nx
		tBoard = [[(SolTree(None, x, y, False)) for y in range(self.side)] for x in range(self.side)]

		board = inBoard
		queue = [tBoard[0][0]]
		#print(queue[0].x, queue[0].y)
		bool1 = True


		while len(queue) != 0 and bool1 is True:
			tempSolTree = queue.pop(0)
			tBoard[tempSolTree.x][tempSolTree.y].isVisited = True
			z = board[tempSolTree.x][tempSolTree.y]
			#print("z[0]: ", z, "x: ", tempSolTree.x, "y: ", tempSolTree.y)			
			
			for x in range(4):
				try:
					if x == 0 and z[0] is False and tBoard[tempSolTree.x][tempSolTree.y - 1].isVisited is False:#If there is no wall above and above cell isn't visited
						queue.append(tBoard[tempSolTree.x][tempSolTree.y - 1])#add cell to queue
						tBoard[tempSolTree.x][tempSolTree.y - 1].parent = (tempSolTree.x, tempSolTree.y)#Tell the new cell who its parent is
						tBoard[tempSolTree.x][tempSolTree.y - 1].isVisited = True

					if x == 1 and z[1] is False and tBoard[tempSolTree.x + 1][tempSolTree.y].isVisited is False:
						queue.append(tBoard[tempSolTree.x + 1][tempSolTree.y])
						tBoard[tempSolTree.x + 1][tempSolTree.y].parent = (tempSolTree.x, tempSolTree.y)
						tBoard[tempSolTree.x + 1][tempSolTree.y].isVisited = True		

					if x == 2 and z[2] is False and tBoard[tempSolTree.x][tempSolTree.y + 1].isVisited is False:
						queue.append(tBoard[tempSolTree.x][tempSolTree.y + 1])	
						tBoard[tempSolTree.x][tempSolTree.y + 1].parent = (tempSolTree.x, tempSolTree.y)
						tBoard[tempSolTree.x][tempSolTree.y + 1].isVisited = True

					if x == 3 and z[3] is False and tBoard[tempSolTree.x - 1][tempSolTree.y].isVisited is False:
						queue.append(tBoard[tempSolTree.x - 1][tempSolTree.y])
						tBoard[tempSolTree.x - 1][tempSolTree.y].parent = (tempSolTree.x, tempSolTree.y)
						tBoard[tempSolTree.x - 1][tempSolTree.y].isVisited = True

				except IndexError:
					print("indexerror")
					pass
			for x in range(len(queue)):
				if queue[x].x == self.side - 1 and queue[x].y == self.side - 1:
					bool1 = False
					tempSolTree = queue.pop(x)
					break	
		#after broken out of while loop
		route = self.parentTrap(tempSolTree, tBoard)
		
		return(route)
		

	def boardGen(self, iterations, solved=False):
		y = 0
		for x in range(iterations):
			#masterBoard = self.boardInit(self.board)
			masterBoard = self.contentGen(self.boardInit(self.board))

			route = self.solutionGen(masterBoard)
			routeLength = len(route) - 1

			if route[routeLength][0] == self.side - 1 and route[routeLength][1] == self.side - 1:
				self.displayMaze(masterBoard)
				# outFile = open(".\mazes\%s.json" % x, 'w')
				# json.dump(masterBoard, outFile)
				# outFile.close()
				pygame.image.save(self.screen,".\mazes\%s.png" % y)
				y += 1
				#pygame.time.wait(100)

		

#MAIN	
main_board = BaseMaze(20)#20 is board side length, adjust here

main_board.boardGen(1000)#number of times to generate a board and test it. The larger the side length, the larger this number needs to be.
pygame.quit()
