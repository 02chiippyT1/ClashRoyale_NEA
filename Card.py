import uuid

from Card1Display import Card1Display
from Card2Display import Card2Display
from Card3Display import Card3Display
from Card4Display import Card4Display
from Card5Display import Card5Display
from Card6Display import Card6Display
from Card7Display import Card7Display
from Card8Display import Card8Display
from Global import board, coltitlesize, rowtitlesize, guiLock, setBoard
from Location import Location
from Troop import Archer, Goblin, HogRider, Musketeer, Giant, Pekka, Skeleton, Barbarian


class Card:

    def __init__(self, name, icon, elixirRequired, side):
        self.objectId = uuid.uuid4()
        self.name = name
        self.icon = icon
        self.elixirRequired = elixirRequired
        self.location = Location(0, 0)
        self.troops = []
        self.side = side

        self.visible_sprites = None

    def spawnTroop(self, selectedLocation, troop):
        print("Spawns: " + self.__str__())
        # board[selectedLocation.row][selectedLocation.col] = troop
        setBoard(selectedLocation, troop)
        x = troop.location.col * coltitlesize
        y = troop.location.row * rowtitlesize
        with guiLock:
            troop.display((x, y), [self.visible_sprites])
            troop.visible_sprites = self.visible_sprites

        troop.spawn(selectedLocation)

    def clicked(self, selectedLocation):
        self.spawnTroop(selectedLocation) # calling the instance's spawnTroop method depends the subclass type of the Card.

    def __str__(self):
        # return f'Attributes objectId={self.objectId} name={self.name} elixirRequired={self.elixirRequired} location={self.location}'

        return f'name={self.name}-{self.location}-{self.side}'

    def display(self, pos, groups):
        if self.location.row == 0  and self.location.col == 2:
            Card1Display(pos, groups, self.icon)
            # at specified row and col, so when they are clicked, correct location can be retrieved

        if self.location.row == 0  and self.location.col == 4:
            Card2Display(pos, groups, self.icon)

        if self.location.row == 0  and self.location.col == 6:
            Card3Display(pos, groups, self.icon)

        if self.location.row == 0  and self.location.col == 8:
            Card4Display(pos, groups, self.icon)

        if self.location.row == 28  and self.location.col == 2:
            Card5Display(pos, groups, self.icon)

        if self.location.row == 28  and self.location.col == 4:
            Card6Display(pos, groups, self.icon)

        if self.location.row == 28  and self.location.col == 6:
            Card7Display(pos, groups, self.icon)

        if self.location.row == 28  and self.location.col == 8:
            Card8Display(pos, groups, self.icon)


class ArcherCard(Card):
    def __init__(self, side):
        super().__init__("ArcherCard", "ArcherCard.png", 3, side)

    def spawnTroop(self, selectedLocation):
        troop = Archer(self.side)  # instance of Archer is created.
        troop.location = selectedLocation
        self.troops.append(troop)  # added the instance to the troops llist
        super().spawnTroop(selectedLocation, troop) # calling super class to carry on with the spawning


class GoblinCard(Card):
    def __init__(self, side):
        super().__init__("GoblinCard", "GoblinCard.png", 2, side)

    def spawnTroop(self, selectedLocation):
        troop = Goblin(self.side)
        troop.location = selectedLocation
        self.troops.append(troop)
        super().spawnTroop(selectedLocation, troop)


class HogRiderCard(Card):
    def __init__(self, side):
        super().__init__("HogRiderCard", "HogRiderCard.png", 4, side)

    def spawnTroop(self, selectedLocation):
        troop = HogRider(self.side)
        troop.location = selectedLocation
        self.troops.append(troop)
        super().spawnTroop(selectedLocation, troop)


class MusketeerCard(Card):
    def __init__(self, side):
        super().__init__("MusketeerCard", "MusketeerCard.png", 4, side)

    def spawnTroop(self, selectedLocation):
        troop = Musketeer(self.side)
        troop.location = selectedLocation
        self.troops.append(troop)
        super().spawnTroop(selectedLocation, troop)


class GiantCard(Card):
    def __init__(self, side):
        super().__init__("GiantCard", "GiantCard.png", 5, side)

    def spawnTroop(self, selectedLocation):
        troop = Giant(self.side)
        troop.location = selectedLocation
        self.troops.append(troop)
        super().spawnTroop(selectedLocation, troop)


class PekkaCard(Card):
    def __init__(self, side):
        super().__init__("PekkaCard", "PekkaCard.png", 8, side)

    def spawnTroop(self, selectedLocation):
        troop = Pekka(self.side)
        troop.location = selectedLocation
        self.troops.append(troop)
        super().spawnTroop(selectedLocation, troop)


class SkeletonCard(Card):
    def __init__(self, side):
        super().__init__("SkeletonCard", "SkeletonCard.png", 1, side)

    def spawnTroop(self, selectedLocation):
        troop = Skeleton(self.side)
        troop.location = selectedLocation
        self.troops.append(troop)
        super().spawnTroop(selectedLocation, troop)


class BarbarianCard(Card):
    def __init__(self, side):
        super().__init__("BarbarianCard", "BarbarianCard.png", 2, side)

    def spawnTroop(self, selectedLocation):
        troop = Barbarian(self.side)
        troop.location = selectedLocation
        self.troops.append(troop)
        super().spawnTroop(selectedLocation, troop)


if __name__ == "__main__":
    skeleton = SkeletonCard("User")
    print(skeleton)