from objects import PowerUpBlock, CoinBlock

def reset_powerups(objects):
    for obj in objects:
        if isinstance(obj, PowerUpBlock):
            obj.reset()
        if isinstance(obj, CoinBlock):
            obj.reset()