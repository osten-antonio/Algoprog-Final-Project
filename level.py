from settings import *
from sprites import *
from entities import *
from collections import defaultdict
import random

class Level:
    def __init__(self, tmx_map):
        self.display_surface = pygame.display.get_surface()

        # Groups for different types of objects
        self.all_sprites = pygame.sprite.Group()
        self.damage_sprite = pygame.sprite.Group() # Damage numbers
        self.collision_sprites = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.player_skill = pygame.sprite.Group()
        self.bounding_box = pygame.sprite.Group()
        self.hpbar = pygame.sprite.Group()
        self.spawn_borders_group = pygame.sprite.Group()
        self.rooms = defaultdict(pygame.sprite.Sprite)
        self.current_room = [0, 0]
        self.cleared_rooms = []
        self.visited_room = []
        self.enemy_classes = [BrittleArcher, GhastlyEye, ToxicHound, NormalZomb, DismemberedCrawler, Slime, BlindedGrimlock]

        self.room_size = (15 * TILE_SIZE, 15 * TILE_SIZE)
        self.setup(tmx_map)
        self.spawned_enemies_pos = []
        self.spawned_enemies=[]
    def setup(self, tmx_map):

        self.layers = {
            'water':[],
            'floor': [],
            'walls': [],
            'decorations': [],
            'decorations2': [],
            'spawn_border':[]
        }
        offset_x = (WIDTH / 2) - (tmx_map.width * TILE_SIZE / 2) + TILE_SIZE-10
        offset_y = (HEIGHT / 2) - (tmx_map.height * TILE_SIZE / 2) + TILE_SIZE

        self.rooms["[0, 0]"] =  BoundingBox(offset_x-30,offset_y-25, tmx_map.width*TILE_SIZE, tmx_map.height*TILE_SIZE, self.bounding_box) # 30 and 25 is magic number im sorry
        
        # Fix this, move the rect relative to the player
 
        for x, y, surf in tmx_map.get_layer_by_name('Water').tiles():
            self.layers['water'].append(Sprite((x * TILE_SIZE + offset_x, y * TILE_SIZE + offset_y), surf, (self.all_sprites,self.collision_sprites)))
        # Load the floor layer (bg tiles, path, etc.)
        for x, y, surf in tmx_map.get_layer_by_name('Floor').tiles():
            self.layers['floor'].append(Sprite((x * TILE_SIZE + offset_x, y * TILE_SIZE + offset_y), surf, (self.all_sprites,)))

        # Load decorations layer
        for x, y, surf in tmx_map.get_layer_by_name('Decorations').tiles():
            self.layers['decorations'].append(Sprite((x * TILE_SIZE + offset_x, y * TILE_SIZE + offset_y), surf, (self.all_sprites,)))

        # Set up the player (always on top of other layers)
        self.player = Player((WIDTH // 2, HEIGHT // 2), self.all_sprites, self.collision_sprites, self.enemy_group, self.player_skill)
        # Load the walls layer (collidable objects)
        for x, y, surf in tmx_map.get_layer_by_name('Walls').tiles():
            self.layers['walls'].append(Sprite((x * TILE_SIZE + offset_x, y * TILE_SIZE + offset_y), surf, (self.all_sprites, self.collision_sprites)))
        
        # Load decorations2 layer
        for x, y, surf in tmx_map.get_layer_by_name('Decorations2').tiles():
            self.layers['decorations2'].append(Sprite((x * TILE_SIZE + offset_x, y * TILE_SIZE + offset_y), surf, (self.all_sprites,)))
    def generate(self,pos):
        possible_rooms = {
            101: load_pygame('./Rooms/Level 1/01.tmx'),
            102: load_pygame('./Rooms/Level 1/02.tmx'),
            103: load_pygame('./Rooms/Level 1/03.tmx'),
            104: load_pygame('./Rooms/Level 1/04.tmx'),
            105: load_pygame('./Rooms/Level 1/05.tmx'),
            106: load_pygame('./Rooms/Level 1/06.tmx'),
            107: load_pygame('./Rooms/Level 1/07.tmx'),
            108: load_pygame('./Rooms/Level 1/08.tmx'),
            109: load_pygame('./Rooms/Level 1/09.tmx'),
            110: load_pygame('./Rooms/Level 1/10.tmx'),
        }
        
        chosen=random.randint(101,110)
        chosen_room=possible_rooms[chosen]
        for x, y, surf in chosen_room.get_layer_by_name('Water').tiles():
            self.layers['water'].append(Sprite((x*TILE_SIZE+pos[0], y*TILE_SIZE+pos[1]), surf, (self.all_sprites,self.collision_sprites)))
        # Load the floor layer (bg tiles, path, etc.)
        for x, y, surf in chosen_room.get_layer_by_name('Floor').tiles():
            self.layers['floor'].append(Sprite((x*TILE_SIZE+pos[0], y*TILE_SIZE+pos[1]), surf, (self.all_sprites)))

        # Load the walls layer (collidable objects)
        for x, y, surf in chosen_room.get_layer_by_name('Walls').tiles():
            self.layers['walls'].append(Sprite((x*TILE_SIZE+pos[0], y*TILE_SIZE+pos[1]), surf, (self.all_sprites, self.collision_sprites)))

        # Load decorations layer
        for x, y, surf in chosen_room.get_layer_by_name('Decorations').tiles():
            self.layers['decorations'].append(Sprite((x*TILE_SIZE+pos[0], y*TILE_SIZE+pos[1]), surf, (self.all_sprites)))

        # Load decorations2 layer
        for x, y, surf in chosen_room.get_layer_by_name('Decorations2').tiles():
            self.layers['decorations2'].append(Sprite((x*TILE_SIZE+pos[0], y*TILE_SIZE+pos[1]), surf, (self.all_sprites)))
        

    def generate_adjacent(self,current_room):
        if current_room not in self.visited_room:
            self.visited_room.append(str(current_room))
        offset_x = (WIDTH / 2) - (15 * TILE_SIZE / 2) + TILE_SIZE-10
        offset_y = (HEIGHT / 2) - (15 * TILE_SIZE / 2) + TILE_SIZE
        adjacent_offsets = [
            (0, 1),   # Down
            (1, 0),   # Right
            (0, -1),  # Up
            (-1, 0),  # Left
        ]

        for offset in adjacent_offsets:
            adjacent_room = [current_room[0] + offset[0], current_room[1] + offset[1]]
            adjacent_room_key = str(adjacent_room)

            # Only generate the room if it doesn't already exist
            if adjacent_room_key not in self.rooms:
                offset_x = self.rooms[str(current_room)].rect.left + offset[0] * self.room_size[0]
                offset_y = self.rooms[str(current_room)].rect.top + offset[1] * self.room_size[1]
                self.rooms[adjacent_room_key] = BoundingBox(offset_x, offset_y, 15 * TILE_SIZE, 15 * TILE_SIZE, self.bounding_box)
                self.generate((offset_x+30, offset_y+25))

    def spawn_enemies(self, bounding_box, max_enemies = 10):
        for _ in range(max_enemies):
            attempts = 0
            valid_position = False

            while not valid_position and attempts < 100:  # Limit attempts to prevent infinite loops
                x = random.randint(int(bounding_box.left)+100, int(bounding_box.right) - TILE_SIZE-100) 
                y = random.randint(int(bounding_box.top)+100, int(bounding_box.bottom) - TILE_SIZE-100) 
                # ^ The 100s are used to prevene the enemy from spawning outside the room
                # Temporary rect for collision check
                temp_rect = pygame.Rect(x, y, TILE_SIZE-20, TILE_SIZE-20)

                chosen_enemy_class = random.choice(self.enemy_classes)
                # Check if the position overlaps with collidable sprites
                if not any(sprite.rect.colliderect(temp_rect) for sprite in self.collision_sprites):
                    valid_position = True
                
                attempts += 1

            if valid_position:
                self.spawned_enemies.append(chosen_enemy_class((x, y), self.all_sprites, self.player, self.collision_sprites, self.damage_sprite, self.hpbar))
                self.spawned_enemies_pos.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))

            for i in self.spawned_enemies:
                i.add(self.enemy_group)

    def spawn_borders(self,current_room):
        border = load_pygame('./Rooms/Level 1/cover.tmx')
        for x, y, surf in border.get_layer_by_name('Walls').tiles():
            self.layers['spawn_border'].append(Sprite((x*TILE_SIZE+current_room.left+30, y*TILE_SIZE+current_room.top+25), surf, (self.all_sprites, self.collision_sprites,self.spawn_borders_group)))

    def run(self, dt):
        # Calculate the camera offset
        camera_offset = vector(WIDTH // 2 - self.player.hitbox.centerx, HEIGHT // 2 - self.player.hitbox.centery)
        self.display_surface.fill('black') 
        
        self.all_sprites.update(dt)
        self.damage_sprite.update(dt)

        # Room boundary
        current_room_key = str(self.current_room)
        current_room_rect = self.rooms[current_room_key].rect
        moved=False
 
        if current_room_key not in self.visited_room: 
            self.generate_adjacent(self.current_room)
            if current_room_key != str([0,0]):
                self.player.hitbox.center+= self.player.direction*150 
                self.spawn_enemies(self.rooms[current_room_key].rect)
                self.spawn_borders(self.rooms[current_room_key].rect)

        if self.player.hitbox.left < current_room_rect.left and not moved:
            # Move left
            self.current_room[0] -= 1
            moved = True
        elif self.player.hitbox.right > current_room_rect.right and not moved:
            # Move right
            self.current_room[0] += 1
            moved = True
        elif self.player.hitbox.top < current_room_rect.top and not moved:
            # Move up
            self.current_room[1] -= 1
            moved = True
        elif self.player.hitbox.bottom > current_room_rect.bottom and not moved:
            # Move down
            self.current_room[1] += 1
            moved = True

        # Draw layers with camera offset
        for sprite in self.layers['water']:
            self.display_surface.blit(sprite.image, sprite.rect.topleft + camera_offset)
        for sprite in self.layers['floor']:
            self.display_surface.blit(sprite.image, sprite.rect.topleft + camera_offset)
        for sprite in self.layers['decorations']:
            self.display_surface.blit(sprite.image, sprite.rect.topleft + camera_offset)

        self.display_surface.blit(self.player.swing.image,self.player.swing.rect.topleft+camera_offset)
        self.display_surface.blit(self.player.image, (WIDTH // 2 - self.player.rect.width // 2, HEIGHT // 2 - self.player.rect.height // 2))
        

        for sprite in self.enemy_group:
            self.display_surface.blit(sprite.image, sprite.rect.topleft + camera_offset)

            # Attack range
            # pygame.draw.rect(self.display_surface, "red", sprite.attack_range.move(camera_offset), 2) 



        for sprite in self.layers['walls']:
            self.display_surface.blit(sprite.image, sprite.rect.topleft + camera_offset)
        for sprite in self.layers['decorations2']:
            self.display_surface.blit(sprite.image, sprite.rect.topleft + camera_offset)

        for sprite in self.layers['spawn_border']:
            self.display_surface.blit(sprite.image, sprite.rect.topleft + camera_offset)



        if not self.enemy_group and current_room_key not in self.cleared_rooms: # Checks if there is enemy remaining
            player_difficulty.rooms_cleared += 1
            self.cleared_rooms.append(current_room_key)
            
            player_difficulty.difficulty += player_difficulty.diffculty_modifier
            
            for wall in self.spawn_borders_group:
                wall.kill()
                self.spawned_enemies_pos = []
                self.spawned_enemies = []
                self.layers['spawn_border'] = []
        for sprite in self.hpbar:
            self.display_surface.blit(sprite.image, sprite.rect.topleft + camera_offset)

        self.player_skill.update(dt)
        for sprite in self.player_skill:
            self.display_surface.blit(sprite.image, sprite.rect.topleft + camera_offset)
           

        # DEBUG BOXES

        # pygame.draw.rect(self.display_surface, "green", self.player.swing.rect.move(camera_offset), 2)
        # pygame.draw.rect(self.display_surface, "red", self.player.hitbox.move(camera_offset), 2)  # Player hitbox
        # pygame.draw.rect(self.display_surface, "blue", self.player.rect.move(camera_offset), 2)  # Player image rect
        for enemy_rect in self.spawned_enemies_pos: # Spawned enemies
            pygame.draw.rect(self.display_surface, "green", enemy_rect.move(camera_offset), 2)
        for room_key, room in self.rooms.items():
            pygame.draw.rect(self.display_surface, (255, 0, 0), room.rect.move(camera_offset), 2)  # Room bounding boxes
        for sprite in self.damage_sprite:
            self.display_surface.blit(sprite.image, sprite.rect.topleft + camera_offset)

        # GUI
        self.display_surface.blit(self.player.player_stats.health_bar_background, (10, -15))
        # HP Bar
        pygame.draw.rect(self.display_surface,(255,0,0),self.player.player_stats.health_bar)
        pygame.draw.rect(self.display_surface,(255,255,0),self.player.player_stats.transition_bar)
        pygame.draw.rect(self.display_surface,(255,255,255),(130,70,self.player.player_stats.health_bar_length,25),4)	    
        
        # EXP Bar
        pygame.draw.rect(self.display_surface,(0,255,0),(130, 120, self.player.player_stats.exp / self.player.player_stats.exp_ratio,25))

        pygame.draw.rect(self.display_surface,(255,255,255),(130,120, 180,25),4)
        level_text = pygame.font.SysFont('arial', 20, bold=True).render(f"Lv. {self.player.level}", True, "#009900")
        self.display_surface.blit(level_text, (70, 120))
        
        self.player.upgradeText.update()
        # Upgrade text
        self.display_surface.blit((self.player.upgradeText.text), (10, HEIGHT-40))

        current_room_text = pygame.font.SysFont('arial', 20, bold=True).render(current_room_key, True, (255, 255, 255))
        current_room_rect = current_room_text.get_rect(center=(WIDTH // 2, HEIGHT - 30))
        self.display_surface.blit(current_room_text, current_room_rect)
