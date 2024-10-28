import uuid
from threading import Thread

from Global import emptyValue, board, coltitlesize, rowtitlesize, guiLock, getBoard, \
    setBoard, boardLock
from Location import Location
from time import sleep

from PathDisplay import PathDisplay
from Tower import QueenTower, Tower, KingTower
import random

from Troop1Display import Troop1Display
from Troop2Display import Troop2Display


class Troop:

    def __init__(self, name, health, damage, attackRange, attackDelay, moveRange, moveDelay, side, icon):
        self.objectId = uuid.uuid4()
        self.name = name
        self.health = health
        self.damage = damage
        self.attackRange = attackRange
        self.attackDelay = attackDelay
        self.moveRange = moveRange
        self.moveDelay = moveDelay
        self.location = Location(0, 0)
        self.side = side
        self.thread = None
        self.alive = True
        self.icon = icon

        self.visible_sprites = None

    def display(self, pos, groups):
        if self.side == "User":
            Troop1Display(pos, groups) # for User
        else:
            Troop2Display(pos, groups)

    def spawn(self, startedLocation):
        self.thread = Thread(target=self.moving, args=(startedLocation, "test")) # create the thread and calling the moving() method
        self.thread.start()

    def moving(self, startLocation, msg):

        sleep(3)
        while self.alive:  # denote the health > 0
            nextLocation = Location(startLocation.row, startLocation.col) ## start with the location it spawned
            if self.side == "User":
                nextLocation = self.findPathUser(nextLocation)  # looking for the next available location
            else:
                nextLocation = self.findPathComputer(nextLocation)

            if not self.alive:
                break

            self.move(startLocation, nextLocation)
            self.detect(nextLocation)

            startLocation = Location(nextLocation.row, nextLocation.col)

            # delay = random.randint(1, self.moveDelay)
            delay = self.moveDelay  # this implementing the speed of the movement
            # print(f'{self.side} waiting {delay}')
            sleep(delay)

        print(f'Thread {self.side}-{self.name}  is Terminated.')

    def pathDisplay(self, startedLocation):
        x = startedLocation.col * coltitlesize
        y = startedLocation.row * rowtitlesize

        PathDisplay((x, y), [self.visible_sprites])

    def move(self, startedLocation, targetLocation):
        print(f'{self.side}-{self.name} is moving from {startedLocation} to {targetLocation}')

        # board[startedLocation.row][startedLocation.col] = emptyValue
        # board[targetLocation.row][targetLocation.col] = self

        setBoard(startedLocation, emptyValue)
        setBoard(targetLocation, self)
        self.location = targetLocation

        with guiLock: # lock the event loop to perform the update
            self.pathDisplay(startedLocation)

            x1 = targetLocation.col * coltitlesize
            y1 = targetLocation.row * rowtitlesize
            self.display((x1,y1), [self.visible_sprites])

        # print(board)

    def isEmptyLocation(self, checkLocation) -> bool:
        try:
            if getBoard(checkLocation) == emptyValue:
                return True
            else:
                return False
        except IndexError:
            print(f'Error in IsTEmptyLocation: {checkLocation}')
            return False

    def findPathUser(self, startLocation) -> Location:
        # print("User path ...")
        # location at the left
        if startLocation.col < 2 and startLocation.row > 6:
            while startLocation.col < 2:
                startLocation.col = startLocation.col + 1
                while not self.isEmptyLocation(startLocation):
                    startLocation.row = startLocation.row - 1

            return startLocation

        if (startLocation.col == 2 or startLocation.col == 9) and startLocation.row > 6:
            startLocation.row = startLocation.row - 1
            while not self.isEmptyLocation(startLocation):
                # print(f'{self.name} waiting {startLocation} to be free ..')
                if self.isMySide(startLocation):
                    startLocation.col = startLocation.col + 1
                else:
                    self.attack(startLocation)

            return startLocation

        # location at the right
        if startLocation.col > 9 and startLocation.row > 6:
            while startLocation.col > 9:
                startLocation.col = startLocation.col - 1
                while not self.isEmptyLocation(startLocation):
                    startLocation.row = startLocation.row - 1

            return startLocation

        # location in the middle
        if (2 < startLocation.col < 9) and not startLocation.row <= 6:
            if startLocation.col < 6:
                # move left toward col 2
                while startLocation.col != 2:
                    tmpLocation = Location(startLocation.row, startLocation.col - 1)

                    if self.isEmptyLocation(tmpLocation):
                        return tmpLocation

                    tmpLocation = Location(startLocation.row - 1, startLocation.col)
                    if self.isEmptyLocation(tmpLocation):
                        return tmpLocation

                    tmpLocation = Location(startLocation.row - 1, startLocation.col - 1)
                    if self.isEmptyLocation(tmpLocation):
                        return tmpLocation
                    else:
                        print(f'{self.name} waiting {tmpLocation} to be free ..')
                        self.attack(tmpLocation)

                        sleep(3)  ## can't move to left.. wait.

            # move to right toward 9
            if startLocation.col >= 6:
                while startLocation.col != 9:
                    tmpLocation = Location(startLocation.row, startLocation.col + 1)

                    if self.isEmptyLocation(tmpLocation):
                        return tmpLocation

                    tmpLocation = Location(startLocation.row, startLocation.col - 1)
                    if self.isEmptyLocation(tmpLocation):
                        return tmpLocation

                    tmpLocation = Location(startLocation.row + 1, startLocation.col - 1)
                    if self.isEmptyLocation(Location(tmpLocation)):
                        return tmpLocation
                    else:
                        print(f'{self.name} waiting {tmpLocation} to be free ..')
                        self.attack(tmpLocation)
                        sleep(3)  ## can't move to left.. wait.

        # Queen(6, 2) is dead, then attack the king
        if startLocation.row <= 6 and startLocation.col < 5:

            while startLocation.row <= 26 and startLocation.col < 5:
                tmpLocation = Location(startLocation.row, startLocation.col + 1)
                if self.isEmptyLocation(tmpLocation):
                    return tmpLocation

                tmpLocation = Location(startLocation.row - 1, startLocation.col + 1)
                if self.isEmptyLocation(tmpLocation):
                    return tmpLocation
                else:
                    print(f'{self.name} waiting {tmpLocation} to be free ..')
                    self.attack(tmpLocation)
                    sleep(3)

        # Queen(6, 9) is dead, then attack the king
        if startLocation.row <= 26 and startLocation.col > 5:
            while startLocation.row <= 26 and startLocation.col > 5:
                tmpLocation = Location(startLocation.row, startLocation.col - 1)
                if self.isEmptyLocation(tmpLocation):
                    return tmpLocation

                tmpLocation = Location(startLocation.row - 1, startLocation.col - 1)
                if self.isEmptyLocation(tmpLocation):
                    return tmpLocation
                else:
                    print(f'{self.name} waiting {tmpLocation} to be free ..')
                    self.attack(tmpLocation)
                    sleep(3)

    def findPathComputer(self, startLocation) -> Location:
        # print("Computer path ..")
        # location at the left
        if startLocation.col < 2 and startLocation.row < 26:
            while startLocation.col < 2:
                startLocation.col = startLocation.col + 1
                while not self.isEmptyLocation(startLocation):
                    startLocation.row = startLocation.row + 1

            return startLocation

        if (startLocation.col == 2 or startLocation.col == 9) and startLocation.row < 26:
            startLocation.row = startLocation.row + 1
            while not self.isEmptyLocation(startLocation):
                # print(f'{self.name} waiting {startLocation} to be free ..')
                if self.isMySide(startLocation) :
                    startLocation.col = startLocation.col + 1
                else:
                    self.attack(startLocation)

            return startLocation

        # location at the right
        if startLocation.col > 9 and startLocation.row < 26:
            while startLocation.col > 9:
                startLocation.col = startLocation.col - 1
                while not self.isEmptyLocation(startLocation):
                    startLocation.row = startLocation.row + 1

            return startLocation

        # location in the middle
        if (2 < startLocation.col < 9) and not startLocation.row >= 26:
            if startLocation.col < 6:
                # move left toward col 2
                while startLocation.col != 2:
                    tmpLocation = Location(startLocation.row, startLocation.col - 1)

                    if self.isEmptyLocation(tmpLocation):
                        return tmpLocation

                    tmpLocation = Location(startLocation.row + 1, startLocation.col)
                    if self.isEmptyLocation(tmpLocation):
                        return tmpLocation

                    tmpLocation = Location(startLocation.row + 1, startLocation.col - 1)
                    if self.isEmptyLocation(tmpLocation):
                        return tmpLocation
                    else:
                        # print(f'{self.name} waiting {tmpLocation} to be free ..')
                        self.attack(tmpLocation)
                        sleep(3)  ## can't move to left.. wait.

            # move to right toward 9
            if startLocation.col >= 6:
                while startLocation.col != 9:
                    tmpLocation = Location(startLocation.col + 1, startLocation.row)

                    if self.isEmptyLocation(tmpLocation):
                        return tmpLocation

                    tmpLocation = Location(startLocation.col, startLocation.row + 1)
                    if self.isEmptyLocation(tmpLocation):
                        return tmpLocation

                    tmpLocation = Location(startLocation.col + 1, startLocation.row + 1)
                    if self.isEmptyLocation(Location(tmpLocation)):
                        return tmpLocation
                    else:
                        # print(f'{self.name} waiting {tmpLocation} to be free ..')
                        self.attack(tmpLocation)
                        sleep(3)  ## can't move to left.. wait.

        # Queen(26, 2) is dead, then attack the king
        if startLocation.row >= 26 and startLocation.col < 5:

            while startLocation.row >= 26 and startLocation.col < 5:
                tmpLocation = Location(startLocation.row, startLocation.col + 1)
                if self.isEmptyLocation(tmpLocation):
                    return tmpLocation

                tmpLocation = Location(startLocation.row + 1, startLocation.col + 1)
                if self.isEmptyLocation(tmpLocation):
                    return tmpLocation
                else:
                    self.attack(tmpLocation)
                    sleep(3)

        # Queen(26, 9) is dead, then attack the king
        if startLocation.row >= 26 and startLocation.col > 5:
            while startLocation.row >= 26 and startLocation.col > 5:
                tmpLocation = Location(startLocation.row , startLocation.col -1)
                if self.isEmptyLocation(tmpLocation):
                    return tmpLocation

                tmpLocation = Location(startLocation.row + 1, startLocation.col - 1)
                if self.isEmptyLocation(tmpLocation):
                    return tmpLocation
                else:
                    # print(f'{self.name} waiting {tmpLocation} to be free ..')
                    self.attack(tmpLocation)
                    sleep(3)

    def detect(self, startLocation):
        #
        # queen1Location = Location(26, 2)
        # queen2Location = Location(26, 9)
        # kingLocation = Location(27, 5)

        i = 1
        while i <= self.attackRange:
            tmpLocation = Location(startLocation.row + i, startLocation.col)  # check row + i, col no change
            if not self.isEmptyLocation(tmpLocation):  # if no empty then perform further check
                self.attack(tmpLocation)  # attack will check if enemy or not, it will only attack if the location
                                          # contains enemy, otherwise, this will return

            tmpLocation = Location(startLocation.row, startLocation.col + i)
            if not self.isEmptyLocation(tmpLocation):
                self.attack(tmpLocation)

            tmpLocation = Location(startLocation.row + i, startLocation.col + i)
            if not self.isEmptyLocation(tmpLocation):
                self.attack(tmpLocation)

            tmpLocation = Location(startLocation.row - i, startLocation.col)
            if not self.isEmptyLocation(tmpLocation):
                self.attack(tmpLocation)

            tmpLocation = Location(startLocation.row, startLocation.col - i)
            if not self.isEmptyLocation(tmpLocation):
                self.attack(tmpLocation)

            tmpLocation = Location(startLocation.row - i, startLocation.col - i)
            if not self.isEmptyLocation(tmpLocation):
                self.attack(tmpLocation)

            tmpLocation = Location(startLocation.row + i, startLocation.col - i)
            if not self.isEmptyLocation(tmpLocation):
                self.attack(tmpLocation)

            tmpLocation = Location(startLocation.row - i, startLocation.col + i)
            if not self.isEmptyLocation(tmpLocation):
                self.attack(tmpLocation)
            i = i + 1

    def isMySide(self, targetLocation ):
        try:
            obj = getBoard(targetLocation)
            result = obj.side == self.side
            return result

        except AttributeError:
            return False

    def attack(self, targetLocation):
        try:
            obj = getBoard(targetLocation)
            if (isinstance(obj, Tower) or isinstance(obj, Troop)) and (obj.side != self.side):
                while not self.isEmptyLocation(targetLocation) and obj.health > 0 :
                    if self.health <= 0:
                        return

                    obj.health = obj.health - self.damage
                    print(f'{obj.side}-{obj.name} health remain {obj.health}')
                    if obj.health > 0:
                        sleep(self.attackDelay)

                if self.isEmptyLocation(targetLocation) and obj.health > 0:
                    return
                else:
                    print(f'Enemy {obj.side} {obj.name} is terminated by {self.name}{self.location}. {obj.health}')
                    setBoard(targetLocation, emptyValue )

                    obj.dead()
                    # if isinstance(obj, KingTower):
                    #     printBoard()
                    #     displayWinner(f'{self.side} has won the game.')
        except IndexError:
            print(f'incorrect index : {targetLocation}')
            return

    def dead(self):
        self.alive = False
        with guiLock:
            self.pathDisplay(self.location)


    def __str__(self):
        # return f'Attributes objectId={self.objectId} name={self.name} health={self.health} damage={self.damage} attackRange={self.attackRange} attackDelay={self.attackDelay} moveRange={self.moveRange} moveDelay={self.moveDelay} location={self.location}'
        return f'name={self.name}-{self.location}:{self.side}'

# name, health, damage, attackRange, attackDelay, moveRange, moveDelay, side
class Skeleton(Troop):

    def __init__(self, side):
        super().__init__("Skeleton", 50, 11, 1, 3, 14, 5, side, "Skeleton.png")


class Barbarian(Troop):

    def __init__(self, side):
        super().__init__("Barbarian", 70, 11, 1, 3, 14, 5, side, "Barbarian.png")


class Archer(Troop):

    def __init__(self, side):
        super().__init__("Archer", 30, 15, 3, 3, 14, 5, side, "Archer.png")


class Pekka(Troop):

    def __init__(self, side):
        super().__init__("Pekka", 35, 11, 1, 3, 14, 5, side, "Pekka.png")


class Goblin(Troop):

    def __init__(self, side):
        super().__init__("Goblin", 15, 8, 1, 3, 14, 5, side, "Goblin.png")


class Musketeer(Troop):

    def __init__(self, side):
        super().__init__("Musketeer", 40, 5, 1, 3, 14, 5, side, "Musketeer.png")


class HogRider(Troop):

    def __init__(self, side):
        super().__init__("HogRider", 60, 11, 1, 3, 14, 5, side, "HogRider.png")


class Giant(Troop):

    def __init__(self, side):
        super().__init__("Giant", 100, 11, 1, 3, 14, 5, side, "Giant.png")


if __name__ == "__main__":
    skeleton = Skeleton("User")
    skeleton3 = Skeleton("User")
    archer = Archer("User")
    board[6][9] = archer

    board[26][2] =  QueenTower("Computer")
    board[27][5] = KingTower("Computer")
    board[26][9] = QueenTower("Computer")

    board[6][2] = QueenTower("User")
    board[5][6] = KingTower("User")
    board[6][9] = QueenTower("User")

    # skeleton3.spawn(Location(6,1))  #test left
    # skeleton.spawn(Location(6,10)) #test right
    # skeleton.spawn(Location(6, 4))  # test middle left
    # skeleton.spawn(Location(6, 7))  # test middle left

    skeleton2 = Skeleton("Computer")
    skeleton2.spawn(Location(25, 7))  # test left

