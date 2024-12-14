from settings import *
from math import degrees,sqrt,atan2
import sprites as sp
import random
import time


spritesheets = {
    "player": {
        "idle": pygame.image.load("./Assets/Soldier-Idle.png"),
        "move": pygame.image.load("./Assets/Soldier-Walk.png"),
        "attack": pygame.image.load("./Assets/Soldier-Attack01.png"),
        "attack-2": pygame.image.load("./Assets/Soldier-Attack02.png"),
        "attack-3": pygame.image.load("./Assets/Soldier-Attack03.png"),
        "hurt": pygame.image.load("./Assets/Soldier-Hurt.png"),
        "death": pygame.image.load("./Assets/Soldier-Death.png"),
    },
    "brittle_arch": pygame.image.load("./Assets/First/BrittleArcher.png"),
    "slime":  pygame.image.load("./Assets/First/DeathSlime.png"),
    "blinded_grimlock":  pygame.image.load("./Assets/First/BlindedGrimlock.png"),
    "toxic_hound":  pygame.image.load("./Assets/First/ToxicHound.png"),
    "crawler":  pygame.image.load("./Assets/First/DismemberedCrawler.png"),
    "ghast":  pygame.image.load("./Assets/First/GhastlyEye.png"),
    "zomb":  pygame.image.load("./Assets/First/MutilatedStumbler.png"),
    "projectile":{
        "arrow":pygame.image.load("./Assets/Arrow.png")
    }
}

def get_frames(sheet, nFrame, width, height, scale):
    frame = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
    frame.blit(sheet, (0, 0), (nFrame * width, 0, width, height))
    frame = pygame.transform.scale(frame, (int(width * scale), int(height * scale)))
    return frame

class Player(pygame.sprite.Sprite): 
    def __init__(self, pos, groups, collision_sprites, enemy_group, player_skill):
        super().__init__(groups)
        self.spritesheets={
            "idle": [get_frames(spritesheets["player"]["idle"], i, 15, 19, 2.7) for i in range(6)],
            "move": [get_frames(spritesheets["player"]["move"], i,  15, 19, 2.7) for i in range(8)],
            "attack-1": [get_frames(spritesheets["player"]["attack"], i,  68, 24, 2.7) for i in range(6)],
            "attack-2": [get_frames(spritesheets["player"]["attack-2"], i,  68, 24, 2.7) for i in range(6)],
            "skill": [get_frames(spritesheets["player"]["attack-3"], i,  72, 20, 2.7) for i in range(9)],
            "hurt": [get_frames(spritesheets["player"]["hurt"], i,  16, 18, 2.7) for i in range(4)],
            "dead": [get_frames(spritesheets["player"]["death"], i,  19, 18, 2.7) for i in range(4)],
        }
        
        # Player attributes
        self.swing_range = 50
        self.health = 100
        self.max_health = 100
        self.attack_speed=0.03
        self.defence = 20
        self.level = 1
        self.current_exp = 0
        self.max_exp = 20
        self.speed=500
        self.attack_damage= 50
        self.rooms_cleared = 0
        self.current_health = 100
        self.target_health=100


        self.player_skill= player_skill
        self.current_sprite = 0
        self.current_state = "idle"
        self.image = self.spritesheets[self.current_state][int(self.current_sprite)]
        
        self.rect = self.image.get_frect(center = pos)
        self.rect.height=16*2.8
        self.rect.width=16*2.8

        self.hitbox=pygame.FRect((pos[0]-2,pos[1]+8),(28,33))
        self.is_moving=False
        # movement 
        self.direction = vector()
        # self.speed = speed
        self.velocity=vector()
        
        self.flipped=False
        self.attack_var=1
        self.swing = sp.PlayerSwing(self.swing_range, self, self.groups())
        self.attack_group = pygame.sprite.Group()
        self.swing.add(self.attack_group)
        self.collision_sprites = collision_sprites
        self.enemy_group = enemy_group


        self.player_stats = sp.PlayerStats(self)

        # Skill attribute
        self.angle=0
        self.projectile_speed = 500
        self.projectile_size=2.5
        self.cooldown = 100
        self.cooldown_count = 0
        self.max_shot=3
        self.shot_count=0
        self.projectile_damage = self.attack_damage * 0.8
        # Projectile sprite sheet
        self.projectile_spritesheet=spritesheets["projectile"]["arrow"]
        self.projectile_width = 32
        self.projectile_height = 32
        self.projectile_frames = 1


    def input(self):
        keys = pygame.key.get_pressed()
        keybinds=[
            pygame.K_RIGHT,pygame.K_LEFT,pygame.K_UP,pygame.K_DOWN
        ]
        input_vector = vector(0,0)
        if keys[pygame.K_RIGHT]:
            input_vector.x += 1
            self.is_moving = True
            self.flipped= False
        if keys[pygame.K_LEFT]:
            input_vector.x -= 1
            self.is_moving = True
            self.flipped= True
        if keys[pygame.K_UP]:
            input_vector.y -= 1
            self.is_moving = True
        if keys[pygame.K_DOWN]:
            input_vector.y += 1
            self.is_moving = True
        if keys[pygame.K_x]:
            self.current_state = "attack" 
        if keys[pygame.K_z]:
            self.skill()
        if not any(keys[key] for key in keybinds):
            self.is_moving = False
        else:
            if not keys[pygame.K_LALT]:
                 # Lock direction
                self.angle = atan2(input_vector.y, input_vector.x)

        self.direction = input_vector.normalize() if input_vector else input_vector
    def attack(self):
        print("AAFADJGHKAG")
        enemies_hit = pygame.sprite.groupcollide(self.enemy_group, self.attack_group, False, False)
        for enemy in enemies_hit:
            if isinstance(enemy, Enemy):
                if self.swing.rect.colliderect(enemy.hitbox):
                    enemy.take_damage(self.attack_damage)
    def skill(self):
        if self.cooldown_count > self.cooldown:     
            self.current_state = "skill"           
            sp.projectile(self.enemy_group,self.attack_damage,self.hitbox.center,self.angle,self.player_skill,self.projectile_spritesheet,
                                self.collision_sprites,self.projectile_speed,self.projectile_width,self.projectile_height,
                                self.projectile_height ,self.projectile_size)
            sp.projectile(self.enemy_group,self.attack_damage,self.hitbox.center,self.angle,self.player_skill,self.projectile_spritesheet,
                    self.collision_sprites,self.projectile_speed+200,self.projectile_width,self.projectile_height,
                    self.projectile_height ,self.projectile_size)
            sp.projectile(self.enemy_group,self.attack_damage,self.hitbox.center,self.angle,self.player_skill,self.projectile_spritesheet,
                    self.collision_sprites,self.projectile_speed+400,self.projectile_width,self.projectile_height,
                    self.projectile_height ,self.projectile_size)
            self.cooldown_count = 0  # Reset cooldown

    def move(self, dt):
        # Save the previous position for resolving collisions
        original_position = vector(self.hitbox.topleft)
        
        # Move the hitbox based on the direction
        self.hitbox.x += self.direction.x * self.speed * dt
        self.check_collision('x')
        self.hitbox.y += self.direction.y * self.speed * dt
        self.check_collision('y')

        # Update velocity based on the new position
        self.velocity = vector(self.hitbox.left - original_position.x, self.hitbox.top - original_position.y)

        # Align the visual rectangle with the hitbox
        self.rect.center = (self.hitbox.centerx, self.hitbox.centery - 8)

    def check_collision(self, axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox):
                if axis == 'x':
                    if self.direction.x > 0:  # Moving right
                        self.hitbox.right = sprite.rect.left
                    elif self.direction.x < 0:  # Moving left
                        self.hitbox.left = sprite.rect.right
                    # Prevent movement after collision
                    self.velocity.x = 0
                elif axis == 'y':
                    if self.direction.y > 0:  # Moving down
                        self.hitbox.bottom = sprite.rect.top
                    elif self.direction.y < 0:  # Moving up
                        self.hitbox.top = sprite.rect.bottom
                    # Prevent movement after collision
                    self.velocity.y = 0
    def take_damage(self,damage):
        self.current_state= "hurt"
        self.target_health -= damage * (1 - (self.defence/400))
        if self.target_health < 0:
            self.target_health = 0
        
        if self.current_health <= 0:
            self.current_state = "dead"
    def update(self, dt):
        print(self.current_exp)
        print(self.level)
        # print(self.target_health)
        # print(f"cur:{self.current_health}")
        if self.current_health >= self.target_health:
            self.current_health -= self.player_stats.health_change_speed
        
        self.player_stats.update()
        if self.current_state == "move" or self.current_state == "idle":
            self.current_sprite += 0.02
            # Animation state based on movement
            if self.is_moving:
                self.current_state = "move"    
            else:
                self.current_state = "idle"
            sprite_list = self.spritesheets[self.current_state]
            if self.current_sprite >= len(sprite_list): # Resets the sprite counter when it exceeded
                self.current_sprite = 0
        elif self.current_state == "attack": # Start attack check here, use the range sprite
            self.current_sprite += self.attack_speed
            sprite_list = self.spritesheets[f"attack-{self.attack_var}"]
            if self.current_sprite >= len(sprite_list):
                self.attack()
                self.current_sprite = 0
                self.current_state = "move" if self.is_moving else "idle"
                self.attack_var = random.randint(1,2)
        elif self.current_state:
            self.current_sprite += 0.06
            sprite_list = self.spritesheets[self.current_state]
            if self.current_sprite >= len(sprite_list): # Resets the sprite counter when it exceeded
                self.current_sprite = 0
                self.current_state="idle"
                sprite_list = self.spritesheets[self.current_state]

        self.cooldown_count+=1

        if self.current_exp > self.max_exp:
            self.level += 1
            self.health = self.max_health
            self.current_exp = 0
            self.max_exp += self.max_exp * (1+(self.level*10)/100)
        # Get the current frame from the spritesheet
        cur_frame = sprite_list[int(self.current_sprite)]
        self.image = pygame.transform.flip(cur_frame, True, False) if self.flipped else cur_frame

        self.rect = self.image.get_rect(center=self.rect.center)

        self.input()
        self.move(dt)
    
class Enemy(pygame.sprite.Sprite):
    def __init__(self,pos, groups, player_instance, spritesheet,collision_sprites,damage_sprite,hpbar, speed = 2):
        super().__init__(groups) 
        self.damage_sprite=damage_sprite
        self.current_frame = 0
        self.animation_speed = 0.01
        self.spritesheet=spritesheet
        self.player = player_instance
        self.hpgroup = hpbar
        self.frames = [get_frames(self.spritesheet,i,16,16,2.7) for i in range(4)]
        self.image = self.frames[int(self.current_frame)]
        self.rect = self.image.get_frect(topleft = pos)
        self.hitbox=pygame.FRect((self.rect.topleft[0]+10,self.rect.topleft[1]+10),(16,32))
        self.flipped = False
        self.speed = speed
        
        self.collision_sprites = collision_sprites
        self.direction = vector()
        self.velocity= vector()
        # Default value
        self.HP = 100 
        self.MAXHP = 100
        self.HPBAR = sp.HPBar(self,self.hpgroup)
        self.ATK = 10
        self.damage = self.ATK # FIX LATER
        self.DEF = 0
        self.attack_speed = 5
        self.exp_value=0

    def check_collision(self, axis):
        self.collided=False
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox):
                self.collided = True
                if axis == 'x':
                    if self.direction.x > 0:  # Moving right
                        self.hitbox.right = sprite.rect.left
                    elif self.direction.x < 0:  # Moving left
                        self.hitbox.left = sprite.rect.right
                    self.velocity.x = 0
                elif axis == 'y':
                    if self.direction.y > 0:  # Moving down
                        self.hitbox.bottom = sprite.rect.top
                    elif self.direction.y < 0:  # Moving up
                        self.hitbox.top = sprite.rect.bottom
                    self.velocity.y = 0

    def update(self, *args, **kwargs):
        self.HPBAR.update()
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        
        cur_frame = self.frames[int(self.current_frame)]
       
        if self.rect.centerx > self.player.hitbox.centerx:
            self.flipped = True
        if self.rect.centerx < self.player.hitbox.centerx:
            self.flipped = False

        self.image = pygame.transform.flip(cur_frame, True, False) if self.flipped else cur_frame

    def take_damage(self, damage): # TODO
        print("AAAAA")
        self.HP -= damage
        sp.DamageNumber(self.rect.center, self.player.attack_damage, self.damage_sprite) # Use the center of the enemy rect for the position
        
        if self.HP <= 0:
            self.dead()

    def dead(self):
        self.player.current_exp += self.exp_value
        self.HPBAR.update()
        self.kill()

class EnemyRanged(Enemy):  # TODO Code moveement
    def __init__(self, pos, groups, player_instance, spritesheet, collision_sprites, hpgroup, range, speed):
        super().__init__(pos, groups, player_instance, spritesheet, collision_sprites,hpgroup, speed)
        self.spritesheet=spritesheet
        self.player = player_instance
        self.is_paused = False
        self.change_direction_timer = random.randint(30, 50)
        self.collision_sprites = collision_sprites
        self.pause_counter = 0
        self.pause_duration = random.randint(60,80)
 
        # Default ranged enemy value
        self.attack_range = pygame.Rect(pos[0] - range, pos[1] - range, range * 6, range * 6)
        self.timer_counter=0
        self.attack_timer=0
        self.projectile_speed = 500
        self.projectile_size=2.5
        # Projectile sprite sheet
        self.projectile_spritesheet=spritesheets["projectile"]["arrow"]
        self.projectile_width = 32
        self.projectile_height = 32
        self.projectile_frames = 1

        
    def check_collision(self, axis):
        super().check_collision(axis)
        if self.collided:
            self.is_paused = True
            self.pause_counter = 0
            # Reset direction to a new random value to avoid repeated collision
            self.direction = vector(random.choice([-100, 100]), random.choice([-100, 100]))
        return self.collided

    def move(self,dt):
        if self.is_paused: return
        self.timer_counter += 1
        movement_vector = vector(0,0)
        if self.timer_counter >= self.change_direction_timer:
            movement_vector.x += random.choice([-20, 20])
            movement_vector.y += random.choice([-20, 20])
            self.timer_counter = 0
            self.is_paused = True 
            self.direction = movement_vector


        original_position = vector(self.hitbox.topleft)
        
        # Move the hitbox based on the direction
        self.hitbox.x += self.direction.x * self.speed  * dt 
        self.check_collision('x')
        self.hitbox.y += self.direction.y * self.speed * dt
        self.check_collision('y')

        # Update velocity based on the new position
        self.velocity = vector(self.hitbox.left - original_position.x, self.hitbox.top - original_position.y)

        # Align the visual rectangle with the hitbox
        self.rect.center = (self.hitbox.centerx, self.hitbox.centery - 8)
   
    def update(self, dt):
        super().update(dt)
        # Manage pausing logic
        if self.is_paused:
            self.pause_counter += 1
            if self.pause_counter >= self.pause_duration:
                self.is_paused = False
                self.collided = False  # Reset collided state
                self.pause_counter = 0
        if self.player.hitbox.colliderect(self.attack_range): 
            # TODO Cast a line to see if the player is visible or not, this also for melee
            self.attack()
        self.move(dt)


    def attack(self):
        # Angle needs to be here so tha tit updates constantly
        self.angle=atan2(self.player.hitbox.centery-self.rect.centery,
                                    self.player.hitbox.centerx-self.rect.centerx)

        self.attack_timer+=0.1
        if self.attack_timer > self.attack_speed:
            self.attack_timer=0
            sp.projectile(self.player,self.damage,self.hitbox.center,self.angle,self.groups(),self.projectile_spritesheet,
                          self.collision_sprites,self.projectile_speed,self.projectile_width,self.projectile_height,
                          self.projectile_height,self.projectile_size)
            

class EnemyMelee(Enemy):
    def __init__(self, pos, groups, player_instance, spritesheet, collision_sprites, hpgroup, detection_range, speed):
        super().__init__(pos, groups, player_instance, spritesheet, collision_sprites, hpgroup, speed)
        self.player = player_instance
        self.notice_range = pygame.Rect(pos[0] - detection_range, pos[1] - detection_range, detection_range * 2, detection_range * 2)
        self.range = range 
        self.change_direction_timer = random.randint(30, 50)
        self.timer_counter=0
        self.pause_counter = 0
    
    def pursue(self,dt):
        dx = self.player.hitbox.centerx - self.hitbox.centerx
        dy = self.player.hitbox.centery - self.hitbox.centery
        distance = sqrt(dx**2 + dy**2)

        if distance > 0:
            self.direction.x = dx / distance 
            self.direction.y = dy / distance

        # Move the enemy
        self.hitbox.x += self.direction.x * self.speed * 40 * dt# DT scaling is messed up fsr
        self.check_collision('x')
        self.hitbox.y += self.direction.y * self.speed * 40 * dt
        self.check_collision('y')
        self.rect.center = self.hitbox.center

    def check_collision(self, axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox):
                if axis == 'x':
                    if self.direction.x > 0:  # Moving right
                        self.hitbox.right = sprite.rect.left
                    elif self.direction.x < 0:  # Moving left
                        self.hitbox.left = sprite.rect.right
                    # Prevent movement after collision
                    self.velocity.x = 0
                elif axis == 'y':
                    if self.direction.y > 0:  # Moving down
                        self.hitbox.bottom = sprite.rect.top
                    elif self.direction.y < 0:  # Moving up
                        self.hitbox.top = sprite.rect.bottom
                    # Prevent movement after collision
                    self.velocity.y = 0

    def update(self, dt):
        super().update(dt)
        if self.notice_range.colliderect(self.player.hitbox):
            self.pursue(dt)
        else:
            self.timer_counter += 1
            movement_vector = vector(0,0)
            if self.timer_counter >= self.change_direction_timer:

                movement_vector.x += random.choice([-0.1, 0.1])
                movement_vector.y += random.choice([-0.1, 0.1])
                self.timer_counter = 0
                self.is_paused = True 
                self.direction = movement_vector


            original_position = vector(self.hitbox.topleft)
            
            # Move the hitbox based on the direction
            self.hitbox.x += self.direction.x * self.speed 
            self.check_collision('x')
            self.hitbox.y += self.direction.y * self.speed 
            self.check_collision('y')

            # Update velocity based on the new position
            self.velocity = vector(self.hitbox.left - original_position.x, self.hitbox.top - original_position.y)

            # Align the visual rectangle with the hitbox
            self.rect.center = (self.hitbox.centerx, self.hitbox.centery - 8)
   
        self.notice_range.center = self.hitbox.center

class BrittleArcher(EnemyRanged):
    def __init__(self, pos,groups,player_instance ,collision_sprites,hpgroup,speed=300):
        super().__init__(pos, groups, player_instance, spritesheets["brittle_arch"], 
        collision_sprites,hpgroup, 60, speed)
        self.exp_value = 4*difficulty
        self.ATK = 10 * difficulty
        self.HP = 50 * difficulty
        self.MAXHP = 50 * difficulty

class GhastlyEye(EnemyRanged):
    def __init__(self, pos,groups,player_instance ,collision_sprites,hpgroup,speed=200):
        super().__init__(pos, groups, player_instance, spritesheets["ghast"], 
        collision_sprites,hpgroup, 10, speed)
        self.exp_value = 5*difficulty
        self.projectile_speed=700
        self.attack_speed=4
        self.ATK = 1 * difficulty
        self.HP = 2 * difficulty
        self.MAXHP = 2 * difficulty

class ToxicHound(EnemyMelee):
    def __init__(self, pos,groups,player_instance ,collision_sprites,hpgroup,speed=100):
        super().__init__(pos, groups, player_instance, spritesheets["toxic_hound"], 
        collision_sprites,hpgroup,200, speed)
        self.exp_value = 8*difficulty
        self.ATK = 10 * difficulty
        self.HP = 80 * difficulty
        self.MAXHP = 70 * difficulty

class NormalZomb(EnemyMelee):
    def __init__(self, pos,groups,player_instance ,collision_sprites,hpgroup,speed=50):
        super().__init__(pos, groups, player_instance, spritesheets["zomb"], 
        collision_sprites,hpgroup, 200, speed)
        self.exp_value = 5*difficulty
        self.ATK = 15 * difficulty
        self.HP = 70 * difficulty
        self.MAXHP = 70 * difficulty

class DismemberedCrawler(EnemyMelee):
    def __init__(self, pos,groups,player_instance ,collision_sprites,hpgroup,speed=25):
        super().__init__(pos, groups, player_instance, spritesheets["crawler"], 
        collision_sprites,hpgroup,200, speed)
        self.exp_value = 2*difficulty
        self.ATK = 7 * difficulty
        self.HP = 40 * difficulty
        self.MAXHP = 40 * difficulty

class Slime(EnemyMelee):
    def __init__(self, pos,groups,player_instance ,collision_sprites,hpgroup,speed=10):
        super().__init__(pos, groups, player_instance, spritesheets["slime"], 
        collision_sprites,hpgroup,200, speed)
        self.exp_value = 2*difficulty
        self.ATK = 5 * difficulty
        self.HP = 120 * difficulty
        self.MAXHP = 50 * difficulty

class BlindedGrimlock(EnemyRanged):
    def __init__(self, pos,groups,player_instance ,collision_sprites,hpgroup,speed=250):
        super().__init__(pos, groups, player_instance, spritesheets["blinded_grimlock"], 
        collision_sprites,hpgroup, 200, speed)
        self.exp_value = 5*difficulty
        self.attack_speed=10
        self.ATK = 20 * difficulty
        self.HP = 80 * difficulty
        self.MAXHP = 80 * difficulty