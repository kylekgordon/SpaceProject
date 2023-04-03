import pygame

from models import Asteroid, Spaceship, NPC
from utils import get_random_position, load_sprite, print_text


import pygame
import math
import random
from pygame.math import Vector2


# Add the ships to a list
ships = ["space_ship1", "space_ship2", "space_ship3", "space_ship4", "space_ship5", "space_ship6", "space_ship7", "space_ship8", "space_ship9", "space_ship10"]

class SpaceRocks:
    MIN_ASTEROID_DISTANCE = 250

    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite("BackgroundSupernovaLarge", False)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.message = ""

        self.asteroids = []
        self.bullets = []
        self.spaceship = Spaceship((400, 300), self.bullets.append)
        self.npc = NPC(
            (200, 200), self.bullets.append, random.choice(ships), [self.spaceship]
        )

        # Griffin changed this to 1 so it would only generate 1 asteroid :)
        for _ in range(0):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.spaceship.position)
                    > self.MIN_ASTEROID_DISTANCE
                ):
                    break

            self.asteroids.append(Asteroid(position, self.asteroids.append))

    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Spacers")

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
                    self.spaceship = None
                    self.message = "You lost!"
                    break

        if self.npc:
            self.npc.choose_target()
            self.npc.follow_target()

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

        # if not self.asteroids and self.spaceship:
        #     self.message = "You won!"

    def _draw(self):
        self.screen.blit(self.background, (0, 0))

        for game_object in self._get_game_objects():
            print(game_object)
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
