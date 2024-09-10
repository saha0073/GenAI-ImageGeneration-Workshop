import streamlit as st
from openai import OpenAI
import io
from PIL import Image
import requests

# Initialize OpenAI client
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("Image Generation Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant" and "image" in message:
            st.image(message["image"])
        else:
            st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What image would you like to generate?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate image
    with st.chat_message("assistant"):
        with st.spinner("Generating image..."):
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            
            image_url = response.data[0].url
            
            # Download the image
            image_response = requests.get(image_url)
            image = Image.open(io.BytesIO(image_response.content))
            
            # Display the image
            st.image(image)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": "Here's the generated image:", "image": image})
st.sidebar.title("About")
st.sidebar.info("This is a Streamlit chatbot that generates images based on your prompts using GPT-4 Vision.")
