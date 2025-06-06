import pygame

# INICJALIZACJA CZCIONKI I PYGAME
pygame.init()
pygame.font.init()

# WYMIARY OKNA
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mario")

# TŁO
BACKGROUND = pygame.transform.scale(pygame.image.load("resources\\graphics\\level_1.png"),(7000,600))


FLOOR_LEVEL = 536

FPS = 60
PLAYER_VEL = 10  # DOCELOWO 5 DLA TESTOW JEST WIECEJ
GAME_ACTIVE = True

class Player(pygame.sprite.Sprite):
    GRAVITY = 1.5  # DO USTALENIA

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y-height, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.direction = "left"
        self.jump = False

    def do_jump(self):
        if not self.jump:
            self.y_vel = -self.GRAVITY * 14
            self.jump = True

    def landed(self):
        self.y_vel = 0
        self.jump = False

    def move_left(self, vel):
        self.x_vel = -vel

    def move_right(self, vel):
        self.x_vel = vel

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    # PĘTLA GRACZA
    def loop(self):
        self.y_vel += self.GRAVITY  # GRAWITACJA, DO ZMIANY JESZCZE
        self.move(self.x_vel, self.y_vel)

    def draw(self, scroll_x):
        adjusted_rect = self.rect.copy()
        adjusted_rect.x -= scroll_x
        pygame.draw.rect(WINDOW, "red", adjusted_rect)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, walk_range, width, height, speed, life):
        super().__init__()
        self.rect = pygame.Rect(x, y - height, width, height)
        self.life = life
        self.walk_range = walk_range
        self.speed = speed
        self.x_pos = x  
        self.side = True  

    def move(self):
        if self.side:
            if self.rect.x < self.x_pos + self.walk_range:
                self.rect.x += self.speed
            else:
                self.side = False
        else:
            if self.rect.x > self.x_pos - self.walk_range:
                self.rect.x -= self.speed
            else:
                self.side = True

    def loop(self):
        self.move()

    def draw(self, scroll_x):
        adjusted_rect = self.rect.copy()
        adjusted_rect.x -= scroll_x
        pygame.draw.rect(WINDOW, "orange", adjusted_rect)

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color="green", visible=True):
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

def handle_horizontal_collision(player, objects):
    for obj in objects:
        if player.rect.colliderect(obj.rect):
            if player.x_vel > 0:  # w prawo
                player.rect.right = obj.rect.left
            elif player.x_vel < 0:  # w lewo
                player.rect.left = obj.rect.right

def handle_vertical_collision(player, objects):
    for obj in objects:
        if player.rect.colliderect(obj.rect):
            if player.y_vel > 0:  # Spada
                player.rect.bottom = obj.rect.top
                player.landed()
            elif player.y_vel < 0:  # Wznosi się
                player.rect.top = obj.rect.bottom
                player.y_vel = 0

# FUNKCJA OBSLUGUJACA RUCH GRACZA
def handle_move(player):
    keys = pygame.key.get_pressed()

    player.x_vel = 0

    if keys[pygame.K_a] and player.rect.x > 0:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_d] and player.rect.x + player.rect.width < 7000:
        player.move_right(PLAYER_VEL)

# FUNKCJA RYSUJACA NA EKRANIE
def draw(player, objects, enemies):
    scroll_x = player.rect.x - WIDTH // 2
    scroll_x = max(0, min(scroll_x, BACKGROUND.get_width() - WIDTH))

    WINDOW.blit(BACKGROUND, (-scroll_x, 0))

    for obj in objects:
        obj.draw(scroll_x)

    for enemy in enemies:
        enemy.draw(scroll_x)

    player.draw(scroll_x)

    pygame.display.update()

def load_sprite_sheets(dir):
    pass  

def main():
    run = True
    clock = pygame.time.Clock()

    player = Player(400, FLOOR_LEVEL, 50, 50)
    enemies = [
        Enemy(800, FLOOR_LEVEL, 100, 50, 50, 5, 1),
        Enemy(1500, FLOOR_LEVEL, 150, 40, 50, 1, 1)
    ]

    floor1 = Object(0, FLOOR_LEVEL, 2279, 5)
    floor2 = Object(2345, FLOOR_LEVEL, 495, 5)
    floor3 = Object(2939, FLOOR_LEVEL, 2113, 5)
    floor4 = Object(5118, FLOOR_LEVEL, 1900, 5)

    pipe1 = Object(926, FLOOR_LEVEL, 64, 86, "green",False) 
    pipe2 = Object(1256, FLOOR_LEVEL, 64, 128, "green",False) 
    pipe3 = Object(1520, FLOOR_LEVEL, 64, 172, "green",False)
    pipe4 = Object(1884, FLOOR_LEVEL, 64, 172, "green",False)
    pipe5 = Object(5384, FLOOR_LEVEL, 64, 86, "green",False) 
    pipe6 = Object(5912, FLOOR_LEVEL, 64, 86, "green",False) 
    
    stairs1 = Object(4424, FLOOR_LEVEL, 32, 43, "brown",False)
    stairs2 = Object(4458, FLOOR_LEVEL, 33, 86, "brown",False)
    stairs3 = Object(4491, FLOOR_LEVEL, 33, 129, "brown",False)
    stairs4 = Object(4524, FLOOR_LEVEL, 33, 172, "brown",False)

    stairs5 = Object(4623, FLOOR_LEVEL, 33, 172, "brown",False)
    stairs6 = Object(4656, FLOOR_LEVEL, 33, 129, "brown",False)
    stairs7 = Object(4689, FLOOR_LEVEL, 33, 86, "brown",False)
    stairs8 = Object(4722, FLOOR_LEVEL, 33, 43, "brown",False)
    
    stairs9 = Object(4886, FLOOR_LEVEL, 33, 43, "brown",False)
    stairs10 = Object(4919, FLOOR_LEVEL, 33, 86, "brown",False)
    stairs11 = Object(4952, FLOOR_LEVEL, 33, 129, "brown",False)
    stairs12 = Object(4985, FLOOR_LEVEL, 33, 172, "brown",False)
    stairs13 = Object(5018, FLOOR_LEVEL, 33, 172, "brown",False)

    stairs14 = Object(5118, FLOOR_LEVEL, 33, 172, "brown",False)   
    stairs15 = Object(5151, FLOOR_LEVEL, 33, 129, "brown",False)   
    stairs16 = Object(5184, FLOOR_LEVEL, 33, 86, "brown",False)   
    stairs17 = Object(5217, FLOOR_LEVEL, 33, 43, "brown",False)

    stairs18 = Object(5977, FLOOR_LEVEL, 33, 43, "brown",False)
    stairs19 = Object(6010, FLOOR_LEVEL, 33, 86, "brown",False)
    stairs20 = Object(6043, FLOOR_LEVEL, 33, 129, "brown",False)
    stairs21 = Object(6076, FLOOR_LEVEL, 33, 172, "brown",False)
    stairs22 = Object(6109, FLOOR_LEVEL, 33, 215, "brown",False)
    stairs23 = Object(6142, FLOOR_LEVEL, 33, 258, "brown",False)
    stairs24 = Object(6175, FLOOR_LEVEL, 33, 301, "brown",False)
    stairs25 = Object(6208, FLOOR_LEVEL, 33, 344, "brown",False)
    stairs26 = Object(6241, FLOOR_LEVEL, 33, 344, "brown",False)

    
    stairs27 = Object(6538, FLOOR_LEVEL, 33, 43, "brown",False)
    
    objects = [floor1, floor2, floor3, floor4,  pipe1,  pipe2,pipe3,pipe4,pipe5,pipe6,stairs1,stairs2,stairs3,stairs4,stairs5,stairs6,stairs7,stairs8,stairs9,stairs10,stairs11,stairs12,stairs13,stairs14,stairs15,stairs16,stairs17,stairs18,stairs19,stairs20,stairs21,stairs22,stairs23,stairs24,stairs25,stairs26,stairs27] 


    # GŁÓWNA PĘTLA GRY
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_w or event.key == pygame.K_SPACE) and not player.jump:
                    player.do_jump()

        handle_move(player)  
        
        player.rect.x += player.x_vel
        handle_horizontal_collision(player, objects)
        
        player.y_vel += player.GRAVITY  # grawitacja
        player.rect.y += player.y_vel
        handle_vertical_collision(player, objects)

        # Sprawdza czy gracz nie spadł za daleko
        if player.rect.y > HEIGHT:
            player.rect.x = 400
            player.rect.y = 300
            player.y_vel = 0
            player.jump = False

        for enemy in enemies:
            enemy.loop()

        draw(player, objects, enemies)

    pygame.quit()
    quit()

if __name__ == "__main__":
    main()