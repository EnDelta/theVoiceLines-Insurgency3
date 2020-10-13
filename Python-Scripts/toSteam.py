# -*- coding: utf-8 -*-

from os import getcwd, listdir
from os.path import split as pathSplit
from re import sub as regexSub
from io import open as oPen
from tkinter import filedialog as fd
from tkinter import Tk, Text, N, E, S, W, END
from tkinter.ttk import Frame, Scrollbar, Button, Combobox, Entry
from threading import Thread, Event

########################## Cfg ##########################

GitFolderLocation = getcwd()[:-14] + 'VL-Original\\' # --- J:\\github\\theVoiceLines-Insurgency3\\VL-Original\\

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

SubLVLvalues = [False,
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

regexSwearPattern = '''`.+?`'''

#########################################################

def WindowTitle(winTitle):
    window.title('Steam | ' + winTitle)

def LoadFolder(arg): 
    global fdrOpen

    fdrOpen = fd.askdirectory()
    WindowTitle(pathSplit(fdrOpen)[1])
    CategoriesShow()
    pathLVL1(0)
    TextInsertion(pathOrigin, pathLocal, 0)
    TextInsertion(pathOrigin, pathLocal, 0)
    FilesShow(pathOrigin)
            

def pathLVL1(arg):
    global pathOrigin, pathLocal

    pathOrigin = GitFolderLocation + FstLVLpath[arg]
    pathLocal = fdrOpen + '\\' + FstLVLpath[arg]
    

def pathLVL2(category, units):
    global pathOrigin, pathLocal

    pathOrigin += str(category+1).zfill(2) + SndLVLpath[units]
    pathLocal += str(category+1).zfill(2) + SndLVLpath[units]
    


def CategoriesShow():
    comboCategories.grid(row=1, column=0, columnspan = 2, sticky = W+E)
    comboCategories.current(0)   

def CategoriesFunc(arg):
    textbox.delete('1.0', 'end')
    global CategoryIndex

    CategoryIndex = ComboboxCategoriesValues.index(comboCategories.get())
    
    comboUnits.grid_forget()
    comboUnits.current(0)

    pathLVL1(CategoryIndex)
    
    if SubLVLvalues[CategoryIndex] == True:
        pathLVL2(CategoryIndex, 0)
        UnitsShow()
        TextInsertion(pathOrigin, pathLocal, 0)
    else:
        TextInsertion(pathOrigin, pathLocal, 0)  
    FilesShow(pathOrigin)

def UnitsShow():
    comboUnits.grid(row=1, column=3, columnspan = 8, sticky = W+E)
    comboUnits.current(0)                        

def UnitsFunc(arg):
    textbox.delete('1.0', 'end')
    UnitsIndex = ComboboxUnitsValues.index(comboUnits.get())

    pathLVL1(CategoryIndex)
    pathLVL2(CategoryIndex, UnitsIndex)
    FilesShow(pathOrigin)
    TextInsertion(pathOrigin, pathLocal, 0)

def FilesShow(arg):
    comboFile.grid_forget
    comboFile['values'] = sorted(listdir(arg))
    comboFile.grid(row=1, column=13, columnspan = 11, sticky = W+E)
    comboFile.current(0)


def FilesFunc(arg):
    textbox.delete('1.0', 'end')
    global FilesIndex

    FilesIndex = (sorted(listdir(pathOrigin))).index(comboFile.get())
    TextInsertion(pathOrigin, pathLocal, FilesIndex)



def OriginalStep(originalPath, Index, step, next_step_set):
    global ostepSWfilter

    fo = oPen(originalPath + sorted(listdir(originalPath))[Index], 'r', encoding='UTF-8')
    
    tempf.write('[olist]')

    for line in fo.readlines():
        step.wait()
        step.clear()

        swFilter = regexSub(regexSwearPattern, SwearFilter, line.rstrip()).split(" ", maxsplit=1)
        
        try:
            # TableOriginal = '\n[*][code][code][b] ▫ ' + swFilter[1] + '[/b][/code]'
            # TableOriginal = '\n[*][table][tr][th][code][b] ▫ ' + swFilter[1] + '[/b][/code]'
            # TableOriginal = '\n[*][code][table][tr][th][b] ▫ ' + swFilter[1] + '[/b][/th][/tr]'
            TableOriginal = '\n[*][code][h3] ▫ ' + swFilter[1] + '[/h3]'

            ostepSWfilter = swFilter[1]
            
            tempf.write(str(TableOriginal))
            
        except:
            tempf.write('\nerror at: ' + originalPath + sorted(listdir(originalPath))[Index] + ' -|- ' + line.rstrip() + '\n')
        next_step_set.set()    
    fo.close()
    

def LocalStep(localPath, Index, step, next_step_set):
    try:
        sortedListdir = sorted(listdir(localPath))[Index]
        if sortedListdir != 'titles.md':
            fl = oPen(localPath + sortedListdir, "r", encoding='UTF-8')
            for line in fl.readlines():
                step.wait()
                step.clear()

                swFilter = regexSub(regexSwearPattern, SwearFilter, line.rstrip()).split(" ", maxsplit=1)
                try:
                    if swFilter[1] != ostepSWfilter:
                        # TableLocal = '[code][b] ▫ ' + swFilter[1] + '[/b][/code][/code]\n'
                        # TableLocal = '[code][b] ▫ ' + swFilter[1] + '[/b][/code][/th][/tr][/table]\n'
                        # TableLocal = '[tr][th][b] ▫ ' + swFilter[1] + '[/b][/th][/tr][/table][/code]\n'
                        TableLocal = '[hr][/hr][h3] ▫ [b]' + swFilter[1] + '[/b][/h3][/code]\n'
                    else:
                        # TableLocal = '[/code]\n'
                        # TableLocal = '[/th][/tr][/table]\n'
                        # TableLocal = '[/table][/code]\n'
                        TableLocal = '[/code]\n'

                    tempf.write(str(TableLocal))
                except:
                    tempf.write('\nerror at: ' + localPath + sortedListdir + ' -|- ' + line.rstrip() + '\n')                
                    
                next_step_set.set()
            fl.close()
        else:
            print('BREAK! Found titles file at ' + pathSplit(localPath)[1])
            # break
    except FileNotFoundError:
        quit(1)

# def titlesMDfile(argCounter, path):
#    titlefile = oPen(path + 'titles.md', 'r', encoding='UTF-8')
#    text = '[hr][/hr][h1]' + titlefile.readlines()[argCounter].split(" ", maxsplit=1)[1]+"[/h1]\n"
#    # textbox.insert('1.end', text)
#    # print(text)
#    titlefile.close()

def TextInsertion(originalPath, localPath, Index):
    global tempf

    tempf = oPen('tmp.txt', 'w', encoding='UTF-8')
    tempf.close
    tempf = oPen('tmp.txt', 'a', encoding='UTF-8')

    step1 = Event()
    step2 = Event()
    
    Thread1 = Thread(target=OriginalStep, args=(originalPath, Index, step1, step2))
    Thread2 = Thread(target=LocalStep, args=(localPath, Index, step2, step1))
    Thread1.start()
    Thread2.start()

    step1.set()
    Thread1.join()
    Thread2.join()

    tempf.write('[/olist]')

    tempf.close
    textbox.delete('1.0', 'end')
    tempf = oPen('tmp.txt', 'r', encoding='UTF-8')
    textbox.insert('0.end', tempf.read())
    tempf.close()  

def SwearFilter(Swear):
    return '⚹' * (len(Swear[0]) - 2)

window = Tk()
# window.geometry("720x576")

textbox = Text(window)
scrollbar = Scrollbar(window)
scrollbar['command'] = textbox.yview
textbox['yscrollcommand'] = scrollbar.set
textbox.grid(row=4, column=0, columnspan = 24, rowspan=18, sticky = S+N+E+W)
scrollbar.grid(row=4, column=25, rowspan=18, sticky = N+E+S+W)

TitleText = Entry(window)
TitleText.grid(row=0, column=1, columnspan = 22, sticky = W+E)

loadBtn = Button(window, text = 'Load Folder')
loadBtn.bind("<Button-1>", LoadFolder)
loadBtn.grid(row=0, column=23, columnspan = 2, sticky = W+N)

comboCategories = Combobox(window, values= ComboboxCategoriesValues)
comboCategories.bind("<<ComboboxSelected>>", CategoriesFunc)

comboUnits = Combobox(window, values= ComboboxUnitsValues)
comboUnits.bind("<<ComboboxSelected>>", UnitsFunc)

comboFile = Combobox(window)
comboFile.bind("<<ComboboxSelected>>", FilesFunc)


textbox.bind("<Control-Key-a>", None)
textbox.bind("<Control-Key-A>", None) # In case caps lock is on

WindowTitle('Select the language folder in "VL-Translations"')
window.mainloop()