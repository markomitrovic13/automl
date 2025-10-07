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
        
        # History field (scrollable)
        self.history_text = tk.Text(self.root, height=15)
        scrollbar = tk.Scrollbar(self.root)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.history_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.history_text.yview)
        
        # Input field
        self.input_text = tk.Text(self.root, height=3)
        self.input_text.pack(pady=10)
        
        # Send button
        self.send_btn = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_btn.pack()
        
    def send_message(self):
        user_input = self.input_text.get("1.0", tk.END).strip()
        if user_input:
            # Add user message to history
            self.history_text.insert(tk.END, f"You: {user_input}\n\n")
            
            # Get Gemini response
            response = self.model.generate_content(user_input)
            
            # Add Gemini response to history
            self.history_text.insert(tk.END, f"Gemini: {response.text}\n\n")
            
            # Clear input and scroll to bottom
            self.input_text.delete("1.0", tk.END)
            self.history_text.see(tk.END)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SimpleGUI()
    app.run()
