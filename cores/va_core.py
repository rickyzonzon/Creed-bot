# Virtual assistant core

import speech_recognition as sr
import pyttsx3
import datetime
import calendar
from pygame import mixer
import webbrowser
import wikipedia


# Record audio, return as str
def record():
    mixer.init()
    mixer.music.load("boop.mp3")
    mixer.music.play()
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)

    data = ''
    try:
        data = r.recognize_google(audio)
        print('You said: ' + data)
    except sr.UnknownValueError:
        print('Google Speech Recognition did not understand the audio, unknown error')
    except sr.RequestError as e:
        print('Request results from Google Speech Recognition service error ' + str(e))

    return data


# Respond to text, vocally and textually
def assistantResponse(text):
    converter = pyttsx3.init()
    voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"
    converter.setProperty('rate', 150)
    converter.setProperty('volume', 0.7)
    converter.setProperty('voice', voice_id)
    converter.say(text)
    converter.runAndWait()

    return f"Creed: {text}"


# Creed activates after hearing/getting the wake word
def wakeWord(text):
    WAKE_WORDS = ['hey creed', 'yo creed']

    text = text.lower()

    for phrase in WAKE_WORDS:
        if phrase in text:
            return True

    return False


# Provide the date
def getDate():
    now = datetime.datetime.now()
    my_date = datetime.datetime.today()
    weekday = calendar.day_name[my_date.weekday()]
    monthNum = now.month
    dayNum = now.day

    month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']

    ordinalNumbers = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th',
                      '10th', '11th', '12th', '13th', '14th', '15th', '16th', '17th',
                      '18th', '19th', '20th', '21st', '22nd', '23rd', '24th', '25th',
                      '26th', '27th', '28th', '29th', '30th', '31st']

    return f'{weekday} {month_names[monthNum - 1]} the {ordinalNumbers[dayNum - 1]}.'


# Provide the time
def getTime():
    now = datetime.datetime.now()
    meridiem = ''
    if now.hour >= 12:
        meridiem = 'p.m'
        hour = now.hour - 12
    else:
        meridiem = 'a.m'
        hour = now.hour

    if now.minute < 10:
        minute = '0' + str(now.minute)
    else:
        minute = str(now.minute)

    return f'{hour}:{minute} {meridiem}.'


# Returns info about a person given a vocabulary (list of strings) and a question (string)
def getPerson(vocabulary, sentence):
    person = ''

    for word in sentence.split():
        if word not in vocabulary:
            person += word + ' '

    person = person.strip()
    try:
        wiki = wikipedia.summary(person, sentences=2)
    except wikipedia.exceptions.PageError:
        wiki = wikipedia.summary(person, sentences=2, auto_suggest=False)

    return wiki


# Opens google search for sentence
def getInfo(sentence):
    sentence = sentence.split()
    sentence = "+".join(sentence)
    webbrowser.open(f'http://google.com/search?q={sentence}')


# Opens youtube for sentence
def howTo(sentence):
    sentence = sentence.split()
    sentence = "+".join(sentence)
    webbrowser.open(f'http://youtube.com/results?search_query={sentence}')

