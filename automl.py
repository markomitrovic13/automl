import os
import tkinter as tk
from tkinter import filedialog
import pandas as pd
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
        
        # Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=5)
        
        self.send_btn = tk.Button(button_frame, text="Send", command=self.send_message)
        self.send_btn.pack(side=tk.LEFT, padx=5)
        
        self.upload_btn = tk.Button(button_frame, text="Upload CSV", command=self.upload_csv)
        self.upload_btn.pack(side=tk.LEFT, padx=5)
        
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

    def upload_csv(self):
        file_path = filedialog.askopenfilename() #Let the user select the file.
        if file_path:
            global data
            data = pd.read_csv(file_path, header = None) #Load the file data into a pandas df.
            self.history_text.insert(tk.END, f"You uploaded CSV: {os.path.basename(file_path)}\n")
            self.history_text.see(tk.END)

            header_query = "These are the first three rows of the csv file: " + data.iloc[:3].to_string() + \
                            "Do you think the first row should be used as the header? Please respond with 'yes' or 'no'."
            header_response = self.model.generate_content(header_query)
            if header_response.text == "yes":
                data.columns = data.iloc[0]
                data = data.iloc[1:]
            
            print(data)

    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SimpleGUI()
    app.run()
