import pygame

pygame.init()
screen = pygame.display.set_mode((1200, 720))
clock = pygame.time.Clock()

# Load spritesheets
spritesheets = {
    "player": {
        "idle": pygame.image.load("./Assets/Soldier-Idle.png").convert_alpha(),
        "move": pygame.image.load("./Assets/Soldier-Walk.png").convert_alpha(),
        "attack": pygame.image.load("./Assets/Soldier-Attack01.png").convert_alpha(),
        "attack-2": pygame.image.load("./Assets/Soldier-Attack02.png").convert_alpha(),
        "attack-3": pygame.image.load("./Assets/Soldier-Attack03.png").convert_alpha(),
        "hurt": pygame.image.load("./Assets/Soldier-Hurt.png").convert_alpha(),
        "death": pygame.image.load("./Assets/Soldier-Death.png").convert_alpha(),
    }
}

# Function to get a frame from a sprite sheet
def get_frames(sheet, nFrame, width, height, scale):
    frame = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
    frame.blit(sheet, (0, 0), (nFrame * width, 0, width, height))
    frame = pygame.transform.scale(frame, (int(width * scale), int(height * scale)))
    return frame

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.hp=100
        self.speed=1
        self.attack=10
        self.defence=10


        self.spritesheets = {
            "idle": [get_frames(spritesheets["player"]["idle"], i, 15, 19, 2.7) for i in range(6)],
            "move": [get_frames(spritesheets["player"]["move"], i,  15, 19, 2.7) for i in range(8)],
            "attack-1": [get_frames(spritesheets["player"]["attack"], i,  15, 19, 2.7) for i in range(6)],
            "attack-2": [get_frames(spritesheets["player"]["attack-2"], i,  15, 19, 2.7) for i in range(6)],
            "skill": [get_frames(spritesheets["player"]["attack-3"], i,  15, 19, 2.7) for i in range(6)],
            "hurt": [get_frames(spritesheets["player"]["hurt"], i,  15, 19, 2.7) for i in range(4)],
        }

        self.current_sprite = 0
        self.current_state = "idle"
        self.image = self.spritesheets[self.current_state][int(self.current_sprite)]
        self.rect = self.image.get_rect(center=(x, y))
        # Set hitbox
        self.rect.height=16*2.8
        self.rect.width=16*2.8
        self.rect.center = (x, y)
        self.flipped=False

    def input(self):
        keys=pygame.key.get_pressed()
        input_vector = vector(0,0)
        if keys[pygame.K_w]:
            input_vector.y-=1
        if keys[pygame.K_a]:
            input_vector.x-=1
        if keys[pygame.K_d]:
            input_vector.x+=1
        if keys[pygame.K_s]:
            input_vector.y+=1
        self.direction = input_vector.normalize() if input_vector else input_vector
    
    def move(self,dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.collision('x')
        self.rect.x += self.direction.y * self.speed * dt
        self.collision('y')
    
    def collision(self,axis):
        for sprite in self.collision_

    def update(self):
        self.current_sprite += 0.1  # Slow down the animation
        if self.current_sprite >= len(self.spritesheets[self.current_state]):
            self.current_sprite = 0
        if self.flipped==False:
            self.image = self.spritesheets[self.current_state][int(self.current_sprite)]
        else:
            self.image = pygame.transform.flip(self.spritesheets[self.current_state][int(self.current_sprite)], True, False)
    
        pygame.draw.rect(screen, (255, 0, 0), self.rect,2)
    def set_state(self, state):
        if state in self.spritesheets:
            if state != self.current_state:  # Only reset if the state changes
                self.current_state = state
                self.current_sprite = 0

    def flip(self):
        self.flipped= not(self.flipped)


# # Base enemy class
# class Enemy(pygame.sprite.Sprite):
#     def __init__(self, x, y, spritesheet, speed, health,width,height,scale, frame_count=4):
#         super().__init__()
#         self.spritesheets = spritesheets
#         self.frames = [get_frames(spritesheet, i, width, height, scale) for i in range(frame_count)]
#         self.current_frame = 0
#         self.image = self.frames[int(self.current_frame)]
#         self.rect = self.image.get_rect(topleft=(x, y))

#         self.health = health
#         self.speed = speed
#         self.flipped = False

#     def update(self):
#         # Animation logic
#         self.current_frame += 0.1  # Adjust speed as needed
#         if self.current_frame >= len(self.frames):
#             self.current_frame = 0
#         self.image = self.frames[int(self.current_frame)]

#     def take_damage(self, damage):
#         self.health -= damage
#         if self.health <= 0:
#             self.kill()

#     def set_state(self, state):
#         if state in self.spritesheets:
#             if state != self.current_state:
#                 self.current_state = state
#                 self.current_sprite = 0

# class MeleeEnemy(Enemy):
#     def __init__(self, x, y, speed,health):
#         super().__init__(x, y, spritesheets, speed, health,scale=3)

#     def update(self):
#         super().update()
#         # Additional melee-specific behavior
        
#         # Move toward player
#         direction = pygame.Vector2(player_pos) - pygame.Vector2(self.rect.topleft)
#         if direction.length() > 0:
#             direction = direction.normalize()
#         self.rect.x += direction.x * self.speed
#         self.rect.y += direction.y * self.speed


        


# Game loop
