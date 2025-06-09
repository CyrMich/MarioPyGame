from utils import get_image_from_sheet
from constants import SPRITE_SHEET_TILE_SET, WINDOW

class Coin:
    GRAVITY = 0.5
    LIFETIME = 20

    def __init__(self, x, y):
        self.image = get_image_from_sheet(SPRITE_SHEET_TILE_SET, 386, 18, 10, 13, 2)
        self.rect = self.image.get_rect(center=(x, y))
        self.y_vel = -3
        self.timer = 0
        self.alive = True

    def update(self):
        self.timer += 1
        if self.timer >= self.LIFETIME:
            self.alive = False

        self.rect.y += self.y_vel

    def draw(self, scroll_x):
        adjusted = self.rect.copy()
        adjusted.x -= scroll_x
        WINDOW.blit(self.image, adjusted)