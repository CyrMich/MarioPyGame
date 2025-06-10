import pygame
from constants import WINDOW, WIDTH, HEIGHT, FONT, WORLD_CLEAR, DIFFICULTY_SETTINGS, CURRENT_DIFFICULTY, BACKGROUND, FINAL_SCORE, TIME_BONUS
import constants

def draw_main_menu(selected_option):
    WINDOW.fill((30, 30, 80))

    title_text = FONT.render("MARIO GAME", True, "yellow")
    title_rect = title_text.get_rect(center=(WIDTH // 2, 30))
    WINDOW.blit(title_text, title_rect)

    mario_start = pygame.image.load("resources\\graphics\\marioStart.png").convert_alpha()
    mario_rect = mario_start.get_rect(center=(WIDTH // 2, 140))
    WINDOW.blit(mario_start, mario_rect)

    menu_options = ["ŁATWY", "ŚREDNI", "TRUDNY", "WYJŚCIE"]
    option_colors = ["white"] * 4
    option_colors[selected_option] = "red"

    descriptions = [
        "5 żyć, wolniejsi przeciwnicy",
        "3 życia, normalny poziom",
        "1 życie, szybsi przeciwnicy",
        "Zamknij grę"
    ]

    start_y = HEIGHT // 2 - 50
    for i, (option, desc) in enumerate(zip(menu_options, descriptions)):
        option_text = FONT.render(option, True, option_colors[i])
        option_rect = option_text.get_rect(center=(WIDTH // 2, start_y + i * 70))
        WINDOW.blit(option_text, option_rect)

        if desc:
            desc_text = FONT.render(desc, True, "lightgray")
            desc_rect = desc_text.get_rect(center=(WIDTH // 2, start_y + i * 70 + 25))
            WINDOW.blit(desc_text, desc_rect)

    instruction1 = FONT.render("↑↓ - Wybierz poziom", True, "white")
    instruction1_rect = instruction1.get_rect(center=(WIDTH // 2, HEIGHT - 80))
    WINDOW.blit(instruction1, instruction1_rect)

    instruction2 = FONT.render("ENTER - Rozpocznij grę", True, "white")
    instruction2_rect = instruction2.get_rect(center=(WIDTH // 2, HEIGHT - 50))
    WINDOW.blit(instruction2, instruction2_rect)

    pygame.display.update()


def draw_pause_screen():
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(128)
    overlay.fill((0, 0, 0))
    WINDOW.blit(overlay, (0, 0))

    pause_text = FONT.render("PAUZA", True, "white")
    pause_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    WINDOW.blit(pause_text, pause_rect)

    instruction1 = FONT.render("ESC - Wznów grę", True, "white")
    instruction1_rect = instruction1.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
    WINDOW.blit(instruction1, instruction1_rect)

    instruction2 = FONT.render("R - Restart gry", True, "white")
    instruction2_rect = instruction2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    WINDOW.blit(instruction2, instruction2_rect)


def draw_end_screen(player, start_time, end_time):
    global FINAL_SCORE
    pygame.mixer.music.stop()
    WORLD_CLEAR.play()

    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(220)
    overlay.fill((0, 0, 0))
    WINDOW.blit(overlay, (0, 0))

    constants.TIME_BONUS= max(0, int(50 - (end_time - start_time) / 1000))
    constants.FINAL_SCORE = int((player.score * 5 + player.lives * 10 + constants.TIME_BONUS) * DIFFICULTY_SETTINGS[constants.CURRENT_DIFFICULTY][
        "score_multiplier"])

    congrats_text = FONT.render("GRATULACJE!", True, "yellow")
    congrats_rect = congrats_text.get_rect(topleft=(40, HEIGHT // 2 - 200))
    WINDOW.blit(congrats_text, congrats_rect)

    difficulty_text = FONT.render(f"Poziom: {constants.CURRENT_DIFFICULTY}", True, "white")
    difficulty_rect = difficulty_text.get_rect(topleft=(40, HEIGHT // 2 - 170))
    WINDOW.blit(difficulty_text, difficulty_rect)

    score_text = FONT.render(f"Punkty za przeciwników: {player.score * 5}", True, "white")
    score_rect = score_text.get_rect(topleft=(40, HEIGHT // 2 - 140))
    WINDOW.blit(score_text, score_rect)

    lives_text = FONT.render(f"Bonus za życia: {player.lives * 10}", True, "white")
    lives_rect = lives_text.get_rect(topleft=(40, HEIGHT // 2 - 110))
    WINDOW.blit(lives_text, lives_rect)

    time_text = FONT.render(f"Bonus za czas: {constants.TIME_BONUS}", True, "white")
    time_rect = time_text.get_rect(topleft=(40, HEIGHT // 2 - 80))
    WINDOW.blit(time_text, time_rect)

    final_text = FONT.render(f"Wynik: {constants.FINAL_SCORE}", True, "gold")
    final_rect = final_text.get_rect(topleft=(40, HEIGHT // 2 - 50))
    WINDOW.blit(final_text, final_rect)

    instruction1 = FONT.render("R - Restart gry", True, "white")
    instruction1_rect = instruction1.get_rect(topleft=(40, HEIGHT // 2 + 100))
    WINDOW.blit(instruction1, instruction1_rect)

    instruction2 = FONT.render("M - Powrót do menu", True, "white")
    instruction2_rect = instruction2.get_rect(topleft=(40, HEIGHT // 2 + 130))
    WINDOW.blit(instruction2, instruction2_rect)

    instruction3 = FONT.render("Z - Zapisz wynik do pliku", True, "white")
    instruction3_rect = instruction3.get_rect(topleft=(40, HEIGHT // 2 + 160))
    WINDOW.blit(instruction3, instruction3_rect)

    mario_end = pygame.image.load("resources\\graphics\\marioEnd.png").convert_alpha()
    mario_rect = mario_end.get_rect(midbottom=(600, HEIGHT + 15))
    WINDOW.blit(mario_end, mario_rect)


def draw(player, objects, coins, enemies, paused=False, finished=False,lost=False, start_time=0, end_time=0):
    scroll_x = player.rect.x - WIDTH // 2
    scroll_x = max(0, min(scroll_x, BACKGROUND.get_width() - WIDTH))

    WINDOW.blit(BACKGROUND, (-scroll_x, 0))

    for obj in objects:
        obj.draw(scroll_x)

    for enemy in enemies:
        enemy.draw(scroll_x)

    for coin in coins:
        coin.draw(scroll_x)

    player.draw(scroll_x)

    text = FONT.render(f"Czas: {int((pygame.time.get_ticks()-constants.START_TIME)/1000)}", True, "white")
    WINDOW.blit(text, (10, 10))

    score_display = FONT.render(f"Wynik: {player.score}", True, "white")
    WINDOW.blit(score_display, (10, 50))

    # Wyświetl poziom trudności w grze
    difficulty_display = FONT.render(f"Poziom: {constants.CURRENT_DIFFICULTY}", True, "white")
    WINDOW.blit(difficulty_display, (10, 80))

    live_img = pygame.image.load("resources\\graphics\\marioLive.png")
    lives = []
    for i in range(player.lives):
        lives.append(live_img.get_rect(center=(750 - i * 50, 50)))
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