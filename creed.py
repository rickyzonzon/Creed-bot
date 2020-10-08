# Creed program

import tkinter as Tk
from gui import GUI
from va_core import record, wakeWord
import warnings

# Ignore any warning messages
warnings.filterwarnings('ignore')

if __name__ == '__main__':

    while True:
        text_or_speech = input("Would you like to use speech or text to communicate ('speech' or 'text')?\n")

        if text_or_speech.lower() != 'speech' and text_or_speech.lower() != 'text':
            print("You did not type 'speech' or 'text'.")
        elif text_or_speech.lower() == 'speech':
            # print("Say 'hey Creed' or 'yo Creed' to activate Creed.")
            # break
            print("not implemented yet")
        else:
            print("Type 'hey Creed' or 'yo Creed' to activate Creed.")
            break

    while True:
        if text_or_speech.lower() == 'speech':
            sentence = record()
            print(f"You: {sentence}")
            if wakeWord(sentence):
                break
        else:
            sentence = input("You: ")
            if wakeWord(sentence):
                break

    root = Tk.Tk()
    root.wm_title("Creed")
    gui = GUI(root)
    gui.text_or_speech = text_or_speech
    gui.pack()
    root.mainloop()
