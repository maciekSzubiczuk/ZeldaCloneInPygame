import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups,obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/testAssets/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.math.Vector2()
        self.speed = 5

        self.obstacle_sprites = obstacle_sprites

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y=-1
        elif keys[pygame.K_DOWN]:
            self.direction.y=1
        else:
            self.direction.y=0

        if keys[pygame.K_RIGHT]:
            self.direction.x=1
        elif keys[pygame.K_LEFT]:
            self.direction.x=-1
        else:
            self.direction.x=0

    def move(self,speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.rect.x += self.direction.x *speed
        self.collision('horizontal')
        self.rect.y += self.direction.y *speed
        self.collision('vertical')

    def collision(self,direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    # if the player is moving right
                    if self.direction.x > 0:
                        # if the player collides with something move him to the left side of the object
                        self.rect.right = sprite.rect.left
                    # movement to the left collision   
                    if self.direction.x < 0:
                        self.rect.left = sprite.rect.right
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:   
                if sprite.rect.colliderect(self.rect):
                    # movement up collision
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top
                    # movement down collision
                    if self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom
                    
        if direction == 'vertical':
            pass

    def update(self):
        self.input()
        self.move(self.speed)