import pygame
from constants import FPS, WIDTH, HEIGHT, BACKGROUND, GAME_ACTIVE, GAME_PAUSED, GAME_STARTED, GAME_FINISHED, CURRENT_DIFFICULTY, DIFFICULTY_SETTINGS
from tools import initialize_level, handle_move
from restart_game import restart_game
from restart_powerups import reset_powerups
from collision import handle_horizontal_collision, handle_vertical_collision
from draw import draw, draw_main_menu


def main():
    global GAME_PAUSED, GAME_FINISHED, GAME_ACTIVE, GAME_STARTED, CURRENT_DIFFICULTY
    
    run = True
    clock = pygame.time.Clock()
    start_time = 0
    end_time = 0
    selected_menu_option = 1  # Domyślnie SREDNI (indeks 1)

    global player
    player = None
    global enemies
    global objects
    global coins
    enemies = []
    objects = []
    coins = []

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
                            reset_powerups(objects)
                            start_time = pygame.time.get_ticks()
                            end_time = 0
                # OBSŁUGA GRY
                elif GAME_ACTIVE and GAME_STARTED:

                    enemies = [enemy for enemy in enemies if not enemy.to_remove]
                   
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
                        constants.START_TIME = pygame.time.get_ticks()
                        end_time = 0
                        player, enemies = restart_game()
                        objects = initialize_level()
                        reset_powerups(objects)
                    
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
                handle_vertical_collision(player, objects, enemies, coins)

                scroll_x = max(0, min(player.rect.x - WIDTH // 2, BACKGROUND.get_width() - WIDTH))

                for enemy in enemies[:]:
                    enemy.update(player, objects)
                    enemy.draw(scroll_x)
                    if enemy.rect.x + WIDTH < player.rect.x or enemy.rect.y - HEIGHT > player.rect.y:
                        enemies.remove(enemy)

                for coin in coins[:]:
                    coin.update()
                    coin.draw(scroll_x)
                    if not coin.alive:
                        coins.remove(coin)
            
           
            draw(player, objects, coins, enemies, GAME_PAUSED, GAME_FINISHED, start_time, end_time)

    pygame.quit()
    quit()

if __name__ == "__main__":
    main()