"""
projekt_2.py: druhý projekt do Engeto Online Python Akademie

author: Tereza Růžičková
email: terkaruzicka@seznam.cz
discord: terka_99
"""
# knihovna random pro generování náhodných čísel
# knihovna time pro meěření času hádání

import random
import time

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


# generace náhodného čtyřmístného čísla
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


# uživatelský vstup

def get_user_input():
    """Gets user input nd prints it"""
    user_input = input(">>> ")
    return user_input


# validace uživatelského vstupu
# ověří, že ve vstup obsahuje 4 číslice, neobsauje nečíselné znaky, nezačíná nulou, které jsou unikátní

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

# počítání bulls a cows

def count_bulls_cows(secret_number, user_number):
    """Counts the number of bulls and cows based on the user's guess."""
    bull_count = 0
    cow_count = 0
    secret_used = [False] * 4
    user_used = [False] * 4
    for i in range(4):
        if secret_number[i] == user_number[i]:
            bull_count += 1
            secret_used[i] = True
            user_used[i] = True
    for j in range(4):
        if not user_used[j]:
            for k in range(4):
                if not secret_used[k] and user_number[j] == secret_number[k]:
                    cow_count += 1
                    secret_used[k] = True
                    break
    return bull_count, cow_count


# výpis počtu bulls a cows se zprávnou koncovkou

def print_results(bull_count, cow_count):
    """Prints the results based on the counts of bulls and cows."""
    bull_word = "bull" if bull_count == 1 else "bulls"
    cow_word = "cow" if cow_count == 1 else "cows"
    print(f"{bull_count} {bull_word}, {cow_count} {cow_word}")


# zhodnocení výsledku

def evaluation(guesses_count, elapsed_time):
    if guesses_count in range(1,5) and elapsed_time in range(0, 301):
        eval_word = "amazing"
    elif guesses_count in range(5, 10) and elapsed_time in range(0, 301):
        eval_word = "average"
    elif guesses_count in range (10, 20) and elapsed_time in range(0, 301):
        eval_word = "not so good"
    else:
        eval_word = "bad"
    return eval_word




# #############################################################

#hlavní funkce, ve které volám předem vytvořené podfunkce

def main():
    print_welcome()
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
    print_line_separator()



if __name__ == "__main__":
    main()


