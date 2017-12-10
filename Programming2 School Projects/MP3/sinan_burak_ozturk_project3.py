from Tkinter import *
import ttk
import csv
import tkMessageBox
from clusters import*

class UserInterface(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.parent = parent
        self.initUI()
        self.cluster_data()


    def initUI(self):

        self.main_label = Label(self.parent,text="Author Clustering", font = "Helvetica 18 bold" , bg="black", fg="green")
        self.main_label.place( width = 850)

        self.line = Label(self.parent, bg="red")
        self.line.place( y=40, width = 850, height = 4)

        self.select_label = Label(self.parent, text = "Select Clustering Criteria", font = "Helvetica 14 bold", bg = "black", fg = "green")
        self.select_label.place(x = 70, y = 55)

        self.cm_label = Label(self.parent, text = "Clustering Method", font = "Helvetica 14 bold", bg = "black", fg = "green")
        self.cm_label.place(x = 500, y = 55)

        self.criteria_combo = ttk.Combobox(self.parent, font = "Helvetica 11 bold", background = "red", state = "readonly")
        self.criteria_combo.place(x = 90, y = 95)
        self.criteria_combo["values"] = ("Groups", "Keywords", "Topics", "Abstract")

        self.var1 = IntVar()
        self.hierarchical_checkbutton=Checkbutton(self.parent, text="Hierarchical", font= "Helvetica 9 bold", bg = "black", fg = "green", variable = self.var1)
        self.hierarchical_checkbutton.place(x=510,y=95)

        self.var = IntVar()
        self.kmean_checkbutton=Checkbutton(self.parent, text="K-means", font= "Helvetica 9 bold", bg = "black", fg = "green", variable = self.var)
        self.kmean_checkbutton.place(x=510,y=125)


        self.kmean_label = Label(self.parent, text = "K:", font = "Helvetica 9 bold", bg = "black", fg = "green")
        self.kmean_label.place(x = 625, y = 125)

        self.recom_entry = Entry(self.parent, font = "Helvetica 11 bold", width = 2, bg = "red", fg = "green")
        self.recom_entry.place(x = 650, y = 125)

        self.line2 = Label(self.parent, bg="red")
        self.line2.place( y=235, width = 850, height = 2)

        self.viewcluster_button = Button(self.parent, text = "View Cluster", font = "Helvetica 11 bold", bg = "black", fg = "green",command= self.view_cluster)
        self.viewcluster_button.place(x = 200, y = 245)

        self.clear_button = Button(self.parent, text="Clear", font="Helvetica 11 bold", bg="black", fg="green", command=self.clear)
        self.clear_button.place(x=500, y=245)

        self.cluster_textbox=Text(self.parent, bg = "black", fg = "green")
        self.cluster_textbox.place(x=15, y = 285, height=355 , width=800)
        self.cluster_scroller = Scrollbar(self.parent)
        self.cluster_scroller.place(x=815, y=285, height=355)
        self.cluster_scroller.config(command=self.cluster_textbox.yview)
        self.cluster_textbox.config(yscrollcommand=self.cluster_scroller.set)


    def cluster_data(self):
        self.openfile = open("AAAI-14_Accepted_Papers.csv", "r")  # opening and read the data
        self.reader=csv.reader(self.openfile)
        self.a=[]
        self.b = []
        self.author = []
        self.authors = []
        self.groups_dict = {}
        self.keywords_dict = {}
        self.topics_dict = {}
        self.abstract_dict = {}

        for r in self.reader:
            self.a.append(r[1])
        self.openfile.seek(0)
        for i in self.a:
            if " and" not in i:
                self.author.append(i)

            elif " and" in i:
                b = i.split(" and")
                if "," in b[0]:
                    c = b[0].split(",")
                    for d in c:
                        self.author.append(d)
                else:
                    for y in b:
                        self.author.append(y)
        self.author.pop(0)
        for i in self.author:
            if i[0] == " ":
                self.authors.append(i[1:])
            else:
                self.authors.append(i)



    def clear(self):
        self.cluster_textbox.delete(1.0,END)

    def matrices(self,n):
        if n == "Groups":
            for i in self.authors: #creating groups dicts
                key = i
                self.groups_dict.setdefault(key, [])
                self.openfile.seek(0)
                for j in self.reader:
                    if i in j[1]:
                        self.groups_dict[key]=j[2].split("\n")

            self.groupsList = []
            self.groupsData = file('groupsData.txt', 'w')
            self.groupsData.write('Author')
            for x,y in self.groups_dict.items():
                for c in y:
                    if c not in self.groupsList:
                        self.groupsList.append(c)
                        self.groupsData.write('\t%s' % c)
            self.groupsData.write('\n')
            for key, value in self.groups_dict.items():

                self.groupsData.write(key)
                for a in self.groupsList:
                    if a in value :
                        self.groupsData.write('\t1')
                    else:
                        self.groupsData.write('\t0')
                self.groupsData.write('\n')

        elif n == "Keywords":
            for i in self.authors: #creating groups dicts
                key = i
                self.keywords_dict.setdefault(key, [])
                self.openfile.seek(0)
                for j in self.reader:
                    if i in j[1]:
                        self.keywords_dict[key]=j[3].split("\n")

            self.keywordsList = []
            self.keywordsData = file('keywordsData.txt', 'w')
            self.keywordsData.write('Author')
            for x, y in self.keywords_dict.items():
                for c in y:
                    if c not in self.keywordsList:
                        self.keywordsList.append(c)
                        self.keywordsData.write('\t%s' % c)

            self.keywordsData.write('\n')
            for key, value in self.keywords_dict.items():
                self.keywordsData.write(key)
                for a in self.keywordsList:
                    if a in value:
                        self.keywordsData.write('\t1')
                    else:
                        self.keywordsData.write('\t0')
                self.keywordsData.write('\n')

        elif n == "Topics":
            for i in self.authors: #creating groups dicts
                key = i
                self.topics_dict.setdefault(key, [])
                self.openfile.seek(0)
                for j in self.reader:
                    if i in j[1]:
                        self.topics_dict[key]=j[4].split("\n")

            self.topicsList = []
            self.topicsData = file('topicsData.txt', 'w')
            self.topicsData.write('Author')
            for x, y in self.topics_dict.items():
                for c in y:
                    if c not in self.topicsList:
                        self.topicsList.append(c)
                        self.topicsData.write('\t%s' % c)
            self.topicsData.write('\n')
            for key, value in self.topics_dict.items():
                self.topicsData.write(key)
                for a in self.topicsList:
                    if a in value:
                        self.topicsData.write('\t1')
                    else:
                        self.topicsData.write('\t0')
                self.topicsData.write('\n')

        elif n == "Abstract":
            for i in self.authors: # creating abstract dictionary
                key = i
                self.abstract_dict.setdefault(key, [])
                self.openfile.seek(0)
                for j in self.reader:
                    if i in j[1]:
                        self.abstract_dict[key]=j[5].replace('\n',' ')
            self.abstractList = []
            self.abstractData = file('abstractData.txt', 'w')
            self.abstractData.write('Author')
            for x, y in self.abstract_dict.items():
                if y not in self.abstractList:
                    self.abstractList.append(y)
                    self.abstractData.write('\t%s' % y)
            self.abstractData.write('\n')
            for key, value in self.abstract_dict.items():
                self.abstractData.write(key)
                for a in self.abstractList:
                    if a in value:
                        self.abstractData.write('\t1')
                    else:
                        self.abstractData.write('\t0')
                self.abstractData.write('\n')






    def view_cluster(self):
        if self.criteria_combo.get() == "":
            tkMessageBox.showinfo(message=" Select a Clustering Criteria", title="ERROR")
        elif self.var.get() == 1 and self.var1.get() == 1:
            tkMessageBox.showinfo(message=" Select Only One Clustering Type", title="ERROR")
        elif self.var.get() == 0 and self.var1.get() == 0:
            tkMessageBox.showinfo(message=" Select a Clustering Type", title="ERROR")

        elif self.var1.get() == 1:
            if self.criteria_combo.get() == "Groups":
                self.matrices("Groups")
                authors, groupsData,data=readfile('groupsData.txt')
                data.pop()
                clust=hcluster(data)
                print printclust(clust,authors)

            elif self.criteria_combo.get() == "Keywords":
                self.matrices("Keywords")
                authors, keywordsData, data = readfile('keywordsData.txt')
                data.pop()
                clust = hcluster(data)
                print printclust(clust, authors)

            elif self.criteria_combo.get() == "Topics":
                self.matrices("Topics")
                authors, topicsData, data = readfile('topicsData.txt')
                data.pop()
                clust = hcluster(data)
                print printclust(clust, authors)

            else:

                self.matrices("Abstract")
                authors, abstractData, data = readfile('abstractData.txt')
                data.pop()
                clust = hcluster(data)
                print printclust(clust, authors)

        elif self.var.get() == 1:
            if self.criteria_combo.get() == "Groups":
                self.matrices("Groups")
                authors, groupsData, data = readfile('groupsData.txt')
                data.pop()
                self.v = 10
                kclust =kcluster(data, k=self.v)
                print kclust
                for i in range(1,self.v):
                    a = [authors[r] for r in kclust[i]]
                    b = [i]
                    print "Cluster" + str(b) + '=' + str(a)

            elif self.criteria_combo.get() == "Keywords":
                self.matrices("Keywords")
                authors, keywordsData, data = readfile('keywordsData.txt')
                clust = hcluster(data)
                print printclust(clust, authors)

            elif self.criteria_combo.get() == "Topics":
                self.matrices("Topics")
                authors, topicsData, data = readfile('topicsData.txt')
                clust = hcluster(data)
                print printclust(clust, authors)

            else:
                self.matrices("Abstract")
                authors, abstractData, data = readfile('abstractData.txt')
                clust = hcluster(data)
                print printclust(clust, authors)










def main():
    root = Tk()
    root.geometry("850x650")
    app = UserInterface(root)
    root.title("Project 3")
    root.configure(background='black')
    root.mainloop()

main()