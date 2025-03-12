import google.generativeai as genai

class CallGemini:
    '''
    This class is used to call the Gemini API.
    '''
    def __init__(self, api:str):
        self.api = api
        self.model = genai
    def configure(self):
        self.model.configure(api_key=self.api)
        return self.model
