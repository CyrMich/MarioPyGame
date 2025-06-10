import pygame

# INICJALIZACJA CZCIONKI I PYGAME
pygame.init()
pygame.font.init()
pygame.mixer.init()

FONT = pygame.font.SysFont("Arial",30)


# WYMIARY OKNA
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mario")

# TŁO
BACKGROUND = pygame.transform.scale(pygame.image.load("D:\\projektPython\\MarioPyGame\\resources\\graphics\\level_1.png"),(7000,600))

# MUZYKA
pygame.mixer.music.load("D:\\projektPython\\MarioPyGame\\resources\\music\\main_theme.ogg")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

# KOD DO ODTWARZANIA DZWIEKOW | DO USUNIECIA PRZED ODDANIEM
# pygame.mixer.music.load("resources\\sound\\stomp.ogg")
# pygame.mixer.music.play(1)
# pygame.mixer.music.set_volume(0.5)

WORLD_CLEAR = pygame.mixer.Sound("D:\\projektPython\\MarioPyGame\\resources\\music\\world_clear.wav")
WORLD_CLEAR.set_volume(0.5)

OUT_OF_TIME_SOUND = pygame.mixer.Sound("D:\\projektPython\\MarioPyGame\\resources\\music\\out_of_time.wav")
OUT_OF_TIME_SOUND.set_volume(0.5)

SMALL_JUMP_SOUND = pygame.mixer.Sound("D:\\projektPython\\MarioPyGame\\resources\\sound\\small_jump.ogg")
SMALL_JUMP_SOUND.set_volume(0.5)

BIG_JUMP_SOUND = pygame.mixer.Sound("D:\\projektPython\\MarioPyGame\\resources\\sound\\big_jump.ogg")
BIG_JUMP_SOUND.set_volume(0.5)

PIPE_SOUND = pygame.mixer.Sound("D:\\projektPython\\MarioPyGame\\resources\\sound\\pipe.ogg")
PIPE_SOUND.set_volume(0.5)

HIT_SOUND = pygame.mixer.Sound("D:\\projektPython\\MarioPyGame\\resources\\sound\\stomp.ogg")
HIT_SOUND.set_volume(0.5)

GAME_OVER_SOUND = pygame.mixer.Sound("D:\\projektPython\\MarioPyGame\\resources\\music\\game_over.ogg")
GAME_OVER_SOUND.set_volume(0.5)

DEATH_SOUND = pygame.mixer.Sound("D:\\projektPython\\MarioPyGame\\resources\\music\\death.wav")
DEATH_SOUND.set_volume(0.5)

COIN_SOUND = pygame.mixer.Sound("D:\\projektPython\\MarioPyGame\\resources\\sound\\coin.ogg")
COIN_SOUND.set_volume(0.5)

POWERUP_SOUND = pygame.mixer.Sound("D:\\projektPython\\MarioPyGame\\resources\\sound\\powerup.ogg")
POWERUP_SOUND.set_volume(0.5)

POWERUP_APPEARS_SOUND = pygame.mixer.Sound("D:\\projektPython\\MarioPyGame\\resources\\sound\\powerup_appears.ogg")
POWERUP_APPEARS_SOUND.set_volume(0.5)

SPRITE_SHEET_MARIO = pygame.image.load("D:\\projektPython\\MarioPyGame\\resources\\graphics\\mario_bros.png").convert_alpha()
SPRITE_SHEET_ENEMIES = pygame.image.load("D:\\projektPython\\MarioPyGame\\resources\\graphics\\smb_enemies_sheet.png").convert_alpha()
SPRITE_SHEET_OBJECTS = pygame.image.load("D:\\projektPython\\MarioPyGame\\resources\\graphics\\item_objects.png").convert_alpha()
SPRITE_SHEET_TILE_SET = pygame.image.load("D:\\projektPython\\MarioPyGame\\resources\\graphics\\tile_set.png").convert_alpha()

FLOOR_LEVEL = 536

FPS = 60

PLAYER_VEL = 5  # DOCELOWO 5 DLA TESTOW JEST WIECEJ

GAME_ACTIVE = False  # Zmienione na False - gra zaczyna się od menu
GAME_PAUSED = False
GAME_FINISHED = False
GAME_STARTED = False  # Nowa zmienna do śledzenia czy gra została rozpoczęta
FINAL_SCORE = 0
TIME_BONUS = 0
START_TIME = 0
TIME = 100

# Poziomy trudności
DIFFICULTY_SETTINGS = {
    "ŁATWY": {
        "player_lives": 5,
        "enemy_speed_multiplier": 0.7,
        "score_multiplier":0.8
    },
    "ŚREDNI": {
        "player_lives": 3,
        "enemy_speed_multiplier": 1.0,
        "score_multiplier":1.2
    },
    "TRUDNY": {
        "player_lives": 1,
        "enemy_speed_multiplier": 1.5,
        "score_multiplier":1.85
    }
}

CURRENT_DIFFICULTY = "ŚREDNI"

global enemies
player=None
enemies=[]
objects=[]
coins = []
