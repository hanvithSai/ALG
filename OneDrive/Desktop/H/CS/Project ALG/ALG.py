!python -m ensurepip --upgrade # install pip on jupyter lab

pip install gradio # install graio for UI

import openai
import os
import gradio as gr
from dotenv import load_dotenv, find_dotenv

# Load environment variables
_ = load_dotenv(find_dotenv())
openai.api_key = os.getenv('OPENAI_API_KEY')

def chat_with_openai(user_input):
    # Create a chat completion
    chat_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_input}],
        max_tokens=50,  # Adjust as needed
        n=1,  # Number of completions to return
        temperature=0.7  # Adjust for creativity vs. accuracy
    )
    
    # Return the response content
    return chat_completion.choices[0].message.content

# Create Gradio interface
demo_chatbot = gr.Interface(
    fn=chat_with_openai,
    inputs="text",
    outputs="text",
    title="OpenAI Chatbot",
    description="Enter your message to chat with the OpenAI model."
)

# Launch the interface with a public URL
demo_chatbot.launch(share=True)

