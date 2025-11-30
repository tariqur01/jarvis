import speech_recognition as sr
import pyttsx3
import wikipedia
import logging
import os
import subprocess
import datetime
import ctypes
import webbrowser
from piper import PiperVoice
import sounddevice as sd
import numpy as np

# Logging configuration
LOG_DIR = 'logs'
LOG_FILE_NAME = 'application.log'
os.makedirs(LOG_DIR, exist_ok=True)
log_path = os.path.join(LOG_DIR,LOG_FILE_NAME)
logging.basicConfig(
    filename= log_path,
    level=logging.INFO,
    format= "[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s"
)

# This project is tested on Ubutu 24.04LTS and has 2 options for voice output
# 1. espeak-ng
# 2. piper + voice model


#  Uncoment this segment to initialize espeak-ng on Linux
#...............................................................
# engine = pyttsx3.init("espeak")
# engine.setProperty('rate',150)
# voices = engine.getProperty('voices')
#...............................................................



# The below code segment is for loading Voice Model to be used with piper
#..........................................................................
# Load your ONNX voice
voice = PiperVoice.load("hfc-female/en_US-hfc_female-medium.onnx")
#..........................................................................



#  This is the speak function
def speak(text):
    """
    This function converts text to voice
    Args:
        test
    Returns:
        None
    """
    # Uncoment this segment to use voice output through espeak-ng
    #...........................................................
    # engine.say(text)
    # engine.runAndWait()
    #...........................................................
    
    
    # This code segment is for using Voice Model with Piper
    #...................................................................
    
    audio = voice.synthesize("Hello, this is Piper TTS speaking!")

    for chunk in voice.synthesize(text):
        # chunk.audio_int16_bytes contains raw 16-bit PCM bytes
        # Convert to NumPy array of int16
        data = np.frombuffer(chunk.audio_int16_bytes, dtype=np.int16)
        fs = chunk.sample_rate
        sd.play(data, samplerate=fs)
        sd.wait()
    #...................................................................



# This function greets the user
def greeting():
    hour = datetime.datetime.now().hour
    if 0<=hour<12:
        speak("Good Morning Sir. How are you doing?")
    elif 12<=hour<18:
        speak("Good Afternoon Sir. How are you doing?")
    else:
        speak("Good Evening Sir. How are you doing?")
    
    speak("I am jarvis. How can I help you today?")



# This function takes input/ voice query from user and returns the query as a text 
def takeCommand():
    """
    This function takes voice commands & recognize it through speech recognition

    Returns:
        text as a query.
    """

    r = sr.Recognizer()
    try:
        with sr.Microphone(device_index=8) as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)
            print("recognizing...")
            query = r.recognize_google(audio,language='en-in')
            print(f"User said: {query}\n")

    except Exception as e:
        logging.error(e)
        print("Say that again please.")
        return "None"

    return query

# Greeting the user.
greeting()


# This is the continuous executio of the while loop until user exits.
while True:
    query = takeCommand().lower()
    print(query)

    if "your name" in query:
        speak("My name is jarvis sir. I am your personal voice assistant.")
        logging.info("User asked for assistant's name.")

    elif "how are you" in query:
        speak("I am functioning at full capacity Sir.")
        logging.info("User asked about assistants well being.")

    elif "who made you" in query:
        speak("I was programmed by you sir. Did you forget?")
        logging.info("User asked about the programmer of this system.")

    elif "open google" in query:
        speak("Opening google sir. Please, go ahead with your search.")
        webbrowser.open("google.com")
        logging.info("User requested to open google on web browser.")

    elif "open calculator" in query:
        speak("Opening calculator sir.")
        subprocess.Popen("gnome-calculator")
        logging.info("User requested to open calculator.")

    elif "open notepad" in query:
        speak("Opening Notepad Sir.")
        logging.info("User requested to open notepad.")

    elif "youtube" in query:
        speak("opening youtube sir.")
        query = query.replace("youtube",'')
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
        logging.info("User requested to open youtube.")

    elif "open terminal" in query:
        speak("Opening terminal sir.")
        subprocess.Popen(["gnome-terminal"])
        logging.info("User requested to open terminal.")

    elif 'time' in query:
        current_hour = datetime.datetime.now().hour
        current_time = datetime.datetime.now().minute
        speak(f"the time is now {current_hour} hours and {current_time} minutes sir.")
        logging.info("User asked for time.")

    elif 'exit' in query:
        speak("Ok sir. Exiting. Have a nice time.")
        logging.info("User asked for exiting the application.")
        exit()
