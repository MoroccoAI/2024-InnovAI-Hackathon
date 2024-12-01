import requests
import os
import re

def sendMail(target, subject, message): 
    url = "https://rapidprod-sendgrid-v1.p.rapidapi.com/mail/send"

    payload = {
        "personalizations": [
            {
                "to": [{"email": target}],
                "subject": subject
            }
        ],
        "from": {"email": "StockSensei@bot.ai"},
        "content": [
            {
                "type": "text/html",
                "value": message
            }
        ]
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "01859bbbdbmsh5ef4be697540182p16dee3jsnd363a79130f7",
        "X-RapidAPI-Host": "rapidprod-sendgrid-v1.p.rapidapi.com"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    