import google.generativeai as genai
from models import CallGemini

class Query:
    def __init__(self, model:str, prompt:str, memory):
        self.model = model
        self.prompt = prompt
        self.memory = memory
    def query_gemini(self):
        model_instance = self.model.GenerativeModel("gemini-1.5-pro")
        response = model_instance.generate_content(self.prompt)
        reply = response.text if response.candidates and response.candidates[0].content.parts else "Unable to generate a response."
        self.memory.save_context({"input": self.prompt}, {"output": reply})
        return reply


