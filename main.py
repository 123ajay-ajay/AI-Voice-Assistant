import os
import eel

from engine.features import *
from engine.command import *
from engine.auth import recoganize
def start():
    eel.init("frontend")
    
    @eel.expose
    def init():
        subprocess.call([r'device.bat'])
        eel.hideLoader()
        speak("Ready for face Authentication")
        flag=recoganize.AuthenticateFace()
        if flag==1:
            eel.hideFaceAuth()
            speak("Face Authentication successful")
            eel.hideFaceAuthSuccess()
            speak("hello, Welcome Sir, How can i Help You")
            eel.hideStart()
            playAssistantSound()
        else:
            speak("Face Authentication Fail")

    os.system('start msedge.exe --app="http://localhost:8000/index.html"')
    eel.start('index.html',mode=None,host='localhost',block=True)
