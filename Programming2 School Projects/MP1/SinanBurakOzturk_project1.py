# -*- coding: cp1254 -*-
from Tkinter import *
import tkFileDialog
import tkMessageBox
import random
from collections import OrderedDict



class UserInterface(Frame):


    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.parent = parent
        self.initUI()
        self.filename = ""
        self.savefile = ""


    def initUI(self):
        #All the widgets in the interface


        self.input_label = Label(self.parent, text="Input File Path", font="Helvetica 11 bold")
        self.input_label.place(y=25, x=5)

        self.output_label = Label(self.parent, text="Output File Path", font="Helvetica 11 bold")
        self.output_label.place(y=55, x=5)

        self.input_listbox = Listbox(self.parent, font="Helvetica 11 bold")
        self.input_listbox.place(x=130, y=25, height=20, width=400)

        self.output_listbox = Listbox(self.parent, font="Helvetica 11 bold")
        self.output_listbox.place(x=130, y=55, height=20, width=400)

        self.browse_button = Button(self.parent, text="Browse", font="Helvetica 9 bold", command=self.browseFile)
        self.browse_button.place(x=540, y=25)

        self.save_button = Button(self.parent, text="Save", font="Helvetica 9 bold",command=self.saveFile)
        self.save_button.place(x=540, y=55)

        self.markov_button = Button(self.parent, text="Markov", font="Helvetica 9 bold", command=self.Markov)
        self.markov_button.place(x=280, y=85)

        self.hintlabel=Label(self.parent, text="Firstly click Browse\nSecondly click Save\nThirdly click Markov", font="Helvetica 8 bold")
        self.hintlabel.place(y=80, x=5)


    def browseFile(self):
        #Selecting the input file
        self.input_listbox.delete(0,END)
        self.filename=tkFileDialog.askopenfilename()

        #Location of the input file
        self.input_listbox.insert(END,self.filename)


    def Markov(self):
        self.openfile = open(self.filename, "r")#Opening the input file
        if self.filename == "" and self.savefile== "":
            #If input file is not selected and the output file is not created, this code will run for Error
            tkMessageBox.showinfo(message="This an error message (find the error yourself)", title="ERROR!!!")
        else:
            #Reading the input and making a list

            self.reading_the_text = self.openfile.read()
            self.list=self.reading_the_text.split()


            #Creating dict
            self.firstdict = OrderedDict()
            for i in range(len(self.list)-2):
                key = (self.list[i] , self.list[i+1])
                value=(self.list[i+2])
                self.firstdict.setdefault(key,[])
                self.firstdict[key]+=[value]

            #Creating first two words of the output
            self.first_two_words=[]
            for x in self.firstdict.keys():
                    self.first_two_words.append(x)
            self.selectedwords =self.first_two_words[0]

            #
            self.outputlist=[]
            self.first, self.second = self.selectedwords
            self.outputlist.append(self.first)
            self.outputlist.append(self.second)

            self.loopcount=len(self.list)-2 #Defining the loop counts

            if self.loopcount>= 500: #Defining words limit and loop count, if the text has more than 500 words.
                for i in range(498):
                    try:
                        #Selecting other words for output
                        self.third = random.choice(self.firstdict[self.selectedwords])
                        self.outputlist.append(self.third)
                        self.selectedwords = (self.second,self.third)
                        self.first,self.second = self.selectedwords
                    except KeyError:
                        break



                self.final_output = " ".join(self.outputlist)#Combining the words for final output text
            else: # Defining loop count, if the text has less than 500 words.
                for i in range(self.loopcount):
                    try:
                        #Selecting other words for output
                        self.third = random.choice(self.firstdict[self.selectedwords])
                        self.outputlist.append(self.third)
                        self.selectedwords = (self.second, self.third)
                        self.first, self.second = self.selectedwords
                    except KeyError:
                        break

                self.final_output = " ".join(self.outputlist)#Combining the words for final output text


        print len(self.final_output.split()) #Word count of the output



        # Writing the final output text to the output file
        self.writing = open(self.savefile, "w")
        self.writing.write(self.final_output)
        self.writing.close()
        #Done message
        self.outputfilename=self.savefile.split("/")[-1]
        tkMessageBox.showinfo(message=" Markov Chain is finished for " + str(self.outputfilename), title="DONE")
        self.openfile.close()


    def saveFile(self):
        self.output_listbox.delete(0, END)
        self.savefile = tkFileDialog.asksaveasfilename(defaultextension='.txt') # Creating a text file to write final output text
        self.output_listbox.insert(END, self.savefile)#Location of the output file

def main():
    root = Tk()
    root.geometry("610x150")
    app = UserInterface(root)
    root.title("Markov Chain Generator")
    root.mainloop()


main()