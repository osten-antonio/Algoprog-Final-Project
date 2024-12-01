from settings import *
from math import ceil

spritesheets = {
    "player": {
        "idle": pygame.image.load("./Assets/Soldier-Idle.png"),
        "move": pygame.image.load("./Assets/Soldier-Walk.png"),
        "attack": pygame.image.load("./Assets/Soldier-Attack01.png"),
        "attack-2": pygame.image.load("./Assets/Soldier-Attack02.png"),
        "attack-3": pygame.image.load("./Assets/Soldier-Attack03.png"),
        "hurt": pygame.image.load("./Assets/Soldier-Hurt.png"),
        "death": pygame.image.load("./Assets/Soldier-Death.png"),
    }
}

def get_frames(sheet, nFrame, width, height, scale):
    frame = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
    frame.blit(sheet, (0, 0), (nFrame * width, 0, width, height))
    frame = pygame.transform.scale(frame, (int(width * scale), int(height * scale)))
    return frame

class Player(pygame.sprite.Sprite):

    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.spritesheets={
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

        self.rect = self.image.get_frect(topleft = pos)
        self.rect.height=16*2.8
        self.rect.width=16*2.8

        self.is_moving=False
        # movement 
        self.direction = vector()
        self.speed = 500
        self.velocity=vector()

        self.flipped=False

        self.collision_sprites = collision_sprites
    def input(self):
        keys = pygame.key.get_pressed()
        keybinds=[
            pygame.K_d,pygame.K_a,pygame.K_w,pygame.K_s
        ]
        input_vector = vector(0,0)
        if keys[pygame.K_d]:
            input_vector.x += 1
            self.is_moving = True
            self.flipped= False
        if keys[pygame.K_a]:
            input_vector.x -= 1
            self.is_moving = True
            self.flipped= True
        if keys[pygame.K_w]:
            input_vector.y -= 1
            self.is_moving = True
        if keys[pygame.K_s]:
            input_vector.y += 1
            self.is_moving = True
        if not any(keys[key] for key in keybinds):
            self.is_moving = False
        self.direction = input_vector.normalize() if input_vector else input_vector

        

    def move(self, dt):
        position = self.rect.topleft
        self.rect.x += self.direction[0] * self.speed * dt
        print(dt)
        self.check_collision('x')
        self.rect.y += self.direction[1] * self.speed * dt
        self.check_collision('y')
        self.velocity=vector(self.rect.x - position[0],self.rect.y - position[1])
    def check_collision(self,axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                print(f"Collision detected on {axis} axis with {sprite}")
                if axis == 'x':
                    # Resolve horizontal collision (left-right)
                    if self.direction.x > 0:  # Moving right
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0:  # Moving left
                        self.rect.left = sprite.rect.right
                elif axis == 'y':
                    
                    # Resolve vertical collision (up-down)
                    if self.direction.y > 0:  # Moving down
                        self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0:  # Moving up
                        self.rect.top = sprite.rect.bottom

    def update(self, dt):
         # Increment the current sprite with a speed modifier (adjust 0.01 as needed)
        self.current_sprite += 0.01  # Adjust the speed of animation
        sprite_list = self.spritesheets[self.current_state]
        
        # Ensure current_sprite is reset when it exceeds the available frames
        if self.current_sprite >= len(sprite_list):
            self.current_sprite = 0

        # Get the current frame from the spritesheet
        base_image = sprite_list[int(self.current_sprite)]

        # Flip the sprite if needed
        self.image = pygame.transform.flip(base_image, True, False) if self.flipped else base_image

        # Hitbox
        pygame.draw.rect(pygame.display.get_surface(), 'red', self.rect, 2)

        # Animation state based on movement
        self.current_state = "move" if self.is_moving else "idle"

        self.input()
        self.move(dt)
