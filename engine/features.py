import os
import re
from shlex import quote
import sqlite3
import struct
import time
import webbrowser
from playsound import playsound
import eel
import pyaudio
import pyautogui
from engine.command import speak
from engine.config import ASSISTANT_NAME
import pywhatkit as kit
import pvporcupine
from engine.helper import adbInput, extract_yt_term, goback, keyEvent, remove_words, tapEvents
from hugchat import hugchat
import subprocess

conn = sqlite3.connect("jarvis.db")
cursor = conn.cursor()

# playAssistantSound
@eel.expose                                            #main.js se access karne ke liye
def playAssistantSound():
    music_dir="frontend//assets//audio//music.mp3"
    playsound(music_dir)


def openCommand(query):
    query=query.replace(ASSISTANT_NAME, "")
    query=query.replace("open", "")
    query.lower()


    app_name = query.strip()
    if app_name != "":

        try:
            cursor.execute('SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT path FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")


    # if query!="":
    #     speak("Opening"+query)
    #     os.system('start'+query)
    # else:
    #     speak("not found")



def PlayYoutube(query):
    search_term=extract_yt_term(query)
    # speak("Playing "+ search_term + " on Youtube")
    speak("Playing "+ search_term )
    kit.playonyt(search_term)


def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["jarvis","alexa"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()


# find contacts
def findContact(query):
    
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])
        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str
            print(mobile_number_str)

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0
    


def whatsApp(mobile_no, message, flag, name):

    if flag == 'message':
        target_tab = 12
        jarvis_message = "message send successfully to "+name

    elif flag == 'call':
        target_tab = 7
        message = ''
        jarvis_message = "calling to "+name

    else:
        target_tab = 6
        message = ''
        jarvis_message = "staring video call with "+name
   
    # Encode the message for URL
    encoded_message = quote(message)

    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"
   
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab+1):
       
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(jarvis_message)

# "C:\Users\vp729\OneDrive\Desktop\WhatsApp Installer.exe"

# chat bot 

def chatBot(query):
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path="engine/cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response =  chatbot.chat(user_input)
    
    print(response)
    speak(response)
    return response

# android automation

def makeCall(name, mobileNo):
    mobileNo =mobileNo.replace(" ", "")
    speak("Calling "+name)
    command = 'adb shell am start -a android.intent.action.CALL -d tel:'+mobileNo
    os.system(command)



    
# Function to delete last sent message to a contact
def deleteMessage(contact_name):
    mobile_no, found_name = findContact(contact_name)

    if mobile_no == 0:
        speak(f"{contact_name} ka number nahi mila.")
        return
    
    speak(f"Deleting last message to {found_name}")


# to send message
def sendMessage(message, mobileNo, name):
    from engine.helper import replace_spaces_with_percent_s, goback, keyEvent, tapEvents, adbInput
    message = replace_spaces_with_percent_s(message)
    mobileNo = replace_spaces_with_percent_s(mobileNo)
    
    speak("sending message")

    goback(4)
    time.sleep(5)
    keyEvent(3)
    # open sms app
    tapEvents(358, 2223)
    #start chat
    tapEvents(806,2325)
    # search mobile no
    adbInput(mobileNo)
    #tap on name
    tapEvents(996, 2336)
    # tap on input
    tapEvents(312, 1528)
    #messagej
    adbInput(message)
    #send
    tapEvents(986, 1468)
    speak("message send successfully to "+name)

# Open Notification Pan
def openNotificationPanel():
    # speak("open notification panel")

    # ADB command to open notification panel
    os.system("adb shell input swipe 500 50 500 1200")


def searchGoogle(query):
    speak(f"Searching {query} on Google in your mobile.")
    
    # ADB command to search on Google (for mobile only)
    command = f"adb shell am start -a android.intent.action.VIEW -d \"https://www.google.com/search?q={query}\""
    # command = f"adb shell am start -a android.intent.action.VIEW -d \"https://www.youtube.com/search?q={query}\""
    os.system(command)


def control_wifi(state):
    if state == "on":
        os.system("adb shell svc wifi enable")
        speak("WiFi has been turned on")  # ✅ Jarvis bolega
    elif state == "off":
        os.system("adb shell svc wifi disable")
        speak("WiFi has been turned off")  # ✅ Jarvis bolega
    else:
        speak("Invalid WiFi state")


def swipe(direction):
    if direction == "up":
        os.system("adb shell input swipe 500 1500 500 500 ")
    elif direction == "down":
        os.system("adb shell input swipe 500 500 500 1500")
    elif direction == "left":
        os.system("adb shell input swipe 1000 1000 100 1000")
    elif direction == "right":
        os.system("adb shell input swipe 100 1000 1000 1000")
    else:
        return
    print(f"Performed swipe {direction}")


def open_recent_apps():
    """Opens the recent apps screen from the home screen."""
    os.system("adb shell input keyevent KEYCODE_HOME")  # Home screen
    time.sleep(1)
    os.system("adb shell input keyevent KEYCODE_APP_SWITCH")  # Open recent apps
    time.sleep(1)
    print("Recent apps opened.")

def move_recent_apps(direction):
    """Moves left or right in the recent apps list."""
    if direction == "left":
        os.system("adb shell input swipe 300 800 700 800")  # Swipe right to move left
    elif direction == "right":
        os.system("adb shell input swipe 700 800 300 800")  # Swipe left to move right
    print(f"Moved {direction} in recent apps.")

def choose_recent_app():
    """Selects the currently focused app from the recent apps list."""
    os.system("adb shell input tap 500 800")  # Tap in the center to open the selected app
    print("Chosen the selected app.")


