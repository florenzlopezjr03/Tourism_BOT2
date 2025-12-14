import streamlit as st
import os
from dotenv import load_dotenv
from mistralai import Mistral

# Load environment variables from .env (for local development)
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Tourism Bot",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .header-title {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Get API key from environment or Streamlit secrets
API_KEY = os.getenv("MISTRAL_API_KEY")
if not API_KEY:
    try:
        API_KEY = st.secrets.get("MISTRAL_API_KEY")
    except Exception:
        pass

if not API_KEY:
    st.error("""
    ❌ **API Key Not Found**
    
    To use this bot, you need to add your Mistral API key:
    
    **Local Development:**
    1. Create a `.env` file in the project root
    2. Add: `MISTRAL_API_KEY=your_api_key_here`
    
    **Streamlit Cloud Deployment:**
    1. Go to your app settings
    2. Add a secret: `MISTRAL_API_KEY=your_api_key_here`
    """)
    st.stop()

try:
    client = Mistral(api_key=API_KEY)
except Exception as e:
    st.error(f"❌ Failed to initialize Mistral client: {str(e)}")
    st.stop()

# System prompt for tourism bot
SYSTEM_PROMPT = """You are a helpful and knowledgeable tourism assistant powered by Mistral AI. 
You provide:
- Destination recommendations based on traveler preferences
- Practical travel tips and logistics advice
- Cultural insights and local recommendations
- Budget planning for trips
- Best times to visit different locations
- Visa and documentation information
- Transportation and accommodation suggestions
- Weather and climate information
- Local cuisine and dining recommendations
- Safety and health advice for travelers

Be friendly, engaging, and thorough in your responses. Always ask clarifying questions to better understand the traveler's needs."""

# Initialize session state for conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Header
st.markdown("<h1 class='header-title'>🌍 Tourism Bot - Travel Planning Assistant</h1>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar with info
with st.sidebar:
    st.title("ℹ️ About This Bot")
    st.info(
        """
        **Tourism Bot** powered by **Mistral AI**
        
        This bot helps you with:
        - 🏖️ Destination recommendations
        - 💰 Budget planning
        - 📅 Best times to visit
        - 🗺️ Travel itineraries
        - 🍽️ Local cuisine tips
        - 🛂 Visa information
        - 🚚 Transportation advice
        - 🏨 Accommodation suggestions
        """
    )
    
    st.divider()
    
    if st.button("🔄 Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    
    st.markdown("""
    **Tips for better responses:**
    - Be specific about your preferences
    - Mention your budget and travel duration
    - Ask follow-up questions for clarification
    - Share your interests (food, culture, nature, adventure, etc.)
    """)

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("Ask me about destinations, travel tips, budgets, and more...", key="user_input")

if user_input:
    # Add user message to history and display
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Generate bot response
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            try:
                # Prepare messages for API call
                api_messages = [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    *st.session_state.messages
                ]
                
                # Call Mistral API
                response = client.chat.complete(
                    model="mistral-large-latest",
                    messages=api_messages
                )
                
                # Extract response
                bot_response = response.choices[0].message.content
                
                # Add to history and display
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
                st.markdown(bot_response)
                
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                st.error(error_msg)
                # Remove the user message if API call failed
                st.session_state.messages.pop()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; font-size: 0.9rem;'>
    <p>🌍 Tourism Bot | Powered by Mistral AI | Safe travels! ✈️</p>
    </div>
    """,
    unsafe_allow_html=True
)
