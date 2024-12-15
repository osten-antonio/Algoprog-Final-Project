from settings import * 
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join
from gui import mainMenu

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WIDTH, HEIGHT))

        self.clock = pygame.time.Clock()

        self.tmx_maps = {
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
        self.stage = Level(load_pygame('./Rooms/Level 1/start.tmx'))
    def run(self):
        while self.stage.player.alive and player_difficulty.playing:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.display_surface.fill('black')
            self.stage.run(dt)
            pygame.display.update()

        

if __name__ == '__main__':
    game = mainMenu()
    