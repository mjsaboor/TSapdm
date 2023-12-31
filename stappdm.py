
#pip install git+https://github.com/pypa/pip
#git clone git+https://github.com/pypa/pip
#pip install git+https://github.com/streamlit/streamlit.git
#pip install openai 
#pip install streamlit
# .streamlit/secrets.toml
#git clone https://github.com/streamlit/streamlit.git 
#pip install git+https://github.com/user/repo.git
git clone git@github.com:https-//github.com/streamlit/streamlit.git
#cd /path/to/streamlit
#python setup.py install -e .

#$ git clone https://github.com/ncbi-nlp/NegBio.git
#$ cd /path/to/negbio
#$ python setup.py install --user

#pip install .

OPENAI_API_KEY = "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"


import streamlit as st
import openai

st.title("ChatGPT-like clone")

# Set OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

for response in openai.ChatCompletion.create(
        model=st.session_state["openai_model"],
        messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
        stream=True,
    ):
        full_response += response.choices[0].delta.get("content", "")
        message_placeholder.markdown(full_response + "▌")
    message_placeholder.markdown(full_response)
st.session_state.messages.append({"role": "assistant", "content": full_response})
