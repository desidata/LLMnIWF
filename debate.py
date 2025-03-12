import google.generativeai as genai
import time
from langchain.memory import ConversationBufferMemory

import sys
sys.stdout.reconfigure(encoding='utf-8')

# Configure first Gemini API (Proponent - FOR the topic)
genai_A = genai
genai_A.configure(api_key="")

# Configure second Gemini API (Opponent - AGAINST the topic)
genai_B = genai
genai_B.configure(api_key="")


def query_gemini(model, prompt, memory):
    model_instance = model.GenerativeModel("gemini-pro")
    
    # Retrieve conversation history from memory
    history = memory.load_memory_variables({}).get("history", [])
    
    # Generate response from model
    response = model_instance.generate_content(prompt)
    reply = response.text

    # Save context for future turns
    memory.save_context({"input": prompt}, {"output": reply})
    
    return reply


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
        response_proponent = query_gemini(genai_A, proponent_prompt, memory_proponent)
        print(f"PROPONENT (FOR the topic): {response_proponent}")

        # Opponent (Gemini_B) argues AGAINST the topic
        response_opponent = query_gemini(genai_B, opponent_prompt, memory_opponent)
        print(f"OPPONENT (AGAINST the topic): {response_opponent}")

        # Refining prompts based on discussion progress
        proponent_prompt = f"Refute the opponent's arguments: {response_opponent}. Strengthen your stance."
        opponent_prompt = f"Counter the proponent's claims: {response_proponent}. Expose weaknesses in their argument."

        time.sleep(1)  # Prevent API rate limits

    print("\nDEBATE CONCLUDED")

# Start Debate
debate("90-hour workweek in India: Good or Bad?")