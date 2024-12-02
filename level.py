from settings import *
from sprites import Sprite,bounding_box
from players import Player
from collections import defaultdict
import random

class Level:
    def __init__(self, tmx_map):
        self.display_surface = pygame.display.get_surface()

        # Groups for different types of objects
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.bounding_box = pygame.sprite.Group()
        self.rooms = defaultdict(pygame.sprite.Sprite)
        self.current_room = [0, 0]
        # Set camera vector (used for following the player)
        self.camera_vector = vector(0, 0)
        self.visited_room = []
        # Room files (for loading different levels)
        self.room_files = [join('./Rooms/Level 1/', file) for file in listdir('./Rooms/Level 1') if file.endswith('.tmx')]
        self.room_size = (15 * TILE_SIZE, 15 * TILE_SIZE)
        self.setup(tmx_map)

    def setup(self, tmx_map):

        self.layers = {
            'water':[],
            'floor': [],
            'walls': [],
            'decorations': [],
            'decorations2': [],
        }
        offset_x = (WIDTH / 2) - (tmx_map.width * TILE_SIZE / 2) + TILE_SIZE-10
        offset_y = (HEIGHT / 2) - (tmx_map.height * TILE_SIZE / 2) + TILE_SIZE

        self.rooms["[0, 0]"] =  bounding_box(offset_x-30,offset_y-25, tmx_map.width*TILE_SIZE, tmx_map.height*TILE_SIZE, self.bounding_box) # 30 and 25 is magic number im sorry
        
        # Fix this, move the rect relative to the player
        # print(f"x={TILE_SIZE + offset_x}")
        # print(f"y={TILE_SIZE + offset_y}")
        for x, y, surf in tmx_map.get_layer_by_name('Water').tiles():
            self.layers['water'].append(Sprite((x * TILE_SIZE + offset_x, y * TILE_SIZE + offset_y), surf, (self.all_sprites,self.collision_sprites)))
        # Load the floor layer (bg tiles, path, etc.)
        for x, y, surf in tmx_map.get_layer_by_name('Floor').tiles():
            self.layers['floor'].append(Sprite((x * TILE_SIZE + offset_x, y * TILE_SIZE + offset_y), surf, (self.all_sprites,)))



        # Load decorations layer
        for x, y, surf in tmx_map.get_layer_by_name('Decorations').tiles():
            self.layers['decorations'].append(Sprite((x * TILE_SIZE + offset_x, y * TILE_SIZE + offset_y), surf, (self.all_sprites,)))

        # Set up the player (always on top of other layers)
        self.player = Player((WIDTH // 2, HEIGHT // 2), self.all_sprites, self.collision_sprites)

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
        # TODO: Implement level system later
        chosen=random.randint(101,110)
        chosen_room=possible_rooms[chosen]
        for x, y, surf in chosen_room.get_layer_by_name('Water').tiles():
            self.layers['water'].append(Sprite((x*TILE_SIZE+pos[0], y*TILE_SIZE+pos[1]), surf, (self.all_sprites,self.collision_sprites)))
        # Load the floor layer (bg tiles, path, etc.)
        for x, y, surf in chosen_room.get_layer_by_name('Floor').tiles():
            self.layers['floor'].append(Sprite((x*TILE_SIZE+pos[0], y*TILE_SIZE+pos[1]), surf, (self.all_sprites,)))

        # Load the walls layer (collidable objects)
        for x, y, surf in chosen_room.get_layer_by_name('Walls').tiles():
            self.layers['walls'].append(Sprite((x*TILE_SIZE+pos[0], y*TILE_SIZE+pos[1]), surf, (self.all_sprites, self.collision_sprites)))

        # Load decorations layer
        for x, y, surf in chosen_room.get_layer_by_name('Decorations').tiles():
            self.layers['decorations'].append(Sprite((x*TILE_SIZE+pos[0], y*TILE_SIZE+pos[1]), surf, (self.all_sprites,)))

        # Load decorations2 layer
        for x, y, surf in chosen_room.get_layer_by_name('Decorations2').tiles():
            self.layers['decorations2'].append(Sprite((x*TILE_SIZE+pos[0], y*TILE_SIZE+pos[1]), surf, (self.all_sprites,)))
        

    def generate_adjacent(self,current_room):
        self.visited_room.append(current_room)
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
                # print(f"Generating {adjacent_room}")
                offset_x = self.rooms[str(current_room)].rect.left + offset[0] * self.room_size[0]
                offset_y = self.rooms[str(current_room)].rect.top + offset[1] * self.room_size[1]
                self.rooms[adjacent_room_key] = bounding_box(offset_x, offset_y, 15 * TILE_SIZE, 15 * TILE_SIZE, self.bounding_box)
                self.generate((offset_x+30, offset_y+25))

    def run(self, dt):
        self.all_sprites.update(dt)
        offset_x = (WIDTH / 2) - (15 * TILE_SIZE / 2) + TILE_SIZE-10
        offset_y = (HEIGHT / 2) - (15 * TILE_SIZE / 2) + TILE_SIZE
        current_room,current_room_key = str(self.current_room),str(self.current_room)
        
        # print(current_room)
            # Ensure the current room exists
        if current_room_key not in self.visited_room:
            self.generate_adjacent(self.current_room)

        # Room boundary checks
        current_room_rect = self.rooms[current_room_key].rect
        moved = False  # Flag to prevent multiple updates in one frame

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

        
        # Draw layers in order
        for sprite in self.layers['water']:
            self.display_surface.blit(sprite.image, sprite.rect)
        for sprite in self.layers['floor']:
            self.display_surface.blit(sprite.image, sprite.rect)
        for sprite in self.layers['decorations']:
            self.display_surface.blit(sprite.image, sprite.rect)
        # self.display_surface.blit(self.player.image, self.player.rect)
        for sprite in self.layers['walls']:
            self.display_surface.blit(sprite.image, sprite.rect)
        for sprite in self.layers['decorations2']:
            self.display_surface.blit(sprite.image, sprite.rect)

        # Moves all sprite relative to player's movement
        for sprite in self.all_sprites:
            sprite.rect.x -= self.player.velocity.x
            sprite.rect.y -= self.player.velocity.y
        for sprite in self.bounding_box:
            sprite.rect.x -= self.player.velocity.x
            sprite.rect.y -= self.player.velocity.y
        pygame.draw.rect(self.display_surface, (255, 0, 0), self.player.hitbox,2)
        pygame.draw.rect(self.display_surface, (255, 0, 0), self.player.rect,2)
        for i in self.rooms:
            pygame.draw.rect(self.display_surface, (255, 0, 0), self.rooms[str(i)],2) # Draw binding box for testing purposes
