# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 10:26:12 2026

@author: Lucia
"""
#install first
#pip install pingram-python
import asyncio
from pingram import Pingram

import os
from dotenv import load_dotenv
# load api variable
load_dotenv()

async def send_email(email,ice_breaker):
    api_key = os.getenv("PINGRAM_API_KEY")
    async with Pingram(api_key=api_key, 
    base_url="https://api.pingram.io") as client:
        await client.send({
            "type": "Coffee_Partner_lottery_email",
            "to": {
                "id": email,
                "email": email,
            },
            "email": {
                "subject": "Weekly Coffee Partner Lottery",
                "html": f"""<h1>Welcome to the Weekly Coffee Partner Lottery!</
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

