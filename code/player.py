import pygame
from settings import *
from support import import_folder
from entity import Entity

class Player(Entity):
    def __init__(self,pos,groups,obstacle_sprites,create_attack,destroy_attack):

        super().__init__(groups)
        self.image = pygame.image.load('graphics/testAssets/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0,-26)

        # graphics setup
        self.import_player_assets()
        self.status='down'

        # movement
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites

        # weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]

        # stats for player character
        self.stats = {'health':100, 'energy':60,'attack':10,'magic':4,'speed':6}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 123
        self.speed = self.stats['speed']
        self.game_over = False

        # damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability = 500

    def import_player_assets(self):
        character_path = 'graphics/player/'
        self.animations = {'up':[],'down':[],'left':[],'right':[],'left_idle': [],'up_idle': [],'down_idle': [],
                            'right_idle':[],'right_attack': [],'left_attack':[],'up_attack':[],'down_attack':[]}
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def get_status(self):

        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'
            
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle','_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack','')

    def input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()

            # input for movement
            if keys[pygame.K_UP]:
                self.direction.y=-1
                self.status='up'
            elif keys[pygame.K_DOWN]:
                self.direction.y=1
                self.status='down'
            else:
                self.direction.y=0

            if keys[pygame.K_RIGHT]:
                self.direction.x=1
                self.status='right'
            elif keys[pygame.K_LEFT]:
                self.direction.x=-1
                self.status='left'
            else:
                self.direction.x=0

            # input for attacking
            if keys[pygame.K_SPACE] and not self.attacking:
                self.attacking=True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()

            # input for magic
            if keys[pygame.K_LCTRL] and not self.attacking:
                self.attacking=True
                self.attack_time = pygame.time.get_ticks()
                print('magic')
              
    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
                self.attacking = False
                self.destroy_attack()
        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability:
                self.vulnerable = True

    def animate(self):
        animation = self.animations[self.status]

        #loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage

    def check_death(self):
        if self.health <= 0:
            self.game_over = True

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
        self.check_death()