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
# pygame.mixer.music.load("resources\\music\\main_theme.ogg")
# pygame.mixer.music.play(-1)
# pygame.mixer.music.set_volume(0.5)

FLOOR_LEVEL = 536

FPS = 60
PLAYER_VEL = 10  # DOCELOWO 5 DLA TESTOW JEST WIECEJ
GAME_ACTIVE = False  # Zmienione na False - gra zaczyna się od menu
GAME_PAUSED = False
GAME_FINISHED = False
GAME_STARTED = False  # Nowa zmienna do śledzenia czy gra została rozpoczęta
TIME=100

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

class Player(pygame.sprite.Sprite):
    GRAVITY = 1.5  # DO USTALENIA

    def __init__(self, x, y, width, height, lives):
        super().__init__()
        self.rect = pygame.Rect(x, y-height, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.direction = "left"
        self.jump = False
        self.lives = lives
        self.max_lives = lives  # Zapamiętaj maksymalną liczbę żyć
        self.score = 0

    def do_jump(self):
        if not self.jump:
            self.y_vel = -self.GRAVITY * 16 
            self.jump = True

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

    def move_right(self, vel):
        self.x_vel = vel

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def loop(self, objects):
        self.check_if_airborne(objects)

        if self.rect.y > HEIGHT + 50:
            self.lives -= 1
            if self.lives <= 0:
                self.reset()
                self.lives = self.max_lives
            else:
                self.rect.x = 400
                self.rect.y = 300
                self.y_vel = 0
                self.jump = False

        self.y_vel += self.GRAVITY 
        self.rect.y += self.y_vel

    def reset(self):
        self.rect.x = 400
        self.rect.y = 300
        self.y_vel = 0
        self.jump = False
        self.lives = self.max_lives
        self.score = 0

    def draw(self, scroll_x):
        adjusted_rect = self.rect.copy()
        adjusted_rect.x -= scroll_x
        pygame.draw.rect(WINDOW, "red", adjusted_rect)


class Enemy(pygame.sprite.Sprite):
    GRAVITY = 1

    def __init__(self, x, y, width, height, speed=2):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.base_speed = speed
        self.speed = speed * DIFFICULTY_SETTINGS[CURRENT_DIFFICULTY]["enemy_speed_multiplier"]
        self.y_vel = 0
        self.alive = True

    def apply_gravity(self):
        self.y_vel += self.GRAVITY
        if self.y_vel > 10:
            self.y_vel = 10

    def move_and_collide(self, objects):
        self.rect.x += self.speed
        for obj in objects:
            if self.rect.colliderect(obj.rect):
                if self.speed > 0:
                    self.rect.right = obj.rect.left
                else:
                    self.rect.left = obj.rect.right
                self.speed *= -1

        self.rect.y += self.y_vel
        for obj in objects:
            if self.rect.colliderect(obj.rect):
                if self.y_vel > 0:
                    self.rect.bottom = obj.rect.top
                    self.y_vel = 0
                elif self.y_vel < 0:
                    self.rect.top = obj.rect.bottom
                    self.y_vel = 0

    def update(self, player, objects):
        if not self.alive:
            return

        self.apply_gravity()
        self.move_and_collide(objects)

        if self.rect.colliderect(player.rect):
            if player.rect.bottom <= self.rect.top+20:
                self.alive = False
                player.y_vel = -15
                player.jump = True
            else:
                player.lives -= 1
                if player.lives <= 0:
                    player.reset()
                    player.lives = player.max_lives
                else:
                    player.rect.x -= 50
                    player.y_vel = -10

    def draw(self, scroll_x):
        if self.alive:
            adjusted = self.rect.copy()
            adjusted.x -= scroll_x
            pygame.draw.rect(WINDOW, "green", adjusted)

    def is_off_screen(self, scroll_x):
        return self.rect.right - scroll_x < 0


class Goomba(Enemy):
    def __init__(self, x, y, width=45, height=45, speed=2, walking_range=200):
        super().__init__(x, y-height, width, height, speed)
        self.original_speed = abs(self.speed)  # Użyj prędkości z trudnością
        self.walking_range = walking_range
        self.start_x = x
        self.left_boundary = x - walking_range // 2
        self.right_boundary = x + walking_range // 2
    
    def move_and_collide(self, objects):
        next_x = self.rect.x + self.speed
        
        if next_x <= self.left_boundary:
            self.rect.x = self.left_boundary
            self.speed = abs(self.speed)
        elif next_x + self.rect.width >= self.right_boundary:
            self.rect.x = self.right_boundary - self.rect.width
            self.speed = -abs(self.speed)
        else:
            self.rect.x = next_x

        for obj in objects:
            if self.rect.colliderect(obj.rect):
                if self.speed > 0:
                    self.rect.right = obj.rect.left
                else:
                    self.rect.left = obj.rect.right
                self.speed *= -1
    
    def update(self, player, objects):
        if not self.alive:
            return

        self.apply_gravity()
        self.move_and_collide(objects)

        if self.rect.colliderect(player.rect):
            if player.rect.bottom <= self.rect.top + 20:
                self.alive = False
                player.score += 2
                player.y_vel = -15
                player.jump = True
            else:
                player.lives -= 1
                if player.lives <= 0:
                    player.reset()
                    player.lives = player.max_lives
                else:
                    player.rect.x -= 50
                    player.y_vel = -10

    def draw(self, scroll_x):
        if self.alive:
            adjusted = self.rect.copy()
            adjusted.x -= scroll_x
            pygame.draw.rect(WINDOW, "brown", adjusted)


class Boo(Enemy):
    def __init__(self, x, y, width=45, height=45, speed=2, patrol_width=200, patrol_height=100):
        super().__init__(x, y, width, height, speed)
        self.start_x = x
        self.start_y = y
        self.patrol_width = patrol_width
        self.patrol_height = patrol_height
        self.current_side = 0
        self.original_speed = abs(self.speed)  # Użyj prędkości z trudnością
    
        self.corners = [
            (self.start_x + self.patrol_width, self.start_y), 
            (self.start_x + self.patrol_width, self.start_y + self.patrol_height),  
            (self.start_x, self.start_y + self.patrol_height),  
            (self.start_x, self.start_y)  
        ]
        
    def update(self, player, objects):
        if not self.alive:
            return

        self.fly_in_rectangle()

        if self.rect.colliderect(player.rect):
            if player.rect.bottom <= self.rect.top + 20:
                self.alive = False
                player.score += 3
                player.y_vel = -15
                player.jump = True
            else:
                player.lives -= 1
                if player.lives <= 0:
                    player.reset()
                    player.lives = player.max_lives
                else:
                    player.rect.x -= 50
                    player.y_vel = -10

    def fly_in_rectangle(self):
        target_corner = self.corners[self.current_side]
        
        dx = target_corner[0] - self.rect.centerx
        dy = target_corner[1] - self.rect.centery
        
        if abs(dx) < self.original_speed + 2 and abs(dy) < self.original_speed + 2:
            self.current_side = (self.current_side + 1) % 4
            self.rect.centerx = target_corner[0]
            self.rect.centery = target_corner[1]
        else:
            distance = max(abs(dx), abs(dy))
            if distance > 0:
                move_x = (dx / distance) * self.original_speed
                move_y = (dy / distance) * self.original_speed
                self.rect.x += int(move_x)
                self.rect.y += int(move_y)

    def draw(self, scroll_x):
        if self.alive:
            adjusted = self.rect.copy()
            adjusted.x -= scroll_x
            pygame.draw.rect(WINDOW, "white", adjusted)


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


class Object_storage(Object):
    def __init__(self, list_of_objects=[]):
        self.list_of_objects = list_of_objects
    
    def add_object(self, obj):
        self.list_of_objects.append(obj)
    
    def add_obj_list(self, obj_list):
        self.list_of_objects += obj_list
    
    def get_obj_list(self):
        return self.list_of_objects


def handle_horizontal_collision(player, objects):
    for obj in objects:
        if player.rect.colliderect(obj.rect):
            if player.x_vel > 0:
                player.rect.right = obj.rect.left
            elif player.x_vel < 0:
                player.rect.left = obj.rect.right


def handle_vertical_collision(player, objects):
    for obj in objects:
        if player.rect.colliderect(obj.rect):
            if player.y_vel > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif player.y_vel < 0:
                player.rect.top = obj.rect.bottom
                player.y_vel = 0


def handle_move(player):
    keys = pygame.key.get_pressed()
    player.x_vel = 0

    if keys[pygame.K_a] and player.rect.x > 0:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_d] and player.rect.x + player.rect.width < 7000:
        player.move_right(PLAYER_VEL)


def draw_main_menu(selected_option):
    WINDOW.fill((30, 30, 80))  
    
    title_text = FONT.render("MARIO GAME", True, "yellow")
    title_rect = title_text.get_rect(center=(WIDTH//2,30))
    WINDOW.blit(title_text, title_rect)

    mario_start=pygame.image.load("D:\\projektPython\\MarioPyGame\\resources\\graphics\\marioStart.png").convert_alpha()
    mario_rect=mario_start.get_rect(center=(WIDTH//2,140))
    WINDOW.blit(mario_start,mario_rect)

    menu_options = ["ŁATWY", "ŚREDNI", "TRUDNY", "WYJŚCIE"]
    option_colors = ["white"] * 4
    option_colors[selected_option] = "red"  
    
    descriptions = [
        "5 żyć, wolniejsi przeciwnicy",
        "3 życia, normalny poziom",
        "1 życie, szybsi przeciwnicy",
        "Zamknij grę"  
    ]
    
    start_y = HEIGHT//2 - 50
    for i, (option, desc) in enumerate(zip(menu_options, descriptions)):
        option_text = FONT.render(option, True, option_colors[i])
        option_rect = option_text.get_rect(center=(WIDTH//2, start_y + i * 70))
        WINDOW.blit(option_text, option_rect)

        if desc:
            desc_text = FONT.render(desc, True, "lightgray")
            desc_rect = desc_text.get_rect(center=(WIDTH//2, start_y + i * 70 + 25))
            WINDOW.blit(desc_text, desc_rect)

    instruction1 = FONT.render("↑↓ - Wybierz poziom", True, "white")
    instruction1_rect = instruction1.get_rect(center=(WIDTH//2, HEIGHT - 80))
    WINDOW.blit(instruction1, instruction1_rect)
    
    instruction2 = FONT.render("ENTER - Rozpocznij grę", True, "white")
    instruction2_rect = instruction2.get_rect(center=(WIDTH//2, HEIGHT - 50))
    WINDOW.blit(instruction2, instruction2_rect)
    
    pygame.display.update()


def draw_pause_screen():
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(128)
    overlay.fill((0, 0, 0))
    WINDOW.blit(overlay, (0, 0))
    
    pause_text = FONT.render("PAUZA", True, "white")
    pause_rect = pause_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
    WINDOW.blit(pause_text, pause_rect)
    
    instruction1 = FONT.render("ESC - Wznów grę", True, "white")
    instruction1_rect = instruction1.get_rect(center=(WIDTH//2, HEIGHT//2 + 20))
    WINDOW.blit(instruction1, instruction1_rect)
    
    instruction2 = FONT.render("R - Restart gry", True, "white")
    instruction2_rect = instruction2.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
    WINDOW.blit(instruction2, instruction2_rect)


def draw_end_screen(player, start_time, end_time):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(220)
    overlay.fill((0, 0, 0))
    WINDOW.blit(overlay, (0, 0))
    
    time_bonus = int(50-(end_time-start_time)/1000)
    final_score = int((player.score*5+player.lives * 10+time_bonus)*DIFFICULTY_SETTINGS[CURRENT_DIFFICULTY]["score_multiplier"])
    
    congrats_text = FONT.render("GRATULACJE!", True, "yellow")
    congrats_rect = congrats_text.get_rect(topleft=(50, HEIGHT//2 - 100))
    WINDOW.blit(congrats_text, congrats_rect)
    
    difficulty_text = FONT.render(f"Poziom: {CURRENT_DIFFICULTY}", True, "white")
    difficulty_rect = difficulty_text.get_rect(topleft=(50, HEIGHT//2 - 70))
    WINDOW.blit(difficulty_text, difficulty_rect)
    
    score_text = FONT.render(f"Punkty za przeciwników: {player.score*5}", True, "white")
    score_rect = score_text.get_rect(topleft=(50, HEIGHT//2 - 40))
    WINDOW.blit(score_text, score_rect)
    
    lives_text = FONT.render(f"Bonus za życia: {player.lives * 10}", True, "white")
    lives_rect = lives_text.get_rect(topleft=(50, HEIGHT//2 - 10))
    WINDOW.blit(lives_text, lives_rect)
    
    time_text = FONT.render(f"Bonus za czas: {time_bonus}", True, "white")
    time_rect = time_text.get_rect(topleft=(50, HEIGHT//2 + 20))
    WINDOW.blit(time_text, time_rect)
    
    final_text = FONT.render(f"Wynik: {final_score}", True, "gold")
    final_rect = final_text.get_rect(topleft=(50, HEIGHT//2 + 60))
    WINDOW.blit(final_text, final_rect)
    
    instruction1 = FONT.render("R - Restart gry", True, "white")
    instruction1_rect = instruction1.get_rect(topleft=(50, HEIGHT//2 + 100))
    WINDOW.blit(instruction1, instruction1_rect)
    
    instruction2 = FONT.render("M - Powrót do menu", True, "white")
    instruction2_rect = instruction2.get_rect(topleft=(50, HEIGHT//2 + 130))
    WINDOW.blit(instruction2, instruction2_rect)

    mario_end=pygame.image.load("D:\\projektPython\\MarioPyGame\\resources\\graphics\\marioEnd.png").convert_alpha()
    mario_rect=mario_end.get_rect(midbottom=(600,HEIGHT+15))
    WINDOW.blit(mario_end,mario_rect)


def draw(player, objects, enemies, paused=False, finished=False, start_time=0, end_time=0):
    scroll_x = player.rect.x - WIDTH // 2
    scroll_x = max(0, min(scroll_x, BACKGROUND.get_width() - WIDTH))

    WINDOW.blit(BACKGROUND, (-scroll_x, 0))

    for obj in objects:
        obj.draw(scroll_x)

    for enemy in enemies:
        enemy.draw(scroll_x)

    player.draw(scroll_x)

    text = FONT.render(f"{player.rect.x, player.rect.y}", True, "white")
    WINDOW.blit(text, (10, 10))
    
    score_display = FONT.render(f"Wynik: {player.score}", True, "white")
    WINDOW.blit(score_display, (10, 50))
    
    # Wyświetl poziom trudności w grze
    difficulty_display = FONT.render(f"Poziom: {CURRENT_DIFFICULTY}", True, "white")
    WINDOW.blit(difficulty_display, (10, 80))

    live_img = pygame.image.load("D:\\projektPython\\MarioPyGame\\resources\\graphics\\marioLive.png")
    lives = []
    for i in range(player.lives):
        lives.append(live_img.get_rect(center=(750-i*50, 50)))
    for i in range(player.lives):
        WINDOW.blit(live_img, lives[i])
    lives_text = FONT.render(f"Życia:", True, "white")
    text_x = lives[-1].x - 80  
    text_y = lives[-1].centery - lives_text.get_height() // 2 
    WINDOW.blit(lives_text, (text_x, text_y))
    
    if finished:
        draw_end_screen(player, start_time, end_time)
    elif paused:
        draw_pause_screen()

    pygame.display.update()


def restart_game():
    global CURRENT_DIFFICULTY
    lives = DIFFICULTY_SETTINGS[CURRENT_DIFFICULTY]["player_lives"]
    player = Player(6400, FLOOR_LEVEL, 50, 50, lives)
    
    speed_mult = DIFFICULTY_SETTINGS[CURRENT_DIFFICULTY]["enemy_speed_multiplier"]
    enemies = [
        Goomba(1000, FLOOR_LEVEL, 45, 45, int(3 * speed_mult), 450),  
        Goomba(1750, FLOOR_LEVEL, 45, 45, int(3 * speed_mult), 400),  
        Boo(2500, 350, 45, 45, int(3 * speed_mult), 200, 120),  
        Boo(3200, 350, 45, 45, int(3 * speed_mult), 200, 120),  
        Goomba(4000, FLOOR_LEVEL, 45, 45, int(3 * speed_mult), 400),  
    ]
    return player, enemies


def initialize_level():
    obj_storage = Object_storage()
    obj_storage.add_object(Object(0, FLOOR_LEVEL+5, 2279, 5))
    obj_storage.add_object(Object(2345, FLOOR_LEVEL+5, 495, 5))
    obj_storage.add_object(Object(2939, FLOOR_LEVEL+5, 2113, 5))
    obj_storage.add_object(Object(5118, FLOOR_LEVEL+5, 1900, 5))
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
    return obj_storage.get_obj_list()


def main():
    global GAME_PAUSED, GAME_FINISHED, GAME_ACTIVE, GAME_STARTED, CURRENT_DIFFICULTY
    
    run = True
    clock = pygame.time.Clock()
    start_time = 0
    end_time = 0
    selected_menu_option = 1  # Domyślnie SREDNI (indeks 1)
    
    player = None
    enemies = []
    objects = []

    # GŁÓWNA PĘTLA GRY
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
            if event.type == pygame.KEYDOWN:
                # OBSŁUGA MENU GŁÓWNEGO
                if not GAME_ACTIVE and not GAME_STARTED:
                    if event.key == pygame.K_UP:
                        selected_menu_option = (selected_menu_option - 1) % 4
                    elif event.key == pygame.K_DOWN:
                        selected_menu_option = (selected_menu_option + 1) % 4
                    elif event.key == pygame.K_RETURN:
                        if selected_menu_option == 3:  
                            run = False
                        else:
                            difficulty_names = ["ŁATWY", "ŚREDNI", "TRUDNY"]
                            CURRENT_DIFFICULTY = difficulty_names[selected_menu_option]
                            
                           
                            GAME_ACTIVE = True
                            GAME_STARTED = True
                            player, enemies = restart_game()
                            objects = initialize_level()
                            start_time = pygame.time.get_ticks()
                            end_time = 0
                
                # OBSŁUGA GRY
                elif GAME_ACTIVE and GAME_STARTED:
                   
                    if player and player.rect.x > 6680 and player.rect.x < 6870 and not GAME_FINISHED:
                        GAME_FINISHED = True
                        end_time = pygame.time.get_ticks()
                        
                    
                    if event.key == pygame.K_ESCAPE and not GAME_FINISHED:
                        GAME_PAUSED = not GAME_PAUSED
                    
                    # Restart 
                    if event.key == pygame.K_r and (GAME_PAUSED or GAME_FINISHED):
                        player, enemies = restart_game()
                        GAME_PAUSED = False
                        GAME_FINISHED = False
                        start_time = pygame.time.get_ticks()
                        end_time = 0
                    
                    if event.key == pygame.K_m and GAME_FINISHED:
                        GAME_ACTIVE = False
                        GAME_STARTED = False
                        GAME_FINISHED = False
                        GAME_PAUSED = False
                        selected_menu_option = 1  

                    if (event.key == pygame.K_w or event.key == pygame.K_SPACE) and player and not player.jump and not GAME_PAUSED and not GAME_FINISHED:
                        player.do_jump()

        # WYŚWIETLANIE MENU GŁÓWNEGO
        if not GAME_ACTIVE and not GAME_STARTED:
            draw_main_menu(selected_menu_option)
            continue

        # AKTUALIZACJA GRY
        if GAME_ACTIVE and GAME_STARTED and player:
            if not GAME_PAUSED and not GAME_FINISHED:
                handle_move(player)

                player.rect.x += player.x_vel
                handle_horizontal_collision(player, objects)

                player.loop(objects)
                handle_vertical_collision(player, objects)

                scroll_x = max(0, min(player.rect.x - WIDTH // 2, BACKGROUND.get_width() - WIDTH))

                for enemy in enemies[:]:
                    enemy.update(player, objects)
                    enemy.draw(scroll_x)
                    if enemy.rect.x + WIDTH < player.rect.x or enemy.rect.y - HEIGHT > player.rect.y:
                        enemies.remove(enemy)
            
           
            draw(player, objects, enemies, GAME_PAUSED, GAME_FINISHED, start_time, end_time)

    pygame.quit()
    quit()

if __name__ == "__main__":
    main()