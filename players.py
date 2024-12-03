from settings import *
from math import ceil
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

class Player(pygame.sprite.Sprite):
    swing_range = 50
    health = 100
    attack_speed=0.03
    defence = 20
    level = 1
    speed=500
    rooms_cleared = 0
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
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
        self.collision_sprites = collision_sprites
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
        print(self.current_state)

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
                self.current_sprite = 0
                self.current_state = "move" if self.is_moving else "idle"
                self.attack_var = random.randint(1,2)


        # Get the current frame from the spritesheet
        cur_frame = sprite_list[int(self.current_sprite)]
        self.image = pygame.transform.flip(cur_frame, True, False) if self.flipped else cur_frame

        # Flip the sprite if needed
        # self.image = pygame.transform.flip(cur_frame, True, False) if self.flipped else cur_framea
        self.rect = self.image.get_rect(center=self.rect.center)

        self.input()
        self.move(dt)
    

    # TODO Dash (I frames)
class Enemy(pygame.sprite.Sprite):  # TODO
    def __init__(self, pos, groups, scale=2.6, speed=2):
        super().__init__(groups)
        self.current_frame = 0
        self.animation_speed = 0.01
        
        # self.frames=[get_frames(spritesheets["test_enemy"], i, 16, 16, 2.7) for i in range(4)]
        # self.image = self.frames[self.current_frame]  # Set the initial frame
        self.rect = pygame.Rect(5,5,5,5)
        
        self.speed = speed
    

    def update(self,*args, **kwargs):
        self.current_frame += self.animation_speed
        # if self.current_frame >= len(self.frames):
        #     self.current_frame = 0
        # self.image = self.frames[int(self.current_frame)]



