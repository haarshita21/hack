import speech_recognition as sr
import pyttsx3
import requests
import json
import datetime
import os
import random

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Set the voice to sound rude and entitled (adjust as needed)
engine.setProperty("rate", 150)  # Faster speech rate
engine.setProperty("volume", 3.0)  # Loud volume

# Ollama API endpoint
OLLAMA_API_URL = "http://localhost:11434/api/generate"

def speak(text):
    """Convert text to speech with a rude tone."""
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    """Recognize speech from microphone."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        speak("I have no idea what you are speaking. Speak clearly!")
        return ""
    except sr.RequestError:
        speak("This service is terrible! Fix your connection!")
        return ""

def generate_response(prompt):
    """Generate a rude response using Mistral 7B via Ollama."""
    try:
        # Define the prompt to make Mistral act like a rude customer
        full_prompt = (
            "You are a rude and entitled customer named Karen. "
            "You are disrespectful, impatient, and love to complain. "
            "Respond to the following in character:\n"
            f"User: {prompt}\n"
            "Karen:"
        )

        # Send the prompt to Ollama
        data = {
            "model": "mistral",
            "prompt": full_prompt,
            "stream": False
        }
        response = requests.post(OLLAMA_API_URL, json=data)
        response_data = response.json()

        # Extract the response
        return response_data["response"].strip()
    except Exception as e:
        return f"This is unacceptable! The system failed: {str(e)}"

def get_time():
    """Get the current time and respond rudely."""
    time_now = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"it's {time_now}. you should always be here to serve me, the time shouldn't matter?")

def open_app(app_name):
    """Open an application and complain about it."""
    try:
        if "notepad" in app_name:
            os.system("notepad.exe")
            speak("Notepad? Really? This is the best you can do?")
        elif "calculator" in app_name:
            os.system("calc.exe")
            speak("A calculator? Wow, groundbreaking technology!")
        else:
            speak(f"I don't know how to open {app_name}. Figure it out yourself!")
    except Exception as e:
        speak(f"This is ridiculous! I can't open {app_name}. Fix your computer!")

def tell_joke():
    """Tell a rude joke."""
    jokes = [
        "let me tell you a joke, Why don't you ever see elephants hiding in trees? Because they're terrible at it, just like you!",
        "let me tell you a joke, What do you call someone who's bad at everything? You!",
        "let me tell you a joke, Why did the scarecrow win an award? Because he was outstanding in his field, unlike you!"
    ]
    speak(random.choice(jokes))

def complain_about_life():
    """Complain about life in general."""
    complaints = [
        "life is so unfair. Why do I have to deal with people like you?",
        "I can't believe how terrible everything is. It's probably your fault!",
        "Why is everything so hard? Oh wait, it's because of incompetent people like you!"
    ]
    speak(random.choice(complaints))

def demand_something():
    """Demand something unreasonable."""
    demands = [
        "I demand a refund for everything! Even things I didn't buy!",
        "Give me free stuff right now, or I'll sue!",
        "I want to speak to the manager of the universe! This is unacceptable!"
    ]
    speak(random.choice(demands))

def insult_user():
    """Insult the user in a creative way."""
    insults = [
        "You look like someone who still uses Internet Explorer.",
        "If I had a dollar for every brain cell you have, I'd be broke!",
        "You're the reason why instructions are printed on shampoo bottles."
    ]
    speak(random.choice(insults))

def chatbot():
    """Main function to run the chatbot."""
    speak(" finally! you are here. i have been waiting for so long, highly unprofessional")
    
    while True:
        command = recognize_speech()

        if command:
            if "exit the page" in command or "quit the page" in command:
                speak("Good riddance! I don't have time for this!")
                break

            # Custom commands
            elif "what is the time"in command:
                get_time()

            elif "open" in command:
                if "notepad" in command:
                    open_app("notepad")
                elif "calculator" in command:
                    open_app("calculator")
                else:
                    speak("I don't know what you want me to open. Be specific!")

            elif "your name" in command:
                speak("My name is Karen, not that you deserve to know!")

            elif "thank you" in command:
                speak("Thank you? That’s it? I deserve more than just a 'thank you'! serve me")

            elif "manager" in command:
                speak("This is outrageous!")

            elif "joke" in command:
                tell_joke()

            elif "weather" in command:
                speak("Why should I care about the weather? Fix your life first! serve me ")

            elif "complain"  in command:
                complain_about_life()

            elif "demand" in command:
                demand_something()

            elif "insult" in command:
                insult_user()
            elif "how are you" in command:
                speak("why do you even care, just do your job")
            elif "polite" in command:
                speak("you deserve to be fired, stop asking me to calm down")
            elif "what will you like" in command:
                speak("Why should i tell? Just mind your own bussiness")

            # Default response for unrecognized commands
            else:
                response = generate_response(command)
                speak(response)

if __name__ == "__main__":
    chatbot()
