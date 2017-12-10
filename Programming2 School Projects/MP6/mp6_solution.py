from Tkinter import *
import tkFileDialog as fd
import tkMessageBox, os, magic, time, re, timeit, math, shelve
from ttk import Scrollbar

# This is for testing the file engr 212
ignorewords = set(['the', 'of', 'to', 'and', 'a', 'in', 'is', 'it'])
class SearchEngine(Frame):
    def font(self,size=20, type='Calibri', bold=''):
        return type + ' ' + str(size) + ' ' + bold

    def __init__(self, parent, color):
        self.parent = parent
        self.bg = color
        self.parent['bg'] = 'orange'
        # Datastructures ===============================================================================================
        self.indexBuilt = False
        self.categories = {'plain':[],'program':[]}  # {fil category -plain or program- : fil path}
        self.lastAccessTime = {}  # {file path: last access time}
        self.fileSize = {}  # {file path: file size}
        self.word_count = {}  #{file: word distance score}
        self.end_time = 0  # to calculate the run time, called in search method
        self.start_time = 0
        self.page = StringVar()
        self.page.set(1)  # Page number, used in self.paging method
        self.runtime = StringVar()
        # HEADER -------------------------------------------------------------------------------------------------------
        Label(self.parent, text='File Searcher', font=self.font(size=26,bold='bold'), fg='white', bg='deepskyblue4').pack(fill=X)
        # Start Search -------------------------------------------------------------------------------------------------
        startSearchingFrame = Frame(self.parent, bg=self.bg)
        startSearchingFrame.pack(side=TOP, fill=X, pady=(5,2))
        Label(startSearchingFrame, text='Folder to start searching:', font=self.font, bg=self.bg)\
            .grid(row=0,column=0,columnspan=2,sticky=W,padx=(30,0))
        self.startingFolder = Entry(startSearchingFrame, font=self.font(size=15), width=40)
        self.startingFolder.grid(row=0, column=2, padx=50, pady=10)
        Label(startSearchingFrame, text='Depth:',font=self.font, bg=self.bg).grid(row=1,column=0,sticky=W,padx=(30,0))
        self.depth = Entry(startSearchingFrame, font=self.font(15),width=3)
        self.depth.grid(row=1, column=1, sticky=W)
        Button(startSearchingFrame, text='Build Index',font=self.font, relief=GROOVE,
               bg='orange',cursor='hand2', command=self.buildIndex).grid(row=1, column=2, pady=10)
        # Search -------------------------------------------------------------------------------------------------------
        searchInputOutputFrame = Frame(self.parent, bg=self.bg)
        searchInputOutputFrame.pack(side=TOP, fill=X)
        self.keywords = Entry(searchInputOutputFrame, font=self.font(22), width=40)
        self.keywords.grid(padx=(50,0),pady=(10,0), columnspan=3)
        # Ranking Criteria
        Label(searchInputOutputFrame, text='Ranking Criteria',bg=self.bg, font=self.font).grid(padx=(45,0),pady=5,row=1,column=0, sticky=W)
        Label(searchInputOutputFrame, text='Weight', bg=self.bg, font=self.font).grid(pady=5,row=1, column=1,sticky=W)
        Label(searchInputOutputFrame, text='Filter', bg=self.bg, font=self.font).grid(padx=(12,0),pady=5,row=1, column=2,sticky=W)
        # Word Distance
        self.word_distance_selected = BooleanVar()
        self.word_distance_selected.set(1)
        Checkbutton(searchInputOutputFrame, text='Word-Distance', font=self.font(15), variable=self.word_distance_selected,
                    cursor='hand2', bg=self.bg).grid(padx=(45, 0), row=2, column=0, sticky=W)
        self.wordDistance = Entry(searchInputOutputFrame,font=self.font(15),width=3)
        self.wordDistance.insert(END,1)
        self.wordDistance.grid(row=2, column=1, sticky=W)
        # Access Time
        self.access_time_selected = BooleanVar()
        self.access_time_selected.set(1)
        Checkbutton(searchInputOutputFrame, text='Access-Time', font=self.font(15), variable=self.access_time_selected,
                    cursor='hand2', bg=self.bg).grid(padx=(45, 0), row=3, column=0, sticky=W)
        self.accessTime = Entry(searchInputOutputFrame, font=self.font(15), width=3)
        self.accessTime.insert(END, 1)
        self.accessTime.grid(row=3, column=1, sticky=W)
        # Filter
        self.filTypeFilter = Listbox(searchInputOutputFrame, height=3, selectmode=MULTIPLE)
        self.filTypeFilter.insert(END,'Plain Text')
        self.filTypeFilter.insert(END, 'Program code')
        self.filTypeFilter.select_set(0,END)
        self.filTypeFilter.grid(row=2,rowspan=2, column=2, sticky=W, padx=15)
        # Search button
        Button(searchInputOutputFrame, text='Search', font=self.font, relief=GROOVE, bg='orange',command=self.search)\
            .grid(row=2, column=3, sticky=W)
        # Results ------------------------------------------------------------------------------------------------------
        self.results = Text(searchInputOutputFrame, font=self.font(12,bold='bold'),height=17)
        self.results.grid(padx=(45,0),pady=10,row=4, column=0, columnspan=4)
        resultsScrollbar = Scrollbar(searchInputOutputFrame, command=self.results.yview)
        self.results['yscrollcommand'] = resultsScrollbar.set
        resultsScrollbar.grid(padx=(45,0),pady=10,row=4, column=3, rowspan=3,sticky=W+N+S)
        # Separating pages
        self.pagesFrame = Frame(self.parent, bg=self.bg)
        self.pagesFrame.pack(side=TOP, fill=BOTH,expand=True)
        self.previousB = Button(self.pagesFrame)
        self.nextB = Button(self.pagesFrame)
        self.pageLabel = Label(self.pagesFrame)
        self.currentPage = Label(self.pagesFrame)
        self.db = shelve.open('searchingDatabase.db', 'c', writeback=True)  # C means read that database, if it is not there, then create it.


    def openDatabase(self,from_search=0):
        try:
            self.lastAccessTime = self.db['accessTime']  # {file path: last access time}
            self.fileSize = self.db['fileSize']  # {file path: file size}
            self.categories = self.db['categories'] # {fil category -plain or program- : fil path}
            self.indexBuilt = True
        except:
            if from_search:
                return tkMessageBox.showwarning("No database", "No index found")
            self.buildIndex(new_search=True)

    def buildIndex(self,path="",new_search=False):
        self.startingFolder.insert(END, path)
        rootDirectory = self.startingFolder.get()
        if (new_search):
            tkMessageBox.showwarning("Invalid directory", "Starting folder does not exist")
            self.startingFolder.delete(0, END)
            self.buildIndex(path=fd.askdirectory())  # import tkfilDialog as fd
        elif not(os.path.isdir(rootDirectory)):
            self.openDatabase()
        new_search = False
        try:
            crawling_depth = int(self.depth.get())
        except ValueError:  # If no valid crawling depth is provided use 0 as default depth, without opening any subdirectories
            crawling_depth = 0
        # os.remove("ChangedFile.csv")
        # Creating {fil category plain or program: fils of that type} dictionary for indexing
        self.crawl(rootDirectory, crawling_depth)
        self.db['accessTime'] = self.lastAccessTime  # {file path: last access time}
        self.db['fileSize'] = self.fileSize  # {file path: file size}
        self.db['categories'] = self.categories  # {fil category -plain or program- : fil path}
        self.indexBuilt = True

    def crawl(self, root, depth):
        if depth < 0:  # Breaking if maximum (deepest) depth is reached
            return
        try:
            for item in os.listdir(root):
                filPath = os.path.join(root, item)
                if os.path.isfile(filPath):
                    if 'plain' in magic.from_file(filPath, mime=True):  # Plain text or program ?
                        self.categories['plain'].append(filPath)
                    else:
                        self.categories['program'].append(filPath)
                    self.lastAccessTime[filPath] = os.stat(filPath).st_atime
                    self.fileSize[filPath] = os.path.getsize(filPath)
                else:
                    self.crawl(filPath, depth - 1)
        except WindowsError:
            return

    # Computing the frequency of each word in each fil
    def getWordDistance(self, fil, queryWords):
        text = open(fil).read()
        cleaned_text = re.compile('[^A-Za-z0-9]').sub(' ', text)
        words = re.split('\s+', cleaned_text)  # Words of the file
        # Checking the assumption that all queryWords should be present
        # in the file in order to be taken among the results
        for word in queryWords:
            if not(word in text):
                return 0
        # If there's only one word, everyone wins!
        if len(queryWords) < 2:
            self.word_count[fil] = 1.0
            return 1
        score = 0
        for word in range(len(queryWords)-1):
            score += min(1000000, abs(words.index(queryWords[word]) - words.index(queryWords[word+1])))  # It should not be more than 1000000
        self.word_count[fil] = score
        return 1


    # SEARCHING BLOCK --------------------------------------------------------------------------------------------------
    def search(self):
        if not(self.indexBuilt):
            self.openDatabase(from_search=1)
        if self.keywords.get() == "":
            return tkMessageBox.showwarning("Insufficient Input","Provide at least one keyword")
        if not(self.word_distance_selected.get() or self.access_time_selected.get()):
            return tkMessageBox.showwarning("Insufficient Input", "Choose at least one ranking measure")
        if (self.word_distance_selected.get() and self.wordDistance.get()=='') or (self.access_time_selected.get() and self.accessTime.get() == ''):
            return tkMessageBox.showwarning("Insufficient Input", "Please provide proper weight")
        if not(len(self.filTypeFilter.curselection())):
            return tkMessageBox.showwarning("Insufficient Input", "Choose at least one fil category")
        self.start_time = timeit.default_timer()
        self.results.delete(0.0, END)  # Clearing the Text widget from previous results
        self.double_ranking = {}
        self.accessTime_scores = {}
        self.worddistance_scores = []
        fils = []
        file_scores = {}  # {fil : score}
        selected_categories = list(self.filTypeFilter.curselection())
        for cat in range(len(selected_categories)):
            if selected_categories[cat] == 0:
                selected_categories[cat] = 'plain'
            else:
                selected_categories[cat] = 'program'
        queueWords = re.split('\s+', re.compile('[^A-Za-z0-9]').sub(' ', self.keywords.get()))
        # queryWords are the words we are searching for, cleaned just like the previous two lines
        filtered = self.filter_categories(selected_categories,queueWords)
        # {fil:[word distance score,access_times]}
        file_scores = self.rank_method(filtered)  #{file: final score}
        fil_scores_normalized = self.normalizescores(file_scores)
        for fil in fil_scores_normalized:
            fils.append([fil_scores_normalized[fil], fil])
        # RANKING ---------------------------------------------------
        results = sorted(fils)[::-1]  # [[score, file]] sorted from maximum to minimum score
        for count in range(len(results)):
            results[count][1] = str(count + 1) + '. ' + results[count][1] + ' ' + str(self.fileSize[results[count][1]])
        pages = int(math.ceil(len(results) / 10.0))
        self.page_list = {}
        # Separating pages, each will have maximum 10 fils (results)
        for page in range(pages):
            start = page * 10
            limit = (page + 1) * 10
            self.page_list[page + 1] = results[start:limit]  # {page number : [[fil, score]]}
        self.paging()
        self.end_time = timeit.default_timer()

    def filter_categories(self, selected_cat_list, queueWords):
        fils = {}  # {fil:[word distance score,last access time]}
        self.lastAccessTime = self.normalizescores(self.lastAccessTime)
        for cat in selected_cat_list:
            for fil in self.categories[cat]:
                if self.getWordDistance(fil, queueWords):
                    fils[fil] = [0, self.lastAccessTime[fil]]
        self.word_count = self.normalizescores(self.word_count,smallIsBetter=1)  # normalizing word distance scores
        for fil in fils:
            fils[fil][0] = self.word_count[fil]
        return fils

    def rank_method(self, scores_dict):
        scores = {}  # {file:score}
        if self.word_distance_selected.get() and self.access_time_selected.get():
            # scores_dict = {fil:[word distance score, access time score]}
            for fil in scores_dict:
                worddistance_score = scores_dict[fil][0]
                accessTime_score = scores_dict[fil][1]
                worddistance_score = worddistance_score*float(self.wordDistance.get())
                accessTime_score = accessTime_score*float(self.accessTime.get())
                scores[fil] = worddistance_score + accessTime_score
        elif self.word_distance_selected.get():
            for fil in scores_dict:
                scores[fil] = scores_dict[fil][0]
        elif self.access_time_selected.get():
            for fil in scores_dict:
                scores[fil] = scores_dict[fil][1]
        else:
            return tkMessageBox.showwarning('Invalid input','Please provide a valid weight')
        return scores

    def normalizescores(self, scores, smallIsBetter=0):  # modified mysearchengine.py
        vsmall = 0.00001  # Avoid division by zero errors
        if smallIsBetter:
            minscore = min(scores.values())
            minscore = max(minscore, vsmall)
            return dict([(u, float(minscore) / max(vsmall, l)) for (u, l) in scores.items()])
        else:
            maxscore = max(scores.values())
            if maxscore == 0:
                maxscore = vsmall
            return dict([(u, float(c) / maxscore) for (u, c) in scores.items()])

    def paging(self):
        self.page.set(1)
        self.pageLabel.config(bg=self.bg, text='Page: ')
        self.pageLabel.pack(side=LEFT,padx=(275,0))
        self.previousB.config(text='Previous', command=self.previous)
        self.previousB.pack(side=LEFT, padx=10)
        self.currentPage.config(bg='white', textvariable=self.page, relief=GROOVE)
        self.currentPage.pack(side=LEFT, ipadx=5)
        self.nextB.config(text='Next', command=self.Next)
        self.nextB.pack(side=LEFT, padx=10)
        self.buttons_states()
        self.show_page()

    def previous(self):
        self.page.set(int(self.page.get()) - 1)
        self.buttons_states()
        self.show_page()

    def Next(self):
        self.page.set(int(self.page.get()) + 1)
        self.buttons_states()
        self.show_page()

    def buttons_states(self):
        n = len(self.page_list)
        if int(self.page.get()) == 1:
            self.previousB['state'] = DISABLED
        else:
            self.previousB['state'] = NORMAL

        if n > 1 and int(self.page.get()) < n:
            self.nextB['state'] = NORMAL
        else:
            self.nextB['state'] = DISABLED

    def show_page(self):
        self.results.delete(0.0, END)
        countFiles = (len(self.page_list) - 1) * 10 + len(self.page_list[max(self.page_list.keys())])
        self.results.tag_config('score', foreground='red', font=self.font(13,bold='bold'))
        self.results.tag_config('size', foreground='blue', font=self.font(13, bold='bold'))
        for File in self.page_list[int(self.page.get())]:
            self.results.insert(END, File[1] + ' ' + str(File[0]) + '\n\n')
            self.highlight(str(File[0]), 'score')
            self.highlight(File[1].split(' ')[-1], 'size')
        self.runtime.set('%d Files (%g Seconds)' % (countFiles, self.end_time - self.start_time))

    def highlight(self, keyword, tag):
        pos = '1.0'
        while True:
            idx = self.results.search(keyword, pos, END)
            if not idx:
                break
            pos = '{}+{}c'.format(idx, len(keyword))
            self.results.tag_add(tag, idx, pos)
            # I used some code from:
            # http://stackoverflow.com/questions/17829713/tkinter-text-highlight-specific-lines-using-keyword



if __name__ == '__main__':
    root = Tk()
    o = SearchEngine(root, 'honeydew')
    root.geometry('800x750')
    root.mainloop()
