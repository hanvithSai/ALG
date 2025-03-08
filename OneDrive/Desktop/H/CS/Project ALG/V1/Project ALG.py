#!/usr/bin/env python
# coding: utf-8
Project ALG
# In[1]:


get_ipython().system('python -m ensurepip --upgrade # install pip on jupyter lab')


# In[2]:


pip install gradio # install graio for UI


# In[3]:


import openai
import os
import gradio as gr
from dotenv import load_dotenv, find_dotenv

# Load environment variables
_ = load_dotenv(find_dotenv())
openai.api_key = os.getenv('OPENAI_API_KEY')

# Function to generate lyrics based on description, genre, emotion, and languages
def generate_lyrics(description, genre, emotion, languages, english_script):
    output_lyrics = ""
    
    for language in languages:
        # Create a prompt for each selected language, focusing on writing lyrics directly in that language
        prompt = (
            f"Compose original song lyrics directly in {language}, based on the following scene or description:\n{description}\n\n"
            f"Ensure the lyrics follow a {genre} style, evoke the emotion of {emotion}, and have a melodic rhythm with proper rhyming. "
            f"Make sure the lyrics are musically synchronized, and not just a translation, but original lyrics that make sense in {language}."
            "\n\nLyrics:"
        )
        
        # Create a chat completion for each language
        chat_completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=3000,  # Adjust for response length
            temperature=0.8  # Higher creativity for lyrical flow
        )
        
        # Get the generated lyrics
        lyrics = chat_completion.choices[0].message['content']
        
        # Append the language and its generated lyrics to the output
        output_lyrics += f"Language: {language}\n{lyrics}\n\n"
        
        # If the English script is requested and the language is not English
        if english_script and language != "English":
            english_script_prompt = (
                f"Now provide the above lyrics in {language} but written using the English script. "
                "The text should maintain the original meaning while using English letters for representation."
            )
            
            # Get the English transliteration
            english_script_completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": english_script_prompt}],
                max_tokens=300,
                temperature=0.7
            )
            
            # Get the English script version and append it
            english_script_lyrics = english_script_completion.choices[0].message['content']
            output_lyrics += f"English Script for {language}:\n{english_script_lyrics}\n\n"

    return output_lyrics

# Gradio Interface with enhanced inputs
demo_lyrics_generator = gr.Interface(
    fn=generate_lyrics,
    inputs=[
        gr.Textbox(label="Song Description", placeholder="Describe the scene or theme for the song..."),
        gr.Dropdown(choices=["Classical", "Pop", "Rock", "Hip-hop", "Jazz", "Country"], label="Genre", value="Select a genre"),
        gr.Textbox(label="Emotion", placeholder="Enter the emotion (e.g., love, sadness, excitement)..."),
        gr.CheckboxGroup(choices=["English", "Telugu", "Hindi", "Tamil", "Kannada", "Malayalam"], 
                         label="Languages", value=["English"]),
        gr.Checkbox(label="Provide in English Script", value=False)
    ],
    outputs="text",
    title="AI Lyrics Generator",
    description="Enter a description, genre, emotion, and select one or more languages to generate musically synchronized, rhyming lyrics. Optionally, provide the lyrics in the English script for non-English languages."
)

# Launch the interface with a public URL
demo_lyrics_generator.launch(share=True)


# In[ ]:




