from objects import PowerUpBlock, CoinBlock

def handle_horizontal_collision(player, objects):
    for obj in objects:
        if player.rect.colliderect(obj.rect):
            if player.x_vel > 0:
                player.rect.right = obj.rect.left
            elif player.x_vel < 0:
                player.rect.left = obj.rect.right


def handle_vertical_collision(player, objects, enemies, coins):
    for obj in objects:
        if player.rect.colliderect(obj.rect):
            if player.y_vel > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif player.y_vel < 0:
                player.rect.top = obj.rect.bottom
                player.y_vel = 0
                if isinstance(obj, PowerUpBlock):
                    obj.spawn_power_up(enemies)
                if isinstance(obj, CoinBlock):
                    obj.spawn_coin(player,coins)
