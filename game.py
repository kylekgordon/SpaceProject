import pygame

from models import Asteroid, Spaceship, NPC, Wormhole
from utils import get_random_position, load_sprite, print_text, load_sound


import pygame
import math
import random
from pygame.math import Vector2

# Color library
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

time_elapse = 1000

# Add the ships to a list
ships = ["space_ship1", "space_ship2", "space_ship3", "space_ship4", "space_ship5", "space_ship6", "space_ship7", "space_ship8", "space_ship9", "space_ship10"]
display_time = 1000  # Time in milliseconds to display each image
wormhole_path = ["sprites/Portal/portal01.png", "sprites/Portal/portal02.png",
                        "sprites/Portal/portal03.png", "sprites/Portal/portal04.png",
                        "sprites/Portal/portal05.png", "sprites/Portal/portal06.png",
                        "sprites/Portal/portal07.png", "sprites/Portal/portal08.png",
                        "sprites/Portal/portal09.png", "sprites/Portal/portal10.png",
                        "sprites/Portal/portal11.png", "sprites/Portal/portal12.png",
                        "sprites/Portal/portal13.png", "sprites/Portal/portal14.png",
                        "sprites/Portal/portal15.png", "sprites/Portal/portal16.png",
                        "sprites/Portal/portal17.png", "sprites/Portal/portal18.png",
                        "sprites/Portal/portal19.png", "sprites/Portal/portal20.png",
                        "sprites/Portal/portal21.png", "sprites/Portal/portal22.png",
                        "sprites/Portal/portal23.png", "sprites/Portal/portal24.png",
                        "sprites/Portal/portal25.png", "sprites/Portal/portal26.png",
                        "sprites/Portal/portal27.png", "sprites/Portal/portal28.png",
                        "sprites/Portal/portal29.png", "sprites/Portal/portal30.png",
                        "sprites/Portal/portal31.png", "sprites/Portal/portal32.png",
                        "sprites/Portal/portal33.png", "sprites/Portal/portal34.png",
                        "sprites/Portal/portal35.png", "sprites/Portal/portal36.png",
                        "sprites/Portal/portal37.png", "sprites/Portal/portal38.png",
                        "sprites/Portal/portal39.png", "sprites/Portal/portal40.png",
                        "sprites/Portal/portal41.png", "sprites/Portal/portal42.png",
                        "sprites/Portal/portal43.png", "sprites/Portal/portal44.png",
                        "sprites/Portal/portal45.png", "sprites/Portal/portal46.png",
                        "sprites/Portal/portal47.png", "sprites/Portal/portal48.png",
                        "sprites/Portal/portal49.png", "sprites/Portal/portal50.png",
                        "sprites/Portal/portal51.png", "sprites/Portal/portal52.png",
                        "sprites/Portal/portal53.png", "sprites/Portal/portal54.png",
                        "sprites/Portal/portal55.png", "sprites/Portal/portal56.png",
                        "sprites/Portal/portal57.png", "sprites/Portal/portal58.png",
                        "sprites/Portal/portal59.png", "sprites/Portal/portal60.png",
                        "sprites/Portal/portal61.png", "sprites/Portal/portal62.png",
                        "sprites/Portal/portal63.png", "sprites/Portal/portal64.png"]

class SpaceRocks:
    MIN_ASTEROID_DISTANCE = 250

    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite("BackgroundSupernovaLarge", False)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.message = ""

        self.hit = load_sound("DefiniteHit")
        self.explosion = load_sound("MiniExplosionChainReaction")

        self.asteroids = []
        self.bullets = []
        self.spaceship = Spaceship((400, 300), self.bullets.append)
        self.wormhole = Wormhole((random.randrange(10, 790, 1), random.randrange(10, 790, 1)), self.background)
        # self.npc = []
        # self.npc.append(NPC(
        #     (200, 200), self.bullets.append, random.choice(ships), [self.spaceship]
        # ))
        self.npc = NPC((random.randrange(10, 790, 1), random.randrange(10, 790, 1)), self.bullets.append, random.choice(ships), [self.spaceship])
        # Griffin changed this to 1 so it would only generate 1 asteroid :)
        for _ in range(2):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.spaceship.position)
                    > self.MIN_ASTEROID_DISTANCE
                ):
                    break

            self.asteroids.append(Asteroid(position, self.asteroids.append))

    def main_loop(self):
        global time_elapse
        while True:
            self._handle_input()
            self._process_game_logic()
            #self._map_scroll()
            self._draw()
            #Wormhole(self.background)
            # time_elapse -= 1
            # if time_elapse == 0:
            #     Wormhole(self.screen, "True")
            #     time_elapse = 1000
            # else:
            #     Wormhole(self.screen, False)
            # Animate images
            
            # self.animate_images(image_paths, 10, self.screen)
            # for path in wormhole_path:
            #     self.display_image(path, display_time,self.background)

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Spacers")

    def _damage_bar(self, damage):
        damage_bar_width = 100
        damage_bar_height = 10
        #damage_bar_surface = pygame.Surface((damage_bar_width - damage, damage_bar_height))
        damage_bar_rect = pygame.Rect(10, 10, damage_bar_width - damage, damage_bar_height)

        damage_bar_rect.width = int(damage_bar_width - damage)
        pygame.draw.rect(self.background, red, damage_bar_rect)

        pygame.display.update()
        # self.image = pygame.draw.rect(self.background, red, pygame.Rect(10, 10, 10 * damage, 10))

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                quit()
            elif (
                self.spaceship
                and event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
            ):
                self.spaceship.shoot()

        is_key_pressed = pygame.key.get_pressed()

        if self.spaceship:
            if is_key_pressed[pygame.K_RIGHT]:
                self.spaceship.rotate(clockwise=True)
            if is_key_pressed[pygame.K_LEFT]:
                self.spaceship.rotate(clockwise=False)
            if is_key_pressed[pygame.K_UP]:
                self.spaceship.accelerate()
            if is_key_pressed[pygame.K_DOWN]:
                self.spaceship.decelerate()

    def _process_game_logic(self):

        for game_object in self._get_game_objects():
            game_object.move(self.screen)

        if self.spaceship:
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceship):
                    self.hit.play()
                    self.spaceship.damage += 1
                    print(self.spaceship.damage)
                    self._damage_bar(self.spaceship.damage*10)
                    self.asteroids.remove(asteroid)
                    asteroid.split()
                    if self.spaceship.damage == 10:
                        self.spaceship = None
                        self.explosion.play()
                        self.message = "You lost!"
                    #self.message = "You lost!"
                    break

        # for enemy in self.npc:
        #     enemy.choose_target()
        #     enemy.follow_target()
        #     for asteroid in self.asteroids:
        #         if asteroid.collides_with(enemy):
        #             self.npc.remove(enemy)
        #             break
                
        if self.npc:
            self.npc.choose_target()
            self.npc.follow_target()
            #self.npc.shoot()

        if self.wormhole:
            self.wormhole.update()

        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    asteroid.split()
                    break


        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)

            if bullet.collides_with(self.npc):
                self.npc.remove()
                self.bullets.remove(bullet)

        if not self.npc and self.spaceship:
            self.message = "You won!"

    def _draw(self):
        global time_elapse
        self.screen.blit(self.background, (0,0))
        for game_object in self._get_game_objects():
            #print(game_object)
            game_object.draw(self.screen)

        if self.message:
            print_text(self.screen, self.message, self.font)

        pygame.display.flip()
        self.clock.tick(60)

    def _get_game_objects(self):
        game_objects = [*self.asteroids, *self.bullets]

        if self.spaceship:
            game_objects.append(self.spaceship)

        if self.npc:
            game_objects.append(self.npc)

        return game_objects
    
    # def Wormhole(surface):
    # # Create a random wormhole at a random position in pygame as a sprite
    #     wormhole_x = random.randint(0, 800)
    #     wormhole_y = random.randint(0, 600)

    #     for i in range(0, 64):
    #         wormhole = pygame.image.load(wormhole_path[i])
    #         wormhole = pygame.transform.scale(wormhole, (200, 150))
    #         surface.blit(wormhole, (wormhole_x, wormhole_y))
    #         # time.sleep(1)

    def _map_scroll(self):
        # self.spaceship.rect = self.spaceship.get_rect()
        # self.background.rect = self.background.get_rect()
        
        # if self.spaceship.rect.x > self.screen.get_width() / 2:
        #     self.background.rect.x += self.spaceship.speed

        # if self.spaceship.rect.x < self.screen.get_width() / 2:
        #     self.background.rect.x -= self.spaceship.speed
        
        # if self.spaceship.rect.y > self.screen.get_height() / 2:
        #     self.background.rect.y += self.spaceship.speed

        # if self.spaceship.rect.y < self.screen.get_height() / 2:
        #     self.background.rect.y -= self.spaceship.speed
        pass

    # def display_image(self, image_path, display_time, screen):
    #     # Load image
    #     image = pygame.image.load(image_path).convert_alpha()

    #     # Display image
    #     screen.blit(image, (300, 200))
    #     pygame.display.update()
    #     pygame.time.delay(display_time)