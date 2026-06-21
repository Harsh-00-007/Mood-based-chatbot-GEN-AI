import streamlit as st
from pydantic import BaseModel, Field
from typing import List, Optional
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

# 1. Load environment variables
load_dotenv()

# 2. Configure the web page layout
st.set_page_config(page_title="AI Portfolio Hub", layout="wide")
st.title("Enterprise AI Solutions")

# 3. Create UI Tabs for your two different tools
tab1, tab2 = st.tabs(["📊 B2B Mobile Extractor", "🎭 Persona Chatbot"])

# ==========================================
# TAB 1: THE B2B MOBILE RETAILER TOOL
# ==========================================
with tab1:
    st.header("Mobile Inventory Data Extractor")
    st.markdown("Enter a mobile phone model to extract technical specs into a strict JSON format.")

    # A. Define the Pydantic Structure
    class MobileDetails(BaseModel):
        brand: str = Field(description="The brand of the mobile phone (e.g., Apple, Samsung, OnePlus)")
        model_name: str = Field(description="The specific model name and variant details")
        estimated_price_inr: str = Field(description="Approximate market price in INR. Use 'Unknown' if not found.")
        processor: str = Field(description="The processor/chipset details")
        ram_storage_options: List[str] = Field(description="List of available RAM and Storage configurations")
        key_selling_points: List[str] = Field(description="3-4 bullet points highlighting why a customer would buy this phone")

    # B. Initialize the Groq model (Low temperature for accuracy)
    retail_model = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.1 
    )

    # C. Bind schema and create chain
    structured_llm = retail_model.with_structured_output(MobileDetails)
    retail_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert mobile retail inventory assistant. Extract and provide detailed, accurate technical and market specifications for the requested mobile phone. If a specific detail is completely unknown, output 'N/A'."),
        ("human", "Provide details for the phone: {mobile_query}")
    ])
    extraction_chain = retail_prompt | structured_llm

    # D. Build the UI Input
    mobile_query = st.text_input("Enter Mobile Phone Name (e.g., Samsung S24 Ultra):", key="retail_input")
    
    if st.button("Extract Specifications", type="primary"):
        if mobile_query:
            with st.spinner("Fetching and structuring data from LLaMA 3.3..."):
                try:
                    result = extraction_chain.invoke({"mobile_query": mobile_query})
                    
                    st.success("Data Extracted Successfully!")
                    
                    # Display metrics cleanly
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Brand", result.brand)
                    col2.metric("Model", result.model_name)
                    col3.metric("Est. Price (INR)", result.estimated_price_inr)
                    
                    st.divider()
                    
                    # Display Lists
                    st.subheader("Hardware Configurations")
                    st.write(f"**Processor:** {result.processor}")
                    st.write("**Available Variants:**")
                    for option in result.ram_storage_options:
                        st.markdown(f"- {option}")
                        
                    st.subheader("Key Selling Points")
                    for point in result.key_selling_points:
                        st.markdown(f"- {point}")
                        
                    # Display the exact JSON dump from your CLI code
                    with st.expander("View DATABASE READY JSON"):
                        st.code(result.model_dump_json(indent=4), language="json")
                        
                except Exception as e:
                    st.error(f"[SYSTEM ERROR]: An error occurred during extraction: {e}")
        else:
            st.warning("Please enter a valid phone name.")

# ==========================================
# TAB 2: THE MOOD-BASED CHATBOT
# ==========================================
with tab2:
    st.header("Interactive Persona Chatbot")
    
    # A. Initialize model (High temperature for creativity)
    chat_model = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.7 
    )

    # B. Setup Session State to remember the chat history
    if "chat_setup_complete" not in st.session_state:
        st.session_state.chat_setup_complete = False
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    # C. UI Step 1: Mood Selection (Replaces your 1, 2, 3 terminal input)
    if not st.session_state.chat_setup_complete:
        choice = st.radio(
            "Select AI Personality Mode:",
            options=["😡 Angry Mode", "😢 Sad Mode", "🤡 Funny Mode"]
        )
        
        if st.button("Start Conversation", key="start_chat"):
            if "Angry" in choice:
                mode = "You are a very angry ai and answer every message aggressively"
            elif "Sad" in choice:
                mode = "You are a very sad ai and answer every message sadly"
            else:
                mode = "You are a very funny ai and answer every message in a joke way"
                
            # Save the system prompt to memory
            st.session_state.chat_messages = [SystemMessage(content=mode)]
            st.session_state.chat_setup_complete = True
            st.rerun()

    # D. UI Step 2: The Chat Interface
    if st.session_state.chat_setup_complete:
        
        # Determine avatar based on mood
        current_mood_text = st.session_state.chat_messages[0].content
        if "angry" in current_mood_text:
            ai_avatar = "😡"
        elif "sad" in current_mood_text:
            ai_avatar = "😢"
        else:
            ai_avatar = "🤡"

        # Render chat history
        for msg in st.session_state.chat_messages:
            if isinstance(msg, SystemMessage):
                continue
            
            role = "user" if isinstance(msg, HumanMessage) else "assistant"
            avatar = "🧑‍💻" if role == "user" else ai_avatar
            
            with st.chat_message(role, avatar=avatar):
                st.write(msg.content)

        # Handle new user input
        if prompt := st.chat_input("Type your message here..."):
            
            with st.chat_message("user", avatar="🧑‍💻"):
                st.write(prompt)
                
            st.session_state.chat_messages.append(HumanMessage(content=prompt))
            
            with st.chat_message("assistant", avatar=ai_avatar):
                try:
                    response = chat_model.invoke(st.session_state.chat_messages)
                    st.write(response.content)
                    st.session_state.chat_messages.append(AIMessage(content=response.content))
                except Exception as e:
                    st.error(f"[SYSTEM ERROR]: {e}")
            
        st.divider()
        if st.button("End Chat / Choose New Mood"):
            st.session_state.chat_setup_complete = False
            st.session_state.chat_messages = []
            st.rerun()