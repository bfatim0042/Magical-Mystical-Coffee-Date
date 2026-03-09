import pandas as pd
import csv
import random
import copy
import os
#test
#test
#test1

# path to the CSV files with participant data
participants_csv = "Coffee Partner Lottery participants.csv"

# header names in the CSV file (name and e-mail of participants)
header_name = "Your name:"
header_email = "Your e-mail:"

# path to TXT file that stores the pairings of this round
new_pairs_txt = "Coffee Partner Lottery new pairs.txt"

# path to CSV file that stores the pairings of this round
new_pairs_csv = "Coffee Partner Lottery new pairs.csv"

# path to CSV file that stores all pairings (to avoid repetition)
all_pairs_csv = "Coffee Partner Lottery all pairs.csv"
        
# init set of old pairs
opairs = set()

DELIMITER=','

# load all previous pairings (to avoid redundancies)
if os.path.exists(all_pairs_csv):
    with open(all_pairs_csv, "r") as file:
        csvreader = csv.reader(file, delimiter=DELIMITER)
        for row in csvreader:
            group = []
            for i in range(0,len(row)):
                group.append(row[i])                        
            opairs.add(tuple(group))

# load participant's data
formdata = pd.read_csv(participants_csv, sep=DELIMITER)

# create duplicate-free list of participants
participants = list(set(formdata[header_email]))

 # init set of new pairs
npairs = set()

# running set of participants
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
