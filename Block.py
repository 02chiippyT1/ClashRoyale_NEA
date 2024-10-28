import uuid

from BlockDisplay import BlockDisplay
from Location import Location




class Block:


    def __init__(self, name, icon, location):
        self.objectId = uuid.uuid4()
        self.name = name
        self.icon = icon
        self.location = location

    def __str__(self):
        return f'({self.name}-{self.location})'

    def display(self, pos, groups):
        BlockDisplay(pos, groups)