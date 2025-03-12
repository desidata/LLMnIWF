import google.generativeai as genai
import time
from langchain.memory import ConversationBufferMemory
from models import CallGemini
from query import Query
import sys
sys.stdout.reconfigure(encoding='utf-8')


# Updated memory buffers with correct parameters
memory_proponent = ConversationBufferMemory(memory_key="history", return_messages=True)
memory_opponent = ConversationBufferMemory(memory_key="history", return_messages=True)


#  call two models with separate API keys
api_A = "your api"   # API Key for Gemini_A
api_B = "your api"   # API Key for Gemini_B

# Configure the models
gemini_A = CallGemini(api_A)
gemini_B = CallGemini(api_B)

# Updated memory buffers with correct parameters
memory_proponent = ConversationBufferMemory(memory_key="history", return_messages=True)
memory_opponent = ConversationBufferMemory(memory_key="history", return_messages=True)

def debate(topic, rounds=3):
    print(f"DEBATE TOPIC: {topic}\n")

    # Initial Stance Prompts
    proponent_prompt = f"Defend the topic: '{topic}'. Present strong arguments supporting it. Use economic, social, and productivity benefits."
    opponent_prompt = f"Argue against the topic: '{topic}'. Provide strong counterarguments, highlighting risks and disadvantages."

    for i in range(rounds):
        print(f"\nRound {i+1}")

        # Proponent (Gemini_A) argues FOR the topic
        preponent = Query(gemini_A, proponent_prompt, memory_proponent)
        response_proponent = preponent.query_gemini()
        print(f"PROPONENT (FOR the topic): {response_proponent}")

        # Opponent (Gemini_B) argues AGAINST the topic
        oponent = Query(gemini_B, opponent_prompt, memory_opponent)
        response_opponent = oponent.query_gemini()
        print(f"OPPONENT (AGAINST the topic): {response_opponent}")

        # Refining prompts based on discussion progress
        proponent_prompt = f"Refute the opponent's arguments: {response_opponent}. Strengthen your stance."
        opponent_prompt = f"Counter the proponent's claims: {response_proponent}. Expose weaknesses in their argument."

        time.sleep(1)  # Prevent API rate limits

    print("\nDEBATE CONCLUDED")

# Start Debate
debate("90-hour workweek in India: Good or Bad?")




