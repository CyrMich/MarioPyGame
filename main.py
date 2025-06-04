import pygame

# INICJALIZACJA CZCIONKI I PYGAME
pygame.init()
pygame.font.init()

# WYMIARY OKNA
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Mario")

# TŁO
BACKGROUND = pygame.transform.scale(pygame.image.load("resources\\graphics\\level_1.png"),(7000,600))

FLOOR_LEVEL = 536

FPS = 60
PLAYER_VEL = 10 # DOCELOWO 5 DLA TESTOW JEST WIECEJ

class Player(pygame.sprite.Sprite):
    GRAVITY = 1 # DO USTALENIA

    def __init__(self,x,y,width,height):
        super().__init__()
        self.rect = pygame.Rect(x,y,width,height)
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

    def move_left(self,vel):
        self.x_vel = -vel

    def move_right(self,vel):
        self.x_vel = vel

    def move(self,dx,dy):
        self.rect.x += dx
        self.rect.y += dy

    # PĘTLA GRACZA
    def loop(self):
        self.y_vel += self.GRAVITY # GRAWITACJA, DO ZMIANY JESZCZE
        self.move(self.x_vel,self.y_vel)

    def draw(self,scroll_x):
        adjusted_rect = self.rect.copy()
        adjusted_rect.x -= scroll_x
        pygame.draw.rect(WINDOW, "red", adjusted_rect)


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color="green"):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self,scroll_x): # TESTY PODLOGI
        adjusted_rect = self.rect.copy()
        adjusted_rect.x -= scroll_x
        pygame.draw.rect(WINDOW, self.color, adjusted_rect)



def handle_vertical_collision(player,objects):
    player.rect.y += player.y_vel
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
def draw(player,objects,scroll_x):
    scroll_x = player.rect.x - WIDTH // 2
    scroll_x = max(0, min(scroll_x, BACKGROUND.get_width() - WIDTH))  # OGRANICZENIA W POZIOMIE


    WINDOW.blit(BACKGROUND,(-scroll_x,0))

    for obj in objects:
        obj.draw(scroll_x)

    player.draw(scroll_x)

    pygame.display.update()


def load_sprite_sheets(dir):
    ...


def main():
    run = True
    clock = pygame.time.Clock()

    player = Player(400,300,50,50)

    floor1 = Object(0,FLOOR_LEVEL,2279,5)
    floor2 = Object(2345,FLOOR_LEVEL,495,5)
    floor3 = Object(2939,FLOOR_LEVEL,2113,5)
    floor4 = Object(5118,FLOOR_LEVEL,1900,5)

    objects = [floor1, floor2, floor3, floor4]

    scroll_x = player.rect.x - WIDTH // 2

    # GŁÓWNA PĘTLA GRY
    while run:
        clock.tick(FPS)

        # WYJŚCIE
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            # ODPOWIADA ZA SKAKANIE
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and not player.jump:
                    player.do_jump()

        player.loop()
        handle_move(player)
        handle_vertical_collision(player, objects)
        draw(player, objects, scroll_x)


    pygame.quit()


if __name__ == "__main__":
    main()