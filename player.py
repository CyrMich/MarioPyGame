import pygame
from utils import get_image_from_sheet
from constants import SPRITE_SHEET_MARIO, SMALL_JUMP_SOUND, BIG_JUMP_SOUND, PIPE_SOUND, HEIGHT, WINDOW
import constants
class Player(pygame.sprite.Sprite):
    GRAVITY = 1.5

    SMALL_SPRITES = [
        get_image_from_sheet(SPRITE_SHEET_MARIO,178, 32, 12, 16, 2),  # MARIO STOI W MIEJSCU
        get_image_from_sheet(SPRITE_SHEET_MARIO,80,  32, 15, 16, 2),  # MARIO CHÓD [1]
        get_image_from_sheet(SPRITE_SHEET_MARIO,96,  32, 16, 16, 2),  # MARIO CHÓD [2]
        get_image_from_sheet(SPRITE_SHEET_MARIO,112, 32, 16, 16, 2),  # MARIO CHÓD [3]
        get_image_from_sheet(SPRITE_SHEET_MARIO,144, 32, 16, 16, 2),  # MARIO PODSKOK
        get_image_from_sheet(SPRITE_SHEET_MARIO,320, 8,  16, 24, 2)   # SMALL TO BIG
    ]

    BIG_SPRITES = [
        get_image_from_sheet(SPRITE_SHEET_MARIO,176,0,16,32,2), # MARIO STOI W MIEJSCU
        get_image_from_sheet(SPRITE_SHEET_MARIO,81, 0,16,32,2), # MARIO CHÓD [1]
        get_image_from_sheet(SPRITE_SHEET_MARIO,97, 0,15,32,2), # MARIO CHÓD [2]
        get_image_from_sheet(SPRITE_SHEET_MARIO,113,0,15,32,2), # MARIO CHÓD [3]
        get_image_from_sheet(SPRITE_SHEET_MARIO,144,0,16,32,2), # MARIO PODSKOK
        get_image_from_sheet(SPRITE_SHEET_MARIO,272,2,16,29,2)  # BIG TO SMALL
    ]


    def __init__(self, x, y, width, height, lives):
        super().__init__()
        self.rect = pygame.Rect(x, y-height, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.jump = False
        self.size = "small"
        self.sprites = self.SMALL_SPRITES
        self.direction = "right"
        self.animation_count = 0
        self.lives = lives
        self.max_lives = lives
        self.score = 0
        self.invincible = False
        self.invincible_timer = 0
        self.invincibility_duration = 2500

    def to_big(self):
        self.size = "big"
        self.sprite = self.SMALL_SPRITES[5]
        self.sprites = self.BIG_SPRITES

    def to_small(self):
        PIPE_SOUND.play()
        self.size = "small"
        self.sprite = self.BIG_SPRITES[5]
        self.sprites = self.SMALL_SPRITES

    def do_jump(self):
        if not self.jump:
            self.y_vel = -self.GRAVITY * 16
            self.jump = True

            if self.size == "small":
                SMALL_JUMP_SOUND.play()
            elif self.size == "big":
                BIG_JUMP_SOUND.play()

    def check_if_airborne(self, objects):
        rect_below = self.rect.move(0, 1)
        for obj in objects:
            if rect_below.colliderect(obj.rect):
                self.jump = False
                return
        self.jump = True

    def landed(self):
        self.y_vel = 0
        self.jump = False

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, objects):
        self.check_if_airborne(objects)

        if self.invincible:
            now = pygame.time.get_ticks()
            if now - self.invincibility_timer > self.invincibility_duration:
                self.invincible = False

        if self.rect.y > HEIGHT + 50:
            self.lives -= 1
            if self.lives <= 0:
                self.reset()
            else:
                self.rect.x = 100
                self.rect.y = 300
                self.y_vel = 0
                self.jump = False

        self.update_sprite()
        self.update()

        self.y_vel += self.GRAVITY
        self.rect.y += self.y_vel

    def reset(self):
        self.rect.x = 100
        self.rect.y = 300
        self.y_vel = 0
        self.jump = False
        self.lives = self.max_lives
        constants.START_TIME = pygame.time.get_ticks()
        self.score=0

    def update_sprite(self):
        # ANIMACJA SKOKU
        if self.y_vel != 0:
            self.sprite_index = 4

        # ANIMACJA BIEGU
        elif self.x_vel != 0:
            self.animation_counter += 1
            if self.animation_counter >= 6:
                self.animation_counter = 0
                self.sprite_index += 1
                if self.sprite_index > 3:
                    self.sprite_index = 1

        else:
            self.sprite_index = 0
            self.animation_counter = 0

        if self.direction == "right":
            self.sprite = self.sprites[self.sprite_index]
        elif self.direction == "left":
            self.sprite = pygame.transform.flip(self.sprites[self.sprite_index], True, False)

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x,self.rect.y))

    def draw(self, scroll_x):
        adjusted_rect = self.rect.copy()
        adjusted_rect.x -= scroll_x

        WINDOW.blit(self.sprite,(adjusted_rect.x,adjusted_rect.y))