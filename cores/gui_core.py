# GUI

from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import *
import tkinter as Tk
from tkinter import Frame, INSERT
from cores.chat_core import ChatCore
from cores.va_core import record


# GUI class to create a GUI
class GUI(Tk.Frame):

    def __init__(self, parent):
        Tk.Frame.__init__(self, parent)
        self.parent = parent
        self.creed = ChatCore()
        self.emotions = self.creed.emotions
        self.text_or_speech = 'text'
        self.user = Tk.StringVar()
        self.communicate_frame = Frame(master=self, width=300, height=450)
        self.emotions_frame = Frame(master=self, width=500, height=450)
        self.user_input = Tk.Entry(master=self.communicate_frame, textvariable=self.user, relief='sunken', font="Helvetica_Neue 10")
        self.canvas = FigureCanvasTkAgg(self.emotions.fig, master=self.emotions_frame)
        self.close = Tk.Button(master=self.emotions_frame, text="Quit", command=self._quit).pack(anchor='nw')
        self.dummy = Tk.Message(master=self.communicate_frame)
        self.messages = Tk.Text(master=self.communicate_frame, state="disabled", font="Helvetica_Neue 10")
        self.ani = FuncAnimation(self.emotions.fig, self.emotions.update, frames=self.emotions.generator,
                                 interval=1, init_func=self.emotions.initialize)
        self.initialize()

    # initialize the tkinter elements
    def initialize(self):
        self.emotions_frame.pack_propagate(False)
        self.communicate_frame.pack_propagate(False)
        self.messages.pack(side="top", anchor="n")
        self.receive("hi")
        self.dummy.pack(side="top", anchor="center")
        self.user_input.bind('<Return>', self.send)
        self.canvas.get_tk_widget().bind('<Button-1>', self.callback)
        self.communicate_frame.pack(side="right", fill="both")
        self.emotions_frame.pack(side="left", fill="both")
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(anchor='w', padx=50)
        self.user_input.pack(side="top", anchor="s")

    # close Creed
    def _quit(self):
        self.quit()
        self.destroy()

    # Takes focus away from entry when clicking off of it
    def callback(self, event):
        self.canvas.get_tk_widget().focus_set()

    # Send your message to receive, message shows up in textbox
    def send(self, event):
        if self.text_or_speech == 'text':
            sentence = self.user_input.get()
            self.messages.configure(state="normal")
            self.messages.insert(INSERT, 'You: %s\n' % sentence)
            self.user_input.delete(0, 'end')
            self.receive(sentence)
            self.messages.configure(state="disabled")
        else:
            # not functional yet
            sentence = record()
            self.user_input.insert(sentence)
            self.messages.configure(state="normal")
            self.messages.insert(INSERT, 'You: %s\n' % sentence)
            self.user_input.delete(0, 'end')
            self.receive(sentence)
            self.messages.configure(state="disabled")
            self.messages.see("end")

    # Get Creed's response to your message, response shows up in textbox
    def receive(self, sentence):
        self.messages.configure(state="normal")
        response = self.creed.chat(sentence)
        self.messages.insert(INSERT, '%s\n' % response)
        self.messages.configure(state="disabled")
