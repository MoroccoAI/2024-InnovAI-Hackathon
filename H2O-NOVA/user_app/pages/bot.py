import time

import openai
import pandas as pd
import streamlit as st
from constants import DATA_PATH, THRESHOLD

openai.api_key = ""

st.title("Ask for Help")

df = pd.read_csv(DATA_PATH)
last_water_usage = df.iloc[-1]['User Water Usage (liters)']
if last_water_usage > THRESHOLD:
    st.warning(f"Water usage ({last_water_usage} liters) exceeded the threshold "
               f"({THRESHOLD} liters). Ask me for suggestions.")

# Messages for the conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def get_chatgpt_response(messages):
    """Function to call the OpenAI API and get a response"""
    try:
        response = openai.Completion.create(
            model="gpt-3.5-turbo",  # Adjust the model version as needed
            messages=messages,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].message['content']
    except Exception as e:
        st.error(f"Error calling OpenAI API: {str(e)}")
        return "Sorry, there was an issue getting a response. Please try again later."


if prompt := st.chat_input("Hi"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Set up dynamic conversation context
    context = [{"role": "system", "content": "You are an assistant providing water-saving tips."}]

    # Add the last water usage and appliances to the context for a more personalized response
    context.append(
        {"role": "user", "content": f"My last water usage was {last_water_usage} liters, and my threshold is {THRESHOLD} liters. "
         f"I have the following appliances: shower, washing machine, bathtub, and dishwasher."}
    )

    response = get_chatgpt_response(context)

    # Stream the response character by character with a delay
    stream = [word + " " for word in response.split()]
    for word in stream:
        time.sleep(0.1)
        st.write(word, end="")

    # Append the assistant's response to the conversation
    st.session_state.messages.append({"role": "assistant", "content": response})
