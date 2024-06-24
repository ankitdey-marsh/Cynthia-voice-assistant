import pywhatkit
from datetime import datetime
import pyautogui
import time
import sys

def send_msg(msg,person):
    c=datetime.now()
    time=c.strftime('%H:%M:%S')
    hour=int(time[0:2])
    m=int(time[3:5])+1
    sec=int(time[6:8])
    if sec>=50:
        m+=1
    if m>=60:
        m=m%60
        hour+=1
    if hour==24:
        hour=0
    sending(msg,person,hour,m)

def sending(msg,person,hour,m):
    try:

        person='your-country-code'+person 
        pywhatkit.sendwhatmsg(person,msg,hour,m,10)
        time.sleep(2)
        pyautogui.press('enter')
        pyautogui.hotkey('ctrl','w')
        pyautogui.hotkey('ctrl', 'shift', 'w')
        
    except:
        print("Error while sending msg")



