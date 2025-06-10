from constants import  DIFFICULTY_SETTINGS, FINAL_SCORE, TIME_BONUS
import constants
import datetime

def save_score(player, start_time, end_time):
    teraz = datetime.datetime.now()
    data_czas = teraz.strftime("%Y-%m-%d_%H-%M-%S")

    nazwa_pliku = f"mario_{constants.CURRENT_DIFFICULTY}_{data_czas}.txt"
    if constants.CURRENT_DIFFICULTY=="ŚREDNI": difficulty="SREDNI"
    elif constants.CURRENT_DIFFICULTY=="ŁATWY": difficulty="LATWY"
    else: difficulty="TRUDNY"

    # Zapisz wynik do nowego pliku
    with open(nazwa_pliku, 'w') as f:
        f.write(f"=== WYNIK GRY: {constants.FINAL_SCORE} ===\n")
        f.write(f"Poziom: {difficulty}\n")
        f.write(f"Punkty za przeciwnikow: {player.score * 5}\n")
        f.write(f"Bonus za czas: {constants.TIME_BONUS}\n")
        f.write(F"Skonczone w: {int((end_time - start_time) / 1000)}\n")
        f.write(F"Pozostala liczba zyc: {player.lives}\n")
        

    