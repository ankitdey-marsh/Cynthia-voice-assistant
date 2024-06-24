from datetime import datetime
import random

bot_name="Cynthia"
user_name="Genius"

def time_of_day():
    now=datetime.now()
    current_time=now.strftime("%H:%M:%S")
    h=int(current_time[0:2])
    if h>=5 and h<12:
        return "Good Morning!"
    elif h>=12 and h<16:
        return "Good Afternoon!"
    elif h>=16 and h<=23:
        return "Good Evening!"
    elif h>=0 and h<5:
        return "Its Midnight!"

def about_bot():
    text1=f"So hi! I am {bot_name} and I am your virtual assistant. Presently I can check the weather, fetch queries, send whatsapp texts and send your computer to sleep mode."
    text2=f"So hi! I am {bot_name} and I am your virtual assistant. Presently I can check search up queries, send whatsapp texts, check the weather. Oh yes! I can also make the laptop sleep."
    texts=[]
    texts.append(text1)
    texts.append(text2)
    return texts[random.randint(0,1)]

def greetings():
    return f"{time_of_day()} {user_name}. Cynthia is up and waiting for you."
