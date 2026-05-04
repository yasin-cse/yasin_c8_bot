import streamlit as st
import google.generativeai as genai

# Configuration
API_KEY = "AIzaSyBIcCElyH4XgIo0-lCifSStswGfK6Rj8SA"
genai.configure(api_key=API_KEY)

# Model Setup
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 2048,
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Page Configuration
st.set_page_config(page_title="AI Assistant", page_icon="🤖")
st.title("Intelligent Chat Interface")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input and Response Logic
if prompt := st.chat_input("Type your message here..."):
    # Add User Message to History
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI Response
    try:
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(prompt)
        
        full_response = response.text
        
        with st.chat_message("assistant"):
            st.markdown(full_response)
            
        # Add Assistant Response to History
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
    except Exception as e:
        st.error(f"System Error: {str(e)}")
