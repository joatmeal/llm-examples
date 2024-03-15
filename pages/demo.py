import streamlit as st
from openai import OpenAI, OpenAIError

def initialize_client(api_key):
    return OpenAI(api_key=api_key)

def generate_response(client, messages):
    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo",
                                                  messages=messages,
                                                  max_tokens=150,
                                                  n=1,
                                                  stop=None,
                                                  temperature=0.7)
        message = response.choices[0].message.content
        return message.strip()
    except OpenAIError as e:
        st.error(f"An error occurred: {e}")
        return "I'm currently having issues retrieving a response, please try again."

st.title("ChatGPT App")

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="openai_api_key", type="password")
    if openai_api_key:
        client = initialize_client(openai_api_key)
    else:
        client = None
    st.markdown("[Get an OpenAI API key](https://platform.openai.com/account/api-keys)")
    if st.button('Reset Session'):
        st.session_state.clear()
        st.experimental_rerun()

if client:
    if 'messages' not in st.session_state:
        st.session_state['messages'] = [{"role": "system", "content": "You are a helpful assistant."}]

    user_input = st.text_input("Enter your message:")
    if user_input:
        st.session_state['messages'].append({"role": "user", "content": user_input})
        response = generate_response(client, st.session_state['messages'])
        st.session_state['messages'].append({"role": "assistant", "content": response})

    for message in st.session_state['messages']:
        if message['role'] == 'user':
            st.write("You: " + message['content'])
        elif message['role'] == 'assistant':
            st.write("ChatGPT: " + message['content'])
else:
    st.warning("Please enter a valid OpenAI API key to proceed.")
