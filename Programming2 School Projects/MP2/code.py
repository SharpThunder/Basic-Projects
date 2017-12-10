# -*- coding: cp1254 -*-
from Tkinter import *
root = Tk()
import ttk
import tkFileDialog
import tkMessageBox
import random
from collections import OrderedDict





class UserInterface(Frame):


    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.parent = parent
        self.initUI()


    def initUI(self):
        #All the widgets in the interface

        self.master.title('Guess My Grade')
        self.frame = Frame(root, relief=FLAT)
        self.frame.grid(row=0, column=0)

        for r in range(6):
            self.frame.rowconfigure(r, weight=1)
        for c in range(5):
            self.frame.columnconfigure(c, weight=1)

        self.main_label = Label(self.frame, text="Book Recommendation System", font=("Helvetica 11 bold",15))
        self.main_label.grid(row= 0,column=0,rowspan=1,columnspan=5, sticky=EW)

        self.first_sep = ttk.Separator(self.frame, orient="horizontal")
        self.first_sep.grid(row=1, column=0,columnspan=5 ,sticky=EW)

        self.first_button = Button(self.frame, text="List Users With Less Data", font="Helvetica 9 bold",)
        self.first_button.grid(row=2, column=0,columnspan=1,rowspan=1,sticky=EW,padx=5 ,pady=5)

        self.first_box = Listbox(self.frame, font="Helvetica 9 bold")
        self.first_box.grid(row= 2, column=1, sticky=NSEW ,padx=5 ,pady=5)

        self.first_combobox = ttk.Combobox(self.frame,font='Helvetica 10')
        self.first_combobox.grid(row=3,column=3, sticky=NSEW ,padx=5 ,pady=5)



def main():
    UserInterface(root).mainloop()
if __name__ == '__main__':
    main()
