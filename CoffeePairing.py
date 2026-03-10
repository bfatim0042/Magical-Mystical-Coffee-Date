# general libraries
import pandas as pd
import csv
import random
import copy
import os
from itertools import combinations
# import send_email
# import text_functions

# libraries to handle API
import gspread
from google.oauth2.service_account import Credentials


def create_pairings():
    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    # Instructions to access the key are in the documentation
    creds = Credentials.from_service_account_file("key.json", scopes=SCOPES)
    client = gspread.authorize(creds)

    # Opening the sheet attached to the Google Form responses
    sheet = client.open_by_key("1_3pTBJ4FE_9h_2rRM-5GXTPmuSc4UESqrP-Z3Fx3ZxU").sheet1

    # Put entries into variable named data
    data = sheet.get_all_records()

    # Copy sheets data into the participants csv, creating correct headers, etc
    with open("participants.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Your name:", "Your email address:"])

        for row in data:
            writer.writerow([row["Your name:"], row["Your email address:"]])

    # Path to the CSV files with participant data
    participants_csv = "participants.csv"

    # Header names in the CSV file (name and e-mail of participants)
    header_name = "Your name:"
    header_email = "Your email address:"

    # Path to TXT file that stores the pairings of this round
    new_pairs_txt = "Coffee Partner Lottery new pairs.txt"

    # Path to CSV file that stores the pairings of this round
    new_pairs_csv = "Coffee Partner Lottery new pairs.csv"

    # Path to CSV file that stores all pairings/groups history
    all_pairs_csv = "Coffee Partner Lottery all pairs.csv"

    DELIMITER = ','

    # load participant data
    formdata = pd.read_csv(participants_csv, sep=DELIMITER)

    participants = list(set(formdata[header_email].dropna()))
    nparticipants = copy.deepcopy(participants)

    # set maximum group size to half of amount of participants
    maximumGSize = float.__floor__(len(nparticipants) / 2)

    while True:
        choise = int(input("Do you want random group sizes (0) or choose manually (1)? "))
        if choise == 0:
            gsize = random.randint(2, maximumGSize)
            print(f"Creating groups of {gsize}...")

        elif choise == 1:
            gsize = int(input(f"  How many participants should be paired together?\n  Input full number between 2 and {maximumGSize}: "))
            if gsize < 2 or gsize > maximumGSize:
                print("This is not a valid input. Please choose again.")
                continue

        else:
            print("This is not a valid input. Please choose again.")
            continue

        break

    def createGroup(newParticipants, groupSize):
        participant = random.choice(newParticipants)
        newParticipants.remove(participant)
        if groupSize < 2:
            return [participant]
        else:
            return [participant] + createGroup(newParticipants, groupSize - 1)
        
        
        #Reads previous groups from the history file and returns a set of pair-tuples like ('a@email.com', 'b@email.com').
    def load_old_pair_history(history_file):
           
        old_pairs = set()

        if not os.path.exists(history_file):
            return old_pairs

        with open(history_file, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=DELIMITER)
            for row in reader:
                # remove empty entries/spaces
                group = [item.strip() for item in row if item.strip() != ""]
                if len(group) < 2:
                    continue

                # store every pair inside the historical group
                for pair in combinations(sorted(group), 2):
                    old_pairs.add(pair)

        return old_pairs

    def group_has_redundant_match(group, old_pair_history):
        """
        Returns True if any pair inside this group has already appeared before.
        """
        for pair in combinations(sorted(group), 2):
            if pair in old_pair_history:
                return True
        return False
    #Returns True only if none of the internal pairs in any group has appeared in previous rounds.
    def all_groups_are_new(groups, old_pair_history):
        
        for group in groups:
            if group_has_redundant_match(group, old_pair_history):
                return False
        return True

    # load old pair history from previous rounds
    old_pair_history = load_old_pair_history(all_pairs_csv)

    # Boolean flag to check if new pairing has been found
    new_pairs_found = False

    # prevent infinite loop if perfect non-redundant solution is impossible
    max_tries = 1000
    tries = 0

    # try creating new pairing until successful
    while not new_pairs_found and tries < max_tries:
        tries += 1

        npairs = set()
        nparticipants = copy.deepcopy(participants)

        remainder = len(participants) % gsize

        # if number of participants is not divisible by group size
        if remainder != 0:
            quotient = len(participants) // gsize

            for i in range(quotient + 1):
                if remainder <= 0:
                    break

                if i == quotient:
                    plist = createGroup(nparticipants, remainder)

                elif remainder > gsize / 2:
                    plist = createGroup(nparticipants, remainder)
                    remainder = 0

                elif remainder % 2 == 0:
                    plist = createGroup(nparticipants, gsize + 2)
                    remainder -= 2

                else:
                    plist = createGroup(nparticipants, gsize + 1)
                    remainder -= 1

                plist.sort()
                npairs.add(tuple(plist))

        # while still participants left to pair...
        while len(nparticipants) > 0:
            plist = createGroup(nparticipants, gsize)
            plist.sort()
            npairs.add(tuple(plist))

        # NEW CHECK:
        # do not accept new groups if any internal pair already happened before
        if all_groups_are_new(npairs, old_pair_history):
            new_pairs_found = True

    # if no perfect new matching was found, fall back to the last generated round
    if not new_pairs_found:
        print("\nWarning: Could not fully avoid redundant matchings.")
        print("A best-effort grouping was generated instead.\n")

    # assemble output for printout
    output_string = ""
    output_string += "------------------------\n"
    output_string += "Today's coffee partners:\n"
    output_string += "------------------------\n"

    for pair in npairs:
        pair = list(pair)
        output_string += "* "
        for i in range(0, len(pair)):
            name_email_pair = f"{formdata[formdata[header_email] == pair[i]].iloc[0][header_name]} ({pair[i]})"
            if i < len(pair) - 1:
                output_string += name_email_pair + ", "
            else:
                output_string += name_email_pair + "\n"

    # write output to console
    print(output_string)

    # write output into text file for later use
    with open(new_pairs_txt, "wb") as file:
        file.write(output_string.encode("utf8"))

    # write new pairs into CSV file (for e.g. use in MailMerge)
    with open(new_pairs_csv, "w", encoding="utf-8") as file:
        header = ["name1", "email1", "name2", "email2", "name3", "email3"]
        file.write(DELIMITER.join(header) + "\n")
        for pair in npairs:
            pair = list(pair)
            for i in range(0, len(pair)):
                name_email_pair = f"{formdata[formdata[header_email] == pair[i]].iloc[0][header_name]}{DELIMITER}{pair[i]}"
                if i < len(pair) - 1:
                    file.write(name_email_pair + DELIMITER)
                else:
                    file.write(name_email_pair + "\n")

    
    # each row is one group; later we convert each row into all internal pairs
    if os.path.exists(all_pairs_csv):
        mode = "a"
    else:
        mode = "w"

    with open(all_pairs_csv, mode, newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=DELIMITER)
        for group in npairs:
            writer.writerow(list(group))

    # print finishing message
    print()
    print("Job done.")
    import text_functions


def introduction():
    print("Welcome to the Coffee Pairing! First you must sign up by going to this link: https://docs.google.com/forms/d/e/1FAIpQLSfTtx1Zv_239qeMjlAAfU8BOABsQGbILvXG9_RGsnLRJbB_BQ/viewform?usp=dialog")
    begin = input("Once you're done, hit enter to proceed")
    if begin == "":
        print("Your group will be formed shortly!")
        create_pairings()
    else:
        print("Invalid input!")
        introduction()


# start the pairings
introduction()