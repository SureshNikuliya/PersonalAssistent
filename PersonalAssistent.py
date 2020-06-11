import pyttsx3
import datetime
import speech_recognition as sr
import webbrowser
import os
import json
import requests

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

#Fetch config properties
with open('config.json') as config_file:
    properties = json.load(config_file)

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

def takeNotes():
    header = "Notes taken on {0} at {1}".format(datetime.datetime.now().date(), datetime.datetime.now().time())
    notes = header + '\n'
    while True:
        speak('Please speak the point to be noted!')
        notes += '- ' + listen('takeCommands') + '\n'
        speak('You want to add more points')
        command = listen('takeCommands').lower()
        if 'no' in command:
            break
        else:
            continue

    speak('You want to send the following point to slack')
    print(notes)
    message = {'text': notes}
    while True:
        command = listen('takeCommands').lower()
        if 'yes' in command:
            sendNotesToSlack(message)
            break
        elif 'no' in command:
            break


def sendNotesToSlack(notes):
    requests.post(properties['web_hook_url'], data=json.dumps(notes))
    speak('Successfully send notes to slack channel Personal Assistent')

if __name__ == "__main__":
#def startAssistent():
    while True:
        command = listen('startAssistent').lower()
        print(command)

        if 'stop' in command:
            speak('Bye Bye, Have a good time with your love ones.')
            break

        if 'hi nancy' in command or 'nancy' in command:
            wishMe()

            while True:
                command = listen('takeCommands').lower()
                _commandSuccess = False
                print(command)

                if 'stop' in command:
                    break

                elif ('open google' in command) or ('open browser' in command):
                    webbrowser.open('google.com')
                    _commandSuccess = True
                
                elif ('open eclipse' in command) or ('eclipse' in command):
                    _eclipsePath = properties['eclipse_path']
                    os.startfile(_eclipsePath)
                    _commandSuccess = True

                elif ('open slack' in command) or ('slack' in command):
                    _slackPath = properties['slack_path']
                    os.startfile(_slackPath)
                    _commandSuccess = True

                elif ('take notes' in command) or ('notes' in command):
                    takeNotes()
                    _commandSuccess = True
                
                if _commandSuccess:
                    _commandSuccess = False
                    speak('Anything else i can do for you. {}'.format(properties['user']))
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
                        speak('Okay {}'.format(properties['user']))
                        speak('If you need anything Say HI NANCY')
                        break
