from settings import * 

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        original_width, original_height = surf.get_size()

        new_width = int(original_width * 4)
        new_height = int(original_height * 4)
        self.image = pygame.transform.scale(surf, (new_width, new_height))

        self.rect = self.image.get_frect(center = pos)

class bounding_box(pygame.sprite.Sprite):
    def __init__(self,x,y,height,width, groups):
        super().__init__(groups)
        self.rect = pygame.FRect(x,y,height,width)

# Enemy sprite, scale