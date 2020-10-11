# Creed program

import tkinter as Tk
from cores.gui_core import GUI
from cores.va_core import record, wakeWord
import warnings
import os, time

# Ignore any warning messages
warnings.filterwarnings("ignore")

if __name__ == "__main__":

    while True:
        train_creed = input("Would you like to retrain creed (y/n)? Note: Retraining Creed may take several minutes.\n")

        if train_creed.lower() == "y":
            print("Creed's speech and emotion will now both be retrained.\n")
            time.sleep(2)
            print("Training speech...")
            os.system("python bot_trainer\\train_speech.py")
            print("Training emotion...")
            os.system("python bot_trainer\\train_emotion.py")
            print("Training complete.\n")
            print("Proceeding to Creed...")
            time.sleep(2)
            break
        elif train_creed.lower() == "n":
            print("Proceeding to Creed...")
            time.sleep(2)
            break
        else:
            print("Type 'y' or 'n' please.")

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
        if text_or_speech.lower() == "speech":
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
    gui.creed.log.close()
