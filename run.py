# To run Jarvis
import multiprocessing
import subprocess



def startJarvis():
        # Code for process 1
        print("Process 1 is running.")
        from main import start
        start()


 # To run hotword
def listenHotword():
        # Code for process 2
        print("Process 2 is running.")
        from engine.features import hotword
        hotword()



#  Start both processes
if __name__ == '__main__':
        p1 = multiprocessing.Process(target=startJarvis)
        p2 = multiprocessing.Process(target=listenHotword)
        p1.start()
        # subprocess.call([r'device.bat'])
        p2.start()
        p1.join()

        if p2.is_alive():
                p2.terminate()
                p2.join()

        print("system stop")  

        # adb shell am start -a android.intent.action.CALL -d tel: 
        # adb shell input tap 358 2223
        # adb shell input keyevent 3
        # selfie functionality
        # spy video recording
        # note taking 
        # audio recording
        # adb.exe: more than one device/emulator