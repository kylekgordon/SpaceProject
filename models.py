from pygame.math import Vector2
from pygame import transform

import time
import pygame
import random
from utils import get_random_velocity, load_sound, load_sprite, wrap_position, distance
import math

UP = Vector2(0, -1)

# Color library
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

# Add the ships to a list
ships = ["space_ship1", "space_ship2", "space_ship3", "space_ship4", "space_ship5", "space_ship6", "space_ship7", "space_ship8", "space_ship9", "space_ship10"]

# Animate images in a list of images
image_paths = ["sprites/Portal/portal01.png", "sprites/Portal/portal02.png",
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

explosion_paths = ["sprites/Explosion/1.png", "sprites/Explosion/2.png",
                    "sprites/Explosion/3.png", "sprites/Explosion/4.png", 
                    "sprites/Explosion/5.png", "sprites/Explosion/6.png",
                    "sprites/Explosion/7.png", "sprites/Explosion/8.png",
                    "sprites/Explosion/9.png", "sprites/Explosion/10.png",
                    "sprites/Explosion/11.png", "sprites/Explosion/12.png",
                    "sprites/Explosion/13.png", "sprites/Explosion/14.png",
                    "sprites/Explosion/15.png", "sprites/Explosion/16.png",
                    "sprites/Explosion/17.png", "sprites/Explosion/18.png",
                    "sprites/Explosion/19.png", "sprites/Explosion/20.png",
                    "sprites/Explosion/21.png", "sprites/Explosion/22.png",
                    "sprites/Explosion/23.png", "sprites/Explosion/24.png",
                    "sprites/Explosion/25.png", "sprites/Explosion/26.png",
                    "sprites/Explosion/27.png", "sprites/Explosion/28.png",
                    "sprites/Explosion/29.png", "sprites/Explosion/30.png"]

# Choose a random bullet sprite
bullet = random.randrange(10, 66, 1)

current_image = 0
current_image_2 = 0

class GameObject:
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self, surface):
        self.position = wrap_position(self.position + self.velocity, surface)
        # print(f"pos: {self.position}")

    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius


# class NPCShip(pygame.sprite.Sprite):
#     def __init__(self, x, y, target_list, projectile_group):
#         super().__init__()
#         self.image = pygame.image.load(
#             "../assets/sprites/space_ship5_40x40.png.png"
#         ).convert_alpha()
#         self.rect = self.image.get_rect()
#         self.rect.x = x
#         self.rect.y = y
#         self.speed = 2
#         self.rotation_speed = 2
#         self.target_list = target_list
#         self.projectile_group = projectile_group
#         self.target = None
#         self.target_time = 0
#         self.target_time_quantum = 120  # 2 seconds at 60 FPS
#         self.shooting_delay = 60
#         self.shooting_timer = 0

#     def choose_target(self):
#         if self.target_time >= self.target_time_quantum:
#             if self.target_list:
#                 self.target = random.choice(self.target_list)
#             else:
#                 self.target = None
#             self.target_time = 0
#         else:
#             self.target_time += 1

#     def follow_target(self):
#         if self.target:
#             direction = Vector2(
#                 self.target.rect.x - self.rect.x, self.target.rect.y - self.rect.y
#             )
#             distance = direction.length()
#             direction.normalize_ip()

#             angle = math.degrees(math.atan2(direction.y, direction.x)) - 90
#             current_angle = (
#                 pygame.transform.rotate(self.image, self.rotation_speed)
#                 .get_rect()
#                 .angle
#             )
#             new_angle = angle - current_angle
#             self.image = pygame.transform.rotate(self.image, new_angle)
#             self.rect = self.image.get_rect(center=self.rect.center)

#             if distance > 100:
#                 self.rect.x += direction.x * self.speed
#                 self.rect.y += direction.y * self.speed

#     def shoot(self):
#         if self.shooting_timer >= self.shooting_delay:
#             if self.target:
#                 projectile = Projectile(
#                     self.rect.x, self.rect.y, self.target.rect.x, self.target.rect.y
#                 )
#                 self.projectile_group.add(projectile)
#             self.shooting_timer = 0
#         else:
#             self.shooting_timer += 1

#     def update(self):
#         self.choose_target()
#         self.follow_target()
#         self.shoot()


class Spaceship(GameObject):
    MANEUVERABILITY = 3
    ACCELERATION = 0
    BULLET_SPEED = 10

    def __init__(self, position, create_bullet_callback, ship=random.choice(ships)):
        self.create_bullet_callback = create_bullet_callback
        self.laser_sound = load_sound("laser")
        # Make a copy of the original UP vector
        self.direction = Vector2(UP)
        self.damage = 0
        self.speed = 5

        super().__init__(position, load_sprite(ship), Vector2(0))

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    def accelerate(self):
        self.ACCELERATION = 0.1
        if self.ACCELERATION > 1:
            self.velocity -= self.direction * self.ACCELERATION
        self.velocity += self.direction * self.ACCELERATION

    def decelerate(self):
        self.ACCELERATION = 0.1
        self.velocity -= self.direction * self.ACCELERATION

    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = transform.rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

    def shoot(self):
        angle = self.direction.angle_to(UP)
        bullet_velocity = self.direction * self.BULLET_SPEED + self.velocity
        bullet = Bullet(self.position, bullet_velocity, angle)
        self.create_bullet_callback(bullet)
        self.laser_sound.play()

class NPC(Spaceship):
    def __init__(
        self, position, create_bullet_callback, ship=random.choice(ships), targets=[]
    ):
        self.targets = targets
        self.damage = 0
        self.speed = 0.01
        self.image = load_sprite(ship)
        self.rect = self.image.get_rect()

        super().__init__(position, create_bullet_callback, ship)

    def choose_target(self):
        closestDistance = pow(2, 20)
        closestTarget = None
        for target in self.targets:
            d = distance(target.position, self.position)
            if distance(target.position, self.position) < closestDistance:
                closestTarget = target
                closestDistance = d

        self.target = closestTarget

    def follow_target(self):
        if self.target:
            self.direction = Vector2(
                self.target.position[0] - self.position[0],
                self.target.position[1] - self.position[1],
            )
            self.direction.normalize()
            #self.velocity = self.direction * self.speed

    def shoot(self):
        angle = self.direction.angle_to(UP)
        bullet_velocity = self.direction * self.BULLET_SPEED + self.velocity
        bullet = Bullet(self.position, bullet_velocity, angle)
        self.create_bullet_callback(bullet)
        self.laser_sound.play()

    def remove(self):
        pass

class Asteroid(GameObject):
    def __init__(self, position, create_asteroid_callback, size=3):
        self.create_asteroid_callback = create_asteroid_callback
        self.size = size

        size_to_scale = {3: 1.0, 2: 0.5, 1: 0.25}
        scale = size_to_scale[size]
        sprite = transform.rotozoom(load_sprite("asteroid"), 0, scale)

        super().__init__(position, sprite, get_random_velocity(1, 3))

    def split(self):
        if self.size > 1:
            for _ in range(2):
                asteroid = Asteroid(
                    self.position, self.create_asteroid_callback, self.size - 1
                )
                self.create_asteroid_callback(asteroid)

class Bullet(GameObject):
    def __init__(self, position, velocity, angle):
        
        super().__init__(position, load_sprite(f"{bullet}"), velocity)
        #self.sprite = pygame.transform.scale(self.sprite, (30, 30))
        self.sprite = pygame.transform.rotozoom(self.sprite, angle, 0.3)
        self.radius = self.sprite.get_width() / 2
        


    def move(self, surface):
        self.position = self.position + self.velocity

class Wormhole(GameObject):
    
    def __init__(self, position, screen, image_paths = image_paths):
        
        # Load images as surfaces
        images = [pygame.image.load(path).convert_alpha() for path in image_paths]

        # Create sprite object and set initial image
        sprite = pygame.sprite.Sprite()
        sprite.image = images[0]
        sprite.rect = sprite.image.get_rect()

        self.screen = screen
        self.position = position
        # Call the superclass constructor
        #for i in range(0, 64):
            #wormhole = images[i]
            #wormhole = pygame.transform.scale(wormhole, (200, 150))
            #screen.blit(wormhole, position)


    def update(self):
        global current_image
        current_image_path = image_paths[current_image]
        current_image_surface = pygame.image.load(current_image_path)
        current_image_surface = pygame.transform.scale(current_image_surface, (200, 150))
        self.screen.blit(current_image_surface, self.position)

        current_image += 1
        if current_image >= len(image_paths):
            current_image = 0

        pygame.display.update()
        # pass

class Damage_bar():
    def __init__(self, surface):
        super().__init__()
        self.damage_bar_width = 0
        self.damage_bar_height = 10
        self.font = pygame.font.SysFont("Arial", 15)
        self.surface = surface
        # damage_bar_surface = pygame.Surface((width, self.damage_bar_rect.height))
        # damage_bar_surface.fill(red)
        #pygame.draw.rect(self.background, red, damage_bar_rect)
        
        # damage_bar_rect.width = int(damage_bar_width - damage)
        # pygame.draw.rect(self.background, red, damage_bar_rect)
        #surface.blit(damage_bar_surface,(10, 10))
        #surface.blit(surface, (10, 10))
    # self.image = pygame.draw.rect(self.background, red, pygame.Rect(10, 10, 10 * damage, 10))

    def update(self, damage):
        width = self.damage_bar_width + damage
        pygame.draw.rect(self.surface, red, (10, 28, width, self.damage_bar_height))
        pygame.draw.rect(self.surface, white, (10, 28, 100, self.damage_bar_height), 2)
        damage_text = self.font.render("Damage" , True, white)
        self.surface.blit(damage_text, (10, 5))
        pygame.display.update()

class Explosion(GameObject):
    
    def __init__(self, position, screen, targets=[], explode_paths = explosion_paths):
        
        # Load images as surfaces
        # images = [pygame.image.load(path).convert_alpha() for path in explosion_paths]

        # # Create sprite object and set initial image
        # sprite = pygame.sprite.Sprite()
        # sprite.image = images[0]
        # sprite.rect = sprite.image.get_rect()

        self.targets = targets
        self.screen = screen
        self.position = position
        # Call the superclass constructor
        #for i in range(0, 64):
            #wormhole = images[i]
            #wormhole = pygame.transform.scale(wormhole, (200, 150))
            #screen.blit(wormhole, position)


    def update(self, pos, explode_paths = explosion_paths):
        global current_image_2
        #current_image_path = explode_paths[current_image_2]
        #current_image_surface = pygame.image.load(current_image_path)
        #current_image_surface = pygame.transform.scale(current_image_surface, (200, 150))
        self.screen.blit(pygame.image.load(explode_paths[current_image_2]), pos)

        current_image_2 += 1
        if current_image_2 >= len(explosion_paths):
            current_image_2 = 0

        pygame.display.update()