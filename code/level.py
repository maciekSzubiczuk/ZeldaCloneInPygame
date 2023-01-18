import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
import numpy as np
from weapon import Weapon
from ui import UI
from enemy import Enemy

class Level:
    def __init__(self):

        # get the display surface of the screen
        self.display_surface = pygame.display.get_surface()

        # grouping sprites into visible to player and colliding with the player
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        
        # attack sprites 
        self.current_attack = None

        #sprite setup
        self.create_map()

        # user interface 
        self.ui = UI()
        
    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('map/map_FloorBlocks.csv'),
            'object': import_csv_layout('map/map_Objects.csv'),
            'entities': import_csv_layout('map/map_Entities.csv')
        }
        graphics = {
            'objects': import_folder('/graphics/objects')
        }

        for style, layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index,col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE  
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites],'invisible')
                        if style == 'object':
                            if(int(col)<np.size(graphics['objects'])):
                                surf = graphics['objects'][int(col)]
                                Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'object',surf)

                        if style == 'entities':
                            if col=='394' :
                                self.player = Player((x,y),[self.visible_sprites],self.obstacle_sprites,self.create_attack,self.destroy_attack)
                            else:
                                if col == '390': monster_name = 'bamboo'
                                elif col == '391': monster_name = 'spirit'
                                elif col == '392': monster_name = 'raccoon'
                                else : monster_name = 'squid'
                                Enemy(monster_name,(x,y),[self.visible_sprites],self.obstacle_sprites)



        #for row_index,row in enumerate(WORLD_MAP):
        #    for col_index,col in enumerate(row):
        #       x = col_index * TILESIZE
        #       y = row_index * TILESIZE
        #       if col == 'x':
        #           Tile((x,y),[self.visible_sprites,self.obstacle_sprites])
        #       if col == 'p':
        #           self.player = Player((x,y),[self.visible_sprites],self.obstacle_sprites)
        

    def create_attack(self):
        self.current_attack = Weapon(self.player,[self.visible_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

            

    def run(self):
        # update and draw the game 
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.ui.display(self.player)
        debug(self.player.direction)

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_heigth = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2(100,200)
    
        # creating the map floor
        self.floor_surf = pygame.image.load('graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0,0))

    def custom_draw(self,player):

        # offset of camera
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_heigth

        #drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf,floor_offset_pos)

        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)

    def enemy_update(self,player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)