"""
projekt_2.py: druhý projekt do Engeto Online Python Akademie

author: Tereza Růžičková
email: terkaruzicka@seznam.cz
discord: terka_99
"""
# v Pythonu používám snake_case, ale v dokumentaci jsem si přečetla, že JSON se používá s camelCase, proto ten nejednotný styl

# knihovna random pro generování náhodných čísel
# knihovna time pro měření času hádání
# knihovna json pro zaznaměnávání statistik hry do zvláštního souboru
# knihovna os pro uložení nového JSON souboru
# knihovna math pro provádění výpočtů

import random
import time
import json
import os
import math


# funkce pro výpis separátoru mezi jednotlivými bloky hry

def print_line_separator():
    print(47 * "-")


# funkce vypisující pozdrav a úvodní text

def print_welcome():
    """Prints the greeting and game introduction"""
    print("Hi there!")
    print_line_separator()
    print("I've generated a random 4 digit number for you.")
    print("Let's play a bulls and cows game.")
    print_line_separator()
    print("Enter a number:")
    print_line_separator()


# funkce pro generování náhodného čtyřmístného čísla
# while cyklus se opakuje dokud se nevygeneruje čtyřmístné číslo s unikátními číslicemi

def generate_number():
    """Generates a random 4-digit number with unique digits"""
    ran_num_list_len = 0
    while ran_num_list_len < 4:
        ran_num_list = list()
        ran_num = random.randint(1000, 9999)
        ran_num_str = str(ran_num)
        for digit in ran_num_str:
            if digit not in ran_num_list:
                ran_num_list.append(digit)
        ran_num_list_len = len(ran_num_list)
    return ran_num_list


# funkce pro získání uživatelského vstupu

def get_user_input():
    """Gets user input and prints it"""
    user_input = input(">>> ")
    return user_input


# funkce pro validaci uživatelského vstupu
# ověří, že vstup obsahuje 4 číslice, neobsauje nečíselné znaky, nezačíná nulou a obsahuje jen číslice, které jsou unikátní

def is_valid(value):
    """Validates the user's input."""
    if len(value) != 4:
        print("Number does not contain four digits.")
        return False
    if not value.isdigit():
        print("Number cannot contain non-numeric values.")
        return False
    if value[0] == "0":
        print("Number cannot start with a zero.")
        return False
    if len(set(value)) != 4:
        print("Number must contain only unique digits.")
        return False
    return True


# funkce, která počítá bulls a cows na základě uživatelského vstupu

def count_bulls_cows(secret_number, user_number):
    """Counts the number of bulls and cows based on user's guess."""
    bull_count = 0
    cow_count = 0
    secret_number_used_pos = set()
    user_number_used_pos = set()
    for i in range(4):
        if secret_number[i] == user_number[i]:
            bull_count += 1
            secret_number_used_pos.add(i)
            user_number_used_pos.add(i)
    for j in range(4):
        if j not in user_number_used_pos:
            for k in range(4):
                if k not in secret_number_used_pos and user_number[j] == secret_number[k]:
                    cow_count += 1
                    secret_number_used_pos.add(k)
                    break
    return bull_count, cow_count


# funkce pro výpis počtu bulls a cows se zprávnou koncovkou

def print_results(bull_count, cow_count):
    """Prints the results based on the counts of bulls and cows."""
    bull_word = "bull" if bull_count == 1 else "bulls"
    cow_word = "cow" if cow_count == 1 else "cows"
    print(f"{bull_count} {bull_word}, {cow_count} {cow_word}")


# funkce pro načtení herních statistik

def load_statistics():
    """Opens a JSON file and reads its contents"""
    json_file = open("game_statistics.json", mode="r")
    statistics_json = json.load(json_file)
    json_file.close()
    return statistics_json


# funkce pro uložení herních statistik

def save_statistics(statistics_json):
    """Saves a dictionary of game statistics as JSON data"""
    json_file = open("game_statistics.json", mode="w")
    json.dump(statistics_json, json_file)
    json_file.close()


# funkce pro kontrolu, jestli soubor se statistikami již existuje, a pokud ne, tak ho vytvoří

def init_statistics():
    """Checks if the file game_statistics.json exists, if not it creates the file with initial game statistics set to zero"""
    if not os.path.exists("game_statistics.json"):
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


# funkce pro update herních statistik (zapisuje se počet odehraných her, celkový počet hádání, celkový čas, chybné hádání, správné hádání)
# nakonec se vypočítá průměr počtu hádání a průměrný čas, za který se podařilo číslo uhádnout

def update_statistics(guesses_count, elapsed_time):
    """Updates and saves cumulative game statistics, including totals, bests, worsts, and averages, based on the latest game’s guesses and time"""
    if guesses_count > 0 and elapsed_time > 0:
        statistics_json = load_statistics()
    
        statistics_json["totalGamesFinished"] += 1
        statistics_json["totalGuessesCount"] += guesses_count
        statistics_json["totalGameTime"] += elapsed_time

        if statistics_json["worstGuessesCount"] <= 0 or guesses_count > statistics_json["worstGuessesCount"]:
            statistics_json["worstGuessesCount"] = guesses_count
        
        if statistics_json["bestGuessesCount"] <= 0 or guesses_count < statistics_json["bestGuessesCount"]:
            statistics_json["bestGuessesCount"] = guesses_count
        
        if statistics_json["worstGameTime"] <= 0 or elapsed_time > statistics_json["worstGameTime"]:
            statistics_json["worstGameTime"] = elapsed_time
        
        if statistics_json["bestGameTime"] <= 0 or elapsed_time < statistics_json["bestGameTime"]:
            statistics_json["bestGameTime"] = elapsed_time
        
        statistics_json["averageGuessesCount"] = math.ceil(statistics_json["totalGuessesCount"] / statistics_json["totalGamesFinished"])
        statistics_json["averageGameTime"] = math.ceil(statistics_json["totalGameTime"] / statistics_json["totalGamesFinished"])

        save_statistics(statistics_json)


# funkce pro zhodnocení výsledku podle uložených statistik hry

def evaluation(guesses_count, elapsed_time):
    """Compares a game's performance to average statistics, returning an evaluation word"""
    statistics_json = load_statistics()
    avg_guesses_count = statistics_json["averageGuessesCount"]
    avg_game_time = statistics_json["averageGameTime"]
    if avg_guesses_count > 0 and avg_game_time > 0:
        if guesses_count == avg_guesses_count and elapsed_time <= avg_game_time:
            eval_word = "average"
        elif guesses_count < avg_guesses_count and elapsed_time <= avg_game_time:
            eval_word = "amazing"
        elif guesses_count > avg_guesses_count and elapsed_time <= avg_game_time:
            eval_word = "not so good"
        else:
             eval_word = "bad"
    else:
        eval_word = "amazing"
    return eval_word


# #############################################################


# hlavní funkce, která volá předem vytvořené podfunkce

def main():
    """Runs the guessing game loop, tracks guesses and time, evaluates performance, updates statistics, and provides feedback to the player"""
    print_welcome()
    init_statistics()
    secret_number = generate_number()
    bull_count = 0
    guesses_count = 0
    start_time = time.time()
    while bull_count != 4:
        user_input = get_user_input()
        if is_valid(user_input):
            bull_count, cow_count = count_bulls_cows(secret_number, user_input)
            print_results(bull_count, cow_count)
            print_line_separator()
            guesses_count +=1
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Correct, you've guessed the right number in {guesses_count} guesses and in {elapsed_time:.2f} seconds!")
    print_line_separator()
    eval_word = evaluation(guesses_count, elapsed_time)
    print(f"That's {eval_word}!")
    update_statistics(guesses_count, elapsed_time)
    print_line_separator()


if __name__ == "__main__":
    main()


