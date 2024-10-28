
import os
import threading

from Location import Location

emptyValue = 'X'
board = [[emptyValue] * 12 for i in range(32)]
high = 32  # rows
width = 12  # colums

rowtitlesize = 20
coltitlesize = 40

computerTowerLocation = [Location(6, 2), Location(5, 6), Location(6, 9)]
userTowerLocation = [Location(26, 2), Location(27, 6), Location(26, 9)]

guiLock = threading.Lock()
boardLock = threading.Lock()
cardLock = threading.Lock()

# global variable that when a result is determined, True/False value will be stored.
isUserWinner = None

# method called when winner/loser is determined.
def displayWinner(side, msg):
    global isUserWinner

    print(msg)
    if side == 'Computer' :
        isUserWinner = True
    else:
        isUserWinner = False


boardLock = threading.Lock()  ## using the threading package that creates a boardlock


def getBoard(location):  ## this is for board read
    with boardLock:
        return board[location.row][location.col]


def setBoard(location, obj): ## this is for board write
    with boardLock:
        board[location.row][location.col] = obj


def printBoard():
    for i in range(high):
        for j in range(width):
            print(f'[{board[i][j]}]', end='')
        print('\n')

if __name__ == '__main__':
    displayWinner("User", "hello")
    print(f'value of isWniderr {isUserWinner}')