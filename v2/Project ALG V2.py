#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('python -m ensurepip --upgrade # install pip on jupyter lab')


# In[2]:


pip install gradio # install graio for UI


# In[3]:


pip install SpeechRecognition


# In[4]:


import openai
import os
import gradio as gr
from dotenv import load_dotenv, find_dotenv
import requests
import speech_recognition as sr  # Speech recognition for live transcription

# Load environment variables
_ = load_dotenv(find_dotenv())
openai.api_key = os.getenv('OPENAI_API_KEY')

# Function to generate lyrics based on description, genre, emotion, and languages
def generate_lyrics(description, genre, emotion, languages, english_script):
    output_lyrics = ""
    
    for language in languages:
        prompt = (
            f"Compose original song lyrics directly in {language}, based on the following scene or description:\n{description}\n\n"
            f"Ensure the lyrics follow a {genre} style, evoke the emotion of {emotion}, and have a melodic rhythm with proper rhyming. "
            f"Make sure the lyrics are musically synchronized, and not just a translation, but original lyrics that make sense in {language}."
            "\n\nLyrics:"
        )
        
        chat_completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=3000,
            temperature=0.8
        )
        
        lyrics = chat_completion.choices[0].message['content']
        output_lyrics += f"Language: {language}\n{lyrics}\n\n"
        
        if english_script and language != "English":
            english_script_prompt = (
                f"Now provide the above lyrics in {language} but written using the English script. "
                "The text should maintain the original meaning while using English letters for representation."
            )
            english_script_completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": english_script_prompt}],
                max_tokens=300,
                temperature=0.7
            )
            english_script_lyrics = english_script_completion.choices[0].message['content']
            output_lyrics += f"English Script for {language}:\n{english_script_lyrics}\n\n"

    return output_lyrics

# Function to generate TTS from lyrics
def generate_audio(lyrics, language_code):
    api_key = "YOUR_API_KEY"  # Replace with your valid VoiceRSS API key
    tts_endpoint = f"https://api.voicerss.org/"
    params = {
        "key": api_key,
        "hl": language_code,
        "src": lyrics,
        "r": "0",  # Speech rate (0 is default, change if needed)
        "c": "wav",  # Audio format (wav)
        "f": "16khz_16bit_stereo"  # Audio quality
    }

    response = requests.get(tts_endpoint, params=params)
    
    # Check if the response was successful
    if response.status_code == 200:
        audio_file = "generated_lyrics.wav"
        with open(audio_file, 'wb') as f:
            f.write(response.content)
        return audio_file
    else:
        print("Error in TTS API request:", response.status_code, response.text)
        return None


# Function to handle real-time transcription
def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        transcription = recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        transcription = "Unable to understand the audio."
    except sr.RequestError:
        transcription = "Speech recognition service is unavailable."
    return transcription

# Function to switch between text or voice input
def process_input(input_type, text_description, voice_description):
    if input_type == "Voice Input":
        return voice_description
    return text_description

# Gradio Interface with voice input, live transcription, and audio output
def create_interface():
    with gr.Blocks() as demo_lyrics_generator:
        gr.Markdown("# AI Lyrics Generator with Text or Voice Input and Audio Output")
        
        input_type = gr.Radio(choices=["Text Input", "Voice Input"], label="Input Method", value="Text Input")

        # Inputs for text and voice (mic) description
        text_description = gr.Textbox(label="Song Description (Text)", placeholder="Describe the scene or theme for the song...")
        voice_description = gr.Audio(label="Speak Your Song Description", type="filepath")
        live_transcription = gr.Textbox(label="Live Transcript", interactive=False, visible=True)

        # Connect live transcription to microphone input
        def update_transcription(audio_file):
            transcription = transcribe_audio(audio_file)
            return transcription

        voice_description.change(fn=update_transcription, inputs=voice_description, outputs=live_transcription)

        genre = gr.Dropdown(choices=["Classical", "Pop", "Rock", "Hip-hop", "Jazz", "Country"], label="Genre", value="Select a genre")
        emotion = gr.Textbox(label="Emotion", placeholder="Enter the emotion (e.g., love, sadness, excitement)...")
        languages = gr.CheckboxGroup(choices=["English", "Telugu", "Hindi", "Tamil", "Kannada", "Malayalam"], 
                                     label="Languages", value=["English"])
        english_script = gr.Checkbox(label="Provide in English Script", value=False)

        # Output fields
        lyrics_output = gr.Textbox(label="Generated Lyrics", interactive=False)
        audio_output = gr.Audio(label="Audio Output (Read Aloud)", type="filepath", interactive=False)
        
        def generate(input_type, text_description, live_transcription, genre, emotion, languages, english_script):
            description = process_input(input_type, text_description, live_transcription)
            lyrics = generate_lyrics(description, genre, emotion, languages, english_script)
            audio_file = generate_audio(lyrics, "en-us")  # Adjust language code as needed
            return lyrics, audio_file
        
        generate_button = gr.Button("Generate Lyrics & Audio")
        generate_button.click(fn=generate, 
                              inputs=[input_type, text_description, live_transcription, genre, emotion, languages, english_script], 
                              outputs=[lyrics_output, audio_output])
        
    return demo_lyrics_generator

# Launch the interface with a public URL
create_interface().launch(share=True)


# In[ ]:




