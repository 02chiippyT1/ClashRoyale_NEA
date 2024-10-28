from random import randrange
from threading import Thread

from Elixir import Elixir
from GameObjects import GameObjects

from time import sleep

from Global import coltitlesize, rowtitlesize
from Location import Location

user_row_min = 4
user_row_max = 14
computer_row_min = 17
computer_row_max = 27


class Player:

    def __init__(self, name, high, width, rowSide, elixir):
        self.name = name
        self.elixir = elixir
        self.gameObject = GameObjects
        self.myRowSide = rowSide
        self.playing = True
        self.visible_sprites = None

    def updateElixir(self, card):
        if card.side != self.gameObject.side:
            return None
        else:

            if card.elixirRequired > self.elixir.value:  # no enough Elixir, then stop the spawn
                return False

            self.elixir.value = self.elixir.value - card.elixirRequired  # update the Elixir as request
            print(f'elixir = {self.elixir}')
            card.visible_sprites = self.visible_sprites
            self.gameObject.nextCard(card)
            return True


class UserPlayer(Player):

    def __init__(self, name, width, groups):
        self.visible_sprites = groups
        x = 10 * coltitlesize
        y = 31 * rowtitlesize
        super().__init__(name, user_row_max, width, user_row_max, Elixir())
        self.gameObject = GameObjects("User")


class ComputerPlayer(Player):
    def __init__(self, width, groups):
        self.visible_sprites = groups
        x = 10 * coltitlesize
        y = 0 * rowtitlesize
        super().__init__("Computer", computer_row_min, width, computer_row_min, Elixir())
        self.gameObject = GameObjects("Computer")
        self.thread = None

    def play(self, groups):
        self.visible_sprites = groups
        self.thread = Thread(target=self.generation)
        self.thread.start()

    def generation(self):
        while self.playing:
            if self.elixir.value >= 10:
                idx = randrange(3)
                print(f'get a index = {idx}')
                newCard = self.gameObject.playingCards[idx]
                newCard.visible_sprites = self.visible_sprites
                idx2 = randrange(11)
                newCard.clicked(Location(7, idx2))
                self.updateElixir(newCard)
            sleep(5)


if __name__ == "__main__":
    user = UserPlayer("marcus", 10)
    computer = ComputerPlayer(10)
