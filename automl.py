import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class GeminiClient:
    def __init__(self):
        """Initialize Gemini API client with API key from environment variables."""
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash-lite')
    
    def send_message(self, message, model_name="gemini-2.5-flash-lite"):
        """
        Send a message to Gemini and get a response.
        
        Args:
            message (str): The message to send to Gemini
            model_name (str): The Gemini model to use
            
        Returns:
            str: Gemini's response
        """
        try:
            # Update model if different from default
            if model_name != "gemini-2.5-flash-lite":
                self.model = genai.GenerativeModel(model_name)
            
            response = self.model.generate_content(message)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"

def main():
    """Example usage of the Gemini client."""
    try:
        gemini = GeminiClient()
        
        # Example message
        message = "Hello! Can you help me with a simple task?"
        response = gemini.send_message(message)
        
        print("User:", message)
        print("Gemini:", response)
        
    except ValueError as e:
        print(f"Setup error: {e}")
        print("Please make sure you have set GEMINI_API_KEY in your .env file")

if __name__ == "__main__":
    main()
