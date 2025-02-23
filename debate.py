import google.generativeai as genai
import time
from langchain.memory import ConversationBufferMemory
import sys

# Configure first Gemini API (Pro-Science)
genai_A = genai
genai_A.configure(api_key="")

# Configure second Gemini API (Anti-Science)
genai_B = genai
genai_B.configure(api_key="")


# Function to Simulate Typing Effect
def typing_effect(text, typing_speed=0.003):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(typing_speed)
    print()  # Add a newline at the end

# Define Query Functions with Memory Usage
def query_gemini_A(prompt, memory):
    model = genai_A.GenerativeModel("gemini-pro")

    # Retrieve past context from memory
    past_context = memory.load_memory_variables({})["history"]
    
    # Combine past context with the new prompt
    full_prompt = f"{past_context}\n{prompt}" if past_context else prompt
    
    response = model.generate_content(full_prompt)
    reply = response.text

    # Save new conversation data
    memory.save_context({"input": prompt}, {"output": reply})

    return reply

def query_gemini_B(prompt, memory):
    model = genai_B.GenerativeModel("gemini-pro")

    # Retrieve past context from memory
    past_context = memory.load_memory_variables({})["history"]
    
    # Combine past context with the new prompt
    full_prompt = f"{past_context}\n{prompt}" if past_context else prompt
    
    response = model.generate_content(full_prompt)
    reply = response.text

    # Save new conversation data
    memory.save_context({"input": prompt}, {"output": reply})

    return reply

# Memory for tracking arguments (Now Actually Used)
memory_pro = ConversationBufferMemory()   # Memory for Pro-Motion (Professor X)
memory_con = ConversationBufferMemory()   # Memory for Anti-Motion (Professor Y)

# Define Debate Function
def debate(topic, rounds=3):
    print(f"\n🎤 **DEBATE BEGINS**: {topic}")

    # Opening statements
    pro_prompt = f"You are Professor X, an economist supporting the motion. Open the debate with strong arguments for why {topic}. Keep it short, max two sentences."
    con_prompt = f"You are Professor Y, an economist against the motion. Respond with strong counterarguments against why {topic}. Keep it short, max two sentences."

    for i in range(rounds):
        print(f"\n🔄 **Round {i+1}**")

        # Opening argument by Pro-Motion
        response_pro = query_gemini_A(pro_prompt, memory_pro)
        print(f"✅ **Pro-Motion (Professor X)**: ", end="")
        typing_effect(response_pro)

        # Rebuttal by Anti-Motion
        response_con = query_gemini_B(con_prompt, memory_con)
        print(f"❌ **Anti-Motion (Professor Y)**")
        typing_effect(response_con)

        # Refining arguments for the next round
        pro_prompt = f"Rebut this counterargument: {response_con}. Strengthen your position with data or logic. Keep it short, just a single paragraph."
        con_prompt = f"Rebut this argument: {response_pro}. Strengthen your position with new angles. Keep it short, just a single paragraph."

        time.sleep(1)  # Prevent API rate limits

    print("\n📢 **CLOSING STATEMENTS**")

    # Closing Arguments
    pro_final = query_gemini_A("Summarize your final argument in one paragraph.", memory_pro)
    con_final = query_gemini_B("Summarize your final argument in one paragraph.", memory_con)

    print(f"✅ **Pro-Motion (Professor X) - Final Words**")
    typing_effect(pro_final)
    print(f"❌ **Anti-Motion (Professor Y) - Final Words**")
    typing_effect(con_final)
    print("\n🏆 **DEBATE CONCLUDED**")

# Start Debate
debate("Indians should work in their workplaces for 90 hours a week to boost the economy. ")