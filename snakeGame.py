import time
from curses import wrapper
import curses
import random
import curses

class Character:
	def __init__(self,character):
		self.posx = 15
		self.posy = 15
		self.viz = character
		self.posList = [[self.posx,self.posy]]
		self.tailCount = 0
	
	def randomChords(self):
		self.posx = int(random.uniform(3,49))
		self.posy = int(random.uniform(3,18))
		
	def addTail(self):
		self.tailCount += 1

class SnakeGame:
	def __init__(self):
		self.screen = curses.initscr()

		# Update the buffer, adding text at different locations
		curses.cbreak()
		self.screen.keypad(1)

		self.screen.refresh()


		# Changes go in to the screen buffer and only get
		# displayed after calling `refresh()` to update
		self.count = 0 
		self.gameCount = 0
		self.highScore = 0
		
	
	def gameStart(self):

		self.myGuy = Character("O")
		self.snakeFood = Character("*")
		self.snakeFood.posx = int(random.uniform(3,50))
		self.snakeFood.posy = int(random.uniform(3,20))
		
		key = ''
		self.positions = []

		self.screen.nodelay(1)
		self.count = 0

		self.right = True
		self.down = None

		self.running = True
		action = 0
		observations = self.frameAdvance(action)
		self.globalScore = 0


	def frameAdvance(self,action):

		self.screen.clear()
		try:
			for i in range(self.myGuy.tailCount + 1):
				i += 1
				poslist = self.myGuy.posList
				self.screen.addstr(poslist[-i][1], poslist[-i][0],self.myGuy.viz)
			self.screen.addstr(self.snakeFood.posy, self.snakeFood.posx,self.snakeFood.viz)
			self.screen.addstr(0, 0,"Score: "+str(self.myGuy.tailCount))
			self.screen.addstr(0, 10,"High Score: "+str(self.highScore))
			self.screen.addstr(0,25 ,"Game Count: "+str((self.gameCount)))
			# self.screen.addstr(0,45 ,"Action: "+str((action)))
		except:
			pass
		for i in range(1,75):
			self.screen.addstr(1, i,"#")
		for i in range(1,75):
			self.screen.addstr(20, i,"#")
		for i in range(1,20):
			self.screen.addstr(i, 1,"#")
		for i in range(1,21):
			self.screen.addstr(i, 75,"#")

			
		if (self.snakeFood.posx == self.myGuy.posx) and (self.snakeFood.posy == self.myGuy.posy):
			self.snakeFood.randomChords()
			self.myGuy.addTail()
			self.globalScore += 10
			
		currentPos = [self.myGuy.posx,self.myGuy.posy]
		latestBuffer = []

		latestBuffer = self.myGuy.posList[-self.myGuy.tailCount - 1:]
		
		#self.screen.addstr(3, 0,"Current Buffer: "+str(latestBuffer))
		#self.screen.addstr(2, 0,"Current Loc: "+str(currentPos))
			
		
		curses.napms(75)
		key = self.screen.getch()
		if key == curses.KEY_UP:
			self.down = False
			self.right = None
		elif key == curses.KEY_DOWN: 
			self.down = True
			self.right = None
		if key == curses.KEY_RIGHT: 
			self.right = True
			self.down = None
		elif key == curses.KEY_LEFT: 
			self.right = False
			self.down = None
		latestBuffer.pop(-1)
		#curses.endwin()
		if self.right:
			self.myGuy.posx += 1
			self.myGuy.posList.append([self.myGuy.posx,self.myGuy.posy])
		if self.right == False:
			self.myGuy.posx -= 1
			self.myGuy.posList.append([self.myGuy.posx,self.myGuy.posy])
		if self.down:
			self.myGuy.posy += 1
			self.myGuy.posList.append([self.myGuy.posx,self.myGuy.posy])
		if self.down == False:
			self.myGuy.posy -= 1
			self.myGuy.posList.append([self.myGuy.posx,self.myGuy.posy])
			
		if self.myGuy.tailCount >= self.highScore:
			self.highScore = self.myGuy.tailCount	
				
		if currentPos in latestBuffer:
			self.running = False
			self.gameCount += 1
			self.globalScore -= 100
			#self.gameStart()
		elif self.myGuy.posx > 74 or self.myGuy.posx < 2:
			self.running = False
			self.gameCount += 1
			self.globalScore -= 100
			#self.gameStart()
		elif self.myGuy.posy < 2 or self.myGuy.posy > 19:
			self.running = False
			self.gameCount += 1
			self.globalScore -= 100
			#self.gameStart()

		actionDict = {0:"UP",
		1:"DOWN",
		2:"RIGHT",
		3:"LEFT",
		}

		if actionDict[action] == "UP":
			self.down = False
			self.right = None
		elif actionDict[action]  == "DOWN": 
			self.down = True
			self.right = None
		if actionDict[action]  == "RIGHT": 
			self.right = True
			self.down = None
		elif actionDict[action]  == "LEFT": 
			self.right = False
			self.down = None

		#if self.running:
		#	self.frameAdvance()

		futurePosright = [self.myGuy.posx + 1 ,self.myGuy.posy]
		futurePosleft = [self.myGuy.posx - 1 ,self.myGuy.posy]
		futurePosdown = [self.myGuy.posx,self.myGuy.posy + 1]
		futurePosup = [self.myGuy.posx,self.myGuy.posy - 1]

		futurePos = [futurePosright,futurePosleft,futurePosdown,futurePosup]
		observations = [0,0,0,0]

		for index, future in enumerate(futurePos):
			if future in latestBuffer:
				observations[index] = 1
				with open('output.log', 'a') as f:
					f.write("TAIL LIMIT OCCURED ")
			if future[0] > 74 or future[0] < 2:
				observations[index] = 1
				with open('output.log', 'a') as f:
					f.write("LEFT OR RIGHT WALL LIMIT ")
			if future[1] < 2 or future[1] > 19:
				observations[index] = 1
				with open('output.log', 'a') as f:
					f.write("UP OR DOWN FOUND ")

		deltaX = abs(self.myGuy.posx - self.snakeFood.posx)
		deltaY = abs(self.myGuy.posy - self.snakeFood.posy)
		observations.append(deltaX)
		observations.append(deltaY)



		#self.screen.addstr(0,45 ,"Global Score: "+str((self.globalScore)))
		self.screen.refresh()
			

		with open('output.log', 'a') as f:
			f.write(" Frame: "+str(self.count))
			f.write(" "+str(observations)+ '\n')

			if self.running == False:
				f.write(" DIED\n")

		self.count += 1
		return observations
		

# Base Game 
if __name__ == "__main__":
	highScore = 0
	gameCount = 0
	game = SnakeGame()
	game.gameStart()

	curses.endwin()
