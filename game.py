# +++++++++++++++++++++++++++++++++
# IN THE NAME OF GOD
# THE PASSIONATE, THE MERCIFUL
# OthellO
# Hesam Sheikh Hasani
# Behnam Esmail Beigi
# +++++++++++++++++++++++++++++++++

#   All Libraries
from tkinter import *
from random import randrange
from time import *
import copy
import winsound as ws
file = 'changed3.wav'

#   Setting up the screen
root = Tk()
screen = Canvas(root, width=600, height=700, background="#339966")
screen.pack()

#   Setting up Variables
clickCounter = 0
difficulty = ''
discSize = 50
starter = ''

#   Class for the whole Board
class Board:
    def __init__(self):
        self.won = False
        self.start = True
        self.tileWidth = 62
        self.player = 0  # 0 for player, 1 for computer
        self.set = [['', '', '', '', '', '', '', ''],
                    ['', '', '', '', '', '', '', ''],
                    ['', '', '', '', '', '', '', ''],
                    ['', '', '', 'w', 'b', '', '', ''],
                    ['', '', '', 'b', 'w', '', '', ''],
                    ['', '', '', '', '', '', '', ''],
                    ['', '', '', '', '', '', '', ''],
                    ['', '', '', '', '', '', '', '']]

    def refresh(self):
        global starter
        if self.start:
            for i in range(8):
                for j in range(8):
                    if self.set[i][j] == 'w':
                        x = 56 + j * (self.tileWidth)
                        y = 56 + i * (self.tileWidth)
                        screen.create_oval(x, y, x + discSize, y + discSize, tags="tile {0}-{1}".format(i, j), fill="white",
                                           outline="black")
                    elif self.set[i][j] == 'b':
                        x = 56 + j * (self.tileWidth)
                        y = 56 + i * (self.tileWidth)
                        screen.create_oval(x, y, x + discSize, y + discSize,
                                           tags="tile {0}-{1}".format(i, j), fill="black",
                                           outline="black")
                        screen.update()

            screen.create_text(240, 620, text='Who Starts?', font=("Ubuntu", 15), tags='starter')
            screen.create_rectangle(300, 600, 350, 640, fill="#000", outline="#000", tags='starter')
            screen.create_rectangle(380, 600, 430, 640, fill="#000", outline="#000", tags='starter')
            screen.create_text(320, 620, text='User', font=("Ubuntu", 12), fill='white', tags='starter')
            screen.create_text(400, 620, text='CPU', font=("Ubuntu", 12), fill='white', tags='starter')

            if starter == 'cpu':
                starter = 'False'
                screen.delete('starter')
                screen.update()
                self.player = 1
                self.refresh()
                sleep(1)
                opMove(self.set)
            elif starter == 'user':
                starter = 'False'
                screen.delete('starter')
                screen.update()

        allValidPoints = []
        #   Show all valid points
        for i in range(8):
            for j in range(8):
                if validPoints(self.set, i, j) != []:
                    allValidPoints.append([i, j])

        if self.player == 0:
            for point in allValidPoints:
                x = 76 + point[1] * (self.tileWidth)
                y = 76 + point[0] * (self.tileWidth)
                pointSize = 10
                screen.create_oval(x, y, x + pointSize, y + pointSize,
                                   fill="yellow", tags='point')
        elif self.player == 1:
            screen.delete('point')
        self.scoreBoard()
        screen.update()

    def drawGridLines(self):
        tileWidth = self.tileWidth
        for i in range(9):
            screen.create_line(50, 50 + i * tileWidth, 546, 50 + i * tileWidth,
                               fill="#111", width=2)
            screen.create_line(50 + i * tileWidth, 50, 50 + i * tileWidth, 546,
                               fill="#111", width=2)
        self.refresh()

    def scoreBoard(self):
        screen.delete("score")
        screen.create_oval(20, 580, 20 + 1.2 * discSize, 580 + 1.2 * discSize,
                           fill="black", outline="black")
        screen.create_oval(470, 580, 470 + 1.2 * discSize, 580 + 1.2 * discSize,
                           fill="white", outline="black")

        wScore = 0
        bScore = 0
        #   Finding player Scores
        for i in self.set:
            for j in i:
                if j == 'w':
                    wScore += 1
                elif j == 'b':
                    bScore += 1
        screen.create_text(130, 610, text=bScore, tags='score', font=("Ubuntu", 40))
        screen.create_text(580, 610, text=wScore, tags='score', font=("Ubuntu", 40), fill='white')

    def put(self, i, j):

        self.start = False
        #   If space not empty return
        if self.set[i][j]:
            return

        #   All the discs that must turn after the move
        turnDiscs = validPoints(self.set, i, j)
        if turnDiscs == []:
            return
        else:
            if self.player == 0:
                discColor = 'black'
                putintoSet = 'b'
            else:
                discColor = 'white'
                putintoSet = 'w'
            self.set[i][j] = putintoSet
            x = 56 + self.tileWidth * j
            y = 56 + self.tileWidth * i
            screen.create_oval(x, y, x + discSize, y + discSize, fill=discColor,
                               tags="tile {0}-{1}".format(i,j),
                               outline="black")
            ws.PlaySound(file, ws.SND_FILENAME)
            screen.update()
            for disc in turnDiscs:
                #   Animation
                screen.delete("{0}-{1}".format(disc[0], disc[1]))
                self.set[disc[0]][disc[1]] = putintoSet
                ws.PlaySound(file, ws.SND_FILENAME)
                for i in range(int(discSize / 2)):
                    x = 50 + 31 + self.tileWidth * disc[1]
                    y = 50 + 31 + self.tileWidth * disc[0]
                    screen.create_oval(x - i, y - i, x + i, y + i, fill=discColor,
                                       tags="tile {0}-{1}".format(disc[0],disc[1]),
                                       outline="black")
                    sleep(0.001)
                    screen.update()

        #   Check if game is won
        if isEnd() == 'b':
            sleep(1)
            endGame('b')
            return
        elif isEnd() == 'w':
            sleep(1)
            endGame('w')
            return

        #   Check if any move is possible
        if self.player == 1:
            checkColor = 'b'
        else:
            checkColor = 'w'
        passed = False
        if passTurn(checkColor):
            passed = True
            print("passed")
            self.player = 1-self.player
            self.refresh()
            print(turnDiscs)
            if self.player == 1:
               opMove(self.set)

        #   If it was user's turn, let computer play
        if self.player == 0:
            board.player = 1
            if not passed:
                self.refresh()
            opMove(self.set)
        else:
            self.player = 0
            if not passed:
                self.refresh()

    def minimax(self, sett, depth, maxOrMin):
        boards = []
        choices = []
        possibleMoves = []

        for i in range(8):
            for j in range(8):
                if validPoints(sett, i, j):
                    possibleMoves.append([i, j])

        #   Make new board
        if depth % 2 == 1:
            newColor = 'w'
            mustChange = 'b'
        else:
            newColor = 'b'
            mustChange = 'w'

        for possiblemove in possibleMoves:
            copyset = copy.deepcopy(sett)
            i, j = possiblemove
            turnDisc = validPoints(copyset, i, j, mustChange)
            copyset[i][j] = newColor
            for disc in turnDisc:
                copyset[disc[0]][disc[1]] = newColor
            boards.append([copyset, [i, j]])
            choices.append([i, j])

        score = 0
        evalTable = [[200 , -100, 100,  50,  50, 100, -100,  200],
                [-100, -200, -50, -50, -50, -50, -200, -100],
                [100 ,  -50, 100,   1,   1, 100,  -50,  100],
                [50  ,  -50,   1,   1,   1,   1,  -50,   50],
                [50  ,  -50,   1,   1,   1,   1,  -50,   50],
                [100 ,  -50, 100,   1,   1, 100,  -50,  100],
                [-100, -200, -50, -50, -50, -50, -200, -100],
                [200 , -100, 100,  50,  50, 100, -100,  200]]

        for i in range(8):
            for j in range(8):
                if sett[i][j] == 'w':
                    score += evalTable[i][j]

        if depth == 0 or len(choices) == 0:
            return [score, []]

        if maxOrMin == 'max':
            bestValue = -float("inf")
            for item in boards:
                val = self.minimax(item[0], depth - 1, 'min')[0]
                if val > bestValue:
                    bestValue = val
            return [bestValue, item[1]]
        else:
            bestValue = float("inf")
            for item in boards:
                val = self.minimax(item[0], depth - 1, 'max')[0]
                if val < bestValue:
                    bestValue = val
            return [bestValue, item[1]]


def endGame(winner):
    screen.delete(ALL)
    board.scoreBoard()
    if winner =='b':
        winner = 'Black'
    else :
        winner = 'White'
    message = winner + ' WON THE GAME'
    screen.create_text(290, 200, text=message, font=("Ubuntu", 30), fill="yellow")
    screen.create_text(290, 195, text=message, font=("Ubuntu", 30), fill="black")


#   Check if Game is Won
def isEnd():
    wCount = 0
    bCount = 0

    noChoiceForWhite = True
    noChoiceForBlack = True

    for i in range(8):
        for j in range(8):
            if validPoints(board.set, i, j, 'b'):
                noChoiceForWhite = False

    for i in range(8):
        for j in range(8):
            if validPoints(board.set, i, j, 'w'):
                noChoiceForBlack = False

    if noChoiceForWhite and noChoiceForBlack:
        for i in range(8):
            for j in range(8):
                if board.set[i][j] == 'b':
                    bCount += 1
                elif board.set[i][j] == 'w':
                    wCount += 1
        if bCount > wCount:
            return 'b'
        else:
            return 'w'
    else:
        return


#   Check to see if must pass this turn
def passTurn(color):
    for i in range(8):
        for j in range(8):
            if validPoints(board.set, i, j, color):
                return False
    return True


def opMove(set):
    if difficulty == 'easy':
        easyPlay(set)
    elif difficulty == 'ai':
        ai(set)
        # aiPlay(set)

def ai(set):
    bestChoice = board.minimax(set, 3, 'max')[1]
    if bestChoice:
        i, j = bestChoice
        board.put(i, j)


def easyPlay(set):
    possibleMoves = []
    #   Finding all possible moves for computer
    for i in range(8):
        for j in range(8):
            validpoints = validPoints(set, i, j)
            if validpoints:
                possibleMoves.append([i, j])

    #   Selecting a random move
    randomMove = possibleMoves[randrange(len(possibleMoves))]
    board.put(randomMove[0], randomMove[1])


def validPoints(array, x, y, givenColor=None):
    if board.player == 1:  # Computer's turn
        color = 'b'
    else:
        color = 'w'

    if givenColor:
        color = givenColor

    allMustTurnDisc = []
    #   If not empty, not valid
    if array[x][y] != '':
        return []
    pointNeighbours = []
    #   Using max and min to avoid index out of range exception
    for i in range(max(0, x - 1), min(x + 2, 8)):
        for j in range(max(0, y - 1), min(y + 2, 8)):
            if array[i][j] == color:
                pointNeighbours.append([i, j])

    if pointNeighbours == []:
        return []

    for neighbour in pointNeighbours:
        yslope = neighbour[1] - y
        xslope = neighbour[0] - x
        xtemp = neighbour[0]
        ytemp = neighbour[1]

        mustTurnDisc = []
        mustTurnDisc.append([xtemp, ytemp])

        #   Avoiding index out of range exception
        while 8 > xtemp >= 0 and 0 <= ytemp < 8:

            if array[xtemp][ytemp] == '':
                mustTurnDisc = []
                break
            elif array[xtemp][ytemp] == color:
                if [xtemp, ytemp] not in mustTurnDisc:
                    mustTurnDisc.append([xtemp, ytemp])
            else:
                break
            xtemp += xslope
            ytemp += yslope
            if xtemp >= 8 or ytemp >= 8 or xtemp < 0 or ytemp < 0:
                mustTurnDisc = []

        for item in mustTurnDisc:
            allMustTurnDisc.append(item)
    return allMustTurnDisc


#   What to do when user clicks
def clicker(event):
    x = event.x
    y = event.y
    #   Just for console
    global clickCounter
    global difficulty
    global starter
    clickCounter += 1
    # print("Click Number %d at : (%d,%d)" % (clickCounter, x, y))

    if intro:
        #   Difficulty easy
        if x < 250 and x > 50 and y < 400 and y > 350:
            difficulty = 'easy'
            setUpBoard()
        #   Difficulty Ai
        elif x < 250 + 300 and x > 50 + 300 and y < 400 and y > 350:
            difficulty = 'ai'
            setUpBoard()
    elif starter == '':
        if 300<=x<=350 and 600<=y<=640:
            starter = 'user'
        elif 380<=x<=430 and 600<=y<=640:
            starter = 'cpu'
        board.refresh()
    elif 50 <= x <= 546 and 50 <= y <= 546:
        #   Find which space was clicked
        i = int((y - 50) / 62)
        j = int((x - 50) / 62)
        board.player = 0
        board.put(i, j)



def setUpBoard():
    global intro
    global board
    intro = False
    screen.delete(ALL)
    board = Board()
    board.drawGridLines()


#   Game Manager
def gameManager():
    global intro
    intro = True
    #   Title
    screen.create_text(290, 200, text="O_(thell)_O", font=("Ubuntu", 50), fill="black")
    screen.create_text(290, 200, text="O_(thell)_O", font=("Ubuntu", 55), fill="yellow")

    #   Options
    screen.create_rectangle(50, 350, 250, 395, fill="yellow", outline="yellow")
    screen.create_rectangle(50, 350, 250, 390, fill="#000", outline="#000")
    screen.create_rectangle(50 + 300, 350, 250 + 300, 395, fill="yellow", outline="yellow")
    screen.create_rectangle(50 + 300, 350, 250 + 300, 390, fill="#000", outline="#000")

    #   Text
    screen.create_text(100, 370, anchor="c", text="EASY", font=("Consolas", 25), fill="yellow")
    screen.create_text(102, 372, anchor="c", text="EASY", font=("Consolas", 25), fill="#666600")
    screen.create_text(380, 370, anchor="c", text="AI", font=("Consolas", 25), fill="yellow")
    screen.create_text(382, 372, anchor="c", text="AI", font=("Consolas", 25), fill="#666600")

    screen.update()


gameManager()

#   Binding, setting
screen.bind("<Button-1>", clicker)

#   Run forever
root.wm_title("Othello")
root.mainloop()
