import shutil
import os

def audiofileremove():
    folder_path1 = "C:/Coding/Own/Python/VoiceChat/speech"      #use own path
    try:
        shutil.rmtree(folder_path1)
    except OSError as e:
        pass
    
    folder_path2= "C:/Coding/Own/Python/VoiceChat/PyWhatKit_DB.txt"      #use own path
    try:
        os.remove(folder_path2)
    except OSError as e:
        pass
