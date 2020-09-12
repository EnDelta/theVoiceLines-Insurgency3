import re, math
from tkinter import filedialog as fd

fileName = fd.askopenfilename()
    
regexPattern_start = '(<start>\d+</start>)'
regexPattern_end = '(<end>\d+</end>)'
regexPatternDuration = '(<duration>\d+</duration>)'
regexPatternClipitem = '(<clipitem id=(.+)>)'

#print(math.ceil())

fileopen = open(fileName, 'r')
filecreate = open(fileName[:-4] + 'EDIT.str', 'w+')

regexCompile_start = re.compile(regexPattern_start)
regexCompile_end = re.compile(regexPattern_end)
regexCompileDuration = re.compile(regexPatternDuration)
regexCompileClipitem = re.compile(regexPatternClipitem)

durationCounter1 = 0
durationCounter2 = 0

NameClipItem = ''


for i in fileopen.readlines():
    if regexCompileClipitem.search(i) != None:
        ClitemRegEX = regexCompileClipitem.search(i)
        if str(ClitemRegEX.group())[14:-11] != NameClipItem:
            NameClipItem = str(ClitemRegEX.group())[14:-11]
        
    
    if regexCompileDuration.search(i) != None:
        durationCounter1 += 1
        if math.ceil(durationCounter1/2) != durationCounter2:
            durationCounter2 += 1
            durationRegEx = regexCompileDuration.search(i)
            duration = str(durationRegEx.group())[10:-11]
            

    elif regexCompile_start.search(i) != None:
        startREGex = regexCompile_start.search(i)
        start = str(startREGex.group())[7:-8]
        filecreate.writelines(str(math.ceil(durationCounter1/2)) + '\n')

    
    elif regexCompile_end.search(i) != None:
        endREGex = regexCompile_end.search(i)
        end = str(endREGex.group())[5:-6]
        #print(start + ' - ' + end)

        ZeroFormat = str(int(int(start)/24/60))
        FirstFormat = str(int((int(start)/24) - (60 * int(ZeroFormat))))
        #print("1st - " + str(int(FirstFormat)))
        SecondFormat = str(math.fmod(int(FirstFormat), 24))#[2:5]
        

        ThrirdFormat = str(int(int(end)/24/60))
        FourthFormat = str(int((int(end)/24) - (60 * int(ThrirdFormat))))
        FifthFromat = str(int(math.fmod(int(FourthFormat), 24))) #str(int(end) % 1440)#[2:5]
        print(SecondFormat + ' - ' + FifthFromat)
        filecreate.writelines('''00:{}:{},{} --> 00:{}:{},{}'''.format(ZeroFormat.zfill(2), FirstFormat.zfill(2), SecondFormat.ljust(3, '0'), ThrirdFormat.zfill(2), FourthFormat.zfill(2), FifthFromat.ljust(3, '0')) + '\n\n\n') # .ljust(3)

    
print('done')
fileopen.close()
filecreate.close()

