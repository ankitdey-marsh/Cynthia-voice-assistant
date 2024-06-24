import azure.cognitiveservices.speech as speech 
import google.generativeai as genai  
import os
import time
from google.cloud import texttospeech
import winsound
import random
import weather as wth
import whatsapp as wp
import junkcleanup as jc
import lockwindows as lw
import threading
import sys
import about as abt
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

#   spotify api
client_id= 'your-spotify-client-key'
client_secret= 'your-client-secret'
redirect_uri = 'your-redirect-uri'

sp_oauth = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=['user-read-playback-state', 'user-modify-playback-state', 'streaming'])
sp=spotipy.Spotify(auth_manager=sp_oauth)


#   genai api for gemini
genai.configure(api_key="your-api-key") 
generation_config={"temperature":0.9,"top_p":1,"top_k":1,"max_output_tokens":75} 
model=genai.GenerativeModel("gemini-pro",generation_config=generation_config)


#   azure api
AZURE_SPEECH_KEY="your-api-key"     
AZURE_SPEECH_REGION="eastus"

#   gcp key file
os.environ['GOOGLE_APPLICATION_CREDENTIALS']='your-gcp-key-file-absolute-path'
client = texttospeech.TextToSpeechClient()


#   function to play the song using spotify api.

def play_song(song_name):
    try:
        sp.start_playback(uris=[])
        os.system('cls' if os.name == 'nt' else 'clear')
        results = sp.search(q=song_name, type="track")
        i=0
        for track in results["tracks"]["items"]:
            i+=1
            print(f"{i}. {track['name']} by {track['artists'][0]['name']}")
            if i==5:
                break
        output=speech_recognise()
        if 'one' in output.lower() or 'first' in output.lower():
            track_id = results["tracks"]["items"][0]["id"]
            sp.start_playback(uris=['spotify:track:'+track_id])
        if 'second' in output.lower() or 'two' in output.lower():
            track_id = results["tracks"]["items"][1]["id"]
            sp.start_playback(uris=['spotify:track:'+track_id])
        if 'three' in output.lower() or 'third' in output.lower():
            track_id = results["tracks"]["items"][2]["id"]
            sp.start_playback(uris=['spotify:track:'+track_id])
        if 'four' in output.lower() or 'fourth' in output.lower():
            track_id = results["tracks"]["items"][3]["id"]
            sp.start_playback(uris=['spotify:track:'+track_id])
        if 'five' in output.lower() or 'fifth' in output.lower():
            track_id = results["tracks"]["items"][4]["id"]
            sp.start_playback(uris=['spotify:track:'+track_id])
        os.system('cls' if os.name == 'nt' else 'clear')
        track1=sp.track(track_id)
        song_name=track1['name']
        print("Playing",song_name)
    except:
        print('err')

#   speech recognition using azure speech model.
def speech_recognise():
    speech_config=speech.SpeechConfig(subscription=AZURE_SPEECH_KEY,region=AZURE_SPEECH_REGION)
    speech_config.recognition_language= "en-US"
    audio_config= speech.audio.AudioConfig(use_default_microphone=True)
    speech_recongnizer=speech.SpeechRecognizer(speech_config=speech_config,audio_config=audio_config)
    speech_recongnition_result= speech_recongnizer.recognize_once_async().get()
    output=speech_recongnition_result.text
    return output 


#   function to clear the screen and colorify the output for an input.

def chat(inp,output):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[32m"+"Your input:" +"\033[0m\t"+f"{inp}")
    print("\033[32m"+"Your output:" +"\033[0m\t")
    write_out(output)


#   function to speak out the response.

def speak(output):
    input_text = texttospeech.SynthesisInput(text=output)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Studio-O",
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16,
        speaking_rate=1.4
    )
    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )
    folder_path = "./speech"
    file_path = os.path.join(folder_path, "output.mp3")
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    with open(file_path, "wb") as out:
        out.write(response.audio_content)
    winsound.PlaySound(file_path,winsound.SND_FILENAME)    


#   primary function to intoduce the bot to the user.
#   Cynthia waits for the user to utter her name. Till then it waits and doesnt take any requests.
#   User has the choice of asking for the abilities of Cynthia, ask weather, play a song, ask any 
#   questions for ai generated answers, send whatsapp messages and put their computer to sleep.
#   Read the 'help.txt' for speech commands or speak 'Help'.

def introduce():
    x=0
    while True:
        if x==0:
            waiting_text="Waiting for you\n"
            speak(waiting_text)
            write_out(waiting_text)
            x=1
        auth=speech_recognise()
        if "cynthia".lower() in auth.lower():
            x=0
            os.system('cls' if os.name == 'nt' else 'clear')
            texts=["Hi! Cynthia here, your personal voice assistant. How may I help you?\n","Hello! I am Cynthia, how may I help you?\n","Cynthia is here to assist you.\n"]
            text=texts[random.randint(0,2)]
            print("\033[32m"+"Your output: " +"\033[0m")
            write_out(text)
            speak(text)
            while(True):
                output=speech_recognise()
                if ("hello" in output.lower() or "hi" in output.lower() or "what's up" in output.lower()) and ("you do" not in output.lower() or "abilities" not in output.lower() or "about you" not in output.lower()):
                    write_out(abt.greetings())
                    speak(abt.greetings())
                elif ("you do" in output.lower() or "about you" in output.lower() or "abilities" in output.lower()):
                    write_out(abt.about_bot())
                    speak(abt.about_bot())
                elif "search" in output or "Search" in output:
                    ai()
                    text1="\nWhat else can I do for you?"
                    write_out(text1)
                    speak(text1)
                elif "pause" in output.lower():
                    sp.pause_playback()
                elif "resume" in output.lower():
                    sp.start_playback()
                elif "play" in output.lower() or "song" in output.lower() or "music" in output.lower():
                    speak("Keep spotify open")
                    write_out("Keep spotify open")
                    x=0
                    y=0
                    while True:
                        if x == 1:
                            break
                        if y == 0:
                            write_out("What song would you like.")
                            speak("What song would you like.")   
                        output=speech_recognise()
                        y=1
                        if output != "":
                            while True:
                                write_out(f"{output}. Correct?")
                                speak(f"{output}. Correct?")
                                yesorno=speech_recognise()
                                if 'yes' in yesorno.lower() or 'fine' in yesorno.lower() or 'correct' in yesorno.lower() or "right" in yesorno.lower():
                                    play_song(output)
                                    x=1
                                    break
                                elif 'no' in yesorno.lower() or 'nope' in yesorno.lower() or 'incorrect' in yesorno.lower() or "wrong" in yesorno.lower():
                                    y=0
                                    break
                                    
                elif "weather" in output or "Weather" in output:
                    output=wth.weather()
                    print("\033[32m"+"Your output: " +"\033[0m")
                    write_out(output)
                    speak(output)
                    text1="\nWhat else can I do for you?"
                    write_out(text1)
                    speak(text1)
                elif "whatsapp" in output or "WhatsApp" in output or "What's up?" in output or "what's up?" in output:
                    text1="\nEnter the text you want to send."
                    write_out(text1)
                    speak(text1)
                    output1=speech_recognise()
                    while True:
                        text1="\nEnter the person whom you want to send to."
                        write_out(text1)
                        speak(text1)
                        output2=speech_recognise()
                        write_out(" "+output2)
                        while True:
                            speak("Is this correct?")
                            correct=speech_recognise()
                            if "Yes" in correct or "fine" in correct or "Fine" in correct or "Ya" in correct:
                                wp.send_msg(output1,output2)
                                break
                            else:
                                break

                elif " lock " in output.lower() or "Lock" in output or "sleep" in output:
                    lw.lock_windows()
                    os.system('cls' if os.name == 'nt' else 'clear')
                    sys.exit()

#   Speak words like 'shut down' or 'goodbye' to put Cynthia in idle mode, 
#   waiting to listen the keyword 'Cynthia' again.


                elif "Shut" in output or "goodbye" in output.lower() or "shut" in output or "See y" in output or "see y" in output:
                    text="\nTake Care"
                    write_out(text)
                    speak(text)
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break

#   'Apple' is the safeword, used to completely stop Cynthia's execution.

        elif "apple" in auth.lower():
            os.system('cls' if os.name == 'nt' else 'clear')
            sys.exit("Turning off Cynthia")

            
#   Function to printout the entire response or prompt to be writen out.

def write_out(output):
    for i in range(0,len(output)):
            time.sleep(0.01)
            print(output[i],end="")

#   Function that handles all the AI generation of answers by Gemini

def ai():
    print("\nSpeak now.") 
    while True:
        output=speech_recognise()
        inp=output
        if "stop" in inp.lower() or "exit" in inp.lower():
            print("\033[31m"+"\nExiting..."+"\033[0m\t")
            break

        if inp!="":
            threading.Thread(target=speech_recognise)
            response= model.generate_content(["You will generate answers within 75 tokens. Write in a continuous flow, avoiding bulleted lists. "+inp])
            s=response.text
            last_dot_index = s.rfind(".")
            if last_dot_index != -1:
                s = s[:last_dot_index+1]
                output=s
            threading.Thread(target=speak,args=[output]).start()
            time.sleep(1.2)
            threading.Thread(target=chat,args=[inp,output]).start()
            print("\nSpeak now.") 
            
        
if __name__=="__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    introduce()
    jc.audiofileremove()