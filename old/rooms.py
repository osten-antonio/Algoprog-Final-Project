from settings import *

class Level:
    def __init__(self, tmx_map, scale_factor=5):
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        self.scale_factor = scale_factor  # Store the scale factor
        self.setup(tmx_map)

        self.width = tmx_map.width * 16 * self.scale_factor  # Calculate the level width
        self.height = tmx_map.height * 16 * self.scale_factor 

    def setup(self, tmx_map):
        for x, y, surf in tmx_map.get_layer_by_name('Walls').tiles():
            # Scale position and surface
            scaled_pos = (16 * x * self.scale_factor, 16 * y * self.scale_factor)
            Sprite(scaled_pos, surf, (self.all_sprites,self.collision_sprites),scale_factor=self.scale_factor)

    def run(self):
        self.display_surface.fill('purple')
        self.all_sprites.draw(self.display_surface)

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, scale_factor):
        super().__init__(groups)
        # Scale the surface proportionally
        original_width, original_height = surf.get_size()
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)
        
        self.image = pygame.transform.scale(surf, (new_width, new_height))
        self.image.fill("white")
        self.rect = self.image.get_rect(topleft=pos)