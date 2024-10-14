"""
projekt_2.py: druhý projekt do Engeto Online Python Akademie

author: Tereza Růžičková
email: terkaruzicka@seznam.cz
discord: terka_99
"""
# knihovna random pro generování náhodných čísel
# knihovna sys pro ukončení programu při nesplnění podmínky

import random
import sys

print("Hi there!")
print("I've generated a random 4 digit number for you.")
print("Let's play a bulls and cows game.")

# generace náhodného čtyřmístného čísla
# while cyklus se opakuje dokud se nevygeneruje čtyřmístné číslo s unikátními číslicemi
ran_num_list = list()

while len(ran_num_list) != 4:
    ran_num_list = list()
    ran_num = random.randint(1000, 9999)
    ran_num_str = str(ran_num)
    for i in ran_num_str:
        if i not in ran_num_list:
            ran_num_list.append(i)
        
print(ran_num_list)
print(ran_num)

print("Let's play a bulls and cows game.")
print("Enter a number:")

# uživatelský vstup
user_input = input()
print(">>>", user_input)

# ověření, že zadaná hodnota neobsahuje nečíselné znaky
if user_input.isdigit() is not True:
    print("Number cannot contain non-numeric values.")
    #sys.exit()

# ověření, že zadaná hodnota nezačíná nulou    
if user_input[0] == "0":
    print("Number cannot start with a zero.")
    #sys.exit()

#ověření, že zadané číslo je čtyřmístné    
input_num = int(user_input)

if input_num not in range(1000, 10000):
    print("Number does not contain four digits.")
    #sys.exit()

# ověření, že zadané číslo obsahuje unikátní číslice
user_input_list = list()
for k in user_input:
    if k not in user_input_list:
        user_input_list.append(k)

if len(user_input_list) != 4:
    print("Číslo musí obsahovat unikátní číslice.")
    #sys.exit()

bull_count = 0
cow_count = 0

for m in range(4):
    if ran_num_str[m] == user_input[m]:
        bull_count += 1
    elif ran_num_str[m] in user_input_list:
        cow_count +=1

if bull_count == 1:
    print(bull_count, "bull")
else:
    print(bull_count, "bulls")

if cow_count == 1:
    print(cow_count, "cow")
else:
    print(cow_count, "cows")
