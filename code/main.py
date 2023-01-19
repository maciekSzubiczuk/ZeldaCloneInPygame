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
                youDiedImage = pygame.image.load('graphics/tilemap/you_died.png').convert()
                self.screen.blit(youDiedImage,(0,0))
                magic_font = pygame.font.Font(UI_FONT, 50)
                instruction_surface = magic_font.render('Nacisnij Spacje aby zrestartowac gre',False, (54.5,0,0))
                instruction_rect = instruction_surface.get_rect(center = (650,600))
                self.screen.blit(instruction_surface,instruction_rect)
                pygame.display.update()
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