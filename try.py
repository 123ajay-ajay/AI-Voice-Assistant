import pyttsx3
import speech_recognition as sr
import eel
import time

from engine.command import takecommand

def speak(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 174)
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('listening...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, 10, 6)
    
    try:
        print('recognizing...')
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return ""
    return query.lower()

def allCommands():
    query = takeCommand()
    print(query)
    if "open" in query:
        print("I run")
        from engine.features import openCommand
        openCommand(query)
    elif "on youtube" in query:
        print(query)
        from engine.features import PlayYoutube
        PlayYoutube(query)


    

    elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp
            message = ""
            contact_no, name = findContact(query)
            if(contact_no != 0):

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
        print("Command not recognized.")

# Example usage
if __name__ == "__main__":
    a = input("Enter something: ")
    speak(a)
    allCommands()
