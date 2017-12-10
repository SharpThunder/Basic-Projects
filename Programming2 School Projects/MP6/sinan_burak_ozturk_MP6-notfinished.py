from Tkinter import *
import tkMessageBox
from collections import OrderedDict
import os
import time
import shelve

class UserInterface(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.parent = parent
        self.initUI()
        self.filter()
        self.filter_category = []

    def initUI(self):
        # All the widgets in the interface
        self.main_label = Label(self.parent,text="File Searcher", font = "Helvetica 18 bold" , bg="black", fg="green")
        self.main_label.place( width = 850)

        self.line = Label(self.parent, bg="red")
        self.line.place( y=40, width = 860, height = 4)

        self.folder_label = Label(self.parent, text="Folder to start searching", font="Helvetica 14 bold", bg="black", fg="red")
        self.folder_label.place(x= 30, y = 60)

        self.folder_entry = Entry(self.parent, fg="green",font="Helvetica 10 bold", bg = "black")
        self.folder_entry.place(x=300, y=60, height=25, width=350)

        self.depth_label = Label(self.parent, text="Depth", font="Helvetica 14 bold", bg="black", fg="red")
        self.depth_label.place(x=40, y=95)

        self.depth_entry = Entry(self.parent, font="Helvetica 9 bold", width=3, bg="red", fg="green")
        self.depth_entry.place(x=130, y=100)

        self.builtindex_button=Button(self.parent, text = "Build Index", font = "Helvetica 11 bold" , bg="black", fg="green", command = self.built_index)
        self.builtindex_button.place(x = 300, y = 95)

        self.line2 = Label(self.parent, bg="red")
        self.line2.place(y=130, width=860, height=2)

        self.keywords_entry = Entry(self.parent, fg="green", bg = "black", font="Helvetica 10 bold")
        self.keywords_entry.place(x=100, y=150, height=25, width=350)

        self.ranking_label = Label(self.parent, text="Ranking Criteria", font="Helvetica 12 bold", bg="black", fg="red")
        self.ranking_label.place(x=100, y=190)

        self.var = IntVar()
        self.wordistance_checkbutton = Checkbutton(self.parent, text="Word-Distance", font="Helvetica 9 bold", bg="black", fg="green", variable=self.var)
        self.wordistance_checkbutton.place(x=100, y=220)

        self.var1 = IntVar()
        self.accesstime_checkbutton = Checkbutton(self.parent, text="Access-Time", font="Helvetica 9 bold", bg="black", fg="green", variable=self.var1)
        self.accesstime_checkbutton.place(x=100, y=250)

        self.weights_label = Label(self.parent, text="Weights", font="Helvetica 12 bold", bg="black", fg="red")
        self.weights_label.place(x=300, y=190)

        self.wordistance_entry = Entry(self.parent, font="Helvetica 10 bold", width=3, bg="red", fg="green")
        self.wordistance_entry.place(x=305, y=220)

        self.accestime_entry = Entry(self.parent, font="Helvetica 10 bold", width=3, bg="red", fg="green")
        self.accestime_entry.place(x=305, y=250)

        self.filter_label = Label(self.parent, text="Filter", font="Helvetica 12 bold", bg="black", fg="red")
        self.filter_label.place(x=450, y=190)

        self.filter_listbox = Listbox(self.parent, bg="black", fg="green", selectmode = "multiple")
        self.filter_listbox.place(x=450, y=220, height=60, width=150)
        self.filter_listbox.bind('<<ListboxSelect>>', self.getfilter)

        self.search_button = Button(self.parent, text="Search", font="Helvetica 11 bold", bg="black", fg="green", command = self.search)
        self.search_button.place(x=650, y=235)

        self.results_textbox=Listbox(self.parent, bg = "black", fg = "green", exportselection = 0, )
        self.results_textbox.place(x=100, y = 320, height=250 , width=600)
        self.results_textbox_scrollery = Scrollbar(self.parent)
        self.results_textbox_scrollery.place(x=700, y=320, height=250)
        self.results_textbox_scrollery.config(command=self.results_textbox.yview)
        self.results_textbox.config(yscrollcommand=self.results_textbox_scrollery.set)

        self.page_label = Label(self.parent, text="Page:", font="Helvetica 12 bold", bg="black", fg="red")
        self.page_label.place(x=520, y=590)

        self.prev_button = Button(self.parent, text="Prev", font="Helvetica 10 bold", bg="black", fg="green", command = self.prev_button)
        self.prev_button.place(x=580, y=590)

        self.pagenum_list = Listbox(self.parent, font="Helvetica 11 bold", width=3, height= 1, bg="red", fg="green")
        self.pagenum_list.place(x=635, y=590)

        self.next_button = Button(self.parent, text="Next", font="Helvetica 10 bold", bg="black", fg="green", command = self.next_button)
        self.next_button.place(x=680, y=590)

    def filter(self):
        self.filter_listbox.insert(END, "Plain Text")
        self.filter_listbox.insert(END, "Program Code")


    def built_index(self):
        current_time=time.time()
        self.data = OrderedDict()
        self.database=OrderedDict()
        folder=self.folder_entry.get()
        depth = len(folder.split("\\"))
        if folder == "":
            tkMessageBox.showinfo("ERROR", "give a starting folder")
        elif folder != "":
            for root, dirs, files in os.walk(folder):
                if files != [] :
                    for i in files:
                        sec = time.time()
                        search_time=str(sec-current_time)
                        a=str(root) + "\\" + str(i)
                        self.data.setdefault(a, [])
                        self.data[a]=search_time[:4], a.split("\\")

            for i,j in self.data.items():
                if self.depth_entry.get()!= "":
                    if len(j[1]) <= int(self.depth_entry.get()) + depth:
                        self.database.setdefault(i, [])
                        self.database[i] = j[0]
                else:
                    self.database.setdefault(i, [])
                    self.database[i] = j[0]
            d = shelve.open("database.db")
            d["data"] = self.database
            d.close()

        if self.data == OrderedDict():
            tkMessageBox.showinfo("ERROR", "The starting folder is not exist")

    def search(self):
        if self.keywords_entry.get() == "":
            tkMessageBox.showinfo("ERROR", "Provide at least one keyword")
        elif self.var.get() == 0 and self.var1.get() == 0:
            tkMessageBox.showinfo("ERROR", "Choose at least one ranking measure")
        elif self.var.get() == 1 and self.wordistance_entry.get() == "":
            tkMessageBox.showinfo("ERROR", "Provide a weights for Word-Distance")
        elif self.var1.get()== 1 and self.accestime_entry.get() == "":
            tkMessageBox.showinfo("ERROR", "Provide a weights for Access-Time")
        elif self.filter_category == []:
            tkMessageBox.showinfo("ERROR", "Choose at least one file category")
        else:
            keywords =self.keywords_entry.get().split(" ")
            for i,j in self.database.items():
                self.results_textbox.insert(END, i + "       " +  j)





    def prev_button(self):
        print "prev"




    def next_button(self):
        print "next"







    def getfilter(self,evt):
        self.filter_category=[]
        self.w = evt.widget
        self.index = self.w.curselection()
        for i in self.index:
            self.filter_category.append(self.w.get(i))

def main():
    root = Tk()
    root.geometry("800x630")
    app = UserInterface(root)
    root.title("Project 6")
    root.configure(background='black')
    root.mainloop()

main()