import pygame, sys
from settings import *
from level import Level

class Game:
    def __init__(self):
          
        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
        pygame.display.set_caption('Greed Island')
        self.clock = pygame.time.Clock()
        self.level = Level()

    def run(self):
        while True:
            if not self.level.player.game_over:
                self.screen.fill('black')
                self.level.run()
                pygame.display.update()
                self.clock.tick(FPS)
            else:
                key = pygame.key.get_pressed()
                if key[pygame.K_SPACE]:
                    self.__init__()
                    self.level.player.game_over = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

if __name__ == '__main__':
    while True:
        game = Game()
        game.run()