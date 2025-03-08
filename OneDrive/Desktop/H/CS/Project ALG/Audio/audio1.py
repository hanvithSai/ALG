# QUESTION: HOW TO MAKE AUDIO TRANSCRIPTION INTERACTIVE?

import speech_recognition as sr
import time

# Function to perform speech recognition
def recognize_speech(duration):
    recognizer = sr.Recognizer()
    
    # Use the microphone for input
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source)
        print(f"Start speaking! You have {duration} seconds.")
        
        start_time = time.time()
        transcript = ""
        
        # Listen for the specified duration
        while time.time() - start_time < duration:
            try:
                print("Listening...")
                audio_data = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                print("Processing...")
                
                # Convert the audio to text (live transcript)
                text = recognizer.recognize_google(audio_data)
                transcript += text + " "
                print(f"Live Transcript: {text}")
                
            except sr.UnknownValueError:
                print("Couldn't understand, please speak clearly.")
            except sr.RequestError:
                print("Sorry, there was an issue with the recognition service.")
            except sr.WaitTimeoutError:
                print("Listening timed out, no speech detected.")

        # Return the full transcript after the time limit
        return transcript.strip()

# Main function
def main():
    print("Welcome to the interactive speech-to-text program!")
    
    # Ask the user how long they want to speak
    duration = int(input("For how many seconds would you like to speak? "))
    
    # Recognize the speech for the given duration
    full_transcript = recognize_speech(duration)
    
    print("\nFinished! Here's the full transcript of what you said:")
    print(full_transcript)

# Run the program
if __name__ == "__main__":
    main()
