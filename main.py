from tkinter import *
from tkinter.scrolledtext import ScrolledText
import threading
from openai import OpenAI

# My API key
client = OpenAI(api_key="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")

# Root window
root = Tk()
root.title("Love Interest")
root.config(bg='#ffc0cb', pady=50, padx=50, )

# Icon
image_1 = PhotoImage(file="./Heart3.ppm")
root.iconphoto(False, image_1)

# Labels
Title = Label(text="Heart2Heart: A Romantic Chat Experience", font=("Ariel", 15, "italic"), bg="#ffc0cb")
Title.grid(row=0, column=0)

enter_here = Label(text="Type here:", font=("Ariel", 10, "italic"), bg="#ffc0cb")
enter_here.place(x=31, y=372)

# Chat log area
chat_log = ScrolledText(root, state='disabled', width=50, height=20, highlightthickness=0)
chat_log.grid(padx=10, pady=10, row=1, column=0)

# Message entry field
message_var = StringVar()
message_entry = Entry(root, textvariable=message_var, width=40, highlightthickness=0)
message_entry.grid(padx=10, pady=(0, 10), row=2, column=0)


# Handles the API response and displays it
def display_response(response):
    chat_log.config(state='normal')
    chat_log.insert(END, "AI: " + response + "\n \n")
    chat_log.yview(END)  # Auto-scroll to the end
    chat_log.config(state='disabled')


# Calls API asynchronously
def call_openai_api_async(message):
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "This is a charming and flirtatious conversational agent designed to "
                                              "act as a romantic partner for Valentine's Day. It exudes warmth, "
                                              "compliments generously, and engages in playful banter, creating a "
                                              "loving and affectionate atmosphere. The agent has its own unique "
                                              "personality, making the conversation engaging and full of romantic "
                                              "flirtation. You Limit your messages to under 40 words"},
                {"role": "user", "content": message}
            ],
            max_tokens=50,
            temperature=0.5,
            frequency_penalty=0.5

        )
        # Accesses the messages content
        response_text = completion.choices[0].message.content  # Corrected line
        root.after(0, display_response, response_text)
    except Exception as e:
        print("Error calling OpenAI API:", e)
        root.after(0, display_response, "Sorry, I couldn't fetch a response.")


# Send messages AI API
def send_message():
    message = message_var.get()
    if message:  # If the message is not empty
        chat_log.config(state='normal')
        chat_log.insert(END, "You: " + message + "\n \n")
        chat_log.yview(END)  # Auto-scroll
        chat_log.config(state='disabled')
        message_var.set("")  # Clears the entry field
        # Calls API
        threading.Thread(target=call_openai_api_async, args=(message,)).start()


message_entry.bind("<Return>", lambda event: send_message())

# Send button
send_button = Button(root, text="Send", command=send_message)
send_button.grid(pady=(0, 10))

# Runs the application
root.mainloop()
