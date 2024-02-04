# SPEAR
this is an ai chatbot
import pyttsx3
import speech_recognition as sr
import re
import webbrowser
import json

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"User: {query}\n")
    except sr.UnknownValueError:
        print("Sorry, I didn't get that. Can you repeat it?")
        return "None"
    except sr.RequestError as e:
        print(f"Error recognizing speech: {e}")
        return "None"
    return query.lower()

def extract_url(user_input):
    url_pattern = re.compile(r'https?://[^\s]+')
    url = url_pattern.search(user_input)
    if url:
        return url.group()
    else:
        common_websites = {
            "google": "https://www.google.com",
            "youtube": "https://www.youtube.com",
            "github": "https://www.github.com",
            "facebook": "https://www.facebook.com",
            "twitter": "https://www.twitter.com",
            "wikipedia": "https://www.wikipedia.org",
            "chatgpt": "https://www.chatgpt.com"

        }
        for website in common_websites:
            if website in user_input:
                return common_websites[website]
    return None

def open_website(url):
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"Error opening website: {e}")

def get_config():
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
            return config
    except FileNotFoundError:
        return {}

def set_config(config):
    with open('config.json', 'w') as f:
        json.dump(config, f)

def main():
    config = get_config()
    if 'name' not in config:
        speak("Hello! What's your name?")
        name = listen()
        config['name'] = name
        set_config(config)
        speak(f"Nice to meet you, {name}! Before we start, please enter the passkey to access SPEAR.")
    else:
        speak(f"Hello {config['name']}! Before we start, please enter the passkey to access SPEAR.")

    passkey = None
    while passkey != '123':
        passkey = listen()
        if passkey.lower() == '123':
            config['passkey'] = passkey
            set_config(config)
            speak("Access granted! How can I help you today?")
        else:
            speak("Access denied. Please enter the correct passkey.")

    while True:
        user_input = listen()

        if "stop" in user_input or "goodbye" in user_input or "bye" in user_input:
            speak("Goodbye!")
            break
        elif "open" in user_input:
            url = extract_url(user_input)
            if url:
                speak("Sure! Opening the website.")
                open_website(url)
            else:
                speak("Sorry, I didn't get that. Can you repeat it?")
        elif "ok, thank you" in user_input:
            speak("You're welcome! Goodbye!")
            break


if __name__ == "__main__":
    main()
