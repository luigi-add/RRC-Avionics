from tkinter import *
import tkinter.messagebox
import tkinter.font as tkfont
import os, sys, random, socket
from PIL import ImageTk, Image, ImageDraw

# resolution of the screen
height = 480
width = 320
statusBackGround = 'cyan'


class Display:

    def __init__(self, master):
        self.__master = master
        # Set window parameters
        self.__master.resizable(width=False, height=False)
        self.__master.geometry('{}x{}'.format(height, width))
        # To make window borderless
        self.__master.overrideredirect(True)

        #Place main frame where items are to be displayed on
        self.__placeMainFrame()

        # Load compass image and render image
        load = Image.open(os.path.dirname(os.path.realpath(__file__)) + "/../appImages/rocketry.png")
        load.thumbnail(size=(220, 435))
        render = ImageTk.PhotoImage(load)

        self.__img = Label(self.__mainFrame, image=render, bg=statusBackGround)
        self.__img.image = render
        self.__img.pack()

    def __placeMainFrame(self):
        self.__mainFrame = Frame(self.__master, height=220, width=475, bg=statusBackGround)
        self.__mainFrame.pack_propagate(False)
        self.__mainFrame.place(x=4, y=22)

root = Tk()
display = Display(root)
root.mainloop()