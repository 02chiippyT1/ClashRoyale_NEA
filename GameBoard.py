import pygame

from BlockDisplay import BlockDisplay
from Debug import debug
from Elixir import Elixir
from Global import high, width, board, coltitlesize, rowtitlesize, emptyValue, guiLock
from KingTowerDisplay import KingTowerDisplay
from Location import Location
from PathDisplay import PathDisplay
from Player import UserPlayer, ComputerPlayer
from time import sleep
from threading import Thread


class GameBoard:
    gametimer: int
    image: str

    players = []

    # Suppose that two numbers are given: the number of rows of n and the number of columns m. You must create a list of size n×m, filled with, say, zeros.

    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.visible_sprites = pygame.sprite.Group()
        self.obstacles_sprites = pygame.sprite.Group()

    def exit(self):
        exit(0)

    def startGame(self):
        pass

    def options(self):
        pass

    def playGame(self):
        user = UserPlayer()
        computer = ComputerPlayer()

    def quickExit(self):
        pass

    def cardClick(self, cardLocation, selectedLocation):
        clickedCard = board[cardLocation.row][cardLocation.col]

        if clickedCard.side == 'User':
            if not self.players[0].updateElixir(clickedCard):
                print(
                    f'User No enough Elixir for the Card : {self.players[0].elixir.value}/{clickedCard.elixirRequired}')
                return  ## uncomment this to enable Elixir check on User.
        elif clickedCard.side == 'Computer':
            if not self.players[1].updateElixir(clickedCard):
                print(
                    f'Computer No enough Elixir for the Card : {self.players[1].elixir.value}/{clickedCard.elixirRequired}')
                return

        clickedCard.visible_sprites = self.visible_sprites
        clickedCard.clicked(selectedLocation)

    def computerPayer(self):
        self.players[1].play(self.visible_sprites)

    def printBoard(self):
        for i in range(high):
            for j in range(width):
                print(f'[{board[i][j]}]', end='')
            print('\n')

    def credit_mapping(self):
        # pass the visible_sprites as parameter to create Player,so that we can add all the displayable objects
        # into the list.
        self.players.append(UserPlayer("Marcu", width, self.visible_sprites))
        self.players.append(ComputerPlayer(width, self.visible_sprites))
        self.players[0].visible_sprites = self.visible_sprites
        self.players[1].visible_sprites = self.visible_sprites

        for row_index in range(high):  # this loop goes through the board array to create empty value as PathDisplay.
            for col_index in range(width):
                if row_index in range(0, 1) and col_index in range(0, 12):
                    continue

                if row_index in range(31, 32) and col_index in range(0, 12):
                    continue

                x = col_index * coltitlesize
                y = row_index * rowtitlesize
                obj = board[row_index][col_index]
                if obj == emptyValue:
                    PathDisplay((x, y), [self.visible_sprites])  # create PathDisplay which uses path.png
                if obj != emptyValue:
                    obj.display((x, y), [self.visible_sprites])  # added to the display list

            # print(row_index)
            # print(row)
        # self.test()
        self.computerPayer()  # start the computer player

    def test(self):
        testThread = Thread(target=self.testplay)
        testThread.start()

    def testplay(self):
        sleep(10)
        # self.cardClick(Location(0, 2), Location(7, 2))
        # self.cardClick(Location(0, 4), Location(10, 5))
        # self.cardClick(Location(28, 4), Location(23, 5))
        self.computerPayer()

    def run(self):
        with guiLock:
            self.visible_sprites.draw(self.display_surface)
            self.visible_sprites.update()


if __name__ == "__main__":
    gb = GameBoard()
    gb.gametimer = 100
    print(high)
    print(gb.gametimer)

    gb.players.append(UserPlayer("Marcus", 10, None))
    gb.players.append(ComputerPlayer(width, None))
    gb.computerPayer()

    # while True:
    #
    #     location1 = None
    #     location2 = None
    #     try:
    #         card = input("please enter Card Location in the format of <Row1,Column1>:")
    #         if card == "exit":
    #             break
    #         row1, col1 = card.split(",")
    #         location1 = Location(int(row1), int(col1))
    #     except Exception as e:
    #         print("Try again")
    #         continue
    #
    #     try:
    #         spawnLocation = input("please enter Spawn Location in the format of <Row2, Column2>:")
    #         row2, col2 = spawnLocation.split(",")
    #         location2 = Location(int(row2), int(col2))
    #
    #         gb.cardClick(location1, location2)
    #     except Exception as e:
    #         print("Try again")
    #         continue

    gb.cardClick(Location(0, 8), Location(6, 4))
    #
    # gb.cardClick(Location(28, 4), Location(26, 1))

    for x in range(2):
        p = gb.players[x]
        p.elixir.stop()

    # gb.printBoard()

    gb.exit()
