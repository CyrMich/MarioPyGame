import pygame

def get_image_from_sheet(sprite_sheet, x, y, width, height, scale=1):
    image = pygame.Surface((width, height), pygame.SRCALPHA)
    image.blit(sprite_sheet, (0, 0), pygame.Rect(x, y, width, height))
    if scale != 1:
        image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
    return image