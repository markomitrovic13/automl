import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class GeminiClient:
    def __init__(self, default_model="gemini-2.5-flash-lite"):
        #Initialize Gemini API with API key from .env file
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.default_model = default_model
        self.model = genai.GenerativeModel(self.default_model)
    
    def send_message(self, message, model_name="gemini-2.5-flash-lite"):
        # Update model if different from default
        if model_name != self.default_model:
            self.model = genai.GenerativeModel(model_name)
            
        response = self.model.generate_content(message)
        return response.text

def main():
    gemini = GeminiClient()
        
    # Example message
    message = "Hello! Can you help me with a simple task?"
    response = gemini.send_message(message)
        
    print("User:", message)
    print("Gemini:", response)

if __name__ == "__main__":
    main()
