# QUESTION: HOW TO CONVERT AUDIO INPUT TO TEXT IN PYTHON?

import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

# Use the microphone for input
with sr.Microphone() as source:
    print("Please say something...")
    # Listen to the input
    audio_data = recognizer.listen(source)
    
    try:
        # Convert the audio to text
        text = recognizer.recognize_google(audio_data)
        print("You said: ", text)
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
    except sr.RequestError:
        print("Sorry, there seems to be an issue with the request.")
