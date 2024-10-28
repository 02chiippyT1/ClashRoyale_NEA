
def attack(self, targetLocation):
    obj = board[targetLocation.row][targetLocation.col]
    if (isinstance(obj, Tower) or isinstance(obj, Troop)) and (obj.side != self.side):  # only attack if one of these
        while not self.isEmptyLocation(targetLocation) and obj.health > 0:
            if self.health <= 0:  # someone killed the target
                return

            obj.health = obj.health - self.damage  # taking target's health with my damage
            print(f'{obj.side}-{obj.name} health remain {obj.health}')
            if obj.health > 0:
                sleep(self.attackDelay)   # apply the attackDelay

        if self.isEmptyLocation(targetLocation) and obj.health > 0:  # target moved away
            return
        else:
            print(f'Enemy {obj.side} {obj.name} is terminated by {self.name}{self.location}. {obj.health}')
            board[targetLocation.row][targetLocation.col] = emptyValue  # target is dead
            obj.dead()  # mark it as dead to stop target's thread
            if isinstance(obj, KingTower):  # if  target is enemy King towner, the game is finished
                printBoard()
                displayWinner(f'{self.side} has won the game.')

def move(self, startedLocation, targetLocation):
    print(f'{self.side}-{self.name} is moving from {startedLocation} to {targetLocation}')
    board[startedLocation.row][startedLocation.col] = emptyValue
    board[targetLocation.row][targetLocation.col] = self


class ComputerPlayer(Player):
        def __init__(self, width, groups):
            self.visible_sprites = groups
            x = 10 * coltitlesize
            y = 0 * rowtitlesize
            super().__init__("Computer", computer_row_min, width, computer_row_min, Elixir())
            self.gameObject = GameObjects("Computer")
            self.thread = None

        def play(self, groups):
            self.thread = Thread(target=self.generation)
            self.thread.start()

        def generation(self):  # generator
            while self.playing:  # user no quit the game
                if self.elixir.value > 10:  # assuming only when it has maximum elixir, then it tries to spawn troop
                    idx = randrange(3) # generating a random number to select a card.
                    print(f'get a index = {idx}')
                    newCard = self.gameObject.playingCards[idx]  # simulating a mouse click
                    idx2 = randrange(11)  # a random column at row #7
                    newCard.clicked(Location(7, idx2))
                    self.updateElixir(newCard)
                sleep(5)


 def run(self):
        obj = None

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    # sys.exit()
                    os._exit(1)

            self.gameboard.run()  # entry for the engine
            pygame.display.update()
            # pygame.display.flip()
            self.clock.tick(30)  ##FPS.

    def run(self):
        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update()