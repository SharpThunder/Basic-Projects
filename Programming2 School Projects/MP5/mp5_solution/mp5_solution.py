# -*- coding: utf-8 -*-

"""
ENGR 212 Fall 2016 Mini Project 5 Solution File
Doğukan Kotan <dogukankotan@std.sehir.edu.tr>

Starting '_<method_name>' functions are related to GUI.
"""
import copy
import csv
import random
import ttk
from Tkinter import *
from tkMessageBox import showerror
import docclass as ml


class AAAIClassifer(Frame):
    def __init__(self, master):
        """
        Constructor of the program. It contains every component of the GUI and initial values
        :param master: initial window object of tkinter
        :return:
        """

        """ Variables """
        Frame.__init__(self, master)
        self.root = master
        self.root.columnconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.radio_var = IntVar()
        self.radio_var.set(1)
        self.thresholds = []
        self.classifier_dataset = []

        # Frames
        self.top_frame = Frame(self.root)
        self.middle_frame = Frame(self.root)
        self.bottom_frame = Frame(self.root)
        self.middle2_frame = Frame(self.bottom_frame)
        self.area_frame = Frame(self.bottom_frame)

        # Labels
        self.title = Label(self.top_frame, text="AAAI Classifier", bg="brown", fg="white",
                           font=("Comic Sans", 13), height=2)
        self.set_threshold_label = Label(self.middle2_frame, text="Set Thresholds",
                                         font=("Comic Sans", 10))
        self.method_label = Label(self.middle2_frame, text="Choose Classifier", font=("Comic Sans", 10))
        self.load_data_label = Label(self.middle_frame, bg="white", text="Waiting Dataset...", font=("Comic Sans", 10))
        # Buttons

        self.calculate_accuracy_button = Button(self.middle2_frame, text="Calculate Accuracy", font=("Comic Sans", 10),
                                                command=self._calculate_accuracy_button)
        self.set_threshold_button = Button(self.middle2_frame, text="Set", font=("Comic Sans", 10),
                                           command=self._set_threshold_to_listbox)
        self.remove_threshold_button = Button(self.middle2_frame, text="Remove Selected", font=("Comic Sans", 10),
                                              command=self._remove_selected_threshold)
        self.load_data_button = Button(self.middle_frame, text="Load Dataset", font=("Comic Sans", 10),
                                       command=self._load_data)

        # Radio
        self.radio_naive = Radiobutton(self.middle2_frame, text="Naive-Bayes", font=("Comic Sans", 10),
                                       value=1,
                                       variable=self.radio_var)
        self.radio_fisher = Radiobutton(self.middle2_frame, text="Fisher", font=("Comic Sans", 10), value=2,
                                        variable=self.radio_var)
        # Entry
        self.threshold_entry = Entry(self.middle2_frame, width=3)
        self.threshold_entry.insert(0, 0.3)

        # Combobox
        self.combobox = ttk.Combobox(self.middle2_frame, height=5, width=15)

        # Canvas
        self.canvas_area = Canvas(self.area_frame, bg="white", width=800, height=350, scrollregion=(0, 0, 0, 0))

        # Listbox
        self.threshold_listbox = Listbox(self.middle2_frame, selectmode=EXTENDED)

        # Scrollbar
        self.hbar = Scrollbar(self.area_frame, orient=VERTICAL, command=self.canvas_area.yview)
        self._customize()

    def _customize(self):
        """
        Customize grid geometry
        :return:
        """
        # Frames
        self.top_frame.grid(row=0, sticky=W + E)
        self.top_frame.columnconfigure(0, weight=1)
        self.middle_frame.grid(row=1, pady=10)
        self.bottom_frame.grid(row=2)
        self.area_frame.grid(row=1, column=0, sticky=W + E + N + S)
        self.middle2_frame.grid(row=0)

        # Top Frame
        self.title.grid(sticky=W + E)

        # Middle Frame
        self.load_data_button.grid(row=0, column=0, columnspan=3)
        self.load_data_label.grid(row=0, column=4, columnspan=5)

        # Middle2 Frame
        self.method_label.grid(row=0, column=0, columnspan=2)
        self.set_threshold_label.grid(row=0, column=2, columnspan=3)
        self.radio_naive.grid(row=1, column=0, columnspan=2)
        self.threshold_entry.grid(row=1, column=2, columnspan=1)
        self.combobox.grid(row=1, column=3, columnspan=2)
        self.set_threshold_button.grid(row=1, column=5)
        self.threshold_listbox.grid(row=1, column=6, rowspan=5)
        self.remove_threshold_button.grid(row=1, column=7)
        self.radio_fisher.grid(row=2, column=0, columnspan=2)
        self.calculate_accuracy_button.grid(row=3, column=2)

        # Area Frame
        self.canvas_area.grid(row=0, column=0)
        self.canvas_area.config(yscrollcommand=self.hbar.set)
        self.hbar.grid(sticky=N + S, row=0, column=1)

    def _calculate_accuracy_button(self):
        """
        Main program function.
        :return:
        """
        if not self.combobox.get():
            showerror("Error", "You should load dataset before calculating it")
        else:
            self._clear()
            cl = None
            if self.radio_var.get() == 1:
                cl = ml.naivebayes(ml.getwords)
            elif self.radio_var.get() == 2:
                cl = ml.fisherclassifier(ml.getwords)
            self.set_thresholds(cl)
            self.load_data_label.config(text="Training classifier and calculating accuracies. Loading...", fg="brown")
            self.root.update()
            for i in range(4):
                train_set, test_set = self.decompose_dataset()
                self.train_classifer(cl, train_set)
                self.predict_classifier(cl, test_set)
            output = ""
            output += "Topics\t\t\tClassifier Accuracy\n"
            output += "-------\t\t\t-------------------\n"
            for topic, accuracy in self.calculate_accuracy().iteritems():
                output += "{0}\t\t\t{1:.2f}%\n".format(topic, accuracy)
            self._write_to_canvas(output)
            self.load_data_label.config(text="Accuracies calculated", fg="green")
            self.root.update()

    def decompose_dataset(self):
        """
        This function separates test and train set
        :return: list of tuples trains_set and test_set ([(), ...], [(), ...])
        """
        test_set = copy.deepcopy(self.classifier_dataset)
        train_set = []
        for i in range(300):
            selected = self.select_random_data_with_remove(test_set)
            train_set.append(selected)
        return train_set, test_set

    def _set_threshold_to_listbox(self):
        """
        It will set threshold to listbox,
        and also update its value
        :return:
        """
        selected = self.combobox.get()
        if not selected:
            showerror("Error", "You should load dataset before setting threshold")
        else:
            thresh = self.threshold_entry.get()
            if 0.0 < float(thresh) <= 1.0:
                text = "{0}-{1}".format(selected, thresh)
                self.thresholds.append(tuple((selected, float(thresh))))
                for index, item in enumerate(self.threshold_listbox.get(0, END)):
                    if item.split("-")[0] == selected:
                        self.threshold_listbox.delete(index)
                self.threshold_listbox.insert(0, text)
            else:
                showerror("Error", "You should select threshold value between 0.0 and 1.0")

    def set_thresholds(self, classifier):
        """
        It will set threshold values from thresholds list of tuples
        :param classifier: classifier method
        :return:
        """
        if self.radio_var.get() == 1:
            for threshold in self.thresholds:
                classifier.setthreshold(threshold[0], threshold[1])
        elif self.radio_var.get() == 2:
            for threshold in self.thresholds:
                classifier.setminimum(threshold[0], threshold[1])

    @staticmethod
    def train_classifer(classifier, train_set):
        """

        :param classifier: naive or fisher classifier
        :param train_set: list of tuples
        :return:
        """
        for item in train_set:
            classifier.train(item[1], item[0])

    def predict_classifier(self, classifier, test_set):
        """

        :param classifier: naive or fisher classifier
        :param test_set: list of tuples
        :return:
        """
        for item in test_set:
            if item not in self.results:
                self.results.setdefault(item[0], [0, 0])
            predicted = classifier.classify(item[1])
            if predicted == item[0]:
                self.results[item[0]][0] += 1
            self.results[item[0]][1] += 1

    def _remove_selected_threshold(self):
        """
        It will remove selected items in listbox
        :return:
        """
        item_index = map(int, self.threshold_listbox.curselection())
        for index in item_index:
            self.threshold_listbox.delete(index)

    @staticmethod
    def select_random_data_with_remove(dataset):
        """
        It will select random data from given dataset
        :param dataset: list of tuples
        :return: a tuple
        """
        return dataset.pop(random.randint(0, len(dataset) - 1))

    def calculate_accuracy(self):
        """
        returns average accuracy dictionary
        :return: accuracy dictionary {cat:accuracy, ...}
        """
        accuracy_dict = {}
        for key, value in self.results.iteritems():
            accuracy_dict[key] = value[0] * 100.0 / value[1]
        return accuracy_dict

    @staticmethod
    def create_data():
        """
        Read data from Mini Project 3
        :return: list of dictionaries [{"title", "abstract"...}, ...]
        """
        papers = []
        with open("AAAI-14_Accepted_Papers_corrected.txt", "r") as csvfile:
            aaai_reader = csv.reader(csvfile, delimiter=',')
            first_line = True
            for row in aaai_reader:
                if first_line:
                    first_line = False
                else:
                    paper_dict = {}
                    author_list = []
                    group_list = []
                    title = "".join(row[0])
                    authors = "".join(row[1])
                    groups = "".join(row[2])
                    keywords = "".join(row[3])
                    topics = "".join(row[4])
                    abstract = "".join(row[5:])
                    if 'and' in authors:
                        author_names = authors.split('and')
                        for name in author_names:
                            for x in name.split(','):
                                author_list.append(x.strip())
                    else:
                        author_names = authors.split(',')
                        for name in author_names:
                            author_list.append(name.strip())
                    if 'and' in groups:
                        group_names = groups.split('and')
                        for name in group_names:
                            for x in name.split(','):
                                group_list.append(x.strip())
                    else:
                        group_names = groups.split('and')
                        for name in group_names:
                            group_list.append(name.strip())
                    paper_dict['title'] = title
                    paper_dict['authors'] = author_list
                    paper_dict['groups'] = group_list
                    paper_dict['keywords'] = keywords
                    paper_dict['topics'] = topics
                    paper_dict['abstract'] = abstract
                    papers.append(paper_dict)
        return papers

    def _write_to_canvas(self, out):
        """
        It will write string to canvas
        :param out: string of word
        :return:
        """
        self.canvas_area.create_text(10, 10, anchor="nw", text=out, font=("Comic Sans", 10))
        self.canvas_area.config(scrollregion=(0, 0, 0, len(out) * 1.2))

    def _load_data(self):
        """
        Load data button
        :return:
        """
        self.load_data_label.config(text="Loading Dataset...", fg="brown")
        self.root.update()
        # self.transform_dataset()
        self.classifier_dataset = []
        with open('dataset.txt', 'r') as classifier_dataset:
            dataset_reader = csv.reader(classifier_dataset, delimiter=',')
            topics = []
            for row in dataset_reader:
                topics.append(row[0])
                paper = (row[0], row[1])
                self.classifier_dataset.append(paper)
        self.topics = sorted(list(set(topics)))
        self.combobox.config(values=self.topics)
        self.combobox.current(0)
        self.load_data_label.config(text="Dataset Loaded", fg="Green")

    def transform_dataset(self):
        """
        Adaptor creates a dataset file
        :return:
        """
        papers = self.create_data()
        dataset = []
        for paper in papers:
            topics = paper['topics']
            main_topic = topics.split(":")[0]
            if main_topic == "":
                main_topic = "XYZ"
            feature = ""
            for value in paper.values():
                try:
                    transformed_value = "".join(value)
                except:
                    feature += value + " "
                else:
                    feature += transformed_value + " "
            dataset.append((main_topic, feature))
        dataset_file = open('dataset.txt', 'w')
        for paper in dataset:
            topic = paper[0]
            rest = paper[1]
            dataset_file.write('"{0}","{1}"\n'.format(topic, rest))
        dataset_file.close()

    def _clear(self):
        """
        clear canvas and results
        :return:
        """
        self.canvas_area.config(scrollregion=(0, 0, 0, 0))
        self.canvas_area.delete("all")
        self.results = {}


if __name__ == '__main__':
    root = Tk()  # Root frame of Tkinter
    root.resizable(width=FALSE, height=FALSE)  # Prevent all resize actions
    root.title('AAAI Classifier')  # Set GUI Title
    root.geometry('1000x650+250+0')  # Set GUI geometry
    app = AAAIClassifer(root)  # Starting our app
    root.mainloop()  # Sh ow GUI to user
