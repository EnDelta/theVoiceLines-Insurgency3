# -*- coding: utf-8 -*-
import os, re

#pattern = 'Gun(.+)[\t]C:'
pattern = "[\t]Gun(.+)[\t]C:"

dirfile = "H:\\proj\\8SupGunship\\VO_Gunship.txt"
folder = "H:\\proj\\output"

fileopen = open(dirfile, "r").readlines()


for k, j in zip(os.listdir(folder), fileopen):
    regexdone = str(re.findall(pattern, j))
    print(k, 'Gun' + regexdone[2:-2] + '.wav')
    if os.path.exists(folder + '\\' + 'Gun' + regexdone[2:-2] + '.wav') == True:
        os.rename(folder + '\\' + k, folder + '\\' + 'Dub-' + 'Gun' + regexdone[2:-2] + '.wav')
        print(folder + '\\' + 'Dub-' + 'Gun' + regexdone[2:-2] + '.wav')

    #elif os.path.exists(folder + '\\' + 'Dub-' + 'Gun' + regexdone[2:-2] + '.wav') == True:
    #    os.rename(folder + '\\' + k, folder + '\\' + 'Dub2-' + 'Gun' + regexdone[2:-2] + '.wav')

    #elif os.path.exists(folder + '\\' + 'Dub2-' + 'Gun' + regexdone[2:-2] + '.wav') == True:
    #    os.rename(folder + '\\' + k, folder + '\\' + 'Dub3-' + 'Gun' + regexdone[2:-2] + '.wav')

    else:
        os.rename(folder + '\\' + k, folder + '\\' + 'Gun' + regexdone[2:-2] + '.wav')