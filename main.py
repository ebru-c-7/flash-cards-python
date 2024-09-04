import tkinter
import pandas
import random
import os

BACKGROUND_COLOR = "#B1DDC6"

data = pandas.read_csv("data/words.csv")
to_learn = list(filter(lambda x: x["Done"] != "ok", data.to_dict(orient="records")))

current_card = {}


def reset():
    global to_learn

    data["Done"] = data["Done"].replace("ok", "")
    data.to_csv("data/words.csv", index=False)

    to_learn = data.to_dict(orient="records")

    button_right.config(image=right)
    button_wrong.config(image=wrong)

    canvas_reset.place(x=330, y=550)

    next_card()


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)

    if len(to_learn) == 0:
        canvas.itemconfig(card_bg, image=canvas_front)
        canvas.itemconfig(canvas_title, text="DONE!!", fill="black")
        canvas.itemconfig(canvas_word, text="", fill="black")
        canvas.itemconfig(canvas_stat, text="", fill="black")

        button_right.config(image="")
        button_wrong.config(image="")

        canvas_reset.place(x=330, y=263)

        return

    current_card = random.choice(to_learn)
    canvas.itemconfig(card_bg, image=canvas_front)
    canvas.itemconfig(canvas_title, text="Deutsch", fill="black")
    canvas.itemconfig(canvas_word, text=current_card["Deutsch"], fill="black")
    canvas.itemconfig(canvas_stat, text=f"{len(to_learn)}/{len(data)}", fill="black")

    flip_timer = window.after(3000, func=flip_card)


def card_done():
    # locate the row to update
    row_index = data.loc[data["Deutsch"] == current_card["Deutsch"]].index[0]
    # update the row with new values
    data.loc[row_index, "Done"] = "ok"
    list_index = to_learn.index(current_card)
    if list_index >= 0:
        to_learn.pop(list_index)
    data.to_csv("data/words.csv", index=False)

    next_card()


def flip_card():
    global current_card
    canvas.itemconfig(canvas_title, text="English", fill="white")
    canvas.itemconfig(canvas_stat, fill="white")
    canvas.itemconfig(canvas_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_bg, image=canvas_back)


window = tkinter.Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

# card canvas
canvas = tkinter.Canvas(width=800, height=526)
canvas_front = tkinter.PhotoImage(file="images/card_front.png")
canvas_back = tkinter.PhotoImage(file="images/card_back.png")
canvas.config(background=BACKGROUND_COLOR, highlightthickness=0)
card_bg = canvas.create_image(
    400, 263, image=canvas_front
)  # center coordinates, half values relative to canvas
canvas.grid(row=0, column=0, columnspan=2)
canvas_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
canvas_word = canvas.create_text(400, 263, text="", font=("Ariel", 40, "bold"))
canvas_stat = canvas.create_text(700, 50, text="", font=("Ariel", 20, "bold"))

canvas_reset = tkinter.Button(
    text="Restart",
    font=("Ariel", 25, "bold"),
    background="red",
    command=reset,
    highlightthickness=0,
    foreground="white",
)

canvas_reset.place(x=330, y=550)

right = tkinter.PhotoImage(file="images/right.png")
button_right = tkinter.Button(
    image=right,
    highlightthickness=0,
    background=BACKGROUND_COLOR,
    borderwidth=0,
    command=card_done,
)
button_right.grid(row=1, column=1)

wrong = tkinter.PhotoImage(file="images/wrong.png")
button_wrong = tkinter.Button(
    image=wrong,
    highlightthickness=0,
    background=BACKGROUND_COLOR,
    borderwidth=0,
    command=next_card,
)
button_wrong.grid(row=1, column=0)

next_card()

window.mainloop()
