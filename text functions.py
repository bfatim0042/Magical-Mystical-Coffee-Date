#defining function to create a text file document
#write on it, and close it
def create_text_file(text_file, comment):
    file=open(f"{text_file}", "w")
    file.write(comment)
    file.close()
    if file.close()==True:
       return print(f"Text file document created and /n comment written succesfully in {text_file}") 
   
#defining function to write a comment in an already
#existing text file, then close it
def add_text(text_file, comment):
        file=open(f"{text_file}", "a")
        file.write(comment)
        file.close()
        if file.close()==True:
           return print(f"Comment written succesfully in {text_file}") 

#defining function to print the content of a text file
#on the console
def print_text_file(file):
        myFile=open(f"{file}", "r")
        content = myFile.read()
        print(content)
        myFile.close()
        
def group_len(group):
          g_size=len(group)
          return g_size
      
#install first
#pip install pingram-python
import asyncio
from pingram import Pingram

import os
from dotenv import load_dotenv
# load api variable
load_dotenv()

#define function that sends emails. Variables: email of the participant, 
#and ice_breaker of this round
async def send_email(email, name, ice_breaker):
#load our API key, docuemnt containing it must be in the sam efolder as this PY document
    api_key = os.getenv("PINGRAM_API_KEY")
    async with Pingram(api_key=api_key,
#Pingram main page as base url
    base_url="https://api.pingram.io") as client:
        await client.send({
            "type": "Coffee_Partner_lottery_email",
            "to": {
                "id": email,
                "email": email,
            },
            "email": {
                "subject": "Weekly Coffee Partner Lottery",
#\033[1m and \033[0m open and closes bold text respectively
                "html": f"""<h1>Welcome to the Weekly Coffee Partner Lottery \033[1m{name}\033[0m !</
                h1><p>Thanks for joining our Weekly Coffee Partner Lottery. /n
                It is a pleasure to have you with us.

                As every week, you have been assigned to a group for an \033[1minformal coffee meeting\033[0m./n
                Here is the \033[1mice breaker\033[0m of the week:
                    
                {ice_breaker}
                
                Tahnk you again for participating! /n
                
                We wish you the best in the coffee hang out with the rest of your team!/n
                
                Best,
                Bea, Markus, Fatih and Lucía
                
                 </p>
                """,
                "senderName": "Group 1",
                "senderEmail":
                "coffeeprojectgroup1@gmail.com"
            }
        })

asyncio.run(send_email())
      
        
name1="Ice_breaker_round_1"
comment_ice_breaker1="Why did the coffee file a police report?\n\nBecause it got mugged!"
writting=create_text_file(name1, comment_ice_breaker1)

name2="Ice_breaker_round_2"
comment_ice_breaker2="Why was the coffee rude earlier? \n\nBecause it had no filter!"
writting=create_text_file(name2, comment_ice_breaker2)

name3="Ice_breaker_round_3"
comment_ice_breaker3="Decide in which order to introduce each other by playing a \n\nRock-Paper-Scissors tournament!"
writting=create_text_file(name3, comment_ice_breaker3)

name4="Ice_breaker_round_4"
comment_ice_breaker4="SHOW AND TELL time! \n\nStart the hang out showing your fit and explaining where you got each item. \n(be oddly specific)"
writting=create_text_file(name4, comment_ice_breaker4)

name5="Ice_breaker_round_5"
comment_ice_breaker5="Bring to the meeting your favourite pen \n\nTell the rest of the group why you like it and how did you get it."
writting=create_text_file(name5, comment_ice_breaker5)

name6="Ice_breaker_round_6"
comment_ice_breaker6="DEBATE time! \n\nStart the hang out debating whether you think coffee is good for human's health."
writting=create_text_file(name6, comment_ice_breaker6)

name7="Ice_breaker_round_7"
comment_ice_breaker7="Talk about:\nDo you have any games on your phone? \n\nIf so, which ones and why you like them? \n\nIf not, why not?"
writting=create_text_file(name7, comment_ice_breaker7)

import random
random_ice_breaker=random.randint(1,7)
print(f"The random ice breaker of this round is:\n{random_ice_breaker}\n")

#Print the random ice_breaker
if random_ice_breaker==1:
    print_text_file(name1)
    ice_breaker_n=comment_ice_breaker1
elif random_ice_breaker==2:
    print_text_file(name2)
    ice_breaker_n=comment_ice_breaker2
elif random_ice_breaker==3:
    print_text_file(name3)
    ice_breaker_n=comment_ice_breaker3
elif random_ice_breaker==4:
    print_text_file(name4)
    ice_breaker_n=comment_ice_breaker4
elif random_ice_breaker==5:
    print_text_file(name5)
    ice_breaker_n=comment_ice_breaker5
elif random_ice_breaker==6:
    print_text_file(name6)
    ice_breaker_n=comment_ice_breaker6
elif random_ice_breaker==7:
    print_text_file(name7)
    ice_breaker_n=comment_ice_breaker7


group=[0,1]
group_len=group_len(group)
print(f"There are {group_len} participants in this group")

for email in range(group):
    email_participant=send_email(email, name_part, ice_breaker_n)