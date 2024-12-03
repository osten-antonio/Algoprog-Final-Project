from settings import *
from math import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        original_width, original_height = surf.get_size()

        new_width = int(original_width * 4)
        new_height = int(original_height * 4)
        self.image = pygame.transform.scale(surf, (new_width, new_height))

        self.rect = self.image.get_frect(center = pos)

class BoundingBox(pygame.sprite.Sprite):
    def __init__(self,x,y,height,width, groups):
        super().__init__(groups)
        self.rect = pygame.FRect(x,y,height,width)

class PlayerSwing(pygame.sprite.Sprite):
    def __init__(self,range,player,groups):
        super().__init__(groups)
        self.range = range
        self.player = player
        self.rect = pygame.FRect((self.player.hitbox.center), (self.range,self.range))
        self.angle = 90

    def update(self, *args, **kwargs):
        # Update the swing rectangle to follow the player
        direction = self.player.direction
        if direction.x != 0 or direction.y != 0:
            self.angle = degrees(atan2(direction.x,direction.y)) if\
                degrees(atan2(direction.x,direction.y)) >=0 else\
                    degrees(atan2(direction.x,direction.y))+360
              
        # Direction
        if self.angle == 0:
            self.rect.top=self.player.hitbox.centery
            self.rect.centerx=self.player.hitbox.centerx
        if self.angle == 90:
            self.rect.centery=self.player.hitbox.centery
            self.rect.left=self.player.hitbox.centerx
        if self.angle == 270:
            self.rect.centery=self.player.hitbox.centery
            self.rect.right=self.player.hitbox.centerx
        if self.angle == 180:
            self.rect.centerx=self.player.hitbox.centerx
            self.rect.bottom=self.player.hitbox.centery
        if self.angle == 45: # bottom left
            self.rect.topleft = self.player.hitbox.center
        if self.angle == 135: # Top right
            self.rect.bottomleft = self.player.hitbox.center
        if self.angle == 225: # Top left
            self.rect.bottomright = self.player.hitbox.center
        if self.angle == 315: # Bottom right
            self.rect.topright = self.player.hitbox.center
        # self.rect.top=self.player.rect.top


