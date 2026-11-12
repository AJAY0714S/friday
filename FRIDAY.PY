import os
import numpy as np
import sounddevice as sd
import speech_recognition as sr
import pyttsx3
from google import genai
from google.genai import types

# 1. Voice Engine Setup
engine = pyttsx3.init()
voices = engine.getProperty('voices')

for voice in voices:
    if "female" in voice.name.lower() or "zira" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

engine.setProperty('rate', 175)

def speak(text):
    print(f"FRIDAY: {text}")
    engine.say(text)
    engine.runAndWait()

# 2. Gemini AI Setup
client = genai.Client(api_key="AQ.Ab8RN6KhXnYDUTwY3UXbMSnVQB4iwD423aueR4QBw0a7LJBxhg")

sys_instruction = "You are F.R.I.D.A.Y., a smart, polite, and witty AI assistant like in Iron Man. Keep your responses concise, natural, and friendly for voice conversation."

# Model-a 'gemini-3.8-flash'-ukku update pannirukkom
chat = client.chats.create(
    model="gemini-3.8-flash",
    config=types.GenerateContentConfig(
        system_instruction=sys_instruction,
        temperature=0.7
    )
)

# 3. Mic Voice Listening Function
def listen():
    recognizer = sr.Recognizer()
    fs = 44100  # Sample rate
    duration = 5  # 5 seconds recording window
    
    print("\nListening...")
    try:
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()
        
        audio_data = sr.AudioData(recording.tobytes(), fs, 2)
        
        print("Recognizing...")
        query = recognizer.recognize_google(audio_data, language='en-US')
        print(f"You: {query}")
        return query
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# Local app opening helper function
def handle_local_commands(command):
    cmd = command.lower()
    if "open chrome" in cmd:
        speak("Opening Google Chrome, Boss.")
        os.system("start chrome")
        return True
    elif "open notepad" in cmd:
        speak("Opening Notepad, Boss.")
        os.system("start notepad")
        return True
    elif "open calculator" in cmd:
        speak("Opening Calculator, Boss.")
        os.system("start calc")
        return True
    elif "open WhatsApp" in cmd:
        speak("Opening WhatsApp, Boss.")
        os.system("start whatsapp")
        return True
    elif "open Telegram" in cmd:
        speak("Opening Telegram, Boss.")
        os.system("start telegram")
        return True
    elif "open VLC" in cmd:
        speak("Opening VLC Media Player, Boss.")
        os.system("start vlc")
        return True
    elif "open This" in cmd:
        speak("Opening This PC, Boss.")
        os.system("start shell:ThisPC")
        return True
    elif "open Power" in cmd:
        speak("Opening Power Options, Boss.")
        os.system("start shell:PowerOptions")
        return True
    elif "powerpoint" in cmd:
        speak("Opening PowerPoint, Boss.")
        os.system("start powerpnt")
        return True
    elif "word" in cmd:
        speak("Opening Word, Boss.")
        os.system("start winword")
        return True
    elif "excel" in cmd:
        speak("Opening Excel, Boss.")
        os.system("start excel")
        return True
    elif "open download" in cmd:
        speak("Opening Downloads, Boss.")
        os.system("start shell:DownloadsFolder")
        return True
    elif "open images" in cmd:
        speak("Opening Images, Boss.")
        os.system("start shell:PicturesFolder")
        return True
    elif "open youtube" in cmd:
        speak("Opening YouTube, Boss.")
        webbrowser.open("https://www.youtube.com")
        return True
    return False

# 4. Main Loop
if __name__ == "__main__":
    speak("Online and ready, Boss. How can I help you today?")
    
    while True:
        user_input = listen()
        
        if user_input:
            # Exit command
            if any(word in user_input.lower() for word in ["exit", "quit", "bye", "goodbye"]):
                speak("Goodbye, Boss. Powering down.")
                break
            
            # Check local PC commands first (like opening Chrome)
            if handle_local_commands(user_input):
                continue
                
            # Otherwise send to Gemini AI
            try:
                response = chat.send_message(user_input)
                speak(response.text)
                
            except Exception as e:
                speak("I encountered an error processing that request.")
                print(f"Error: {e}")