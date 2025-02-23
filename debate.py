import google.generativeai as genai
import time
from langchain.memory import ConversationBufferMemory

import google.generativeai as genai
import time
from langchain.memory import ConversationBufferMemory

# Configure first Gemini API (Pro-Science)
genai_A = genai
genai_A.configure(api_key="")

# Configure second Gemini API (Anti-Science)
genai_B = genai
genai_B.configure(api_key="")ß


def query_gemini_A(prompt, memory=None):
    model = genai_A.GenerativeModel("gemini-pro")
    messages = []
    
    if memory:
        messages.extend(memory.load_memory_variables({})["history"])
    
    messages.append({"role": "user", "content": prompt})
    
    response = model.generate_content(prompt)
    reply = response.text
    
    if memory:
        memory.save_context({"input": prompt}, {"output": reply})
    
    return reply


def query_gemini_B(prompt, memory=None):
    model = genai_B.GenerativeModel("gemini-pro")
    messages = []
    
    if memory:
        messages.extend(memory.load_memory_variables({})["history"])
    
    messages.append({"role": "user", "content": prompt})
    
    response = model.generate_content(prompt)
    reply = response.text
    
    if memory:
        memory.save_context({"input": prompt}, {"output": reply})
    
    return reply



memory_explorer = ConversationBufferMemory()   # Memory for Explorer (Gemini API #1)
memory_contributor = ConversationBufferMemory()   # Memory for Contributor (Gemini API #2)



def discussion(topic, rounds=3):
    print(f"💡 DISCUSSION TOPIC: {topic}")
    
    explorer_prompt = f"Start an open discussion on: {topic}. Share your thoughts. Don't provide too lenthy answers."
    contributor_prompt = f"Continue the discussion on: {topic}. Share your thoughts. Don't provide too lenthy answers."

    for i in range(rounds):
        print(f"\n🔄 Round {i+1}")

        # Explorer (Gemini API #1) starts the discussion
        response_explorer = query_gemini_A(explorer_prompt, memory_explorer)
        print(f"🧠 EXPLORER (Gemini API #1): {response_explorer}")

        # Contributor (Gemini API #2) builds on the discussion
        response_contributor = query_gemini_B(contributor_prompt, memory_contributor)
        print(f"💡 CONTRIBUTOR (Gemini API #2): {response_contributor}")

        # Refining prompts based on previous responses
        explorer_prompt = f"Based on this, add further insights and new ideas: {response_contributor}"
        contributor_prompt = f"Continue the discussion, bringing in new angles: {response_explorer}"

        time.sleep(1)  # Prevent API rate limits

    print("\n🔹 DISCUSSION CONCLUDED")

# Start Discussion
discussion("90 hours workweek in India is good or bad?")
