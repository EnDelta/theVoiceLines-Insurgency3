# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
from os import *
import threading, re, io


########################## Cfg ##########################

GitFolderLocation = getcwd()[:-14] + 'VL-Original\\'

ComboboxCategoriesValues = ['Tutorial',
                            "Spec Ops", 
                            'Mercenary', 
                            "Militia", 
                            'Rebel', 
                            "Regular", 
                            'Operative', 
                            "Warlock", 
                            'Assassin', 
                            "Cleric", 
                            'Station', 
                            "Outpost"]

FstLVLpath = ['01-Tutorial-Mission\\', 
                "02-Spec-Ops\\", 
                '03-Mercenary\\', 
                '04-Militia\\', 
                "05-Rebel\\", 
                '06-Regular\\', 
                "07-Operative\\", 
                '08-Warlock\\', 
                "09-Assassin\\", 
                '10-Cleric\\', 
                "11-Station\\", 
                '12-Outpost\\']

SndLVLcheck = [False,
                True, 
                True, 
                True, 
                True, 
                True, 
                True, 
                False, 
                False, 
                False, 
                False, 
                False]

ComboboxUnitsValues = ['Radial Menu',
                        "(SUPP) Radial Menu", 
                        'Interactions', 
                        "(SUPP) Interactions", 
                        'Bot', 
                        "Commander", 
                        '(SUPP) Commander', 
                        "Observer", 
                        '(SUPP) Observer', 
                        "Gameplay", 
                        'Fire Support', 
                        "Reactions"]

SndLVLpath = ['.01-Radial-Menu\\', 
                ".02-Radial-Menu-SUPPRESSED\\", 
                '.03-Interactions\\', 
                ".04-Interactions-SUPPRESSED\\", 
                '.05-Bot\\', 
                ".06-Commander\\", 
                '.07-Commander-SUPPRESSED\\', 
                ".08-Observer\\", 
                '.09-Observer-SUPPRESSED\\', 
                ".10-Gameplay\\", 
                '.11-Fire-Support\\', 
                ".12-Reactions\\"]

regexSwearPattern = '`.+?`'
Counter = 0

#########################################################

def WindowTitle(winTitle):
    window.title('Steam | ' + winTitle)


def LoadFolder(arg): 
    global fdrOpen
    fdrOpen = fd.askdirectory()
    CategoriesShow()
    pathLVL1(0)
    Thread(pathOrigin, pathLocal, Counter)


def pathLVL1(arg):
    global pathOrigin, pathLocal
    pathOrigin = GitFolderLocation + FstLVLpath[arg]
    pathLocal = fdrOpen + '\\' + FstLVLpath[arg]

def pathLVL2(category, units):
    global pathOrigin, pathLocal
    pathOrigin += str(category+1).zfill(2) + SndLVLpath[units]
    pathLocal += str(category+1).zfill(2) + SndLVLpath[units]


def CategoriesShow():
    comboCategories.grid(row=1, column=4, columnspan = 1, sticky = E)   

def CategoriesFunc(arg):
    textbox.delete('1.0', 'end')
    global CategoryIndex
    CategoryIndex = ComboboxCategoriesValues.index(comboCategories.get())
    
    comboUnits.grid_forget()
    comboUnits.current(0)

    pathLVL1(CategoryIndex)
    if SndLVLcheck[CategoryIndex] == True:
        pathLVL2(CategoryIndex, 0)
        UnitsShow()
        Thread(pathOrigin, pathLocal, Counter)
    else:
        Thread(pathOrigin, pathLocal, Counter)


def UnitsShow():
    comboUnits.grid(row=1, column=6, columnspan = 1, sticky = E)                        

def UnitsFunc(arg):
    textbox.delete('1.0', 'end')
    UnitsIndex = ComboboxUnitsValues.index(comboUnits.get())

    pathLVL1(CategoryIndex)
    pathLVL2(CategoryIndex, UnitsIndex)

    Thread(pathOrigin, pathLocal, Counter)

def OriginalStep(Counter, originalPath, path, step, next_step_set):
    for mdfiles in sorted(listdir(originalPath)):
        titlesMDfile(Counter, path)
        # textbox.insert('1.0', '[olist]')
        print('[olist]')
        fo = io.open(originalPath + mdfiles, "r", encoding='UTF-8')
        for line in fo.readlines():
            step.wait()
            step.clear()

            swFilter = re.sub(regexSwearPattern, SwearFilter, line.rstrip()).split(" ", maxsplit=1)
            TableOriginal = '[*][table][tr][th]' + swFilter[1] + '[/th][/tr]'
            # textbox.insert('1.0', TableOriginal)
            print(TableOriginal)

            next_step_set.set()
        # textbox.insert('1.0', "[/olist]")
        Counter += 1
        fo.close()
        print('[/olist]')

def titlesMDfile(argCounter, path):
    titlefile = io.open(path + 'titles.md', 'r', encoding='UTF-8')
    text = '[hr][/hr][h1]' + titlefile.readlines()[argCounter].split(" ", maxsplit=1)[1]+"[/h1]\n"
    # textbox.insert('1.0', text)
    print(text)
    # titlefile.close()

def LocalStep(localPath, step, next_step_set):
    for mdfiles in sorted(listdir(localPath)):
        if mdfiles != 'titles.md':
            fl = io.open(localPath + mdfiles, "r", encoding='UTF-8')
            for line in fl.readlines():
                step.wait()
                step.clear()

                swFilter = re.sub(regexSwearPattern, SwearFilter, line.rstrip()).split(" ", maxsplit=1)
                if swFilter[1] != "None":
                    TableLocal = '[tr][th][b]' + swFilter[1] + '[/b][/th][/tr][/table]'
                else:
                    TableLocal = '[/table]'
                # textbox.insert('1.0', TableLocal)
                print(TableLocal)

                next_step_set.set()
            fl.close()
        else:
            print('BREAK! Found titles file at ' + path.split(localPath)[1])
            # break
            

def Thread(originalPath, localPath, Counter):
    step1= threading.Event()
    step2= threading.Event()

    # init and start threads
    Thread1 = threading.Thread(target=OriginalStep, args=(Counter, originalPath, localPath, step1, step2))
    Thread2 = threading.Thread(target=LocalStep, args=(localPath, step2, step1))
    Thread1.start()
    Thread2.start()

    step1.set() # initiate the first event

    # join threads to the main thread
    Thread1.join()
    Thread2.join()

def ShortcutSelAll(e):
    e.select(0, Tk.END)

def SwearFilter(Swear):
    return '⚹' * (len(Swear[0]) - 2)


window = Tk()

ButtonsFrame = Frame(window, height = 15)
textFrame = Frame(window, height = 500, width = 800)
ButtonsFrame.grid(row=0, column=0, columnspan = 10, sticky = N) 
textFrame.grid(row=1, column=0, columnspan = 10, sticky = E) 

textbox = Text(textFrame, wrap='word')
scrollbar = Scrollbar(textFrame)
scrollbar['command'] = textbox.yview
textbox['yscrollcommand'] = scrollbar.set
textbox.grid(row=1, column=0, columnspan = 9, sticky = W)
scrollbar.grid(row=1, column=10, sticky = E)

loadBtn = Button(ButtonsFrame, text = 'Load Folder')
loadBtn.bind("<Button-1>", LoadFolder)
loadBtn.grid(row=0, column=0, columnspan = 2, sticky = W)

comboCategories = ttk.Combobox(ButtonsFrame, values= ComboboxCategoriesValues)
comboCategories.current(0)
comboCategories.bind("<<ComboboxSelected>>", CategoriesFunc)

comboUnits = ttk.Combobox(ButtonsFrame, values= ComboboxUnitsValues)
comboUnits.current(0)
comboUnits.bind("<<ComboboxSelected>>", UnitsFunc)



textbox.bind("<Control-Key-a>", ShortcutSelAll)
textbox.bind("<Control-Key-A>", ShortcutSelAll) # In case caps lock is on

window.mainloop()
