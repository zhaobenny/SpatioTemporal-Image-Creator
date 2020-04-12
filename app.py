import tkinter as tk
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from functions import STI
import time


class App(tk.Tk):

    def __init__(self):
        self.getSTI = None
        self.fileName = None
        tk.Tk.__init__(self)
        self.title('CMPT 365 Final Project')
        self.geometry("580x380")
        load = Image.open("white.jpg")
        render = ImageTk.PhotoImage(load)
        self.img = Label(self, image=render)
        self.img.image = render
        self.img.grid(row = 0, column = 2)
        self.open = tk.Button(self, text='Open Video', width=25, command=self.getFileAction)
        self.open.grid(row = 1, column = 1)
        self.getHistogram = tk.Button(self, text='Run Histogram Difference', width=25, command=self.runHistogram)
        self.getHistogram.grid(row = 1, column = 2)
        self.getMiddleCol = tk.Button(self, text='Run Middle Col', width=9, command=self.runMiddleCol)
        self.getMiddleCol.grid(row = 1, column = 3)
        self.getMiddleRow = tk.Button(self, text='Run Middle Row', width=10, command=self.runMiddleRow)
        self.getMiddleRow.grid(row = 1, column = 4)
        self.rowconfigure(0, weight=2)

    def getFileAction(self):
        try:
            self.fileName = filedialog.askopenfilename()
            self.getSTI = STI(self.fileName)
        except:
            self.popupError("Something went wrong.")

    def runHistogram(self):
        if (self.getSTI):
            self.loading()
            if self.getSTI.histogramSTI():
                self.updateImage("histogramdifference.jpg")
        else:
            self.popupError("Error: No video loaded.")

    def runMiddleCol(self):
        if (self.getSTI):
            self.loading()
            if self.getSTI.columnSTI():
                self.updateImage("middlecolumn.jpg")
        else:
            self.popupError("Error: No video loaded.")

    def runMiddleRow(self):
        if (self.getSTI):
            self.loading()
            if self.getSTI.rowSTI():
                self.updateImage("middlerow.jpg")
        else:
            self.popupError("Error: No video loaded.")

    def updateImage(self, jpg):
        load = Image.open(jpg)
        render = ImageTk.PhotoImage(load)
        self.img.configure(image = render)
        self.img.photo_ref = render

    def loading(self):
        load = Image.open("loading.jpg")
        render = ImageTk.PhotoImage(load)
        self.img.configure(image = render)
        self.img.photo_ref = render
        self.img.update()

    def popupError(self, msg):
        popup = tk.Tk()
        popup.wm_title("!")
        label = tk.Label(popup, text=msg)
        label.pack(side="top", fill="x", pady=10)
        B1 = tk.Button(popup, text="Okay", command = popup.destroy)
        B1.pack()
        popup.mainloop()


if __name__ == "__main__":
    app = App()
    app.mainloop()