from collections import deque

from Block import Block
from Card import ArcherCard, GoblinCard, HogRiderCard, MusketeerCard, GiantCard, PekkaCard, SkeletonCard, BarbarianCard

from Global import high, width, board, userTowerLocation, computerTowerLocation, cardLock, rowtitlesize, coltitlesize, \
    guiLock
from Location import Location
from Tower import QueenTower, KingTower


class GameObjects:

    def __init__(self, side):

        self.avaliableCards = deque([ArcherCard(side),
                                     GoblinCard(side),
                                     HogRiderCard(side),
                                     MusketeerCard(side),
                                     GiantCard(side),
                                     PekkaCard(side),
                                     SkeletonCard(side),
                                     BarbarianCard(side)])

        self.towers = [QueenTower(side), KingTower(side), QueenTower(side)]
        self.playingCards = deque([])

        self.side = side

        for i in range(12):
            if i != 2 and i != 9:
                board[15][i] = Block("r15" + str(i), "block.ico", Location(15, i))
                board[16][i] = Block("r16" + str(i), "block.ico", Location(16, i))

        if "Computer".__eq__(side):
            location = [Location(0, 2), Location(0, 4), Location(0, 6), Location(0, 8)]
            # towerLocation = [Location(6, 2), Location(5, 6), Location(6, 9)]

            for i in range(4):
                newCard = self.avaliableCards.popleft()
                newCard.location = location[i]
                self.playingCards.append(newCard)
                self.avaliableCards.append(newCard)
                for j in range(4):
                    board[j][location[i].col] = newCard
                    board[j][location[i].col + 1] = newCard

            for i in range(3):
                newTower = self.towers[i]
                newTower.location = computerTowerLocation[i]
                board[newTower.location.row][newTower.location.col] = newTower

            board[0][0] = Block("u1", "block.ico", Location(0, 0))
            board[1][0] = Block("u2", "block.ico", Location(0, 1))
            board[2][0] = Block("u3", "block.ico", Location(0, 2))
            board[3][0] = Block("u4", "block.ico", Location(0, 3))
            board[0][1] = Block("u5", "block.ico", Location(1, 0))
            board[1][1] = Block("u6", "block.ico", Location(1, 1))
            board[2][1] = Block("u7", "block.ico", Location(1, 2))
            board[3][1] = Block("u8", "block.ico", Location(1, 3))

            board[0][10] = Block("u9", "block.ico", Location(10, 0))
            board[1][10] = Block("u10", "block.ico", Location(10, 1))
            board[2][10] = Block("u11", "block.ico", Location(10, 2))
            board[3][10] = Block("u12", "block.ico", Location(10, 3))
            board[0][11] = Block("u13", "block.ico", Location(11, 0))
            board[1][11] = Block("u14", "block.ico", Location(11, 1))
            board[2][11] = Block("u15", "block.ico", Location(11, 2))
            board[3][11] = Block("u16", "block.ico", Location(11, 3))

        else:
            location2 = [Location(28, 2), Location(28, 4), Location(28, 6), Location(28, 8)]
            # towerLocation = [Location(26, 2), Location(27, 6), Location(26, 9)]

            for i in range(3):
                newTower = self.towers[i]
                newTower.location = userTowerLocation[i]
                board[newTower.location.row][newTower.location.col] = newTower

            for i in range(4):
                newCard = self.avaliableCards.popleft()
                newCard.location = location2[i]
                self.playingCards.append(newCard)
                self.avaliableCards.append(newCard)
                for j in range(28, 32):
                    board[j][location2[i].col] = newCard
                    board[j][location2[i].col + 1] = newCard

            board[28][0] = Block("u1", "block.ico", Location(0, 28))
            board[29][0] = Block("u2", "block.ico", Location(0, 29))
            board[30][0] = Block("u3", "block.ico", Location(0, 30))
            board[31][0] = Block("u4", "block.ico", Location(0, 31))
            board[28][1] = Block("u5", "block.ico", Location(1, 28))
            board[29][1] = Block("u6", "block.ico", Location(1, 29))
            board[30][1] = Block("u7", "block.ico", Location(1, 30))
            board[31][1] = Block("u8", "block.ico", Location(1, 31))

            board[28][10] = Block("u9", "block.ico", Location(10, 28))
            board[29][10] = Block("u10", "block.ico", Location(10, 29))
            board[30][10] = Block("u11", "block.ico", Location(10, 30))
            board[31][10] = Block("u12", "block.ico", Location(10, 31))
            board[28][11] = Block("u13", "block.ico", Location(11, 28))
            board[29][11] = Block("u14", "block.ico", Location(11, 29))
            board[30][11] = Block("u15", "block.ico", Location(11, 30))
            board[31][11] = Block("u16", "block.ico", Location(11, 31))

    def guiNextCard(self, index, newCard):
        row = index * rowtitlesize
        col = newCard.location.col * coltitlesize
        newCard.display((col, row), newCard.visible_sprites)

        row = index * rowtitlesize
        col = (newCard.location.col + 1) * coltitlesize
        newCard.display((col, row), newCard.visible_sprites)

    def nextCard(self, card):
        with cardLock:
            newCard = self.avaliableCards.popleft()
            while self.playingCards.__contains__(newCard):
                self.avaliableCards.append(newCard)
                newCard = self.avaliableCards.popleft()

            newCard.location = card.location
            newCard.visible_sprites = card.visible_sprites
            self.playingCards.remove(card)
            self.playingCards.append(newCard)
            self.avaliableCards.append(newCard)
            print(f'playing = {self.playingCards}')
            print(f'avaliable = {self.avaliableCards}')

            if "Computer".__eq__(self.side):
                with guiLock:
                    for j in range(4):
                        board[j][newCard.location.col] = newCard
                        board[j][newCard.location.col + 1] = newCard

                        if j == 0:
                            continue

                        self.guiNextCard(j, newCard)

            if "User".__eq__(self.side):
                with guiLock:
                    for j in range(28, 32):
                        board[j][newCard.location.col] = newCard
                        board[j][newCard.location.col + 1] = newCard
                        if j == 31:
                            continue

                        self.guiNextCard(j, newCard)

if __name__ == "__main__":

    go = GameObjects("User")
    go2 = GameObjects("Computer")

    ## User bottom   Computer top
    for i in range(high):
        for j in range(width):
            print(board[i][j], end=',')
        print('\n')

    print(go.playingCards)
    print(go.avaliableCards)
    print(go2.playingCards)
    print(go2.avaliableCards)
