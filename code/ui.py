import pygame 
from settings import *

class UI:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)

        # bar setup 
        self.health_bar_rect = pygame.Rect(60,600,HEALTH_BAR_WIDTH,BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(60,650,ENERGY_BAR_WIDTH,BAR_HEIGHT)

    def show_bar(self,current,max_amount,bg_rect,color):
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)

        # converting int stats to pixel to display in a bar
        


    def display(self,player):
        self.show_bar(player.health,player.stats['health'],self.health_bar_rect,HEALTH_COLOR)
        self.show_bar(player.energy,player.stats['energy'],self.energy_bar_rect,ENERGY_COLOR)