import pygame
from constants import WINDOW, SPRITE_SHEET_TILE_SET, COIN_SOUND, POWERUP_APPEARS_SOUND
from utils import get_image_from_sheet
from enemies import PowerUp
from coin import Coin


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color="green", visible=False):
        super().__init__()
        self.rect = pygame.Rect(x, y - height, width, height)
        self.color = color
        self.visible = visible

    def draw(self, scroll_x):
        if not self.visible:
            return

        adjusted_rect = self.rect.copy()
        adjusted_rect.x -= scroll_x
        pygame.draw.rect(WINDOW, self.color, adjusted_rect)


class PowerUpBlock(Object):
    SPRITES = [
        get_image_from_sheet(SPRITE_SHEET_TILE_SET, 384, 0, 16, 16, 2),  # JASNY
        get_image_from_sheet(SPRITE_SHEET_TILE_SET, 400, 0, 16, 16, 2),  # CIEMNIEJSZY
        get_image_from_sheet(SPRITE_SHEET_TILE_SET, 416, 0, 16, 16, 2),  # CIEMNY
        get_image_from_sheet(SPRITE_SHEET_TILE_SET, 432, 0, 16, 16, 2),  # ZUŻYTY
    ]

    def __init__(self, x, y, width, height, color="green", visible=False, num_of_power_up=1):
        super().__init__(x, y - height, width, height, color, visible)
        self.num_of_power_up = num_of_power_up
        self.initial_num_of_power_up = num_of_power_up

        # Animacja
        self.animation_index = 0
        self.animation_timer = 0
        self.animation_speed = 18  # im mniejsza liczba, tym szybciej się animuje

    def spawn_power_up(self, enemies):
        if self.num_of_power_up > 0:
            POWERUP_APPEARS_SOUND.play()
            enemies.append(PowerUp(self.rect.x, self.rect.y - self.rect.height))
            self.num_of_power_up -= 1

    def reset(self):
        self.num_of_power_up = self.initial_num_of_power_up
        self.animation_index = 0
        self.animation_timer = 0

    def update_animation(self):
        if self.num_of_power_up > 0:
            self.animation_timer += 1
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.animation_index = (self.animation_index + 1) % 3  # tylko 3 klatki animacji

    def draw(self, scroll_x):
        if not self.visible:
            return

        self.update_animation()

        adjusted_rect = self.rect.copy()
        adjusted_rect.x -= scroll_x

        if self.num_of_power_up > 0:
            sprite = self.SPRITES[self.animation_index]
        else:
            sprite = self.SPRITES[3]  # zużyty blok

        WINDOW.blit(sprite, adjusted_rect)


class CoinBlock(Object):
    SPRITES = [
        get_image_from_sheet(SPRITE_SHEET_TILE_SET, 384, 0, 16, 16, 2),  # JASNY
        get_image_from_sheet(SPRITE_SHEET_TILE_SET, 400, 0, 16, 16, 2),  # CIEMNIEJSZY
        get_image_from_sheet(SPRITE_SHEET_TILE_SET, 416, 0, 16, 16, 2),  # CIEMNY
        get_image_from_sheet(SPRITE_SHEET_TILE_SET, 432, 0, 16, 16, 2),  # ZUŻYTY
    ]

    def __init__(self, x, y, width, height, color="yellow", visible=False, num_of_coins=1):
        super().__init__(x, y - height, width, height, color, visible)
        self.num_of_coins = num_of_coins
        self.initial_num_of_coins = num_of_coins
        self.coins = []

        # Animacja
        self.animation_index = 0
        self.animation_timer = 0
        self.animation_speed = 18

    def spawn_coin(self, player, coins):
        if self.num_of_coins > 0:
            COIN_SOUND.play()
            coins.append(Coin(self.rect.centerx, self.rect.y))
            player.score += 50
            self.num_of_coins -= 1

    def reset(self):
        self.num_of_coins = self.initial_num_of_coins
        self.animation_index = 0
        self.animation_timer = 0

    def update_animation(self):
        if self.num_of_coins > 0:
            self.animation_timer += 1
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.animation_index = (self.animation_index + 1) % 3

    def draw(self, scroll_x):
        if not self.visible:
            return

        self.update_animation()

        adjusted_rect = self.rect.copy()
        adjusted_rect.x -= scroll_x

        if self.num_of_coins > 0:
            sprite = self.SPRITES[self.animation_index]
        else:
            sprite = self.SPRITES[3]

        WINDOW.blit(sprite, adjusted_rect)


class Bricks(Object):
    def __init__(self, x, y, width, height, color="green", visible=False):
        super().__init__(x, y - height, width, height, color, visible)

    def draw(self, scroll_x):
        if not self.visible:
            return

        adjusted_rect = self.rect.copy()
        adjusted_rect.x -= scroll_x
        platform_obj = get_image_from_sheet(SPRITE_SHEET_TILE_SET, 16, 0, 16, 16, 2)
        platform_obj_surf = platform_obj.get_rect(topleft=(adjusted_rect.x, adjusted_rect.y))
        WINDOW.blit(platform_obj, platform_obj_surf)


class Object_storage(Object):
    def __init__(self, list_of_objects=[]):
        self.list_of_objects = list_of_objects

    def add_object(self, obj):
        self.list_of_objects.append(obj)

    def add_obj_list(self, obj_list):
        self.list_of_objects += obj_list

    def get_obj_list(self):
        return self.list_of_objects