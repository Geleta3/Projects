from tkinter import *
import codecs
import csv
import matplotlib.pyplot as plt


class Dictionary:
    def __init__(self, master):
        self.master = master
        self.top_frame()
        self.input_letter = self.entries(self.searchFrame, 0, 1, 40)
        self.match_word = self.entries(self.frame(), 0, 0, 30, columnspan=3)
        self.oncursor_entry = self.entries(self.frame, 1, 0, 20)
        self.word_type = self.entries(self.frame, 1, 1, 5)
        self.show_info = self.entries(self.frame, 1, 2, 35)
        self.dict()

    @staticmethod
    def file():
        file_csv = codecs.open('.Folder\\allwords.csv', 'r', encoding='utf-8')
        file = csv.reader(file_csv, delimiter='\n')
        files = []
        for row in file:
            files.append(row[0])
        return files

    def dict(self):
        self.EtoC_dict = {}
        self.CtoE_dict = {}
        for word in self.file():
            try:
                replace = word.replace('；', '，')
                first_split = replace.split(' ')
                second_split = first_split[1].split('.')
                comma_count = second_split[1].count('，')
                chinese_split = []
                if comma_count > 0:
                    commasplit = second_split[1].split('，', comma_count)
                    for i in range(len(commasplit)):
                        chinese_split.append(commasplit[i])

                else:
                    chinese_split.append(second_split[1])
            except IndexError:
                continue
            if word is not None and len(second_split) == 2:  # Filtering words from our file.
                self.EtoC_dict[first_split[0]] = second_split
                for chinese in chinese_split:
                        if chinese not in  self.CtoE_dict:
                            self.CtoE_dict[chinese] = [second_split[0], first_split[0]]
                        else:
                            self.CtoE_dict[chinese].append(',')
                            self.CtoE_dict[chinese].append(first_split[0])

    def label(self):
        search_label = Label(self.searchFrame, text='Search',  bg='gainsboro', font=20)
        search_label.grid(row=0, column=0, sticky='e', padx=10)

    def search(self, event):
        self.search = self.input_letter.get()
        self.match_word['state'] = 'normal'
        self.listbox.delete(0, END)
        i = 0
        if self.chosen.get() == 'English':
            for word in self.EtoC_dict:
                if str(word.lower()).startswith(str(self.search).lower()) and word is not None:
                    self.listbox.insert(i, word)
                    i += 1
        if self.chosen.get() == 'Chinese':
            for word in self.CtoE_dict:
                if str(word.lower()).startswith(str(self.search).lower()) and word is not None:
                    self.listbox.insert(i, word)
                    i += 1
            self.match_word.insert(0, '{}个字以“{}”开头'.format(i, self.search))

        self.match_word.delete(0, END)
        if self.chosen.get() == 'English':
            if len(self.search) == 0:
                self.match_word.delete(0, END)
            elif i == 1 or i == 0:
                self.match_word.insert(0, '{} word starts with \'{}\''.format(i, self.search))
            else:
                self.match_word.insert(0, '{} words start with \'{}\''.format(i, self.search))
        else:
            self.match_word.insert(0, '{} 个字以“{}”开头'.format(i, self.search))
        self.match_word['state'] = 'disabled'

    def search_bind(self):
        self.input_letter.bind('<KeyRelease>', self.search)

    def frame(self):
        self.frame = Frame(self.master, bg='lightblue')
        self.frame.grid(row=2, column=0, columnspan=3, sticky='w')
        return self.frame

    def top_frame(self):
        self.searchFrame= Frame(self.master, bg = 'lightblue')
        self.searchFrame.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        return self.searchFrame

    def entries(self, root, row, column, width,  columnspan=1):
        self.entry= Entry(root, width=width, bd=3,  fg='black', disabledforeground = 'black', font=( 'bold', 12))
        self.entry.grid(row=row, column=column, padx=15, pady=10, columnspan=columnspan, sticky='w')
        return self.entry

    def wordbank(self):  # this is the function that displays our words.
        yscroll = Scrollbar(self.master, orient=VERTICAL)
        yscroll.grid(row=1, column=1, sticky='ns')
        self.listbox = Listbox(self.master, bg='snow', font=('BODY',11, 'normal'), bd=0, height=20, width=60)
        self.listbox['yscrollcommand'] = yscroll.set
        self.listbox.grid(row=1, column=0, columnspan=1,  padx=15, sticky='w')
        yscroll['command'] = self.listbox.yview
        self.listbox.bind("<<ListboxSelect>>", self.get_word)

    def fill_box(self):
        self.listbox.delete(0, END)
        i = 0
        for word in self.EtoC_dict:
            if len(self.EtoC_dict[word]) == 2 and word is not None:
                self.listbox.insert(i, word)
                i += 1

    def chinese_fill(self):
        self.listbox.delete(0, END)
        i = 0
        for word in self.CtoE_dict:
            self.listbox.insert(i, word)
            i += 1

    def get_word(self, event):   # function that displays info of the choosen word.
        self.oncursor_entry['state'], self.word_type['state'], self.show_info['state'] = 'normal', 'normal', 'normal'
        self.oncursor_entry.delete(0, END)
        self.word_type.delete(0, END)
        self.show_info.delete(0, END)
        getindex = self.listbox.curselection()
        line = str(self.listbox.get(getindex))
        self.oncursor_entry.insert(0, line)
        if self.chosen.get() == 'English':
            self.word_type.insert(0, self.EtoC_dict[line][0])
            self.show_info.insert(0, self.EtoC_dict[line][1])
        else:
            self.word_type.insert(0, self.CtoE_dict[line][0])
            self.show_info.insert(0, self.CtoE_dict[line][1:])
        self.oncursor_entry['state'], self.word_type['state'], self.show_info['state']  = 'disabled', 'disabled', 'disabled'

    def option(self):
        self.chosen = StringVar()
        self.chosen.set('English')
        engOrChin = OptionMenu(self.searchFrame, self.chosen, *['English', 'Chinese'], command=self.optional_call)
        engOrChin.grid(row=0, column=2, sticky='w')
        engOrChin['bd'], engOrChin['bg'], engOrChin['activebackground'] = 1, 'lightblue', '#999999'

    def optional_call(self, event):
        if self.chosen.get() == "English":
            self.fill_box()
        if self.chosen.get() == 'Chinese':
            self.chinese_fill()


class Visualization:
    def __init__(self):
        self.letter_count = {}

    def count(self):
        self.letter_count = {}
        for word in dictionary_gui.EtoC_dict:
            for letter in word:
                upper_case = letter.upper()
                disturbance = ['无', '效', '文', '档', '-', '本', '地', "'", '.', '(', ')'] # to filter english character from these
                if upper_case not in self.letter_count and letter not in disturbance:
                    self.letter_count[upper_case] = 1
                if upper_case in self.letter_count:
                    self.letter_count[upper_case] += 1
        return self.letter_count

    def bar(self):
        letters = [letter for letter in self.count()]
        letters.sort()
        letter_count = [self.count()[letter] for letter in letters]
        plt.style.use('seaborn')
        plt.barh(letters, letter_count)
        plt.title('Numbers of letters in the Dictionary')
        plt.ylabel('Letters')
        plt.xlabel('Number of occurence in the dictionary')
        plt.tight_layout()
        plt.show()


root = Tk()
root.geometry('650x550')
icon = PhotoImage(file='.Folder\\dict.png')
root.iconphoto(False, icon)
root.title('Moke Dictionary')
root.configure(bg='lightblue')
root.resizable(0, 0)

############################
dictionary_gui = Dictionary(root)
dictionary_gui.file()
dictionary_gui.wordbank()
dictionary_gui.fill_box()
dictionary_gui.search_bind()
dictionary_gui.label()
dictionary_gui.option()
############################

plot = Visualization()
plot.bar()
root.mainloop()
