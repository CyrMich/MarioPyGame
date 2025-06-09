import pygame
import math
from constants import DIFFICULTY_SETTINGS, CURRENT_DIFFICULTY, WINDOW, SPRITE_SHEET_ENEMIES, SPRITE_SHEET_OBJECTS, HIT_SOUND, DEATH_SOUND, POWERUP_SOUND, HEIGHT
from utils import get_image_from_sheet

class Enemy(pygame.sprite.Sprite):
    GRAVITY = 1

    def __init__(self, x, y, width, height, speed=2):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.base_speed = speed
        self.speed = speed * DIFFICULTY_SETTINGS[CURRENT_DIFFICULTY]["enemy_speed_multiplier"]
        self.y_vel = 0
        self.alive = True

    def apply_gravity(self):
        self.y_vel += self.GRAVITY
        if self.y_vel > 10:
            self.y_vel = 10

    def move_and_collide(self, objects):
        self.rect.x += self.speed
        for obj in objects:
            if self.rect.colliderect(obj.rect):
                if self.speed > 0:
                    self.rect.right = obj.rect.left
                else:
                    self.rect.left = obj.rect.right
                self.speed *= -1

        self.rect.y += self.y_vel
        for obj in objects:
            if self.rect.colliderect(obj.rect):
                if self.y_vel > 0:
                    self.rect.bottom = obj.rect.top
                    self.y_vel = 0
                elif self.y_vel < 0:
                    self.rect.top = obj.rect.bottom
                    self.y_vel = 0

    def update(self, player, objects):
        if not self.alive:
            return

        self.apply_gravity()
        self.move_and_collide(objects)

        if self.rect.colliderect(player.rect):
            if player.rect.bottom <= self.rect.top+20:
                self.alive = False
                player.y_vel = -15
                player.jump = True
            else:
                player.lives -= 1
                if player.lives <= 0:
                    global enemies
                    player.reset()
                else:
                    player.rect.x -= 50
                    player.y_vel = -10

    def draw(self, scroll_x):
        if self.alive:
            adjusted = self.rect.copy()
            adjusted.x -= scroll_x
            pygame.draw.rect(WINDOW, "green", adjusted)

    def is_off_screen(self, scroll_x):
        return self.rect.right - scroll_x < 0


class Goomba(Enemy):
    SPRITES = [
        get_image_from_sheet(SPRITE_SHEET_ENEMIES, 0, 4, 16, 16, 2),   # CHÓD [1]
        get_image_from_sheet(SPRITE_SHEET_ENEMIES, 30, 4, 16, 16, 2),  # CHÓD [2]
        get_image_from_sheet(SPRITE_SHEET_ENEMIES, 61, 4, 16, 16, 2)   # UMIERA
    ]

    def __init__(self, x, y, width=32, height=32, speed=2, walking_range=200):
        super().__init__(x, y - height, width, height, speed)
        self.original_speed = abs(self.speed)
        self.walking_range = walking_range
        self.start_x = x
        self.left_boundary = x - walking_range // 2
        self.right_boundary = x + walking_range // 2
        self.animation_count = 0
        self.sprite_index = 0
        self.sprite = self.SPRITES[0]
        self.alive = True
        self.to_remove = False
        self.death_timer = 0
        self.death_duration = 10

    def move_and_collide(self, objects):
        next_x = self.rect.x + self.speed

        if next_x <= self.left_boundary:
            self.rect.x = self.left_boundary
            self.speed = abs(self.speed)
        elif next_x + self.rect.width >= self.right_boundary:
            self.rect.x = self.right_boundary - self.rect.width
            self.speed = -abs(self.speed)
        else:
            self.rect.x = next_x

        for obj in objects:
            if self.rect.colliderect(obj.rect):
                if self.speed > 0:
                    self.rect.right = obj.rect.left
                else:
                    self.rect.left = obj.rect.right
                self.speed *= -1

    def update(self, player, objects):
        if not self.alive:
            self.sprite = self.SPRITES[2]
            self.death_timer += 1

            if self.death_timer >= self.death_duration:
                self.to_remove = True
            return

        self.animation_count += 1
        if self.animation_count >= 20:
            self.animation_count = 0
            self.sprite_index = 1 if self.sprite_index == 0 else 0
        self.sprite = self.SPRITES[self.sprite_index]

        self.rect = self.sprite.get_rect(topleft=(self.rect.x,self.rect.y))

        self.apply_gravity()
        self.move_and_collide(objects)

        # KOLIZJA Z GRACZEM
        if self.rect.colliderect(player.rect):
            if player.invincible:
                return

            if player.rect.bottom <= self.rect.top + 20 and player.y_vel > 0:
                self.alive = False
                player.score += 2
                player.y_vel = -15
                player.jump = True

            elif player.size == "big":
                player.to_small()
                player.invincible = True
                player.invincibility_timer = pygame.time.get_ticks()

            else:
                HIT_SOUND.play()
                player.lives -= 1
                player.invincible = True
                player.invincibility_timer = pygame.time.get_ticks()

                if player.lives <= 0:
                    DEATH_SOUND.play()
                    player.reset()
                else:
                    player.rect.x -= 50
                    player.y_vel = -10



    def draw(self, scroll_x):
        adjusted = self.rect.copy()
        adjusted.x -= scroll_x
        WINDOW.blit(self.sprite, (adjusted.x, adjusted.y))


class Boo(Enemy):
    SPRITES = [
        get_image_from_sheet(SPRITE_SHEET_ENEMIES, 120, 184, 16, 16, 2),  # LOT W LEWO [1]
        get_image_from_sheet(SPRITE_SHEET_ENEMIES, 150, 184, 16, 16, 2),  # LOT W LEWO [2]
        get_image_from_sheet(SPRITE_SHEET_ENEMIES, 180, 184, 16, 16, 2),  # LOT W PRAWO [1]
        get_image_from_sheet(SPRITE_SHEET_ENEMIES, 210, 184, 16, 16, 2)  # LOT W PRAWO [2]
    ]

    def __init__(self, x, y, width=32, height=32, speed=2, patrol_width=200):
        super().__init__(x, y, width, height, speed)
        self.start_x = x
        self.start_y = y
        self.patrol_width = patrol_width
        self.current_side = 0
        self.original_speed = abs(speed)
        self.animation_count = 0
        self.sprite_index = 0
        self.sprite = self.SPRITES[0]
        self.alive = True
        self.to_remove = False
        self.death_timer = 0
        self.death_duration = 30
        self.float_timer = 0
        self.rect = self.sprite.get_rect(topleft=(x, y))


    def update(self, player, objects):
        if not self.alive:
            self.sprite = self.SPRITES[2]
            self.death_timer += 1
            if self.death_timer >= self.death_duration:
                self.to_remove = True
            return

        self.fly_left_right()

        self.float_timer += 0.1
        self.rect.y = self.start_y + int(math.sin(self.float_timer) * 5)

        self.animation_count += 1
        if self.animation_count >= 10:
            self.animation_count = 0

            if self.speed < 0:
                self.sprite_index = 0 if self.sprite_index != 0 else 1
            else:
                self.sprite_index = 2 if self.sprite_index != 2 else 3

        self.sprite = self.SPRITES[self.sprite_index]

        self.move_and_collide(objects)

        # KOLIZJA Z GRACZEM
        if self.rect.colliderect(player.rect):
            if player.invincible:
                return

            if player.rect.bottom <= self.rect.top + 20 and player.y_vel > 0:
                self.alive = False
                player.score += 3
                player.y_vel = -15
                player.jump = True

            elif player.size == "big":
                player.to_small()
                player.invincible = True
                player.invincibility_timer = pygame.time.get_ticks()

            else:
                HIT_SOUND.play()
                player.lives -= 1
                player.invincible = True
                player.invincibility_timer = pygame.time.get_ticks()
                if player.lives <= 0:
                    DEATH_SOUND.play()
                    global enemies
                    player.reset()
                else:
                    player.rect.x -= 50
                    player.y_vel = -10


    def fly_left_right(self):
        self.rect.x += self.speed

        if self.rect.x <= self.start_x - self.patrol_width // 2:
            self.rect.x = self.start_x - self.patrol_width // 2
            self.speed *= -1

        elif self.rect.x + self.rect.width >= self.start_x + self.patrol_width // 2:
            self.rect.x = self.start_x + self.patrol_width // 2 - self.rect.width
            self.speed *= -1

    def draw(self, scroll_x):
        if self.alive:
            adjusted = self.rect.copy()
            adjusted.x -= scroll_x
            WINDOW.blit(self.sprite, (adjusted.x, adjusted.y))

class PowerUp(Enemy):
    SPRITES = [
        get_image_from_sheet(SPRITE_SHEET_OBJECTS, 0, 16, 16, 15, 2),  # CAŁY
        get_image_from_sheet(SPRITE_SHEET_OBJECTS, 0, 16, 16, 4, 2),   # 1/4
        get_image_from_sheet(SPRITE_SHEET_OBJECTS, 0, 16, 16, 8, 2),   # 2/4
        get_image_from_sheet(SPRITE_SHEET_OBJECTS, 0, 16, 16, 12, 2)   # 3/4
    ]

    EMERGE_DISTANCE = 16
    EMERGE_SPEED = 1

    def __init__(self, x, y, width=32, height=32):
        super().__init__(x, y + height, width, height)  # startuje "pod" blokiem
        self.alive = True
        self.to_remove = False
        self.x_vel = 0
        self.emerging = True
        self.emerged_distance = 0
        self.y_vel = 0

    def emerge(self):
        if self.emerged_distance < self.EMERGE_DISTANCE:
            self.rect.y -= self.EMERGE_SPEED
            self.emerged_distance += self.EMERGE_SPEED
        else:
            self.emerging = False
            self.x_vel = -2

    def apply_gravity(self):
        if not self.emerging:
            self.y_vel += self.GRAVITY
            if self.y_vel > 10:
                self.y_vel = 10
            self.rect.y += self.y_vel
            if self.rect.y > HEIGHT + 50:
                self.to_remove = True
                self.alive = False

    def move(self, objects):
        self.rect.x += self.x_vel
        for obj in objects:
            if self.rect.colliderect(obj.rect):
                if self.x_vel > 0:
                    self.rect.right = obj.rect.left
                elif self.x_vel < 0:
                    self.rect.left = obj.rect.right
                self.x_vel *= -1

    def update(self, player, objects):
        if not self.alive:
            return

        if self.emerging:
            self.emerge()
            return

        for obj in objects:
            if self.rect.colliderect(obj.rect):
                if self.y_vel > 0:
                    self.rect.bottom = obj.rect.top
                    self.y_vel = 0

        if self.rect.colliderect(player.rect):
            POWERUP_SOUND.play()
            player.to_big()
            player.score += 100
            self.alive = False
            self.to_remove = True

        self.move(objects)
        self.apply_gravity()

    def draw(self, scroll_x):
        if not self.alive:
            return

        adjusted = self.rect.copy()
        adjusted.x -= scroll_x

        if self.emerging:
            stage = min(len(self.SPRITES) - 1, self.emerged_distance // (self.EMERGE_DISTANCE // (len(self.SPRITES))))
            sprite = self.SPRITES[stage]
        else:
            sprite = get_image_from_sheet(SPRITE_SHEET_OBJECTS, 0, 16, 16, 16, 2)

        WINDOW.blit(sprite, adjusted)