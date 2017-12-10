# -*- coding: cp1254 -*-
from Tkinter import *
import ttk
import tkFileDialog
import tkMessageBox
from collections import OrderedDict



class UserInterface(Frame):


    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.parent = parent
        self.parsing_csv()
        self.initUI()
        self.a=[]


    def initUI(self):
        #All the widgets in the interface


        self.main_label = Label(self.parent, text="Book Recommendation System", font="Helvetica 17 bold", bg = "blue", fg= "white")
        self.main_label.place(y=0,x=200)

        self.line1_label = Label(self.parent, bg="red")
        self.line1_label.place(y=35,  width = 700, height = 1)

        self.lessdata_button = Button(self.parent, text="List Users With Less Data", font="Helvetica 8 bold", command=self.student_less_data)
        self.lessdata_button.place(x=5, y=45)

        self.userless_list = Listbox(self.parent, font="Helvetica 11")
        self.userless_list.place(y=45, x=170, height= 100, width= 200)
        self.userless_list.bind('<<ListboxSelect>>',self.getname)
        self.userless_scroller = Scrollbar(self.parent)
        self.userless_scroller.place(x=370, y=45, height=100)
        self.userless_scroller.config(command=self.userless_list.yview)
        self.userless_list.config(yscrollcommand=self.userless_scroller.set)


        self.selectbook_combo = ttk.Combobox(self.parent, font="Helvetica 9", values = self.booknames, state='readonly')
        self.selectbook_combo.place(x=400, y=70, width=160)
        self.selectbook_combo.set("Select Book")

        self.selectrate_combo = ttk.Combobox(self.parent, font="Helvetica 9",state='readonly')
        self.selectrate_combo.place(x=570, y=70, width=120)
        self.selectrate_combo["values"] = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10")
        self.selectrate_combo.set("Select Rating")

        self.add_button = Button(self.parent, text="Add", font="Helvetica 10 bold", command=self.add)
        self.add_button.place(x=470, y=110)

        self.line2_label = Label(self.parent, bg="red")
        self.line2_label.place(y=155, width=700, height=1)

        self.settings_label = Label(self.parent, text="Settings", font="Helvetica 14 bold", bg="blue", fg="yellow")
        self.settings_label.place(y=160, x=290)

        self.settings_label = Label(self.parent, text="Total Number of Recommendations", font="Helvetica 12 bold", bg="blue", fg="yellow")
        self.settings_label.place(y=205, x=10)

        self.recnum_entry = Entry(self.parent, font="Helvetica 11 bold", width=2)
        self.recnum_entry.place(x=290, y=205, width=25)

        self.recmodel_combo = ttk.Combobox(self.parent, font="Helvetica 9",state='readonly')
        self.recmodel_combo.place(x=330, y=205, width=160)
        self.recmodel_combo["values"] = ("User-based", "Item-based")
        self.recmodel_combo.set("Recommendation Model")

        self.simmet_combo = ttk.Combobox(self.parent, font="Helvetica 9",state='readonly')
        self.simmet_combo.place(x=510, y=205, width=135)
        self.simmet_combo["values"] = ("Euclidian", "Pearson", "Jaccard")
        self.simmet_combo.set("Similarity Metric")


        self.line3_label = Label(self.parent, bg="red")
        self.line3_label.place(y=240, width=700, height=1)

        self.settings_label = Label(self.parent, text="Select a User", font="Helvetica 14 bold", bg="blue", fg="yellow")
        self.settings_label.place(y=245, x=270)

        self.user_list = Listbox(self.parent, font="Helvetica 11")
        self.user_list.place(y=280, x=235, height= 100, width= 200)
        self.user_scroller = Scrollbar(self.parent)
        self.user_scroller.place(x=435, y=280, height=100)
        self.user_scroller.config(command=self.user_list.yview)
        self.user_list.config(yscrollcommand=self.user_scroller.set)

        self.listsimuser_button = Button(self.parent, text="List Similar Users", font="Helvetica 8 bold")
        self.listsimuser_button.place(x=80, y=385)

        self.getrec_button = Button(self.parent, text="Get Recommendations", font="Helvetica 8 bold")
        self.getrec_button.place(x=440, y=385)

        self.similarusers_list = Listbox(self.parent, font="Helvetica 11")
        self.similarusers_list.place(y=420, x=10, height=140, width=270)
        self.simscroller = Scrollbar(self.parent)
        self.simscroller.place(x=280, y=420, height=140)
        self.simscroller.config(command=self.similarusers_list.yview)
        self.similarusers_list.config(yscrollcommand=self.simscroller.set)

        self.getrec_list = Listbox(self.parent, font="Helvetica 11")
        self.getrec_list.place(y=420, x=380, height=140, width=270)
        self.getrec_scroller = Scrollbar(self.parent)
        self.getrec_scroller.place(x=650, y=420, height=140)
        self.getrec_scroller.config(command=self.getrec_list.yview)
        self.getrec_list.config(yscrollcommand=self.getrec_scroller.set)

    def parsing_csv(self):
        self.list = []
        self.openfile = open("Book-Ratings.csv", "r")
        for i in self.openfile:
            self.list.append(i[0:-1])
        self.list.pop(0)     #Removing tags from list
        self.list.sort()
        self.firstdict = OrderedDict()
        for i in self.list:
            a = i.split(";")
            key = (a[0])
            value = [a[1] + "/" + a[2] + "/" + a[3]]
            self.firstdict.setdefault(key, [])
            self.firstdict[key] += [value]
        print self.firstdict
        self.bookid=[]
        for i in self.list:
            b=i.split(";")
            if [b[3],b[1]] not in self.bookid:
                self.bookid.append([b[3],b[1]])
        self.booknames=[]

        for i in self.list:
            b=i.split(";")
            if b[3] not in self.booknames:
                self.booknames.append(b[3])
        print self.bookid

        self.booknames.sort()
        print self.booknames
        print self.firstdict

    def student_less_data(self):
        self.lesslist=[]
        for x , y in self.firstdict.items():
            if len(y)<2:
                self.lesslist.append(x)
        for i in self.lesslist:
            self.userless_list.insert(END,str(i))

    def getname(self,evt):
        self.w = evt.widget
        self.index = int(self.w.curselection()[0])
        self.value = self.w.get(self.index)



    def add(self):

        if self.value == "":
            tkMessageBox.showinfo(message=" Select a Student", title="ERROR")
        elif self.selectbook_combo.get() == "Select Book":
            tkMessageBox.showinfo(message=" Select a Book", title= "ERROR")
        elif self.selectrate_combo.get() == "Select Rating":
            tkMessageBox.showinfo(message=" Select a Rating", title="ERROR")

        else:
            for i,j in self.firstdict.items():
                if i == self.value:
                    for x in j:
                        for r in x:
                            r += ''
                            print r
                            t=r.split('/')
                            print t
                            if t[2] == self.selectbook_combo.get() :
                                t[1]=self.selectrate_combo.get()
                                self.firstdict[i]= [[t[0]+'/'+self.selectrate_combo.get()+'/'+t[2]]]
                                print self.firstdict
                            else:
                                print 'zaaaaaaaaa'
                                t[1] = self.selectrate_combo.get()
                                self.firstdict[i]= [[t[0]+'/'+t[1]+'/'+t[2]],[str(1)+'/'+self.selectrate_combo.get()+'/'+self.selectbook_combo.get()]]
                                print self.firstdict



























def main():
    root = Tk()
    root.geometry("700x600")
    app = UserInterface(root)
    root.title("Book Recommendation System")
    root.configure(background='blue')
    root.mainloop()


main()