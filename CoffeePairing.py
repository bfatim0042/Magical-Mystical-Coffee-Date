#general libraries 
import pandas as pd
import csv
import random
import copy
import os
#import send_email
#import text_functions  

#libraries to handle API
import gspread
from google.oauth2.service_account import Credentials

def create_pairings(): 
    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    #Instructions to access the key are in the documentation 
    creds = Credentials.from_service_account_file("key.json", scopes=SCOPES)
    client = gspread.authorize(creds)

    #Opening the sheet attached to the Google Form responses 
    sheet = client.open_by_key("1_3pTBJ4FE_9h_2rRM-5GXTPmuSc4UESqrP-Z3Fx3ZxU").sheet1

    #Put entries into variable named data
    data = sheet.get_all_records()

    #Copy sheets data into the participants csv, creating correct headers, etc
    with open("participants.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Your name:", "Your email address:"])

        for row in data:
            writer.writerow([row["Your name:"], row["Your email address:"]])

    #Path to the CSV files with participant data
    participants_csv = "participants.csv"

    #Header names in the CSV file (name and e-mail of participants)
    header_name = "Your name:"
    header_email = "Your email address:"

    # path to TXT file that stores the pairings of this round
    new_pairs_txt = "Coffee Partner Lottery new pairs.txt"

    # path to CSV file that stores the pairings of this round
    new_pairs_csv = "Coffee Partner Lottery new pairs.csv"

    # path to CSV file that stores all pairings (to avoid repetition)
    all_pairs_csv = "Coffee Partner Lottery all pairs.csv"

    # init set of old pairs
    opairs = set()
    # init set of new pairs
    npairs = set()

    DELIMITER=','
    # load participant's data
    formdata = pd.read_csv(participants_csv, sep=DELIMITER)

    participants = list(set(formdata[header_email]))
    nparticipants = copy.deepcopy(participants)
    # set maximum group size to *half* of amount of participants
    maximumGSize = float.__floor__(len(nparticipants) / 2)

    while True:
        choise = int(input("Do you want random group sizes (0) or choose manually (1)? "))
        if choise == 0:
            gsize = random.randint(2, maximumGSize)
            print(f"Creating groups of {gsize}...")

        elif choise == 1:
            # ask for group sizes between 2 and maximum group size
            gsize = int(input(f"  How many participants should be paired together?\n  Input full number between 2 and {maximumGSize}: "))
            # check for valid input
            if gsize < 2 or gsize > maximumGSize:
                print("This is not a valid input. Please choose again.")
                continue

        else:
            print("This is not a valid input. Please choose again.")
            continue

        break

    # Boolean flag to check if new pairing has been found
    new_pairs_found = False

    def createGroup(newParticipants, groupSize):
        participant = random.choice(newParticipants)
        newParticipants.remove(participant)
        if groupSize < 2:
            return [participant]
        else:
            return [participant] + createGroup(newParticipants, groupSize - 1)

    # try creating new pairing until successful
    while not new_pairs_found:   # to do: add a maximum number of tries

        remainder = len(participants) % gsize
        # if odd number of participants
        if remainder != 0:
            quotient = len(participants) // gsize

            # try creating groups of other sizes for the amount of possible groups + 1
            for i in range(quotient + 1):
                # if even groups can be created, end loop
                if remainder <= 0:
                    break

                # if at last loop, just put all remaining people in a group
                if i == quotient:
                    plist = createGroup(nparticipants, remainder)

                # else if remainder is big enough just put all in 1 group
                elif remainder > gsize / 2:
                    plist = createGroup(nparticipants, remainder)
                    remainder = 0
                # else if remainder is even add 2 to group size
                elif remainder % 2 == 0:
                    plist = createGroup(nparticipants, gsize + 2)
                    remainder -= 2
                # or just 1
                else:
                    plist = createGroup(nparticipants, gsize + 1)
                    remainder -= 1
                
                # whatever group is created, sort it
                plist.sort()
                                
                # add alphabetically sorted list to set of pairs
                npairs.add(tuple(plist))

        # while still participants left to pair...
        while len(nparticipants) > 0:

            # create alphabetically sorted list of participants
            plist = createGroup(nparticipants, gsize)
            plist.sort()

            # add alphabetically sorted list to set of pairs
            npairs.add(tuple(plist))

        # check if all new pairs are indeed new, else reset
        if npairs.isdisjoint(opairs):
            new_pairs_found = True
        else:
            npairs = set()
            nparticipants = copy.deepcopy(participants)

        
            # check if all new pairs are indeed new, else reset
            if npairs.isdisjoint(opairs):
                new_pairs_found = True
            else:
                npairs = set()
                nparticipants = copy.deepcopy(participants)


        # assemble output for printout
        output_string = ""

        output_string += "------------------------\n"
        output_string += "Today's coffee partners:\n"
        output_string += "------------------------\n"

        for pair in npairs:
            pair = list(pair)
            output_string += "* "
            for i in range(0,len(pair)):
                name_email_pair = f"{formdata[formdata[header_email] == pair[i]].iloc[0][header_name]} ({pair[i]})"
                if i < len(pair)-1:
                    output_string += name_email_pair + ", "
                else:
                    output_string += name_email_pair + "\n"
            
        # write output to console
        print(output_string)

        # write output into text file for later use
        with open(new_pairs_txt, "wb") as file:
            file.write(output_string.encode("utf8"))

        # write new pairs into CSV file (for e.g. use in MailMerge)
        with open(new_pairs_csv, "w") as file:
            header = ["name1", "email1", "name2", "email2", "name3", "email3"]
            file.write(DELIMITER.join(header) + "\n")
            for pair in npairs:
                pair = list(pair)
                for i in range(0,len(pair)):
                    name_email_pair = f"{formdata[formdata[header_email] == pair[i]].iloc[0][header_name]}{DELIMITER} {pair[i]}"
                    if i < len(pair)-1:
                        file.write(name_email_pair + DELIMITER + " ")
                    else:
                        file.write(name_email_pair + "\n")
                        
        # append pairs to history file
        if os.path.exists(all_pairs_csv):
            mode = "a"
        else:
            mode = "w"

        with open(all_pairs_csv, mode) as file:
            for pair in npairs:
                pair = list(pair)
                for i in range(0,len(pair)):
                    if i < len(pair)-1:
                        file.write(pair[i] + DELIMITER)
                    else:
                        file.write(pair[i] + "\n")
                    
        # print finishing message
        print()
        print("Job done.")
        import text_functions



#function to 
def introduction():
    print("Welcome to the Coffee Pairing! First you must sign up by going to this link: https://docs.google.com/forms/d/e/1FAIpQLSfTtx1Zv_239qeMjlAAfU8BOABsQGbILvXG9_RGsnLRJbB_BQ/viewform?usp=dialog")
    begin = input("Once you're done, hit enter to proceed")
    if begin == "":
        print("Your group will be formed shortly!")
        create_pairings()
    else:
        print("Invalid input!")
        introduction()

#start the pairings
introduction()
