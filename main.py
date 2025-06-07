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
BACKGROUND = pygame.transform.scale(pygame.image.load("resources\\graphics\\level_1.png"),(7000,600))

# MUZYKA
pygame.mixer.music.load("resources\\music\\main_theme.ogg")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

JUMP_SOUND = pygame.mixer.Sound("resources\\sound\\small_jump.ogg")
JUMP_SOUND.set_volume(0.5)

SPRITE_SHEET = pygame.image.load("resources\\graphics\\mario_bros.png").convert_alpha()

FLOOR_LEVEL = 536

FPS = 60
PLAYER_VEL = 10  # DOCELOWO 5 DLA TESTOW JEST WIECEJ
GAME_ACTIVE = True
GAME_PAUSED = False
GAME_FINISHED = False
TIME = 100

class Player(pygame.sprite.Sprite):
    GRAVITY = 1.5  # DO USTALENIA

    def __init__(self, x, y, width, height, sprites, lives):
        super().__init__()
        self.rect = pygame.Rect(x, y-height, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.jump = False
        self.sprites = sprites
        self.direction = "right"
        self.animation_count = 0
        self.lives=lives
        self.score=0  # Zmienione z 1 na 0 dla lepszej logiki

    def do_jump(self):
        if not self.jump:
            self.y_vel = -self.GRAVITY * 16
            self.jump = True
            JUMP_SOUND.play()

    def check_if_airborne(self, objects):
        # PROSTOKĄT POD GRACZEM SPRAWDZA CZY WYLĄDOWAŁ
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

    # PĘTLA GRACZA
    def loop(self,objects):
        self.check_if_airborne(objects)

        if self.rect.y > HEIGHT + 50:
            self.lives -= 1
            if self.lives <= 0:
                self.reset()
                self.lives = 3  # Reset liczby żyć po śmierci
            else:
                self.rect.x = 400
                self.rect.y = 300
                self.y_vel = 0
                self.jump = False

        self.update_sprite()
        self.update()

        self.y_vel += self.GRAVITY  # GRAWITACJA
        self.rect.y += self.y_vel

    def reset(self):
        self.rect.x = 400
        self.rect.y = 300
        self.y_vel = 0
        self.jump = False
        self.lives = 3 
        self.score = 0  # RESET WYNIKU

    def update_sprite(self):
        # Animacja skoku
        if self.y_vel != 0:
            self.sprite_index = 4  # skacze

        # Animacja biegu
        elif self.x_vel != 0:
            self.animation_counter += 1
            if self.animation_counter >= 6:  # zmiana co 10 klatek
                self.animation_counter = 0
                self.sprite_index += 1
                if self.sprite_index > 3:
                    self.sprite_index = 1  # pętla 1-3 (bieganie)

        # Postać stoi
        else:
            self.sprite_index = 0
            self.animation_counter = 0

        # Ustaw sprite zgodnie z kierunkiem
        if self.direction == "right":
            self.sprite = self.sprites[self.sprite_index]
        elif self.direction == "left":
            self.sprite = pygame.transform.flip(self.sprites[self.sprite_index], True, False)

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))

    def draw(self, scroll_x):
        adjusted_rect = self.rect.copy()
        adjusted_rect.x -= scroll_x

        WINDOW.blit(self.sprite, (adjusted_rect.x, adjusted_rect.y))


class Enemy(pygame.sprite.Sprite):
    GRAVITY = 1

    def __init__(self, x, y, width, height, speed=2):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.y_vel = 0
        self.alive = True

    def apply_gravity(self):
        self.y_vel += self.GRAVITY
        if self.y_vel > 10:
            self.y_vel = 10

    def move_and_collide(self, objects):
        # RUCH W POZIOMIE
        self.rect.x += self.speed
        for obj in objects:
            if self.rect.colliderect(obj.rect):
                if self.speed > 0:
                    self.rect.right = obj.rect.left
                else:
                    self.rect.left = obj.rect.right
                self.speed *= -1  # ZMIANA KIERUNKU

        # RUCH W PIONIE
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

        # KOLIZJA Z GRACZEM
        if self.rect.colliderect(player.rect):
            if player.rect.bottom <= self.rect.top+20:
                self.alive = False
                player.y_vel = -15
                player.jump = True
            else:
                player.lives -= 1
                if player.lives <= 0:
                    player.reset()
                    player.lives = 3  # Reset żyć po śmierci
                else:
                    player.rect.x -= 50  # Cofa gracza
                    player.y_vel = -10   # Daje odrzut po uderzeniu

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
        self.original_speed = abs(speed)
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

        # KOLIZJA Z GRACZEM
        if self.rect.colliderect(player.rect):
            if player.rect.bottom <= self.rect.top + 20:
                self.alive = False
                player.score+=2
                player.y_vel = -15
                player.jump = True
            else:
                player.lives -= 1
                if player.lives <= 0:
                    player.reset()
                    player.lives = 3
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
        self.original_speed = abs(speed)
    
        self.corners = [
            (self.start_x + self.patrol_width, self.start_y), 
            (self.start_x + self.patrol_width, self.start_y + self.patrol_height),  
            (self.start_x, self.start_y + self.patrol_height),  
            (self.start_x, self.start_y)  
        ]
        
    def update(self, player,objects):
        if not self.alive:
            return

        self.fly_in_rectangle()

        if self.rect.colliderect(player.rect):
            if player.rect.bottom <= self.rect.top + 20:
                self.alive = False
                player.score+=3
                player.y_vel = -15
                player.jump = True
            else:
                player.lives -= 1
                if player.lives <= 0:
                    player.reset()
                    player.lives = 3
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

# FUNKCJA RYSUJACA EKRAN PAUZY
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

# FUNKCJA RYSUJACA EKRAN KOŃCOWY
def draw_end_screen(player, start_time):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    WINDOW.blit(overlay, (0, 0))
    
    # Obliczanie wyniku końcowego
    current_time = pygame.time.get_ticks()
    time_bonus = 100 - int(start_time/1000)  # Bonus za czas
    final_score = player.score * 10 + player.lives * 50 + time_bonus
    
    # Wyświetlanie wyniku
    congrats_text = FONT.render("GRATULACJE!", True, "yellow")
    congrats_rect = congrats_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 100))
    WINDOW.blit(congrats_text, congrats_rect)
    
    score_text = FONT.render(f"Punkty za przeciwników: {player.score * 10}", True, "white")
    score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
    WINDOW.blit(score_text, score_rect)
    
    lives_text = FONT.render(f"Bonus za życia: {player.lives * 50}", True, "white")
    lives_rect = lives_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 20))
    WINDOW.blit(lives_text, lives_rect)
    
    time_text = FONT.render(f"Bonus za czas: {time_bonus}", True, "white")
    time_rect = time_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 10))
    WINDOW.blit(time_text, time_rect)
    
    final_text = FONT.render(f"KOŃCOWY WYNIK: {final_score}", True, "gold")
    final_rect = final_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
    WINDOW.blit(final_text, final_rect)
    
    instruction = FONT.render("R - Restart gry", True, "white")
    instruction_rect = instruction.get_rect(center=(WIDTH//2, HEIGHT//2 + 100))
    WINDOW.blit(instruction, instruction_rect)

# FUNKCJA RYSUJACA NA EKRANIE
def draw(player, objects, enemies, paused=False, finished=False, start_time=0):
    scroll_x = player.rect.x - WIDTH // 2
    scroll_x = max(0, min(scroll_x, BACKGROUND.get_width() - WIDTH))

    WINDOW.blit(BACKGROUND, (-scroll_x, 0))

    for obj in objects:
        obj.draw(scroll_x)

    for enemy in enemies:
        enemy.draw(scroll_x)

    player.draw(scroll_x)

    # X,Y GRACZA I ŻYCIA DO TESTOW
    text = FONT.render(f"{player.rect.x, player.rect.y}",True,"white")
    WINDOW.blit(text,(10,10))

    # Życia
    live_img=pygame.image.load("resources\\graphics\\marioLive.png")
    lives=[]
    for i in range(player.lives):
        lives.append(live_img.get_rect(center=(750-i*50,50)))
    for i in range(player.lives):
        WINDOW.blit(live_img,lives[i])
    lives_text = FONT.render(f"Życia:",True,"white")
    text_x = lives[-1].x - 80  
    text_y = lives[-1].centery - lives_text.get_height() // 2 
    WINDOW.blit(lives_text, (text_x, text_y))
    
    # Rysuj odpowiedni ekran
    if finished:
        draw_end_screen(player, start_time)
    elif paused:
        draw_pause_screen()

    pygame.display.update()

def get_image_from_sheet(x, y, width, height, scale=1):
    image = pygame.Surface((width, height), pygame.SRCALPHA)
    image.blit(SPRITE_SHEET, (0, 0), pygame.Rect(x, y, width, height))
    if scale != 1:
        image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
    return image

def restart_game(sprites):
    # Funkcja resetująca grę do stanu początkowego
    player = Player(400, FLOOR_LEVEL, 50, 50, sprites, 3)
    enemies = [
        Goomba(1000, FLOOR_LEVEL, 45, 45, 3, 450),  
        Goomba(1750, FLOOR_LEVEL, 45, 45, 3, 400),  
        Boo(2500, 350, 45, 45, 3, 200, 120),  
        Boo(3200, 350, 45, 45, 3, 200, 120),  
        Goomba(4000, FLOOR_LEVEL, 45, 45, 3, 400),  
    ]
    return player, enemies

def main():
    global GAME_PAUSED, GAME_FINISHED
    run = True
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()

    small_mario_imgs = [
        get_image_from_sheet(178, 32, 12, 16, 3),  # MARIO STOI W MIEJSCU
        get_image_from_sheet(80, 32, 15, 16, 3),  # MARIO CHÓD [1]
        get_image_from_sheet(96, 32, 16, 16, 3),  # MARIO CHÓD [2]
        get_image_from_sheet(112, 32, 16, 16, 3),  # MARIO CHÓD [3]
        get_image_from_sheet(144, 32, 16, 16, 3)  # MARIO SKACZE
    ]

    big_mario_imgs = []

    player, enemies = restart_game(small_mario_imgs)

    floor1 = Object(0, FLOOR_LEVEL+5, 2279, 5)
    floor2 = Object(2345, FLOOR_LEVEL+5, 495, 5)
    floor3 = Object(2939, FLOOR_LEVEL+5, 2113, 5)
    floor4 = Object(5118, FLOOR_LEVEL+5, 1900, 5)

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

    winning_gate=Object(6715,FLOOR_LEVEL,20,70,"brown",True)
    
    objects = [
        floor1, floor2, floor3, floor4,
        pipe1, pipe2,pipe3,pipe4,pipe5,pipe6,
        stairs1,stairs2,stairs3,stairs4,stairs5,stairs6,stairs7,
        stairs8,stairs9,stairs10,stairs11,stairs12,stairs13,stairs14,
        stairs15,stairs16,stairs17,stairs18,stairs19,stairs20,stairs21,
        stairs22,stairs23,stairs24,stairs25,stairs26,stairs27,
        winning_gate
    ]

    # GŁÓWNA PĘTLA GRY
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
                
            # Sprawdzenie czy gracz dotarł do strefy końcowej
            if player.rect.x > 6680 and player.rect.x < 6770 and not GAME_FINISHED:
                GAME_FINISHED = True
                
            if event.type == pygame.KEYDOWN:
                # Obsługa pauzy (tylko gdy gra nie jest skończona)
                if event.key == pygame.K_ESCAPE and not GAME_FINISHED:
                    GAME_PAUSED = not GAME_PAUSED
                
                # Restart 
                if event.key == pygame.K_r and (GAME_PAUSED or GAME_FINISHED):
                    player, enemies = restart_game(small_mario_imgs)
                    GAME_PAUSED = False
                    GAME_FINISHED = False
                    start_time = pygame.time.get_ticks()  # Reset czasu
                
                if (event.key == pygame.K_w or event.key == pygame.K_SPACE) and not player.jump and not GAME_PAUSED and not GAME_FINISHED:
                    player.do_jump()

        # Aktualizuj grę tylko gdy nie jest zatrzymana ani skończona
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
            
        draw(player, objects, enemies, GAME_PAUSED, GAME_FINISHED, start_time)

    pygame.quit()
    quit()

if __name__ == "__main__":
    main()