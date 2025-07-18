import os
import pyttsx3
import speech_recognition as sr
import eel
import time



# from engine.features import openNotificationPanel

def speak(text):
    text=str(text)
    engine = pyttsx3.init('sapi5')
    voices=engine.getProperty('voices')
    engine.setProperty('voice',voices[1].id)
    engine.setProperty('rate',174)
    eel.DisplayMessage(text)
    # print(voices)
    # speak(voices)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()

def takecommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print('listening...')
        eel.DisplayMessage('listening...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source,10,6)
    try:
        print('recognizing..')
        eel.DisplayMessage('recognizing...')

        query=r.recognize_google(audio, language='en-in')
        # query=r.recognize_google_cloud(audio,language='en-in')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        # speak(query)
              
        time.sleep(2)
       
        # eel.ShowHood()
       
    except Exception as e:
        return ""
    
    return query.lower()

@eel.expose
def allCommands(message=1):
    if message==1:
         
        query = takecommand()
        # query = 'python tutorial on youtube'
        print(query)
        eel.senderText(query)
    else:
        query=message
        eel.senderText(query)
    try:
        from engine.features import swipe
        if "swipe up" in query:
            speak("Swiping up")
            swipe("up")

        elif "swipe down" in query:
            speak("Swiping down")
            swipe("down")

        elif "move left" in query:
            speak("Moving left")
            swipe("left")

        elif "move right" in query:
            speak("Moving right")
            swipe("right")
        from engine.features import control_wifi
        if "turn on wifi" in query:
            
            control_wifi("on")

        elif "turn off wifi" in query:
            # from engine.features import control_wifi
            print("Calling control_wifi to turn OFF") 
            control_wifi("off")
        elif "open notification panel" in query:
            from engine.features import openNotificationPanel
            openNotificationPanel()



        from engine.features import open_recent_apps, move_recent_apps, choose_recent_app
        if "open recent apps" in query:
            speak("Opening recent apps")
            open_recent_apps()

            while True:  # Loop to keep it inside Recent Apps screen
                query = takecommand()

                if "move left" in query:
                    speak("Moving left")
                    move_recent_apps("left")

                elif "move right" in query:
                    speak("Moving right")
                    move_recent_apps("right")

                elif "choose this app" in query:
                    speak("Selecting this app")
                    choose_recent_app()
                    break  # Exit loop after selecting app

                elif "exit" in query or "stop" in query:
                    speak("Exiting recent apps mode")
                    break  # Stop listening

                else:
                    speak("Command not recognized. Try again.")

        
            
        elif "search" in query and "google" in query:
            try:
                query = query.replace("search", "").replace("on google", "").strip()
                adb_status = os.popen("adb devices").read()
                if "device" in adb_status:
                    from engine.features import searchGoogle
                    searchGoogle(query)  # Sirf tabhi chalega jab ADB connected ho
                else:
                    speak("Your mobile is not connected. Please connect via ADB.")

            except Exception as e:
                print("Error while searching on Google:", str(e))
                speak("Sorry, I couldn't process your request.")

        
        if "open" in query:
            # print("i run")
            from engine.features import openCommand
            openCommand(query)
        elif "on youtube" in query:
            from engine.features import PlayYoutube
        
            PlayYoutube(query)
        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp, makeCall,sendMessage
            contact_no, name = findContact(query)
            if(contact_no != 0):
                speak("Which mode you want to use whatsapp or mobile")
                preferance = takecommand()
                print(preferance)
            
                if "mobile" in preferance:
                    if "send message" in query or "send sms" in query:
                        speak("what message to send")
                        message = takecommand()
                        sendMessage(message, contact_no, name) 
                    elif "phone call" in query:
                        makeCall(name, contact_no)

                    else:
                        speak("please try again")
                    

                elif "whatsapp" in preferance:
                    message = ""
                    if "send message" in query:
                        message = 'message'
                        speak("what message to send")
                        query = takecommand()
                                        
                    elif "phone call" in query:
                        message = 'call'
                    else:
                        message = 'video call'
                                        
                    whatsApp(contact_no, query, message, name)
   
            
            
        else:
            from engine.features import chatBot 
            # chatBot(query)
            # print('not run')
    # except:
        # print("error")    
    except Exception as e:
        print("Error in allCommands:", str(e))
        speak("There was an error processing your request.")
    
    eel.ShowHood()


   

