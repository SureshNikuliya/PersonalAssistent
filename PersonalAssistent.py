import pyttsx3
import datetime
import speech_recognition as sr
import webbrowser
import os
from tkinter import *

"""
#GUI
_myWindow = Tk()
_myWindow.title("Personal Assistent Nancy")
Label(_myWindow, text="Say Hi Nancy to start commanding....", bg="#EEEEEE").pack()
_myWindow.geometry("300x200+200+250")
"""

#Stop flag
_stop = False

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

#Function to speak the text
def speak(audio):   
    engine.say(audio)
    engine.runAndWait()

#Wish function according to time
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak('Good Morning')

    elif hour >= 12 and hour < 18:
        speak('Good Aftternoon')

    else:
        speak('Good Evening')

    speak('Hi i am Nancy. How may i help you?')

def listen(state):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        #Label(_myWindow, text="Listenning*****", bg="#EEEEEE").pack()
        print("Listenning....")
        r.pause_threshold = 2
        audio = r.listen(source)
    
    if state == 'startAssistent':
        try:
            print('Recognizing....')
            command = r.recognize_google(audio, language='en-in')
        except Exception:
            print('Not able to Reconize the command. Can you say that again!!!!')
            return 'None'

    else:
        try:
            speak('Recognizing....')
            command = r.recognize_google(audio, language='en-in')

        except Exception:
            speak('Not able to Reconize the command. Can you say that again!!!!')
            return 'None'

    return command

if __name__ == "__main__":
#def startAssistent():
    while True:
        command = listen('startAssistent').lower()
        print(command)

        if 'stop' in command:
            break

        if 'hi nancy' in command or 'nancy' in command:
            wishMe()

            while True:
                command = listen('takeCommands').lower()
                _commandSuccess = False

                if 'stop' in command:
                    break

                if 'open google' or 'open browser' in command:
                    webbrowser.open('google.com')
                    _commandSuccess = True
                
                elif 'open eclipse' in command:
                    _eclipsePath = 'C:\\Users\\SureshNikuliya\\eclipse\\java-2019-09\\eclipse\\eclipse.exe'
                    os.startfile(_eclipsePath)
                    _commandSuccess = True

                elif 'open slack' in command:
                    _slackPath = 'C:\\Users\\SureshNikuliya\\AppData\\Local\\slack\\slack.exe'
                    os.startfile(_slackPath)
                    _commandSuccess = True
                
                if _commandSuccess:
                    speak('Anything else i can do for you. Suresh')
                    _askAgain = False
                    while True:
                        command = listen('takeCommands').lower()

                        if 'stop' in command:
                            break

                        if 'yes' in command:
                            _askAgain = True
                            break

                        elif 'no' in command:
                            _askAgain = False
                            break

                    if not _askAgain:
                        speak('Okay Suresh')
                        speak('If you need anything Say HI NANCY')
                        break

#_startButton = Button(_myWindow, text="Start", command = startAssistent).pack()
#_myWindow.mainloop()
             



        
        
        
