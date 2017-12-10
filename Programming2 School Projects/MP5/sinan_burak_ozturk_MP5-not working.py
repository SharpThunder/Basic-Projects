from Tkinter import *
import ttk
import csv
import tkMessageBox
from collections import OrderedDict
import random
from docclass import*


class UserInterface(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        # All the widgets in the interface
        self.main_label = Label(self.parent,text="AAAI Classifier", font = "Helvetica 18 bold" , bg="black", fg="green")
        self.main_label.place( width = 850)

        self.line = Label(self.parent, bg="red")
        self.line.place( y=40, width = 860, height = 4)

        self.load_button=Button(self.parent, text = "Load Dataset", font = "Helvetica 11 bold" , bg="black", fg="green", command = self.load_dataset)
        self.load_button.place(x = 130, y = 60)

        self.load_label = Label(self.parent, text="Waiting Dataset...", font="Helvetica 14 bold", bg="black", fg="red")
        self.load_label.place(width=250, x= 350, y = 60)

        self.line2 = Label(self.parent, bg="red")
        self.line2.place(y=100, width=860, height=2)

        self.chooseclas_label = Label(self.parent, text = "Choose Classifier", font = "Helvetica 14 bold", bg = "black", fg = "green")
        self.chooseclas_label.place(x = 70, y = 115)

        self.var = IntVar()
        self.naivebayes_radiobutton=Radiobutton(self.parent, text="Naive-Bayes", font= "Helvetica 9 bold", bg = "black", fg = "green", variable = self.var, value = 1)
        self.naivebayes_radiobutton.place(x=80,y=155)
        self.fisher_radiobutton=Radiobutton(self.parent, text="Fisher", font= "Helvetica 9 bold", bg = "black", fg = "green", variable = self.var, value = 2)
        self.fisher_radiobutton.place(x=80,y=185)

        self.num_entry = Entry(self.parent, font="Helvetica 11 bold", width=3, bg="red", fg="green")
        self.num_entry.place(x=265, y=150)

        self.setThresholds_label = Label(self.parent, text="Set Thresholds", font="Helvetica 14 bold", bg="black",fg="green")
        self.setThresholds_label.place(x=300, y=115)

        self.abbreviated_topic_combo = ttk.Combobox(self.parent, font="Helvetica 11 bold", background="red", state="readonly")
        self.abbreviated_topic_combo.place(x=310, y=150)

        self.set_button = Button(self.parent, text="Set", font="Helvetica 11 bold", bg="black", fg="green", command = self.set)
        self.set_button.place(x=520, y=160)

        self.set_listbox = Listbox(self.parent, bg="black", fg="green")
        self.set_listbox.place(x=580, y=150, height=90, width=150)
        self.set_listbox.bind('<<ListboxSelect>>', self.getname)

        self.remove_button = Button(self.parent, text="Remove\n Selected", font="Helvetica 11 bold", bg="black", fg="green", command = self.remove)
        self.remove_button.place(x=760, y=150)

        self.line3 = Label(self.parent, bg="red")
        self.line3.place( y=270, width = 860, height = 2)

        self.calaccuraty_button = Button(self.parent, text = "Calculate Accuracy", font = "Helvetica 11 bold", bg = "black", fg = "green", command = self.calculate_accuracy)
        self.calaccuraty_button.place(x = 170, y = 295)

        self.results_textbox=Text(self.parent, bg = "black", fg = "green", exportselection = 0, )
        self.results_textbox.place(x=15, y = 340, height=250 , width=800)
        self.results_textbox_scrollery = Scrollbar(self.parent)
        self.results_textbox_scrollery.place(x=815, y=340, height=250)
        self.results_textbox_scrollery.config(command=self.results_textbox.yview)
        self.results_textbox.config(yscrollcommand=self.results_textbox_scrollery.set)

    def getname(self,evt):
        self.w = evt.widget
        self.index = int(self.w.curselection()[0])
        self.value = self.w.get(self.index)

    def load_dataset(self):
        self.topiclist = []
        self.a = []
        self.b = []
        self.abbreviated = []
        self.data_set = open("MP5 Data Set.txt", "w+") #Creating the data set
        self.openfile = open("AAAI-14_Accepted_Papers_corrected.txt", "r") #Opening the AAAI-14 datas
        self.AAAIreader = csv.reader(self.openfile)  # reading the datas

        # Taking the abbreviated topics
        for i in self.AAAIreader:
            self.topiclist.append(i[4])
        for i in self.topiclist:
            self.a.append(i.split(" "))
        for i in self.a:
            for j in i:
                if ":" in j and j[0].isupper():
                    if j not in self.b:
                        self.b.append(j)
        for i in self.b:#deleting ":" symbol
            self.abbreviated.append(i[:-1])
        self.abbreviated.sort()
        self.abbreviated_topic_combo["value"] = self.abbreviated # adding the abbreviated topics to the combobox

        self.openfile.seek(0)
        self.addtopics = []
        self.dataset_dict = OrderedDict()

        for i in self.AAAIreader:#creating the dictionary for making the dataset file
            a=""
            for j in i[4]:
                if j != ":":
                    a += str(j)
                else:
                    break
            self.dataset_dict[i[0]]=a
        del self.dataset_dict["title"]

        for i, j in self.dataset_dict.items():#writing the data to dataset
            self.data_set.write(i + "|" + j + "\n")
        self.data_set.close()

        self.load_label = Label(self.parent, text="Dataset Loaded", font="Helvetica 14 bold", bg="black", fg="green")
        self.load_label.place(width=250, x=350, y=60)

    def set(self):
        if self.num_entry.get() == "":
            tkMessageBox.showinfo(message=" Enter a number to the entry", title="ERROR")
        elif self.var.get() == 0:
            tkMessageBox.showinfo(message="Select a classifier method", title="ERROR")
        elif self.abbreviated_topic_combo.get() == "":
            tkMessageBox.showinfo(message= "Select a topic in the combobox", title="ERROR")
        else:
            self.set_listbox.insert(END,str(self.abbreviated_topic_combo.get()) + "-->" + str(self.num_entry.get()))

    def remove(self): #removing the selected items from the listbox
        i = self.set_listbox.get(0,END).index(self.value)
        self.set_listbox.delete(i)

    def randomsample(self):
        # selecting random data for training
        dataset = open("MP5 Data Set.txt", "r+")
        self.list = []
        for i in dataset:
            b =i.split('|')
            a = (b[0], b[1][:-1])
            self.list.append(a)
        dataset.close()
        self.randomlist = random.sample(self.list, 300)
        for i in self.randomlist: # remove the selected random items from the all data list
            self.list.remove(i)


    def training(self,selection): #training part
        for i, j in self.randomlist:
            selection.train(i, j)
    def test(self,selection): #test part
        self.testdict1 = {}
        self.testdict2 = {}
        z = 0
        for i, j in self.list:
            cat = selection.classify(i)
            if j not in self.testdict1:
                self.testdict1[j]=1
            else:
                self.testdict1[j] += 1
            if j == cat:
                z +=1
                self.testdict2[j]= z
            else: z+=0

    def accuracy(self,selection): #accuracy part
        self.randomsample()
        self.training(selection)
        self.test(selection)
        accuracydict= {}
        for j in self.testdict1:
            if j in self.testdict2:
                ac = self.testdict2[j]/self.testdict1[j] * 100
                accuracydict[j]= ac
            else:
                ac = 0/self.testdict1[j] * 100
                accuracydict[j] = ac

        return accuracydict

    def average(self,selection): #getting avarage
        self.averages_dict = {}
        for i in range(4):
            accurate = self.accuracy(selection)
            for j in accurate:
                if j not in self.averages_dict:
                    self.averages_dict[j] = accurate[j]/ 4
                else:
                    self.averages_dict[j] += accurate[j] / 4



    def calculate_accuracy(self):
        self.results_textbox.delete(1.0, END)
        if self.set_listbox.get(0,END) == ():
            tkMessageBox.showinfo(message=" There is no data in the listbox", title="ERROR")
        elif self.var.get() == 1: #Naive-bayes classifier
            cl = naivebayes(getwords)
            for i in self.set_listbox.get(0,END):
                b=i.split("-->")
                cl.setthreshold(b[0],float(b[1]))
            self.average(cl)
            self.results_textbox.insert(END,"Topics" + "        " + "Classifier Accuracy \n_____        ____________\n")
            for j in self.averages_dict:
                self.results_textbox.insert(END,j+'     '+str(self.averages_dict[j]) + '\n')

        elif self.var.get() == 2:#Fister Classifier
            cl1 = fisherclassifier(getwords)
            for i in self.set_listbox.get(0,END):
                b=i.split("-->")
                cl1.setminimum(b[0],b[1])
            self.average(cl1)

            self.results_textbox.insert(END, "Topics" + "        " + "Classifier Accuracy \n_____        ____________\n")
            for j in self.averages_dict:
                self.results_textbox.insert(END, j + '        ' + str(self.averages_dict[j]) + '\n')

        self.load_label = Label(self.parent, text="Accuracies Calculated", font="Helvetica 14 bold", bg="black", fg="green")
        self.load_label.place(width=350, x=300, y=60)




def main():
    root = Tk()
    root.geometry("860x650")
    app = UserInterface(root)
    root.title("Project 3")
    root.configure(background='black')
    root.mainloop()

main()