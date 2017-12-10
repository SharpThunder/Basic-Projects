from Tkinter import *
import tkFileDialog
import string
import urllib2
import ttk
import tkMessageBox
from BeautifulSoup import BeautifulSoup

class UserInterface(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.parent = parent
        self.initUI()
        self.letters()
        self.details()
        self.value = ""
        self.value1= ""
        self.data = []

    def initUI(self):
        # All the widgets in the interface
        self.main_label = Label(self.parent,text="Stock Exchange Presentation Tool", font = "Helvetica 18 bold" , bg="black", fg="green")
        self.main_label.place( width = 800)

        self.line = Label(self.parent, bg="red")
        self.line.place( y=40, width = 800, height = 4)

        self.getstock_button = Button(self.parent, text = "Get Stock Data", font = "Helvetica 11 bold", bg = "black", fg = "green", command = self.get_data)
        self.getstock_button.place(x = 330, y = 53)

        self.line2 = Label(self.parent, bg="red")
        self.line2.place( y=95, width = 800, height = 2)

        self.select_label = Label(self.parent, text = "Select Initial Letters", font = "Helvetica 13 bold", bg = "black", fg = "green")
        self.select_label.place(x = 20, y = 110)

        self.select_letter = Listbox(self.parent, height=6, width=10, font="Helvetica 11 bold", bg="black", fg="green")
        self.select_letter.place(x=230, y=110)
        self.select_letter.bind('<<ListboxSelect>>', self.get_letter)
        self.letter_scroller = Scrollbar(self.parent)
        self.letter_scroller.place(x=308, y=110, height=119)
        self.letter_scroller.config(command=self.select_letter.yview)
        self.select_letter.config(yscrollcommand=self.letter_scroller.set)

        self.lower_label = Label(self.parent, text = "Lower Price Limit", font = "Helvetica 13 bold", bg = "black", fg = "green")
        self.lower_label.place(x = 400, y = 110)

        self.lower_entry = Entry(self.parent, font="Helvetica 11 bold", width=2, bg="red", fg="green")
        self.lower_entry.place(x=580, y=110, width = 30)

        self.upper_label = Label(self.parent, text="Upper Price Limit", font="Helvetica 13 bold", bg="black", fg="green")
        self.upper_label.place(x=400, y=160)

        self.upper_entry = Entry(self.parent, font="Helvetica 11 bold", width=2, bg="red", fg="green")
        self.upper_entry.place(x=580, y=160, width=30)

        self.displaystock_button = Button(self.parent, text = "Display Stocks", font = "Helvetica 11 bold", bg = "black", fg = "green", command = self.dis_stocks)
        self.displaystock_button.place(x = 90, y = 250)

        self.stocks_textbox=Listbox(self.parent, bg = "black", fg = "green")
        self.stocks_textbox.place(x=20, y = 300, height=350, width=280)
        self.stocks_textbox.bind('<<ListboxSelect>>', self.get_detail)
        self.stocks_scroller = Scrollbar(self.parent)
        self.stocks_scroller.place(x=282, y=300, height=350)
        self.stocks_scroller.config(command=self.stocks_textbox.yview)
        self.stocks_textbox.config(yscrollcommand=self.stocks_scroller.set)

        self.detail_button = Button(self.parent, text="Details", font="Helvetica 11 bold", bg="black", fg="green",command = self.detail)
        self.detail_button.place(x=320, y=300)

        self.last_textbox = Text(self.parent, font="Helvetica 9 bold", bg="black", fg="green")
        self.last_textbox.place(x=320, y=340, height=70, width=58)

        self.yesterday_textbox = Text(self.parent, font="Helvetica 9 bold", bg="black", fg="green")
        self.yesterday_textbox.place(x=378, y=340, height=70, width=62)

        self.percentage_textbox = Text(self.parent, font="Helvetica 9 bold", bg="black", fg="green")
        self.percentage_textbox.place(x=440, y=340, height=70, width=58)

        self.hight_textbox = Text(self.parent, font="Helvetica 9 bold", bg="black", fg="green")
        self.hight_textbox.place(x=498, y=340, height=70, width=58)

        self.low_textbox = Text(self.parent, font="Helvetica 9 bold", bg="black", fg="green")
        self.low_textbox.place(x=556, y=340, height=70, width=58)

        self.avg_textbox = Text(self.parent, font="Helvetica 9 bold", bg="black", fg="green")
        self.avg_textbox.place(x=614, y=340, height=70, width=58)

        self.LOT_textbox = Text(self.parent, font="Helvetica 9 bold", bg="black", fg="green")
        self.LOT_textbox.place(x=672, y=340, height=70, width=60)

        self.TL_textbox = Text(self.parent, font="Helvetica 9 bold", bg="black", fg="green")
        self.TL_textbox.place(x=732, y=340, height=70, width=60)




    def letters(self): # inserting letters to select letter listbox
        letters = string.ascii_uppercase
        self.select_letter.insert(END, "All")
        for i in letters:
            self.select_letter.insert(END,i + "\n")

    def details(self): # inserting the details names of the companies
        self.last_textbox.insert(END, "  Last\n")
        self.yesterday_textbox.insert(END, "Yesterday\n")
        self.percentage_textbox.insert(END, "  %\n")
        self.hight_textbox.insert(END, "  Hight\n")
        self.low_textbox.insert(END, "  Low\n")
        self.avg_textbox.insert(END, "  Avg\n")
        self.LOT_textbox.insert(END, " Vol(LOT)\n")
        self.TL_textbox.insert(END, "  Vol(TL)\n")


    def get_letter(self,evt): #getting selected letter
        self.w = evt.widget
        self.index = str(self.w.curselection()[0])
        self.value = self.w.get(self.index)
        self.value = self.value[:-1]

    def get_detail(self,evt): #getting selected company name
        self.w = evt.widget
        self.index = str(self.w.curselection()[0])
        self.value1 = self.w.get(self.index)
        self.value1 = self.value1[:-1]

    def get_data(self):
        # opening and reading the website datas
        url= "http://www.bigpara.com/borsa/hisse-fiyatlari/"
        response = urllib2.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html)
        htmlContent = soup.find("div", attrs={"class": "tBody"}).findAll('ul')
        for i in htmlContent: # taking the datas in first page
            company=""
            for c in i.findAll("li"):
                print c.text
                company+=str(c.text)+" |"
            self.data.append(company.split(" |")) # adding the datas of the first page to the list
        for i in range(2,9): # taking the datas in other pages
            url = "http://www.bigpara.com/borsa/hisse-fiyatlari/" + str(i)
            response = urllib2.urlopen(url)
            html = response.read()
            soup = BeautifulSoup(html)
            htmlContent = soup.find("div", attrs={"class": "tBody"}).findAll('ul')
            for i in htmlContent:
                company = ""
                for c in i.findAll("li"):
                    company += str(c.text) + " |"
                self.data.append(company.split(" |")) # adding the datas of the other pages to the list
        for i in self.data: #deletin the empty character of the list
            i.pop()
        for i in self.data: #changing the prices to compare it with lower and upper prices
            new_data = i[1].replace(",",".")
            i.pop(1)
            i.insert(1, new_data)

    def dis_stocks(self):
        self.stocks_textbox.delete(0, END)
        if self.value == "":
            tkMessageBox.showinfo("ERROR", "Select one on Select Initial Letter Textbox")
        elif self.data == []:
            tkMessageBox.showinfo("ERROR", "Click the Get Stock Data button")

        elif self.lower_entry.get() == "" and self.upper_entry.get() == "": # selecting the companies without upper and lower prices
            if self.value == "Al": #selecting all companies
                for i in self.data:
                    self.stocks_textbox.insert(END, i[0] + "\n")
            else: #selecting the companies that start with the selected letter
                for i in self.data:
                    if self.value == i[0][0]:
                        self.stocks_textbox.insert(END, i[0] + "\n")
        elif self.lower_entry.get() != "" and self.upper_entry.get() == "":# selecting the companies with lower prices without upper prices
            if self.value == "Al":#selecting the all companies
                for i in self.data:
                    if float(i[1])> float(self.lower_entry.get()):
                        self.stocks_textbox.insert(END, i[0] + "\n")
            else:# selecting the companies that start with the selected letter
                for i in self.data:
                    if self.value == i[0][0] and float(i[1])> float(self.lower_entry.get()):
                        self.stocks_textbox.insert(END, i[0] + "\n")
        elif self.lower_entry.get() == "" and self.upper_entry.get() != "":# selecting the companies with upper prices without lower prices
            if self.value == "Al":#selecting the all companies
                for i in self.data:
                    if float(i[1])< float(self.upper_entry.get()):
                        self.stocks_textbox.insert(END, i[0] + "\n")
            else:#selecting the companies that start with the selected letter
                for i in self.data:
                    if self.value == i[0][0] and float(i[1])< float(self.upper_entry.get()):
                        self.stocks_textbox.insert(END, i[0] + "\n")
        else:# selecting the companies with upper and lower prices
            if self.value == "Al":#selecting the all companies
                for i in self.data:
                    if float(i[1])< float(self.upper_entry.get()) and float(i[1])> float(self.lower_entry.get()):
                        self.stocks_textbox.insert(END, i[0] + "\n")
            else:#selecting the companies that start with the selected letter
                for i in self.data:
                    if self.value == i[0][0] and float(i[1])< float(self.upper_entry.get())and float(i[1])> float(self.lower_entry.get()):
                        self.stocks_textbox.insert(END, i[0] + "\n")

    def detail(self):
        #deleting the text boxes to second working of the program
        self.last_textbox.delete(1.0, END)
        self.yesterday_textbox.delete(1.0, END)
        self.percentage_textbox.delete(1.0, END)
        self.hight_textbox.delete(1.0, END)
        self.low_textbox.delete(1.0, END)
        self.avg_textbox.delete(1.0, END)
        self.LOT_textbox.delete(1.0, END)
        self.TL_textbox.delete(1.0, END)

        # inserting the details names of the companies
        self.last_textbox.insert(END, "  Last\n")
        self.yesterday_textbox.insert(END, "Yesterday\n")
        self.percentage_textbox.insert(END, "  %\n")
        self.hight_textbox.insert(END, "  Hight\n")
        self.low_textbox.insert(END, "  Low\n")
        self.avg_textbox.insert(END, "  Avg\n")
        self.LOT_textbox.insert(END, " Vol(LOT)\n")
        self.TL_textbox.insert(END, "  Vol(TL)\n")

        if self.value1 == "":
            tkMessageBox.showinfo("ERROR", "Select a company")
        else: # adding the details to the text boxes
            for i in self.data:
                if self.value1 == i[0]:
                    self.last_textbox.insert(END, i[1])
                    self.yesterday_textbox.insert(END, i[2])
                    self.percentage_textbox.insert(END, i[3])
                    self.hight_textbox.insert(END, i[4])
                    self.low_textbox.insert(END, i[5])
                    self.avg_textbox.insert(END, i[6])
                    self.LOT_textbox.insert(END, i[7])
                    self.TL_textbox.insert(END, i[8])








def main():
    root = Tk()
    root.geometry("800x670")
    app = UserInterface(root)
    root.title("File Editor")
    root.configure(background='black')
    root.mainloop()

main()