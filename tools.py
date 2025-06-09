import pygame
from objects import PowerUpBlock, CoinBlock, Object, Object_storage, Bricks
from constants import PLAYER_VEL, FLOOR_LEVEL


def handle_move(player):
    keys = pygame.key.get_pressed()
    player.x_vel = 0

    if keys[pygame.K_a] and player.rect.x > 0:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_d] and player.rect.x + player.rect.width < 7000:
        player.move_right(PLAYER_VEL)


def initialize_level():
    obj_storage = Object_storage()
    obj_storage.add_object(Object(0, FLOOR_LEVEL + 5, 2279, 5))
    obj_storage.add_object(Object(2345, FLOOR_LEVEL + 5, 495, 5))
    obj_storage.add_object(Object(2939, FLOOR_LEVEL + 5, 2113, 5))
    obj_storage.add_object(Object(5118, FLOOR_LEVEL + 5, 1900, 5))
    obj_storage.add_object(Object(926, FLOOR_LEVEL, 64, 86, "green"))
    obj_storage.add_object(Object(1256, FLOOR_LEVEL, 64, 128, "green"))
    obj_storage.add_object(Object(1520, FLOOR_LEVEL, 64, 172, "green"))
    obj_storage.add_object(Object(1884, FLOOR_LEVEL, 64, 172, "green"))
    obj_storage.add_object(Object(5384, FLOOR_LEVEL, 64, 86, "green"))
    obj_storage.add_object(Object(5912, FLOOR_LEVEL, 64, 86, "green"))
    obj_storage.add_object(Object(4424, FLOOR_LEVEL, 32, 43, "brown"))
    obj_storage.add_object(Object(4458, FLOOR_LEVEL, 33, 86, "brown"))
    obj_storage.add_object(Object(4491, FLOOR_LEVEL, 33, 129, "brown"))
    obj_storage.add_object(Object(4524, FLOOR_LEVEL, 33, 172, "brown"))
    obj_storage.add_object(Object(4623, FLOOR_LEVEL, 33, 172, "brown"))
    obj_storage.add_object(Object(4656, FLOOR_LEVEL, 33, 129, "brown"))
    obj_storage.add_object(Object(4689, FLOOR_LEVEL, 33, 86, "brown"))
    obj_storage.add_object(Object(4722, FLOOR_LEVEL, 33, 43, "brown"))
    obj_storage.add_object(Object(4886, FLOOR_LEVEL, 33, 43, "brown"))
    obj_storage.add_object(Object(4919, FLOOR_LEVEL, 33, 86, "brown"))
    obj_storage.add_object(Object(4952, FLOOR_LEVEL, 33, 129, "brown"))
    obj_storage.add_object(Object(4985, FLOOR_LEVEL, 33, 172, "brown"))
    obj_storage.add_object(Object(5018, FLOOR_LEVEL, 33, 172, "brown"))
    obj_storage.add_object(Object(5118, FLOOR_LEVEL, 33, 172, "brown"))
    obj_storage.add_object(Object(5151, FLOOR_LEVEL, 33, 129, "brown"))
    obj_storage.add_object(Object(5184, FLOOR_LEVEL, 33, 86, "brown"))
    obj_storage.add_object(Object(5217, FLOOR_LEVEL, 33, 43, "brown"))
    obj_storage.add_object(Object(5977, FLOOR_LEVEL, 33, 43, "brown"))
    obj_storage.add_object(Object(6010, FLOOR_LEVEL, 33, 86, "brown"))
    obj_storage.add_object(Object(6043, FLOOR_LEVEL, 33, 129, "brown"))
    obj_storage.add_object(Object(6076, FLOOR_LEVEL, 33, 172, "brown"))
    obj_storage.add_object(Object(6109, FLOOR_LEVEL, 33, 215, "brown"))
    obj_storage.add_object(Object(6142, FLOOR_LEVEL, 33, 258, "brown"))
    obj_storage.add_object(Object(6175, FLOOR_LEVEL, 33, 301, "brown"))
    obj_storage.add_object(Object(6208, FLOOR_LEVEL, 33, 344, "brown"))
    obj_storage.add_object(Object(6241, FLOOR_LEVEL, 33, 344, "brown"))
    obj_storage.add_object(Object(6538, FLOOR_LEVEL, 33, 43, "brown"))

    obj_storage.add_object(CoinBlock(400, FLOOR_LEVEL - 100, 32, 32, "orange", True))
    obj_storage.add_object(Bricks(500, FLOOR_LEVEL - 100, 32, 32, "orange", True))
    obj_storage.add_object(PowerUpBlock(532, FLOOR_LEVEL - 100, 32, 32, "orange", True))
    obj_storage.add_object(Bricks(564, FLOOR_LEVEL - 100, 32, 32, "orange", True))
    obj_storage.add_object(CoinBlock(596, FLOOR_LEVEL - 100, 32, 32, "orange", True))
    obj_storage.add_object(Bricks(628, FLOOR_LEVEL - 100, 32, 32, "orange", True))
    obj_storage.add_object(CoinBlock(564, FLOOR_LEVEL - 250, 32, 32, "orange", True))

    obj_storage.add_object(CoinBlock(1720, FLOOR_LEVEL - 125, 32, 32, "orange", True))

    obj_storage.add_object(Bricks(2632, FLOOR_LEVEL - 100, 32, 32, "orange", True))
    obj_storage.add_object(CoinBlock(2664, FLOOR_LEVEL - 100, 32, 32, "orange", True))
    obj_storage.add_object(Bricks(2696, FLOOR_LEVEL - 100, 32, 32, "orange", True))

    obj_storage.add_object(Bricks(2728, FLOOR_LEVEL - 250, 32, 32, "orange", True))
    obj_storage.add_object(Bricks(2760, FLOOR_LEVEL - 250, 32, 32, "orange", True))
    obj_storage.add_object(Bricks(2792, FLOOR_LEVEL - 250, 32, 32, "orange", True))
    obj_storage.add_object(Bricks(2824, FLOOR_LEVEL - 250, 32, 32, "orange", True))

    obj_storage.add_object(Bricks(2920, FLOOR_LEVEL - 250, 32, 32, "orange", True))
    obj_storage.add_object(Bricks(2952, FLOOR_LEVEL - 250, 32, 32, "orange", True))
    obj_storage.add_object(Bricks(2984, FLOOR_LEVEL - 250, 32, 32, "orange", True))
    obj_storage.add_object(CoinBlock(3016, FLOOR_LEVEL - 250, 32, 32, "orange", True))
    obj_storage.add_object(Bricks(3016, FLOOR_LEVEL - 100, 32, 32, "orange", True))

    obj_storage.add_object(Bricks(3300, FLOOR_LEVEL - 100, 32, 32, "orange", True))
    obj_storage.add_object(Bricks(3332, FLOOR_LEVEL - 100, 32, 32, "orange", True))
    obj_storage.add_object(PowerUpBlock(3500, FLOOR_LEVEL - 100, 32, 32, "orange", True))

    obj_storage.add_object(CoinBlock(3900, FLOOR_LEVEL - 100, 32, 32, "orange", True))
    obj_storage.add_object(CoinBlock(4000, FLOOR_LEVEL - 100, 32, 32, "orange", True))
    obj_storage.add_object(CoinBlock(4000, FLOOR_LEVEL - 250, 32, 32, "orange", True))
    obj_storage.add_object(CoinBlock(4100, FLOOR_LEVEL - 100, 32, 32, "orange", True))

    obj_storage.add_object(CoinBlock(5600, FLOOR_LEVEL - 100, 32, 32, "orange", True))
    obj_storage.add_object(Bricks(5632, FLOOR_LEVEL - 100, 32, 32, "orange", True))
    obj_storage.add_object(CoinBlock(5664, FLOOR_LEVEL - 100, 32, 32, "orange", True))
    obj_storage.add_object(Bricks(5696, FLOOR_LEVEL - 100, 32, 32, "orange", True))
    obj_storage.add_object(CoinBlock(5728, FLOOR_LEVEL - 100, 32, 32, "orange", True))

    return obj_storage.get_obj_list()