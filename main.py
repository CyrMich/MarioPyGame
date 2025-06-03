import pygame

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Mario")

FPS = 60
PLAYER_VEL = 5

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
            self.y_vel = -self.GRAVITY * 10
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
        # self.y_vel += min(1,5) # GRAWITACJA, DO ZMIANY JESZCZE
        self.move(self.x_vel,self.y_vel)

    def draw(self):
        pygame.draw.rect(WINDOW,"red",self.rect)

# FUNKCJA OBSLUGUJACA RUCH GRACZA
def handle_move(player):
    keys = pygame.key.get_pressed()

    player.x_vel = 0

    if keys[pygame.K_a]:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_d]:
        player.move_right(PLAYER_VEL)

# FUNKCJA RYSUJACA NA EKRANIE
def draw(player):
    # WINDOW.blit(background,(0,0))
    WINDOW.fill("white")
    player.draw()
    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()

    player = Player(400,300,50,50)

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
        draw(player)


    pygame.quit()


if __name__ == "__main__":
    main()