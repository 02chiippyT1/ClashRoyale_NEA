import os
import time
import webbrowser

import pygame, sys

import Global
from Card import Card
from Tower import Tower
from Troop import Troop
from Block import Block
from Debug import debug
from GameBoard import GameBoard
from Global import board, rowtitlesize, coltitlesize, getBoard
from Card1Display import Card1Display
from Card2Display import Card2Display
from Card3Display import Card3Display
from Card4Display import Card4Display
from Card5Display import Card5Display
from Card6Display import Card6Display
from Card7Display import Card7Display
from Card8Display import Card8Display
from Location import Location

WIDTH = 480
HIGTH = 640
FPS = 60
TITLESIZE = 40


# defining a font for Play and Exit
smallfont = pygame.font.SysFont('Corbel', 35)
# defining the front for 'How to Play', as the sentence is long, gives it smaller font.
smallfont2 = pygame.font.SysFont('Corbel', 25)


white = (255, 255, 255)
# rendering a text written in this font
playText = smallfont.render('Play', True, white)
exitText = smallfont.render('Exit', True, white)
howToText = smallfont2.render('How To Play', True, white)

# button colors to distinguish of armed or unarmed
color_light = (170, 170, 170)
color_dark = (100, 100, 100)

# loading the menu bitmap with the game's default resolution
initiating_window = pygame.image.load("menu.png")
initiating_window = pygame.transform.scale(
            initiating_window, (WIDTH, HIGTH))

# screen for declare user Win
win_ending_window = pygame.image.load("user_win_ending.png")
win_ending_window= pygame.transform.scale(
            win_ending_window, (WIDTH, HIGTH))

# screen for declare user loss
loss_ending_window = pygame.image.load("user_loss_ending.png")
loss_ending_window= pygame.transform.scale(
            loss_ending_window, (WIDTH, HIGTH))


class Game:
    def __init__(self):

        # general setup for pygame
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HIGTH))
        pygame.display.set_caption('Marcus Royale')
        self.clock = pygame.time.Clock()

        self.gameboard = None
        # self.gameboard.credit_mapping()
        self.selected = False
        self.selectedPos = None
        self.cardLocation = None

    def game_ending_window(self, isWin):

        if isWin :
            # load the winner window
            self.screen.blit(win_ending_window, (0, 0))
        else:
            # load the losing window
            self.screen.blit(loss_ending_window, (0, 0))

        # updating the display
        pygame.display.update()
        self.screen.fill(white)
        time.sleep(5)
        pygame.quit()
        os._exit(1)

    def game_initiating_window(self):
        # displaying over the screen

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    # sys.exit()
                    os._exit(1)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # start the game window
                    if 28 <= mouse[0] <= 185 and 118 <= mouse[1] <= 225:
                        self.gameboard = GameBoard()
                        self.gameboard.credit_mapping()
                        self.run()

                    # open the broswer with the url
                    if 28 <= mouse[0] <= 185 and 270 <= mouse[1] <= 380:
                        url = "https://www.wikihow.com/Play-Clash-Royale"
                        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
                        webbrowser.get(chrome_path).open(url)

                    # if the mouse is clicked on the
                    # button the game is terminated
                    if 28 <= mouse[0] <= 185 and 423 <= mouse[1] <= 530:
                        pygame.quit()
                        os._exit(1)

            # load the menu page
            self.screen.blit(initiating_window, (0, 0))

            mouse = pygame.mouse.get_pos()
            # print(f'x={mouse[0]}:y={mouse[1]}')

            # arm or unarm the Play option
            if 28 <= mouse[0] <= 185 and 118 <= mouse[1] <= 225:
                pygame.draw.rect(self.screen, color_light, [28,115, 165, 105])
            else:
                pygame.draw.rect(self.screen, color_dark, [28, 115, 165, 105])
            # arm or unarm the "how to play" option
            if 28 <= mouse[0] <= 185 and 270 <= mouse[1] <= 380:
                pygame.draw.rect(self.screen, color_light, [28, 270, 165, 105])
            else:
                pygame.draw.rect(self.screen, color_dark, [28, 270, 165, 105])
            # arm/unarm the Exit option
            if 28 <= mouse[0] <= 185 and 423 <= mouse[1] <= 530:
                pygame.draw.rect(self.screen, color_light, [28, 423, 165, 105])
            else:
                pygame.draw.rect(self.screen, color_dark, [28, 423, 165, 105])

            # label the Play option
            self.screen.blit(playText, (75, 150))

            # label the "how to play" option
            self.screen.blit(howToText, (45, 315))
            # label the Exit option
            self.screen.blit(exitText, (75, 465))

            # updating the display
            pygame.display.update()
            self.screen.fill(white)


    def run(self):
        obj = None

        while True:

            if Global.isUserWinner is not None:
                self.game_ending_window(Global.isUserWinner)



            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    os._exit(1)

                # if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed(3)[2]:
                if pygame.mouse.get_focused():
                    col, row = pygame.mouse.get_pos()
                    row = row // rowtitlesize
                    col = col // coltitlesize
                    # print("mpouse lcocked " + str(row) + " " + str(col))
                    obj = getBoard(Location(row,col))
                    # if obj != 'X':
                    #     print(obj)
                        # debug(obj, 0, 10)

                    # clicked_sprites = [s for s in self.gameboard.visible_sprites if
                    #                    s.rect.collidepoint(pos)]
                    # print(clicked_sprites)



                if event.type == pygame.MOUSEBUTTONUP and not self.selected:
                    self.selectedPos = pygame.mouse.get_pos()

                    clicked_sprites = [s for s in self.gameboard.visible_sprites if
                                       s.rect.collidepoint(self.selectedPos)]
                    if len(clicked_sprites) > 0:
                        if isinstance(clicked_sprites[0], Card5Display):  # card display objects
                            self.cardLocation = Location(28, 2)
                        if isinstance(clicked_sprites[0], Card6Display):
                            self.cardLocation = Location(28, 4)
                        if isinstance(clicked_sprites[0], Card7Display):
                            self.cardLocation = Location(28, 6)
                        if isinstance(clicked_sprites[0], Card8Display):
                            self.cardLocation = Location(28, 8)

                        if self.cardLocation is not None:
                            self.selected = True    # first click selects the CARD.
                            print(f'selected {self.cardLocation}')

                elif event.type == pygame.MOUSEBUTTONDOWN and self.selected:
                    mousex, mousey = pygame.mouse.get_pos()

                    print(f'{mousex}-{mousey}')
                    if 560 > mousey > 320:
                        row = mousey // rowtitlesize
                        col = mousex // coltitlesize
                        self.selected = False            # 2nd click selects the Spawn location
                        print(f'Target = {row}-{col}')
                        # now call the cardClick method with the calculated  location values
                        self.gameboard.cardClick(Location(self.cardLocation.row, self.cardLocation.col), Location(row, col))
                        self.cardLocation = None
                    else:
                        print("out of range.")

                    # pos = pygame.mouse.get_pos()
                    #
                    # # get a list of all sprites that are under the mouse cursor
                    # clicked_sprites = [s for s in self.gameboard.visible_sprites if s.rect.collidepoint(pos)]
                    # if len(clicked_sprites) > 0:
                    #     if isinstance(clicked_sprites[0], Card1Display):
                    #         self.gameboard.cardClick(Location(0,2), Location(7, 4))
                    #     if isinstance(clicked_sprites[0], Card2Display):
                    #         self.gameboard.cardClick(Location(0,4), Location(7, 5))
                    #     if isinstance(clicked_sprites[0], Card3Display):
                    #         self.gameboard.cardClick(Location(0,6), Location(7, 6))
                    #     if isinstance(clicked_sprites[0], Card4Display):
                    #         self.gameboard.cardClick(Location(0,8), Location(7, 7))
                    #     # if isinstance(clicked_sprites[0], Card5Display):
                    #     #     self.gameboard.cardClick(Location(28,2), Location(25, 4))
                    #     # if isinstance(clicked_sprites[0], Card6Display):
                    #     #     self.gameboard.cardClick(Location(28,4), Location(25, 5))
                    #     # if isinstance(clicked_sprites[0], Card7Display):
                    #     #     self.gameboard.cardClick(Location(28,6), Location(25, 6))
                    #     # if isinstance(clicked_sprites[0], Card8Display):
                    #     #     self.gameboard.cardClick(Location(28,8), Location(25, 7))

                    # do something with the clicked sprites...

            self.screen.fill('black')
            # debug('hello gavin: :)', 0, 10)
            self.gameboard.run()  # entry for the engine

            # when mouse hoovering on an object that no empty or Block objs
            if  obj != 'X' and obj is not None and not isinstance(obj, Block):

                text = obj.__str__()
                if  isinstance(obj, Troop) or isinstance(obj, Tower): # displays the health
                    text = obj.__str__() + "(health=" + str(obj.health) + ")"

                if isinstance(obj, Card):  # display the Card Elixir required
                    text = "Elixir Required: " + str(obj.elixirRequired)

                if obj.side == 'Computer':
                    debug(text , 0, 1)
                else:
                    debug(text, 31 * rowtitlesize, 1)

            debug("User Elixir    :" + str(self.gameboard.players[0].elixir.value), 31 * rowtitlesize, 8 * coltitlesize)
            debug("Computer Elixir:" + str(self.gameboard.players[1].elixir.value), 0 * rowtitlesize,  8 * coltitlesize)

            pygame.display.update()
            # pygame.display.flip()
            self.clock.tick(30)  ##FPS.


if __name__ == '__main__':
    game = Game()
    # game.game_ending_window(True)
    # Global.isUserWinner = True
    game.game_initiating_window()
    # game.run()
