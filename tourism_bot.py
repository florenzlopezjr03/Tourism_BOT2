#!/usr/bin/env python3
"""
Tourism Bot powered by Mistral AI
A conversational assistant for travel planning, destination recommendations, and tourism advice.
"""

import os
from dotenv import load_dotenv
from mistralai import Mistral

# Load environment variables from .env file
load_dotenv()

# Initialize Mistral client
API_KEY = os.getenv("MISTRAL_API_KEY")
if not API_KEY:
    raise ValueError("MISTRAL_API_KEY not found in environment variables")

client = Mistral(api_key=API_KEY)

# Conversation history for multi-turn dialogue
conversation_history = []

# System prompt for the tourism bot
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


def chat(user_message: str) -> str:
    """
    Send a message to the tourism bot and get a response.
    
    Args:
        user_message: The user's input message
        
    Returns:
        The bot's response
    """
    # Add user message to conversation history
    conversation_history.append({
        "role": "user",
        "content": user_message
    })
    
    # Call Mistral API with conversation history
    response = client.chat.complete(
        model="mistral-large-latest",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            *conversation_history
        ]
    )
    
    # Extract and store the bot's response
    bot_response = response.choices[0].message.content
    conversation_history.append({
        "role": "assistant",
        "content": bot_response
    })
    
    return bot_response


def main():
    """Main function to run the tourism bot in interactive mode."""
    print("\n" + "="*60)
    print("🌍 Welcome to the Tourism Bot powered by Mistral AI!")
    print("="*60)
    print("I'm here to help you plan your next adventure.")
    print("Ask me about destinations, travel tips, recommendations, and more!")
    print("Type 'exit' or 'quit' to end the conversation.\n")
    
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("\nBot: Thank you for chatting with me! Have a wonderful journey ahead! 🚀")
                break
            
            # Skip empty input
            if not user_input:
                print("Bot: Please enter a message.\n")
                continue
            
            # Get bot response
            print("\nBot: ", end="", flush=True)
            response = chat(user_input)
            print(response)
            print()
            
        except KeyboardInterrupt:
            print("\n\nBot: Goodbye! Safe travels! 👋")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again.\n")


if __name__ == "__main__":
    main()
