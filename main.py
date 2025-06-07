import tkinter as tk
from tkinter import scrolledtext
import threading
from time import sleep
from queue import Queue
from supportbot import process_nltk, closed, login  # Import necessary functions

# Create queues for input, output, and conversation end
input_queue = Queue()
output_queue = Queue()
end_queue = Queue()

# Custom functions for the bot thread
def get_input_bot():
    return input_queue.get()

def respond_bot(text):
    output_queue.put(text)

# Bot thread function to run CLI logic
def bot_thread():
    result = login(respond_bot, get_input_bot)
    if result:
        username, plan, Id = result
        while True:
            data = get_input_bot()
            process_nltk(data, respond_bot, get_input_bot, plan, Id)
            if closed():
                respond_bot("Conversation closed. This window will be close automatically. Exiting...")
                sleep(3)
                root.destroy()  # Exit the GUI if conversation is closed   
    end_queue.put(True)  # Signal conversation end

# Function to check output queue and update GUI
def check_output():
    while not output_queue.empty():
        text = output_queue.get()
        history.configure(state='normal')
        history.insert(tk.END, f"SupportBot: {text}\n")
        history.configure(state='disabled')
        history.see(tk.END)
    if not end_queue.empty():
        end_queue.get()
        entry.config(state='disabled')
    root.after(100, check_output)

# GUI setup
root = tk.Tk()
root.title("SupportBot GUI")
root.geometry("500x400")
root.attributes('-fullscreen', True)  # Fullscreen mode
root.configure(bg="black")

# Chat history
text_frame = tk.Frame(root, bg="light blue")
text_frame.pack(fill="both", expand=True)

scrollbar = tk.Scrollbar(text_frame)
scrollbar.pack(side="right", fill="y")

history = scrolledtext.ScrolledText(text_frame, wrap="word", font=("Arial", 12), bg="white", fg="black")
history.pack(side="left", fill="both", expand=True)
history.configure(state='disabled')

# Input field
input_frame = tk.Frame(root, bg="black")
input_frame.pack(fill="x", padx=10, pady=10)

label = tk.Label(input_frame, text="You: ", font=("Arial", 12), bg="black", fg="white")
label.pack(side="left")

entry = tk.Entry(input_frame, font=("Arial", 12), bg="white", fg="black", width=40)
entry.pack(side="left", fill="x", expand=True)

# Submit function
def submit(event=None):
    user_input = entry.get().strip()
    if user_input:
        history.configure(state='normal')
        history.insert(tk.END, f"You: {user_input}\n")
        history.configure(state='disabled')
        history.see(tk.END)
        entry.delete(0, tk.END)
        input_queue.put(user_input)

entry.bind('<Return>', submit)

# Start bot thread
thread = threading.Thread(target=bot_thread)
thread.start()

# Start checking output queue
check_output()

# Run GUI
root.mainloop()