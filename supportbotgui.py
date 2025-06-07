import tkinter as tk
from tkinter import scrolledtext, font
import threading
from queue import Queue
from supportbot import process_nltk, closed, login  # Import your existing functions

# Queues for communication
input_queue = Queue()
output_queue = Queue()
end_queue = Queue()

# Functions for bot thread
def get_input_bot():
    return input_queue.get()

def respond_bot(text):
    output_queue.put(text)

# Bot thread logic
def bot_thread():
    result = login(respond_bot, get_input_bot)
    if result:
        username, plan, Id = result
        while True:
            data = get_input_bot()
            process_nltk(data, respond_bot, get_input_bot, plan, Id)
            if closed():
                break
    end_queue.put(True)  # Signal conversation end

# Function to insert messages in chat bubbles
def insert_message(text, tag):
    history.configure(state='normal')
    history.insert(tk.END, text + "\n", tag)
    history.configure(state='disabled')
    history.see(tk.END)

# Function to check output queue and update GUI
def check_output():
    while not output_queue.empty():
        text = output_queue.get()
        insert_message("SupportBot: " + text, 'bot')
    if not end_queue.empty():
        end_queue.get()
        entry.config(state='disabled')
        send_btn.config(state='disabled')
    root.after(100, check_output)

# GUI setup
root = tk.Tk()
root.title("SupportBot - AI Assistant")
root.geometry("700x550")
root.configure(bg="#f0f2f5")

# Fonts
chat_font = font.Font(family="Segoe UI", size=12)
button_font = font.Font(family="Segoe UI", size=10, weight="bold")

# Chat history frame
history_frame = tk.Frame(root, bg="#ffffff", bd=0)
history_frame.pack(padx=20, pady=15, fill="both", expand=True)

# ScrolledText for chat history
history = scrolledtext.ScrolledText(
    history_frame,
    wrap=tk.WORD,
    font=chat_font,
    bg="#ffffff",
    fg="#222222",
    padx=12,
    pady=12,
    insertbackground="#666666",
    selectbackground="#e0f0ff",
    bd=0,
    relief=tk.FLAT,
    state='disabled'
)
history.pack(fill="both", expand=True)

# Configure message tags for chat bubbles
history.tag_configure('bot',
    lmargin1=10, lmargin2=10, rmargin=80,
    spacing3=8, background="#e9f5ff",
    foreground="#222222", wrap=tk.WORD,
    borderwidth=0, relief="flat"
)
history.tag_configure('user',
    lmargin1=80, lmargin2=10, rmargin=10,
    spacing3=8, background="#0084ff",
    foreground="white", justify=tk.RIGHT,
    wrap=tk.WORD, borderwidth=0, relief="flat"
)

# Input frame
input_container = tk.Frame(root, bg="#ffffff", height=60)
input_container.pack(fill="x", padx=20, pady=(0, 20))

# Entry for user input
entry = tk.Entry(
    input_container,
    font=chat_font,
    bg="#f7f7f7",
    fg="#222222",
    insertbackground="#0084ff",
    relief=tk.FLAT,
    bd=0,
    highlightthickness=2,
    highlightcolor="#0084ff",
    highlightbackground="#cccccc"
)
entry.pack(side=tk.LEFT, fill="x", expand=True, padx=(0, 10), ipady=6)

# Send button with hover effects
def on_enter(e):
    send_btn.config(bg="#0066cc")

def on_leave(e):
    send_btn.config(bg="#0084ff")

def submit(event=None):
    user_input = entry.get().strip()
    if user_input:
        insert_message("You: " + user_input, 'user')
        entry.delete(0, tk.END)
        input_queue.put(user_input)

send_btn = tk.Button(
    input_container,
    text="Send",
    command=submit,
    font=button_font,
    bg="#0084ff",
    fg="white",
    activebackground="#0066cc",
    activeforeground="white",
    relief=tk.FLAT,
    bd=0,
    padx=20,
    pady=8,
    cursor="hand2"
)
send_btn.pack(side=tk.RIGHT)
send_btn.bind("<Enter>", on_enter)
send_btn.bind("<Leave>", on_leave)

entry.bind('<Return>', submit)

# Start bot thread
thread = threading.Thread(target=bot_thread, daemon=True)
thread.start()

# Start checking output queue
check_output()

# Run GUI
root.mainloop()
