# -*- coding: utf-8 -*-

"""
ENGR 212 Fall 2016 Mini Project 1 Solution File
Doğukan Kotan <dogukankotan@std.sehir.edu.tr>

Starting '_<method_name>' functions are related to GUI.
"""
import random
import tkMessageBox
from tkFileDialog import askopenfilename, asksaveasfilename
from Tkinter import *
import os


class MarkovChainTextGenerator(Frame):
    def __init__(self, master):
        """

        :param master: initial frame object of tkinter
        :return: None

        """

        """ Variables """
        Frame.__init__(self, master)
        self.root = master
        self.input_v = StringVar()
        self.output_v = StringVar()
        self.first_two = str()

        """ Widgets """
        # Labels
        self.input_label = Label(self.root, text="Input File Path:",
                                 height=1, fg='black',
                                 font=("Helvetica", 12))
        self.output_label = Label(self.root, text="Output File Path:",
                                  height=1, fg='black',
                                  font=("Helvetica", 12))

        # Entries
        self.input_path = Entry(width=55, textvariable=self.input_v)
        self.output_path = Entry(width=55, textvariable=self.output_v)
        self.input_v.set(os.getcwd())
        self.output_v.set(os.getcwd())

        # Buttons
        self.browse_button = Button(self.root, text='Browse', command=self._on_click_browse)
        self.save_button = Button(self.root, text='Save', command=self._on_click_save)
        self.markov_button = Button(self.root, text='Markov', command=self._on_click_markov)

        self._customize()  # calling custom initialize()

    def _customize(self):
        """

        :return: None

        Our custom initialize methods here.
        """

        # Labels
        self.input_label.grid(row=0, column=0)
        self.output_label.grid(row=1, column=0)
        self.input_path.grid(row=0, column=2)
        self.output_path.grid(row=1, column=2)

        # Buttons
        self.browse_button.grid(row=0, column=3)
        self.save_button.grid(row=1, column=3)
        self.markov_button.grid(row=2, column=2)

    def _on_click_browse(self):
        """

        :return: None

        Open text file then update label with file path
        """
        filename = askopenfilename(parent=self.root, title='Choose a file',
                                   initialdir=os.getcwd(), filetypes=[('Text File', ('.txt',)), ('All Files', ('*',))]
                                   )
        if filename:
            self.input_v.set(filename)

    def _on_click_save(self):
        """

        :return: None

        Save text file and update label with file path
        """
        filename = asksaveasfilename(parent=self.root, title='Save a file',
                                     initialdir=os.getcwd(), filetypes=[('Text File', ('.txt',),)]
                                     )
        if filename:
            self.output_v.set(filename)

    def _on_click_markov(self):
        """

        :return: None

         - Open text file then reads and saves on dictionary as {(word1,word2):[word3]}.
         - Do markov chain
         - Show Info Message
        """
        _ = self.read_input()
        self.markov_chain(_)

        tkMessageBox.showinfo("Finished", "Markov Chain Process has completed.")

    def read_input(self):
        """
        :return dictionary as {(word1,word2):[word3]}

        - open input file get words
        - put that word dictionary in return format

        """
        data = dict()
        first = True
        with open(self.input_v.get(), 'r') as input_text:
            words = input_text.read().split()
            for i in range(len(words) - 2):
                word1 = words[i]
                word2 = words[i + 1]
                if first:
                    self.first_two = (word1, word2)
                    first = False
                word3 = words[i + 2]
                pairs = (word1, word2)
                if pairs not in data:
                    data.setdefault(pairs, list())
                    data[pairs].append(word3)
                else:
                    data[pairs].append(word3)
        return data

    def markov_chain(self, data):
        """
        :param data: our {(word1,word2):[word3]} format dictionary

        :return: None

         - Create a new file
         - Do Markov Chain Process

        """
        word_count = 0
        with open(self.output_v.get(), 'w') as output_text:
            for w in self.first_two:
                output_text.write(w + ' ')
                word_count += 1
            while word_count <= 500:
                if self.first_two in data:
                    word_combinations = data[self.first_two]
                    word_count += 1
                    word3 = random.choice(word_combinations)
                output_text.write(word3 + ' ')
                word_count += 1
                word2 = self.first_two[1]
                self.first_two = (word2, word3)


if __name__ == '__main__':
    root = Tk()  # Root frame of Tkinter
    root.resizable(width=FALSE, height=FALSE)  # Prevent all resize actions
    root.title('Markov Chain Generator')  # Set GUI Title
    root.geometry('{}x{}'.format('590', '100'))  # Set GUI geometry
    app = MarkovChainTextGenerator(root)  # Starting our app
    root.mainloop()  # Show GUI to user
