import uuid
from threading import Thread
from time import sleep

import Global
from Global import board, emptyValue, printBoard, userTowerLocation, computerTowerLocation
from KingTowerDisplay import KingTowerDisplay
from Location import Location
from QueenTowerDisplay import QueenTowerDisplay


class Tower:


    def __init__(self, name, health, damage, attackDelay, side):
        self.objectId = uuid.uuid4()
        self.name = name
        self.health = health
        self.damage = damage
        self.attackDelay = attackDelay
        self.location = Location(0, 0)
        self.alive = True
        self.side = side
        self.thread = None


    def __str__(self):
        # return f'Attributes objectId={self.objectId} name={self.name} health={self.health} damage={self.damage} attackRane={self.attackRange} attackDelay={self.attackDelay} location={self.location}'

        return f'name={self.name}-{self.location}:{self.side}'

    def getQueenTowerIndex(self, objId):
        for i in range(0, 3):
            if self.side == "User":
                if userTowerLocation[i] == self.location:
                    return i;
            else:
                if computerTowerLocation[i] == self.location:
                    return i;

    def attack(self, targetLocation):
        obj = board[targetLocation.row][targetLocation.col]
        if obj.side != self.side:
            while not self.isEmptyLocation(targetLocation) and obj.health > 0:
                if self.health <= 0:
                    return

                obj.health = obj.health - self.damage
                print(f'{obj.side}-{obj.name} health remain {obj.health}')
                if obj.health > 0:
                    sleep(self.attackDelay)

            if self.isEmptyLocation(targetLocation) and obj.health > 0 and self.health > 0:
                return
            else:
                print(f'Enemy {obj.side} {obj.name} is terminated by {self.name}{self.location}. {obj.health}')
                board[targetLocation.row][targetLocation.col] = emptyValue
                obj.dead()

    def startDetection(self, queenside):
        if self.side == "User":
            self.thread = Thread(target=self.detectFromUser, args=(queenside, ""))
            self.thread.start()
        else:
            self.thread = Thread(target=self.detectFromComputer, args=(queenside, ""))
            self.thread.start()

    def isEmptyLocation(self, checkLocation) -> bool:
        if board[checkLocation.row][checkLocation.col] == emptyValue:
            return True
        else:
            return False

    def detectFromComputer(self, queenSide, msg):
        # while self.location.row == 0 and self.location.col == 0:
        #     continue

        sleep(3)
        pos = self.getQueenTowerIndex(self.objectId)
        rowStart = 0
        rowEnd = 0
        colStart = 0
        colEnd = 0

        if pos == 0:  #LEFT queue
            rowStart = 14
            rowEnd = 4
            colStart = 0
            colEnd = 5

        if pos == 2: #Right Queue
            rowStart = 14
            rowEnd = 4
            colStart = 5
            colEnd = 11

        if pos ==1 and queenSide == 'LEFT':
            rowStart = 11
            rowEnd = 4,
            colStart = 0
            colEnd = 5

        if pos == 1 and queenSide == 'RIGHT':
            rowStart = 11
            rowEnd = 4
            colStart = 5
            colEnd = 11

        print(f'starting {self}  detection between {rowStart} and {rowEnd} ..')
        while self.alive:
            try:
                for row in range(rowStart, rowEnd, -1):
                    for col in range(colStart, colEnd):
                        location = Location(row, col)
                        if not self.isEmptyLocation(location):
                            self.attack(location)
            except TypeError as e:
                print(e)
            sleep(5)
        print(f'{self.side}=-{self.name} detection stops')

    def detectFromUser(self, queenSide, msg):

        sleep(3)

        pos = self.getQueenTowerIndex(self.objectId)
        rowStart = 0
        rowEnd = 0
        colStart = 0
        colEnd = 0

        if pos == 0:  # LEFT queue
            rowStart = 17
            rowEnd = 27
            colStart = 0
            colEnd = 5

        if pos == 2:  # Right Queue
            rowStart = 17
            rowEnd = 27
            colStart = 5
            colEnd = 11

        if pos == 1 and queenSide == 'LEFT':
            rowStart = 17
            rowEnd = 27
            colStart = 0
            colEnd = 5

        if pos == 1 and queenSide == 'RIGHT':
            rowStart = 17
            rowEnd = 27
            colStart = 5
            colEnd = 11

        print(f'starting {self}  detection between {rowStart} and {rowEnd} ..')

        while self.alive:
            try:
                for row in range(rowStart, rowEnd):
                    for col in range(colStart, colEnd):
                        location = Location(row, col)
                        if not self.isEmptyLocation(location):
                            self.attack(location)
            except TypeError as e:
                print(e)
            sleep(5)
        print(f'{self.side}=-{self.name} detection stops')

    def dead(self):
        self.alive = False


class KingTower(Tower):
    def __init__(self, side):
        super().__init__("KingTower",  200, 10,  5, side)

    def dead(self):  # King Tower
        self.alive = False

        printBoard()
        Global.displayWinner(self.side, f'{self.side} has lost the game.')

    def display(self, pos, groups):
        KingTowerDisplay(pos, groups)

class QueenTower(Tower):
    def __init__(self, side):
        super().__init__("QueenTower",  100, 3,  3, side)

        self.startDetection("START")

    def display(self, pos, groups):
        QueenTowerDisplay(pos, groups)

    def getKingTower(self, side) -> Location:
        if side == "User":
            return userTowerLocation[1]
        else:
            return computerTowerLocation[1]

    def dead(self):
        self.alive = False

        # left Queue dead, then King detect left,  if right Queen dead, King detect. If both dead, then both side.
        if self.getQueenTowerIndex(self.objectId) == 0:
            if self.side == "User":
                location = self.getKingTower("User")
                board[location.row][location.col].startDetection("LEFT")
                print(f'started User King detection on LEFT')
            else:
                location = self.getKingTower("Computer")
                board[location.row][location.col].startDetection("LEFT")
                print(f'started Computer King detection on LEFT')

        if self.getQueenTowerIndex(self.objectId) == 2:
            if self.side == "Computer":
                location = self.getKingTower("Computer")
                board[location.row][location.col].startDetection("RIGHT")
                print(f'started Computer King detection on Right')
            else:
                location = self.getKingTower("User")
                board[location.row][location.col].startDetection("RIGHT")
                print(f'started User King detection on Right')

if __name__ == "__main__":
    towers = [QueenTower("User"), KingTower("User"), QueenTower("User")]

    for item in towers:
        print(item.objectId, item.name)
