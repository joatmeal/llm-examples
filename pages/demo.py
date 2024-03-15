import streamlit as st
from openai import OpenAI

client = OpenAI()

with st.sidebar:
       openai_api_key = st.text_input("OpenAI API Key", key="openai_api_key", type="password")
       "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

def generate_response(messages):
   response = client.chat.completions.create(model="gpt-3.5-turbo",
   messages=messages,
   max_tokens=150,
   n=1,
   stop=None,
   temperature=0.7)
   message = response.choices[0].message.content
   return message.strip()
st.title("ChatGPT App")
if 'messages' not in st.session_state:
   st.session_state['messages'] = [{"role": "system", "content": "You are a helpful assistant."}]
user_input = st.text_input("Enter your message:")
if user_input:
   st.session_state['messages'].append({"role": "user", "content": user_input})
   response = generate_response(st.session_state['messages'])
   st.session_state['messages'].append({"role": "assistant", "content": response})
for message in st.session_state['messages']:
   if message['role'] == 'user':
       st.write("You: " + message['content'])
   elif message['role'] == 'assistant':
       st.write("ChatGPT: " + message['content'])