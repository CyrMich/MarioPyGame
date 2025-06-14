from enemies import Goomba, Boo
from player import Player
from constants import DIFFICULTY_SETTINGS, FLOOR_LEVEL, CURRENT_DIFFICULTY
import constants
import pygame

def restart_game():
    pygame.mixer.music.load("resources\\music\\main_theme.ogg")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)
    constants.START_TIME = pygame.time.get_ticks()
    lives = DIFFICULTY_SETTINGS[constants.CURRENT_DIFFICULTY]["player_lives"]
    player = Player(100, FLOOR_LEVEL, 50, 50, lives)
    player.score=0
    speed_mult = DIFFICULTY_SETTINGS[constants.CURRENT_DIFFICULTY]["enemy_speed_multiplier"]
    enemies = [
        Goomba(700, FLOOR_LEVEL + 12, 45, 45, int(3 * speed_mult) + 1, 750),
        Goomba(1000, FLOOR_LEVEL + 12, 45, 45, int(3 * speed_mult), 450),
        Goomba(1750, FLOOR_LEVEL + 12, 45, 45, int(3 * speed_mult), 400),
        Boo(2600, FLOOR_LEVEL - 60, 45, 45, int(3 * speed_mult), 450),
        Boo(3500, FLOOR_LEVEL - 75, 45, 45, int(3 * speed_mult), 800),
        Goomba(3870, FLOOR_LEVEL + 12, 45, 45, int(3 * speed_mult) + 1, 360),
        Goomba(4200, FLOOR_LEVEL + 12, 45, 45, int(3 * speed_mult), 360),
        Boo(5700, FLOOR_LEVEL - 50, 45, 45, int(3 * speed_mult), 500)
    ]
    return player, enemies