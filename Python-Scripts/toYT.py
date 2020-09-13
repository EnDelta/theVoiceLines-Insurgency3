# -*- coding: utf-8 -*-

from os import getcwd, listdir
from os.path import split, basename as pathSplit, basename
from tkinter import filedialog as fd
from shutil import copyfile
from re import sub as regexSub

regexSwearPattern = '`.+?`'

'''srtList = ['01-Tutorial.srt',
            '02-Spec-Radial.srt', 
            '03-Spec-RadialSupp.srt', 
            '04-Spec-Interactions.srt', 
            '05-Spec-Interactions-Supp.srt', 
            '06-Spec-Bot.srt', 
            '07-Spec-Commander.srt', 
            '08-Spec-Commander-Supp.srt', 
            '09-Spec-Observer.srt', 
            '10-Spec-Observer-Supp.srt', 
            '11-Spec-Gameplay.srt', 
            '12-Spec-FireSupport.srt', 
            '13-Spec-Reactions.srt', 
            '14-Merc-Radial.srt', 
            '15-Merc-Radial-Supp.srt', 
            '16-Merc-Interactions.srt', 
            '17-Merc-Interactions-Supp.srt', 
            '18-Merc-Bot.srt', 
            '19-Merc-Commander.srt', 
            '20-Merc-Commander-Supp.srt', 
            '21-Merc-Observer.srt', 
            '22-Merc-Observer-Supp.srt', 
            '23-Merc-Gameplay.srt', 
            '24-Merc-Fire_Support.srt', 
            '25-Merc-Reactions.srt', 
            '26-Mil-Radial.srt', 
            '27-Mil-Radial-Supp.srt', 
            '28-Mil-Interactions.srt', 
            '29-Mil-Interactions-Supp.srt', 
            '30-Mil-Bot.srt', 
            '31-Mil-Commander.srt', 
            '32-Mil-Commander-Supp.srt', 
            '33-Mil-Observer.srt', 
            '34-Mil-Observer-Supp.srt', 
            '35-Mil-Gameplay.srt', 
            '36-Mil-Fire_Support.srt', 
            '37-Mil-Reactions.srt', 
            '38-Reb-Radial.srt', 
            '39-Reb-Radial-Supp.srt', 
            '40-Reb-Interactions.srt', 
            '41-Reb-Interactions-Supp.srt', 
            '42-Reb-Bot.srt', 
            '43-Reb-Commander.srt', 
            '44-Reb-Commander-Supp.srt', 
            '45-Reb-Observer.srt', 
            '46-Reb-Observer-Supp.srt', 
            '47-Reb-Gameplay.srt', 
            '48-Reb-Fire_Support.srt', 
            '49-Reb-Reactions.srt', 
            '50-Reg-Radial.srt', 
            '51-Reg-Radial-Supp.srt', 
            '52-Reg-Interactions.srt', 
            '53-Reg-Interactions-Supp.srt', 
            '54-Reg-Bot.srt', 
            '55-Reg-Commander.srt', 
            '56-Reg-Commander-Supp.srt', 
            '57-Reg-Observer.srt', 
            '58-Reg-Observer-Supp.srt', 
            '59-Reg-Gameplay.srt', 
            '60-Reg-Fire_Support.srt', 
            '61-Reg-Reactions.srt', 
            '62-Oper-Radial.srt', 
            '63-Oper-Radial-Supp.srt', 
            '64-Oper-Interactions.srt', 
            '65-Oper-Interactions-Supp.srt', 
            '66-Oper-Bot.srt', 
            '67-Oper-Commander.srt', 
            '68-Oper-Commander-Supp.srt', 
            '69-Oper-Observer.srt', 
            '70-Oper-Observer-Supp.srt', 
            '71-Oper-Gameplay.srt', 
            '72-Oper-Fire_Support.srt', 
            '73-Oper-Reactions.srt', 
            '74-Warlock.srt', 
            '75-Assassin.srt', 
            '76-Cleric.srt', 
            '77-Outpost.srt', 
            '78-Station.srt']

pathToTemplates = getcwd() + '\\Stuff\\YT-subtitles-templates'
print(pathToTemplates)
'''
def SwearFilter(Swear):
    if len(Swear[0])-2 <= 2:
        return '⚹' * (len(Swear[0]) - 2)
    elif len(Swear[0])-2 <= 5:
        return Swear[0][1:2] + '⚹' * (len(Swear[0]) - 3)
    elif len(Swear[0])-2 > 5:
        return Swear[0][1:2] + '⚹' * (len(Swear[0]) - 4) + Swear[0][-2:-1]

fdrOpen = fd.askdirectory()
srtOpen = fd.askopenfilename()

copyfile(srtOpen, pathSplit(srtOpen))
fileopen = open(pathSplit(srtOpen), 'r', encoding='utf-8')
fileread = fileopen.readlines()
fileopen.close
Counter = 0
for mdfiles in sorted(listdir(fdrOpen)):
    if mdfiles != 'titles.md':
        fo = open(fdrOpen + '\\' + mdfiles, "r", encoding='UTF-8')
        for line in fo.readlines():        

            swFilter = regexSub(regexSwearPattern, SwearFilter, line.rstrip()).split(" ", maxsplit=1)
            fileread[(3*(Counter+1))+Counter-1] = swFilter[1] + '\n'
            # print(swFilter)
            Counter += 1
        
        
        fo.close()

fileopen = open(pathSplit(srtOpen), 'w', encoding='utf-8')
fileopen.close()
fileopen = open(pathSplit(srtOpen), 'a', encoding='utf-8')
# print(fileread)
for i in fileread:
    fileopen.writelines(str(i))
    # print(i)
fileopen.close()