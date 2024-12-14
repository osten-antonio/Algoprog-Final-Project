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
        keys = pygame.key.get_pressed()
        if not keys[pygame.K_LALT]:
            if direction.x != 0 or direction.y != 0:
                self.angle = degrees(atan2(direction.x,direction.y)) if\
                    degrees(atan2(direction.x,direction.y)) >=0 else\
                        degrees(atan2(direction.x,direction.y))+360
            keys = pygame.key.get_pressed()

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
        self.angle = angle
        self.collision_sprite = collision_sprite
        self.current_frame = 0
        self.frames = [get_frames(self.spritesheet,i, width,height,size) for i in range(frames)]
        self.image = self.frames[int(self.current_frame)]
        
        self.image = pygame.transform.rotate(self.image,degrees(-self.angle))
        self.rect = self.image.get_frect(topleft = pos)
        self.hitbox=pygame.FRect((self.rect.topleft[0]+5,self.rect.topleft[1]+5),(10,10))

        self.pos = pos
        self.angle = angle
        self.direction = vector(cos(angle),sin(angle))
    def take_damage(*args,**kwargs):
        pass
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
                    sprite.take_damage(self.damage)
                    print("HIt enemy")
                    self.kill()  # Remove the projectile
                    pass
        else:
            if self.hitbox.colliderect(self.instance.hitbox):
                self.instance.take_damage(self.damage)
                self.kill()  # Remove the projectile
                


class HPBar(pygame.sprite.Sprite):
    def __init__(self, enemy_instance, group, width=40, height=6, border_color=(0, 0, 0), health_color=(255, 0, 0), background_color=(100, 100, 100)):

        super().__init__(group)
        
        self.enemy = enemy_instance
        self.width = width
        self.height = height
        self.border_color = border_color
        self.health_color = health_color
        self.background_color = background_color
        
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA) 
        self.rect = self.image.get_rect()  

    def update(self, *args, **kwargs):
        # print("Take damage")
        self.rect.midbottom = self.enemy.rect.midtop 
        self.rect.y -= 10 
    
        health_percentage = max(self.enemy.HP / self.enemy.MAXHP,0)  
        if health_percentage <=0:
            self.kill()
        current_health_width = int(self.width * health_percentage)

        self.image.fill((0, 0, 0, 0)) 
        pygame.draw.rect(self.image, self.background_color, (0, 0, self.width, self.height))
        
        # Draw the current health bar
        if current_health_width > 0:
            pygame.draw.rect(self.image, self.health_color, (0, 0, current_health_width, self.height))
        
        # Draw the border around the HP bar
        pygame.draw.rect(self.image, self.border_color, (0, 0, self.width, self.height), 1)  # 1 pixel border

class PlayerStats(pygame.sprite.Sprite):
    def __init__(self,player_instance):
        super().__init__()
        self.player= player_instance
        self.current_health = player_instance.current_health
        self.target_health = player_instance.target_health
        self.max_health = player_instance.max_health

        self.exp = player_instance.current_exp 
        self.max_exp = player_instance.max_exp
        self.exp_ratio = self.max_exp / 180 
        self.level = player_instance.level
        self.level_text = pygame.font.SysFont('arial', 20, bold=True).render(f"Lv. {self.level}", True, "#009900")

        self.health_bar_length = 200
        self.health_ratio = self.max_health / self.health_bar_length
        self.health_change_speed = 10
        self.health_bar = pygame.Rect(130,70,self.health_bar_length,25)

        transition_width=0
        self.transition_bar = pygame.Rect(self.health_bar.right,70,transition_width,25)

        # Load the background image
        self.health_bar_background = pygame.image.load('./assets/player_stats_bg.png').convert()
        self.health_bar_background = pygame.transform.scale(self.health_bar_background, (384, 240))

    def get_damage(self,amount):
        if self.target_health > 0:
            self.target_health -= amount
        if self.target_health < 0:
            self.target_health = 0

    def get_health(self,amount):
        if self.target_health < self.max_health:
            self.target_health += amount
        if self.target_health > self.max_health:
            self.target_health = self.max_health

    def update(self, *args , **kwargs):
        # Draw the background image for the health bar
        self.exp = self.player.current_exp
        transition_width = 0
        self.current_health = self.player.current_health
        self.target_health = self.player.target_health
        if self.current_health < self.target_health:
            self.current_health += self.health_change_speed
            transition_width = int((self.target_health - self.current_health) / self.health_ratio)

        if self.current_health > self.target_health:
            self.current_health -= self.health_change_speed 
            transition_width = int((self.target_health - self.current_health) / self.health_ratio)
 

        health_bar_width = int(self.current_health / self.health_ratio)
        self.health_bar = pygame.Rect(130,70,health_bar_width,25)
        self.transition_bar = pygame.Rect(self.health_bar.right,70,transition_width,25)
		





