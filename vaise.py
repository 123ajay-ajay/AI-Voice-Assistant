# import os
# import time
# from engine.command import speak
# from engine.helper import findContact

def deleteMessage(contact_name):
    # Step 1: Contact ka mobile number dhoondo
    mobile_no, found_name = findContact(contact_name)

    if mobile_no == 0:
        speak(f"{contact_name} ka number nahi mila.")
        return
    
    speak(f"Deleting last message to {found_name}")

    # Step 2: Messages app kholein
    os.system("adb shell am start -n com.google.android.apps.messaging/.ui.ConversationListActivity")
    time.sleep(2)

    # Step 3: Contact search karein
    os.system(f"adb shell input text '{mobile_no}'")
    time.sleep(2)
    os.system("adb shell input keyevent 66")  # Enter key press
    time.sleep(2)

    # Step 4: Last message par long press karein
    os.system("adb shell input swipe 500 1300 500 1300 1000")  
    time.sleep(2)

    # Step 5: Delete button press karein
    os.system("adb shell input tap 900 180")  
    time.sleep(1)

    # Step 6: Confirm delete
    os.system("adb shell input tap 700 1200")  
    time.sleep(1)

    speak(f"Last message to {found_name} deleted successfully!")
    print(f"Message to {found_name} deleted successfully!")



#     from engine.features import deleteMessage

def processCommand(command):
    if "delete message to" in command:
        contact_name = command.replace("delete message to", "").strip()
        deleteMessage(contact_name)

