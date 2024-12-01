import pygame,sys
from rooms import Level
from pytmx.util_pygame import load_pygame
from entities import Player


running = True
dt = 0



class Game():
    def __init__(self) -> None:
        pygame.init()
        self.clock = pygame.time.Clock()
        self.display_surface = pygame.display.set_mode((1280, 780))

        self.player_pos = pygame.Vector2(self.display_surface.get_width() / 2, self.display_surface.get_height() / 2)
        self.player = Player(self.player_pos.x, self.player_pos.y)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.tmx_maps={0: load_pygame('./Rooms/Level 1/01.tmx')}
        self.current_stage=Level(self.tmx_maps[0])
        self.all_sprites.add(self.current_stage.all_sprites) 

    def run(self):
        is_moving = False
        while True:
            prev_position = self.player_pos.copy()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                keys = pygame.key.get_pressed()

                if keys[pygame.K_w]:
                    for sprite in self.all_sprites:
                        sprite.rect.y+=200*dt
                    self.player_pos.y -= 200 * dt

                    is_moving = True
                if keys[pygame.K_a]:
                    for sprite in self.all_sprites:
                        sprite.rect.x +=200*dt
                    self.player_pos.x -= 200 * dt
                    is_moving = True
                    if not self.player.flipped:  # Flip only if the player isn't already facing left
                        self.player.flip()
                if keys[pygame.K_s]:
                    for sprite in self.all_sprites:
                        sprite.rect.y-=200*dt
                    self.player_pos.y += 200 * dt
                    is_moving = True
                
                if keys[pygame.K_d]:
                    for sprite in self.all_sprites:
                        sprite.rect.x -= 200*dt
                    self.player_pos.x += 200 * dt
                    is_moving = True
                    if self.player.flipped:  # Flip only if the player is facing left
                        self.player.flip()

            if is_moving:
                self.player.set_state("move")  # Set moving animation
            else:
                self.player.set_state("idle")  # Set idle animation
            self.player.rect.center = self.player_pos

            # if pygame.sprite.spritecollide(self.player, self.current_stage.collision_sprites, False):
            #     print("AFAKG<LJAIUY")




            # Update and draw sprites
            self.all_sprites.update()


            self.all_sprites.draw(self.display_surface)

            pygame.display.flip()
            dt = self.clock.tick() / 1000
            self.current_stage.run()
            pygame.display.update()


        pygame.quit()

if __name__ == '__main__':
    game=Game()
    game.run()

