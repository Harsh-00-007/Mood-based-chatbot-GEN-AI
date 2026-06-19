import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

# Load environment variables
load_dotenv()

# Initialize the model exactly as you had it
primary_model = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.7
)

st.title("Mood-Based AI Chatbot")

# 1. Setup Session State
# This ensures Streamlit remembers our choices and chat history after every interaction
if "setup_complete" not in st.session_state:
    st.session_state.setup_complete = False

if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. UI Step 1: Mood Selection
if not st.session_state.setup_complete:
    st.subheader("Choose AI Personality")
    choice = st.radio(
        "Select Mode:",
        options=["Angry Mode", "Sad Mode", "Funny Mode"]
    )
    
    if st.button("Start Chat"):
        # Map the choice to your exact system prompts
        if choice == "Angry Mode":
            mode = "You are a very angry ai and answer every message aggressively"
        elif choice == "Sad Mode":
            mode = "You are a very sad ai and answer every message sadly"
        else:
            mode = "You are a very funny ai and answer every message in a joke way"
            
        # Initialize the messages list with the chosen persona
        st.session_state.messages = [SystemMessage(content=mode)]
        st.session_state.setup_complete = True
        st.rerun() # Refresh the page to hide the menu and show the chat

# 3. UI Step 2: The Chat Interface
if st.session_state.setup_complete:
    
    # Display the existing chat history (hiding the background SystemMessage)
    for msg in st.session_state.messages:
        if isinstance(msg, SystemMessage):
            continue
        
        role = "user" if isinstance(msg, HumanMessage) else "assistant"
        with st.chat_message(role):
            st.write(msg.content)

    # Replaces the while loop and input()
    if prompt := st.chat_input("YOU: "):
        
        # Instantly show the user's message on screen
        with st.chat_message("user"):
            st.write(prompt)
            
        # Append the new prompt to the history
        st.session_state.messages.append(HumanMessage(content=prompt))
        
        # Invoke the model with the FULL history (System prompt + all messages)
        with st.chat_message("assistant"):
            response = primary_model.invoke(st.session_state.messages)
            st.write(response.content)
            
        # Append the AI's response to the history
        st.session_state.messages.append(AIMessage(content=response.content))
        
    # Replaces the 'exit' command to end the chat and reset
    st.divider()
    if st.button("Exit / Reset Chat"):
        st.session_state.setup_complete = False
        st.session_state.messages = []
        st.rerun()