import pygame


class Troop1Display(pygame.sprite.Sprite):

    def __init__(self, pos, groups, img='troop1.png'):
        super().__init__(groups)
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
