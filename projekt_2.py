"""
projekt_2.py: druhý projekt do Engeto Online Python Akademie

author: Tereza Růžičková
email: terkaruzicka@seznam.cz
discord: terka_99
"""

# knihovna random pro generovani nahodnych cisel
# knihovna time pro mereni casu hadani
# knihovna json pro zaznamenavani statistik hry do zvlastniho souboru
# knihovna os pro ulozeni noveho JSON souboru
# knihovna math pro provadeni vypoctu

import random
import time
import json
import os
import math


# funkce pro vypis oddelovace mezi jednotlivymi bloky hry

def print_line_separator():
    print(47 * "-")


# funkce vypisujici pozdrav a uvodni text

def print_welcome():
    """Prints the greeting and game introduction"""
    
    print("Hi there!")
    print_line_separator()

    print("I've generated a random 4 digit number for you.")
    print("Let's play a bulls and cows game.")
    print_line_separator()

    print("Enter a number:")
    print_line_separator()


# funkce pro generovani nahodneho ctyrmistneho cisla


def generate_number():
    """Generates a random 4-digit number with unique digits"""

    ran_num_list = list()

    # while cyklus se opakuje dokud se nevygeneruje ctyrmistne cislo s unikatnimi cislicemi
    while len(ran_num_list) < 4: 

        # reset kolekce cislic - od druhe iterace dal
        if len(ran_num_list) > 0:
            ran_num_list = list()

        # generovani nahodneho cisla
        ran_num = random.randint(1000, 9999)
        ran_num_str = str(ran_num)

        # vytvoreni konecneho cisla s overenim unikatnosti cislic
        for digit in ran_num_str:
            if digit not in ran_num_list:
                ran_num_list.append(digit)

    return ran_num_list


# funkce pro ziskani uzivatelskeho vstupu

def get_user_input():
    """Gets user input and prints it"""

    user_input = input(">>> ")
    return user_input


# funkce pro validaci uzivatelskeho vstupu

def is_valid(value):
    """Validates the user's input."""

    # overeni delky hodnoty ze vstupu - musi mit delku 4
    if len(value) != 4:
        print("Number does not contain four digits.")
        return False
    
    # overeni, ze hodnota predstavuje cislo (neobsahuje neciselne znaky)
    if not value.isdigit():
        print("Number cannot contain non-numeric values.")
        return False
    
    # overeni, ze hodnota nezacina cislici 0
    if value[0] == "0":
        print("Number cannot start with a zero.")
        return False
    
    # overeni, ze hodnota obsahuje pouze unikatni cislice
    if len(set(value)) != 4:
        print("Number must contain only unique digits.")
        return False
    
    return True


# funkce, ktera pocita bulls a cows na zaklade uzivatelskeho vstupu

def count_bulls_cows(secret_number, user_number):
    """Counts the number of bulls and cows based on user's guess."""

    bull_count = 0
    cow_count = 0
    secret_number_used_pos = set()
    user_number_used_pos = set()
    
    # nalezeni vsech bulls - cislice na stejne pozici v generovanem cisle a uzivatelskem vstupu musi byt stejna
    for i in range(4):
        if secret_number[i] == user_number[i]:
            bull_count += 1
            secret_number_used_pos.add(i)
            user_number_used_pos.add(i)

    # nalezeni cows - cislice z uzivatelova cisla je pritomna v generovanem cisle (ne na stejne pozici 
    # - uzivaji se pouze cislice na pozicich, na kterych nejsou bulls)
    for j in range(4):
        if j not in user_number_used_pos:
            for k in range(4):
                if k not in secret_number_used_pos and user_number[j] == secret_number[k]:
                    cow_count += 1
                    secret_number_used_pos.add(k)
                    break

    return bull_count, cow_count


# funkce pro vypis poctu bulls a cows se spravnou koncovkou

def print_results(bull_count, cow_count):
    """Prints the results based on the counts of bulls and cows."""

    bull_word = "bull" if bull_count == 1 else "bulls"
    cow_word = "cow" if cow_count == 1 else "cows"

    print(f"{bull_count} {bull_word}, {cow_count} {cow_word}")



# funkce pro nacteni hernich statistik

def load_statistics():
    """Opens a JSON file and reads its contents"""
    
    json_file = open("game_statistics.json", mode="r")
    statistics_json = json.load(json_file)
    json_file.close()

    return statistics_json


# funkce pro ulozeni hernich statistik

def save_statistics(statistics_json):
    """Saves a dictionary of game statistics as JSON data"""

    json_file = open("game_statistics.json", mode="w")
    json.dump(statistics_json, json_file)
    json_file.close()


# funkce pro kontrolu, jestli soubor se statistikami jiz existuje, a pokud ne, tak ho vytvori

def init_statistics():
    """Checks if the file game_statistics.json exists, if not it creates the file with initial game statistics set to zero"""

    if not os.path.exists("game_statistics.json"):
        # pouziti camelCase dle standardu JSONu
        init_statistics_json = {
            "totalGamesFinished": 0,
            "totalGuessesCount": 0,
            "totalGameTime": 0,
            "worstGuessesCount": 0,
            "worstGameTime": 0,
            "bestGuessesCount": 0,
            "bestGameTime": 0,
            "averageGuessesCount": 0,
            "averageGameTime": 0
        }

        save_statistics(init_statistics_json)


# funkce pro update hernich statistik (zapisuje se pocet odehranyh her, celkovy pocet hadani, celkovy cas, chybne hadani, spravne hadani)
# nakonec se vypocita prumer poctu hadani a prumerny cas, za ktery se podarilo cislo uhadnout

def update_statistics(guesses_count, elapsed_time):
    """Updates and saves cumulative game statistics, including totals, bests, worsts, and averages, based on the latest game’s guesses and time"""

    # vyhodnoceni se provede, pokud se odehrala nejaka hra (hadaci pokus je alespon 1 a ubehl nejaky cas)
    if guesses_count > 0 and elapsed_time > 0:
        # nacteni statistik z predchozich odehranych her
        statistics_json = load_statistics()

        # aktualizace celkovych hodnot ve statistikach
        statistics_json["totalGamesFinished"] += 1
        statistics_json["totalGuessesCount"] += guesses_count
        statistics_json["totalGameTime"] += round(elapsed_time, 2)

        # v nasledujicich ifech je zavedeno porovnani s 0 pro aktualizaci hodnot po prvni odehrane hre 
        # (pred prvni hrou jsou statistiky nastaveny na 0)

        # overeni a aktualizace nejhorsi hry z pohledu poctu pokusu
        if statistics_json["worstGuessesCount"] <= 0 or guesses_count > statistics_json["worstGuessesCount"]:
            statistics_json["worstGuessesCount"] = guesses_count
        
        # overeni a aktualizace nejlepsi hry z pohledu poctu pokusu
        if statistics_json["bestGuessesCount"] <= 0 or guesses_count < statistics_json["bestGuessesCount"]:
            statistics_json["bestGuessesCount"] = guesses_count
        
        # overeni a aktualizace nejhorsi hry z pohledu delky hry v case (zaokrouhelo na dve desetinna cisla)
        if statistics_json["worstGameTime"] <= 0 or elapsed_time > statistics_json["worstGameTime"]:
            statistics_json["worstGameTime"] = round(elapsed_time, 2)
        
        # overeni a aktualizace nejlepsi hry z pohledu delky hry v case (zaokrouhelo na dve desetinna cisla)
        if statistics_json["bestGameTime"] <= 0 or elapsed_time < statistics_json["bestGameTime"]:
            statistics_json["bestGameTime"] = round(elapsed_time, 2)
        
        # vypocet a aktualizace prumernych hodnot

        # zaokrouhleno na cela cisla smerem nahoru
        statistics_json["averageGuessesCount"] = math.ceil(statistics_json["totalGuessesCount"] / statistics_json["totalGamesFinished"])
        # zaokrouhleno na dve desetinna cisla
        statistics_json["averageGameTime"] = round(statistics_json["totalGameTime"] / statistics_json["totalGamesFinished"], 2)

        # ulozeni aktualizovanych statistik zpatky do JSON souboru
        save_statistics(statistics_json)


# funkce pro zhodnoceni vysledku podle ulozenych statistik hry

def evaluation(guesses_count, elapsed_time):
    """Compares a game's performance to average statistics, returning an evaluation word"""
    
    # nacteni statistik z predeslych odehranych her
    statistics_json = load_statistics()

    # ulozeni prumernych hodnot do lokalnich promennych (pro prehlednost)
    avg_guesses_count = statistics_json["averageGuessesCount"]
    avg_game_time = statistics_json["averageGameTime"]

    # pokud byla odehrana alespon jedna hra, provede se detailni vyhodnoceni
    if avg_guesses_count > 0 and avg_game_time > 0:
        # overeni, zda uzivatel odehral prumernou hru
        if guesses_count == avg_guesses_count and elapsed_time <= avg_game_time:
            eval_word = "average"
        # overeni, zda uzivatel zahral vybornou hru (lepsi nez prumer)
        elif guesses_count < avg_guesses_count and elapsed_time <= avg_game_time:
            eval_word = "amazing"
        # overeni, zda zahral ne tak dobrou hru (nejhure v prumernem case)
        elif guesses_count > avg_guesses_count and elapsed_time <= avg_game_time:
            eval_word = "not so good"
        # uzivatel zahral spatnou hru (z pohledu poctu pokusu i casu)
        else:
            eval_word = "bad"
    # jinak uvazujeme vybornou hru (nemame s cim porovnat)
    else:
        eval_word = "amazing"

    return eval_word


# #############################################################


# hlavni funkce, ktera vola predem vytvorene podfunkce

def main():
    """Runs the guessing game loop, tracks guesses and time, evaluates performance, updates statistics, and provides feedback to the player"""

    # inicializace hry
    init_statistics()
    secret_number = generate_number()
    bull_count = 0
    guesses_count = 0

    print_welcome()

    start_time = time.time()

    # while cyklus pro opakovane zadavani vstupu uzivatele, opakuje se, dokud uzivatel netrefi vygenerovane cislo
    while bull_count != 4:
        user_input = get_user_input()

        # pri platnem vstupu se provede vyhodnoceni hadaciho pokusu
        if is_valid(user_input):
            bull_count, cow_count = count_bulls_cows(secret_number, user_input)
            
            print_results(bull_count, cow_count)
            print_line_separator()

            # zvednuti citace pokusu (pocitaji se pouze platne pokusy)
            guesses_count +=1

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Correct, you've guessed the right number in {guesses_count} guesses and in {elapsed_time:.2f} seconds!")
    print_line_separator()

    eval_word = evaluation(guesses_count, elapsed_time)
    print(f"That's {eval_word}!")
    print_line_separator()

    update_statistics(guesses_count, elapsed_time)


if __name__ == "__main__":
    main()


