from settings import *
from math import *
from players import get_frames

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

class DamageNumber(pygame.sprite.Sprite):
    def __init__(self, pos, damage, groups,color=(255, 255, 255)):
        super().__init__(groups)   

        self.image = pygame.font.SysFont('arial', 20, bold=True).render(str(damage), True, color)
        self.pos = (WIDTH // 2, HEIGHT // 2)
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(pos) 
        self.velocity = pygame.math.Vector2(0, -0.1)  
        self.alpha = 255  
        self.lifespan = 120
    
    
    def update(self,dt, *args, **kwargs):
        self.rect.y += self.velocity.y * dt
        self.alpha -= 255 / self.lifespan  
        if self.alpha <= 0:
            self.kill()  
        self.image.set_alpha(max(0, int(self.alpha)))

class projectile(pygame.sprite.Sprite): # TODO test this
    
    def __init__(self, instance, damage, pos, angle, 
                 groups, spritesheet , collision_sprite, speed,
                   width, height, frames, size):
        super().__init__(groups)
        self.instance = instance
        self.damage = damage # PLS INPUT USING DAMAGE CALCULATION LATER
        self.spritesheet  = spritesheet
        self.speed = speed
        self.collision_sprite = collision_sprite
        self.current_frame = 0
        self.frames = [get_frames(self.spritesheet,i, width,height,size) for i in range(frames)]
        self.image = self.frames[int(self.current_frame)]
        self.image = pygame.transform.rotate(self.image,angle)
        self.rect = self.image.get_frect(topleft = pos)
        self.hitbox=pygame.FRect((self.rect.topleft[0]+5,self.rect.topleft[1]+5),(10,10))

        self.pos = pos
        self.angle = angle
        self.direction = vector(cos(angle),sin(angle))
    def update(self, dt, *args, **kwargs):
        # Ensure direction is a pygame vector
        if not isinstance(self.direction, pygame.math.Vector2):
            self.direction = pygame.math.Vector2(self.direction)

        # Move the projectile based on its direction and speed (scale by dt for frame-rate independence)
        movement = self.direction * self.speed * dt

        self.hitbox.center += movement
        self.rect.center = self.hitbox.center

        # Check for collision with walls or other obstacles in the collision group
        for sprite in self.collision_sprite:
            if self.hitbox.colliderect(sprite.rect):
                self.kill()  # Remove the projectile on collision

        # Check for collision with the player
        if isinstance(self.instance,pygame.sprite.Group):
            for sprite in self.instance:
                if self.hitbox.colliderect(sprite.hitbox):
                    # Damage enemy
                    print("HIt enemy")
                    self.kill()  # Remove the projectile
                    pass
        else:
            if self.hitbox.colliderect(self.instance.hitbox):
                # self.player.HP -= self.damage  # Decrease player HP on hit
                self.kill()  # Remove the projectile
                pass



        
    
    




