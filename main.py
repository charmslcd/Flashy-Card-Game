from tkinter import *
import pandas as pd
from random import random, choice, randint

BACKGROUND_COLOR = "#B1DDC6"
LANGAUGE_FONT = "Ariel", 40, "italic"
WORD_FONT = "Ariel", 60, "bold"


try:
    data = pd.read_csv("data/words_to_learn.csv")
    print("words to learn file found...")
except FileNotFoundError:
    original_data = pd.read_csv("data/spanish_words.csv")
    print("words_to_learn does not exist...")
    spanish_words_to_learn = original_data.to_dict(orient="records")
else:
    spanish_words_to_learn = data.to_dict(orient="records")

print(spanish_words_to_learn)
current_card = {}


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = choice(spanish_words_to_learn)
    spanish_word = current_card["spanish"]
    canvas.itemconfig(card_title, text="Spanish", fill="black")
    canvas.itemconfig(card_word, text=spanish_word, fill="black")
    canvas.itemconfig(card, image=card_front_img)
    flip_timer = window.after(3000, flip_card)
    print(len(spanish_words_to_learn))


def is_known():
    spanish_words_to_learn.remove(current_card)
    next_card()


def flip_card():
    global card_back_img
    canvas.itemconfig(card, image=card_back_img)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["english"], fill="white")


def on_closing():
    print("Window closing...")
    words_to_learn_df = pd.DataFrame(spanish_words_to_learn)
    words_to_learn_df.to_csv("data/words_to_learn.csv", index=False)
    print("words_to_learn.csv file updated")
    window.destroy()


# ------------------------------- UI ------------------------------------

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=25, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="Title", font=LANGAUGE_FONT)
card_word = canvas.create_text(400, 263, text="word", font=WORD_FONT)
canvas.grid(row=0, column=0, columnspan=2)

wrong_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_img, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=0)

right_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_img, highlightthickness=0, command=is_known)
right_button.grid(row=1, column=1)

next_card()

window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()

