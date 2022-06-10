#!/usr/bin/env python3

from multielo import MultiElo
import json
import numpy as np
import random
import os
import os.path

on = True
players = {}
elo = MultiElo()
#for elo.get_new_ratings(np.array([a, b])) a is the winner and the return is [new_a, new_b] of type numpy.ndarray

def comparison(comps):
    keys_list = list(players)
    for i in range(int(comps)):
        one = keys_list[random.randint(0, len(keys_list) - 1)]

        same = True
        while same:
            two = keys_list[random.randint(0, len(keys_list) - 1)]
            if one != two:
                same = False

        print("1. " + one + " vs 2. " + two)
        ans = input("Please enter 1 or 2 (any other selection ends comparison): ")

        if ans == "1":
            results = elo.get_new_ratings(np.array([players[one], players[two]]))
            players[one] = results[0]
            players[two] = results[1]
        elif ans == "2":
            results = elo.get_new_ratings(np.array([players[two], players[one]]))
            players[two] = results[0]
            players[one] = results[1]
        else:
            break
    return

def load_new():
    lines = []
    f = open("list.txt", "r")
    for i in f:
        lines.append(i.strip())
    f.close()
    for i in lines:
        players[i] = 1000
    return

def load_sav():
    print("\nIMPORTANT: Please make sure your save data is named list.sav and is in the same directoy as elo-compare.py.")
    input("Press enter to continue:")
    f = open("list.sav", "r")
    data = f.read()
    data = data.replace("\'", "\"")
    players = json.loads(data)
    f.close()
    print("Data loaded")
    return players

while on:
    print("\n---Menu---\n1. Collect Data for Comparisons\n2. Load Previous Data\n3. Run Comparisons\n4. Print Current Rankings\n5. Check Specific Entry\n6. Save & Exit")
    choice = input("Enter the number of your choice: ")

    if choice == "1":
        file_name = "list.sav"
        cur_dir = os.getcwd()
        sav_found = False
        while True:
            file_list = os.listdir(cur_dir)
            parent_dir = os.path.dirname(cur_dir)
            if file_name in file_list:
                sav_found = True
                break
            else:
                break

        if len(players) != 0:
            ask = input("\nA file is already loaded. Overwrite? y/n: ")
            if ask == "y":
                load_new()
                print("Data loaded")
            else:
                print("n or other was recieved. Data was not loaded.")

        elif sav_found:
            print("\nIMPORTANT: A save file with the default name was found in this directoy.")
            input("To not lose data, rename the previous save file before continuing. Press enter to continue: ")
            load_new()
            print("Data loaded")

        else:
            load_new()
            print("Data loaded")


    elif choice == "2":
        if len(players) != 0:
            ask = input("\nIMPORTANT: A file is already loaded. Load another file anyway? y/n: ")
            if ask == "y":
                players = load_sav()
            else:
                print("n or other was selected. Data not loaded.")
        else:
            players = load_sav()

    elif choice == "3":
        if len(players) <= 1:
            print("You have less than two items... What are you comparing?")

        else:
            print("\nHow many comparisons would you like to make?")
            print("The more you make the more accurate your result will be.")
            print("If at any time you wish to stop enter anything other than 1 or 2.")
            comps = input("# of Comparisons: ")
            if comps.isnumeric():
                comparison(comps)

            else:
                print("\nThat wasn't a whole number greater than 0....")

    elif choice == "4":
        kv_list = sorted(players.items(), key = lambda kv:(kv[1], kv[0]), reverse = True)
        ans = input("\nPrint how many? Input a number (as digits) or all: ")

        rank = 1
        prev_ELO = 0
        curr_ELO = 0
        tie = 1
        if ans == "all":
            for i in kv_list:
                curr_ELO = i[1]
                if rank == 1:
                    print(str(rank) + ". " + i[0] + ": ELO score - " + str(i[1]))
                    prev_ELO = i[1]
                elif curr_ELO == prev_ELO:
                    print(str(tie) + ". " + i[0] + ": ELO score - " + str(i[1]))
                else:
                    print(str(rank) + ". " + i[0] + ": ELO score - " + str(i[1]))
                    prev_ELO = i[1]
                    tie = rank
                rank = rank + 1
        elif ans.isnumeric():
            for i in range(0, int(ans)):
                curr_ELO = kv_list[i][1]
                if rank == 1:
                    print(str(rank) + ". " + kv_list[i][0] + ": ELO score - " + str(kv_list[i][1]))
                    prev_ELO = kv_list[i][1]
                elif curr_ELO == prev_ELO:
                    print(str(tie) + ". " + kv_list[i][0] + ": ELO score - " + str(kv_list[i][1]))
                else:
                    print(str(rank) + ". " + kv_list[i][0] + ": ELO score - " + str(kv_list[i][1]))
                    prev_ELO = kv_list[i][1]
                    tie = rank
                rank = rank + 1
        else:
            print("You did not enter a digit or all.")

    elif choice == "5":
        key = input("\nPlease type the name of the entry you'd like to check exactly: ")
        if key in players.keys():
            print(key + "\'s ELO rating is " + str(players[key]))
        else:
            print(key + " was not found. Did you make a typo?")

    elif choice == "6":
        f = open("list.sav", "w")
        save_data = str(players)
        f.write(save_data)
        on = False

    else:
        print("\nI don't know what that was, but it wasn't a number between 1 and 6...")
