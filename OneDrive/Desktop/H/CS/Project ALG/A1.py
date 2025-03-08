!python -m ensurepip --upgrade # install pip on jupyter lab

pip install gradio # install graio for UI


import openai
import os
import gradio as gr
from dotenv import load_dotenv, find_dotenv

# Load environment variables
_ = load_dotenv(find_dotenv())
openai.api_key = os.getenv('OPENAI_API_KEY')

# Function to generate lyrics based on description, genre, emotion, and language
def generate_lyrics(description, genre, emotion, language):
    # Create a more structured prompt for musical synchronization, rhyming, and melody
    prompt = (
        f"Write song lyrics in {language} based on the following scene or description:\n{description}\n\n"
        f"Make sure the lyrics follow a {genre} style, evoke the emotion of {emotion}, "
        f"include a melodic rhythm, and have a rhyming structure.\n\n"
        "Lyrics:"
    )

    # Create a chat completion
    chat_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,  # Adjust for response length
        temperature=0.8  # Higher creativity for lyrical flow
    )

    # Return the generated lyrics
    return chat_completion.choices[0].message['content']

# Gradio Interface with enhanced inputs
demo_lyrics_generator = gr.Interface(
    fn=generate_lyrics,
    inputs=[
        gr.Textbox(label="Song Description", placeholder="Describe the scene or theme for the song..."),
        gr.Dropdown(choices=["Pop", "Rock", "Classical", "Hip-hop", "Jazz", "Country"], label="Genre", value="Pop"),
        gr.Textbox(label="Emotion", placeholder="Enter the emotion (e.g., love, sadness, excitement)..."),
        gr.Dropdown(choices=["English", "Telugu", "Hindi", "Tamil", "Kannada", "Malayalam"], label="Language", value="English")
    ],
    outputs="text",
    title="AI Lyrics Generator",
    description="Enter a description, genre, emotion, and language to generate musically synchronized, rhyming lyrics."
)

# Launch the interface with a public URL
demo_lyrics_generator.launch(share=True)
