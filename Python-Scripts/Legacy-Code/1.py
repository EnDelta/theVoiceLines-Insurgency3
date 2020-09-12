# -*- coding: utf-8 -*-
import os, re

pattern = "(.+)C:"

dirtextfile = "H:\\proj\\Music_Menus.txt"
shuffefolder = "D:\\1"

fileopen = open(dirtextfile, "r").readlines()

for j in fileopen:
    regexdone = str(re.findall(pattern, j))
    regexstrcut = regexdone[3:-3]
    regexsplit = regexstrcut.split(';')
    for element in os.scandir(shuffefolder):
        if element.is_file():
            if element.name == regexsplit[0] + '.wav':
                if os.path.exists(shuffefolder + '\\' + regexsplit[1] + '.wav') == True:
                    os.rename(shuffefolder + '\\' + regexsplit[0] + '.wav', shuffefolder + '\\' + 'Dub-' + regexsplit[1] + '.wav')
                    print(shuffefolder + '\\' + regexsplit[0] + '.wav', shuffefolder + '\\' + 'Dub-' + regexsplit[1] + '.wav')

                else:
                    os.rename(shuffefolder + '\\' + regexsplit[0] + '.wav', shuffefolder + '\\' + regexsplit[1] + '.wav')
                    print(shuffefolder + '\\' + regexsplit[0] + '.wav', shuffefolder + '\\' + regexsplit[1] + '.wav')
