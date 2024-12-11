from settings import *
from math import ceil,sqrt
from sprites import PlayerSwing,DamageNumber
import random

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
    "test_enemy": pygame.image.load("./Assets/First/BrittleArcher.png")
}

def get_frames(sheet, nFrame, width, height, scale):
    frame = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
    frame.blit(sheet, (0, 0), (nFrame * width, 0, width, height))
    frame = pygame.transform.scale(frame, (int(width * scale), int(height * scale)))
    return frame

def get_enemy_frames(sheet, nframe, width =16, height = 16, scale = 2.7):
    frame = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
    frame.blit(sheet, (0, 0), (nframe * width, 0, width, height))
    frame = pygame.transform.scale(frame, (int(width * scale), int(height * scale)))
    return frame
class Player(pygame.sprite.Sprite):
    swing_range = 50
    health = 100
    attack_speed=0.03
    defence = 20
    level = 1
    speed=500
    attack_damage=10000
    rooms_cleared = 0
    def __init__(self, pos, groups, collision_sprites, enemy_group):
        super().__init__(groups)
        self.last_breadcrumb_time = pygame.time.get_ticks() # https://youtu.be/OtSZMeHr_S8?si=HzfZ7XqSqTrw6kzu
        self.spritesheets={
            "idle": [get_frames(spritesheets["player"]["idle"], i, 15, 19, 2.7) for i in range(6)],
            "move": [get_frames(spritesheets["player"]["move"], i,  15, 19, 2.7) for i in range(8)],
            "attack-1": [get_frames(spritesheets["player"]["attack"], i,  34, 24, 2.7) for i in range(6)],
            "attack-2": [get_frames(spritesheets["player"]["attack-2"], i,  34, 24, 2.7) for i in range(6)],
            "skill": [get_frames(spritesheets["player"]["attack-3"], i,  15, 19, 2.7) for i in range(6)],
            "hurt": [get_frames(spritesheets["player"]["hurt"], i,  15, 19, 2.7) for i in range(4)],
        }
        self.current_sprite = 0
        self.current_state = "idle"
        self.image = self.spritesheets[self.current_state][int(self.current_sprite)]
        
        self.rect = self.image.get_frect(topleft = pos)
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
        self.swing = PlayerSwing(self.swing_range, self, self.groups())
        self.attack_group = pygame.sprite.Group()
        self.swing.add(self.attack_group)
        self.collision_sprites = collision_sprites
        self.enemy_group = enemy_group


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
        if keys[pygame.K_LALT]:
            pass # Lock direction
        if not any(keys[key] for key in keybinds):
            self.is_moving = False
        self.direction = input_vector.normalize() if input_vector else input_vector
    def attack(self):
        print("Attacked")
        enemies_hit = pygame.sprite.groupcollide(self.enemy_group, self.attack_group, False, False)
        for enemy in enemies_hit:
            print(enemy)
            if isinstance(enemy, Enemy):
                print("YES")
                if self.swing.rect.colliderect(enemy.hitbox):
                    print("AGLKJAHGLIKJAG")
                    enemy.take_damage(self.attack_damage)

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
    
    def update(self, dt):

        if self.current_state != "attack":
            self.current_sprite += 0.02
            # Animation state based on movement
            self.current_state = "move" if self.is_moving else "idle"
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


        # Get the current frame from the spritesheet
        cur_frame = sprite_list[int(self.current_sprite)]
        self.image = pygame.transform.flip(cur_frame, True, False) if self.flipped else cur_frame

        self.rect = self.image.get_rect(center=self.rect.center)

        self.input()
        self.move(dt)
    
    # TODO Dash (I frames)

class Enemy(pygame.sprite.Sprite):
    def __init__(self,pos, groups, player_instance, spritesheet,collision_sprites,damage_sprite, speed = 2):
        super().__init__(groups) 
        self.damage_sprite=damage_sprite
        self.current_frame = 0
        self.animation_speed = 0.01
        self.spritesheet=spritesheet
        self.player = player_instance
        self.status=1

        self.frames = [get_enemy_frames(self.spritesheet,i) for i in range(4)]
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
        self.ATK = 10
        self.DEF = 0

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

    def update(self, dt):
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
        print("Damage")
        self.HP -= damage
        DamageNumber(self.rect.center, damage, self.damage_sprite) # Use the center of the enemy rect for the position
        
        if self.HP <= 0:

            print("Dead")
            self.dead()
    def dead(self):

        self.status=0
        self.kill()

class EnemyRangedMove(Enemy):  # TODO Code moveement
    def __init__(self, pos, groups, player_instance, spritesheet, collision_sprites, speed=2):
        super().__init__(pos, groups, player_instance, spritesheet, collision_sprites, speed)
        self.spritesheet=spritesheet
        self.player = player_instance

        self.is_paused = False
        self.change_direction_timer = random.randint(30, 50)
        self.collision_sprites = collision_sprites
        self.timer_counter=0
        self.pause_counter = 0
        self.pause_duration = random.randint(60,80)
 
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
        room_size = 15 * TILE_SIZE
        self.timer_counter += 1
        movement_vector = vector(0,0)
        if self.timer_counter >= self.change_direction_timer:
            wait_time=0
            movement_vector.x += random.choice([-20, 20])
            movement_vector.y += random.choice([-20, 20])
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
   
    def update(self, dt):
        super().update(dt)
        # Manage pausing logic
        if self.is_paused:
            self.pause_counter += 1
            if self.pause_counter >= self.pause_duration:
                self.is_paused = False
                self.collided = False  # Reset collided state
                self.pause_counter = 0


        self.move(dt)

class EnemyMelee(Enemy):
    def __init__(self, pos, groups, player_instance, spritesheet, collision_sprites, range, detection_range, speed=200):
        super().__init__(pos, groups, player_instance, spritesheet, collision_sprites, speed)
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
        self.hitbox.x += self.direction.x * self.speed  # DT scaling is messed up fsr
        self.check_collision('x')
        self.hitbox.y += self.direction.y * self.speed 
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
            room_size = 15 * TILE_SIZE
            self.timer_counter += 1
            movement_vector = vector(0,0)
            if self.timer_counter >= self.change_direction_timer:
                wait_time=0
                movement_vector.x += random.choice([-1, 1])
                movement_vector.y += random.choice([-1, 1])
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

class Test_Enemy(EnemyMelee):
    def __init__(self, pos,groups,player_instance,collision_sprites,speed=500):
        super().__init__(pos, groups, player_instance, spritesheets["test_enemy"], collision_sprites, 200,200, speed)

# TODO BIG PRIORITY, Projectiles > Enemy attack > skill

# TODO Player ONLY ATTACK ONCE

# TODO diff enemies

# TODO Fog of war 


