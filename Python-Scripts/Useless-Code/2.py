import re, math
from tkinter import filedialog as fd

fileName = fd.askopenfilename()
regexPattern_start = '(<start>\d+</start>)'
regexPattern_end = '(<end>\d+</end>)'
regexPatternDuration = '(<duration>\d+</duration>)'
regexPatternClipitem = '(<clipitem id=(.+)>)'

#print(math.ceil())

fileopen = open(fileName, 'r')
filecreate = open(fileName[:-4] + 'EDIT.xml', 'w+')

regexCompile_start = re.compile(regexPattern_start)
regexCompile_end = re.compile(regexPattern_end)
regexCompileDuration = re.compile(regexPatternDuration)
regexCompileClipitem = re.compile(regexPatternClipitem)

durationCounter1 = -1
durationCounter2 = 0

NameClipItem = ''
gap = 0
start = 0
end = 0

for i in fileopen.readlines():
    if regexCompileClipitem.search(i) != None:
        ClitemRegEX = regexCompileClipitem.search(i)
        if str(ClitemRegEX.group())[14:-11] != NameClipItem:
            gap = 48
            NameClipItem = str(ClitemRegEX.group())[14:-11]
    
    if regexCompileDuration.search(i) != None:
        durationCounter1 += 1
        if math.ceil(durationCounter1/2) != durationCounter2:
            durationCounter2 += 1
            durationRegEx = regexCompileDuration.search(i)
            duration = str(durationRegEx.group())[10:-11]

    elif regexCompile_start.search(i) != None:
        startREGex = regexCompile_start.search(i)
        start = end + gap
        result = re.sub(str(startREGex.group())[7:-8], str(start), i)
        filecreate.writelines(result)
        gap = 24
    
    elif regexCompile_end.search(i) != None:
        endREGex = regexCompile_end.search(i)
        end = start + int(duration)
        result = re.sub(str(endREGex.group())[5:-6], str(end), i)
        filecreate.writelines(result)
        gap = 24
           
    else:
        filecreate.writelines(i)
print('done')
fileopen.close()
filecreate.close()

