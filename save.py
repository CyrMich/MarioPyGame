from constants import WINDOW, WIDTH, HEIGHT, FONT, WORLD_CLEAR, DIFFICULTY_SETTINGS, CURRENT_DIFFICULTY, BACKGROUND
import constants
import datetime

def save_score(player, start_time, end_time):
    time_bonus = max(0, int(50 - (end_time - start_time) / 1000))
    final_score = int((player.score * 5 + player.lives * 10 + time_bonus) * DIFFICULTY_SETTINGS[constants.CURRENT_DIFFICULTY][
    "score_multiplier"])
    teraz = datetime.datetime.now()
    data_czas = teraz.strftime("%Y-%m-%d_%H-%M-%S")

    nazwa_pliku = f"{data_czas}_mario_{constants.CURRENT_DIFFICULTY}.txt"
    if constants.CURRENT_DIFFICULTY=="ŚREDNI": difficulty="SREDNI"
    elif constants.CURRENT_DIFFICULTY=="ŁATWY": difficulty="LATWY"
    else: difficulty="TRUDNY"

    # Zapisz wynik do nowego pliku
    with open(nazwa_pliku, 'w') as f:
        f.write(f"=== WYNIK GRY: {final_score} ===\n")
        f.write(f"Poziom: {difficulty}\n")
        f.write(f"Punkty za przeciwnikow: {player.score * 5}\n")
        f.write(f"Bonus za czas: {time_bonus}\n")
        f.write(F"Czas: {int((end_time - start_time) / 1000)}\n")
        f.write(F"Pozostala liczba zyc: {player.lives}\n")
        

    