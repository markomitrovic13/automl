import os
import tkinter as tk
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class SimpleGUI:
    def __init__(self):
        # Setup Gemini
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel('gemini-2.5-flash-lite')
        
        # Setup GUI
        self.root = tk.Tk()
        self.root.title("Gemini Chat")
        
        # Input field
        self.input_text = tk.Text(self.root, height=3)
        self.input_text.pack(pady=10)
        
        # Send button
        self.send_btn = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_btn.pack()
        
        # Response field
        self.response_text = tk.Text(self.root, height=10)
        self.response_text.pack(pady=10)
        
    def send_message(self):
        user_input = self.input_text.get("1.0", tk.END).strip()
        if user_input:
            response = self.model.generate_content(user_input)
            self.response_text.delete("1.0", tk.END)
            self.response_text.insert("1.0", response.text)
            self.input_text.delete("1.0", tk.END)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SimpleGUI()
    app.run()
