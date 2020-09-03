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

NameForNums = []
StartTrack = []
MidTrack = []
EndTrack = []

for i in fileopen.readlines():
    if regexCompileClipitem.search(i) != None:
        ClitemRegEX = regexCompileClipitem.search(i)
        NameForNums.append(str(ClitemRegEX.group())[-10:-8])
        #print(NameForNums)
        if str(ClitemRegEX.group())[14:-11] != NameClipItem:
            gap = 48
            NameClipItem = str(ClitemRegEX.group())[14:-11]
            #print(NameForNums)
    
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
        
        StartTrack.append(eval('''[{}, {}]'''.format(start - 24, start)))
        MidTrack.append(eval('''[{}, {}]'''.format(start, end)))
        EndTrack.append(eval('''[{}, {}]'''.format(end, end + 24)))
           
    else:
        filecreate.writelines(i)


print('done - 1')
fileopen.close()
filecreate.close()

filecreate = open(fileName[:-4] + '_cut.xml', 'w+')

Track = []
Track.append(EndTrack)
Track.append(MidTrack)
Track.append(StartTrack)

NumsCount = 0
NumsCountDict = {}
print(len(NameForNums))

for i in range(len(Track)):

    filecreate.write('                <track>' + '\n')
    
    for j in range(len(Track[i])):
        
        try:
            if NumsCountDict[NameForNums[j]] != 0:
                NumsCountDict[NameForNums[j]] += 2
            else:
                NumsCountDict[NameForNums[j]] += 3
            NumsCount = NumsCountDict[NameForNums[j]]

        except KeyError:
            NumsCountDict[NameForNums[j]] = 0
            NumsCount = 0
        #print(int((NumsCount-1)/2))"""
    
        filecreate.write('''                    <clipitem id="[{0}-{0}].png {1}">'''.format(NameForNums[j], NumsCount) + '\n')
        filecreate.write('''                        <name>[{0}-{0}].png</name>'''.format(NameForNums[j]) + '\n')
        filecreate.write('''                        <duration>1440001</duration>''' + '\n')
        filecreate.write('''                        <rate>''' + '\n')
        filecreate.write('''                            <timebase>24</timebase>''' + '\n')
        filecreate.write('''                            <ntsc>FALSE</ntsc>''' + '\n')
        filecreate.write('''                        </rate>''' + '\n')
        filecreate.write('''                        <start>{0}</start>'''.format(Track[i][j][0]) + '\n')
            #print(Track[i][j][0])
        filecreate.write('''                        <end>{0}</end>'''.format(Track[i][j][1]) + '\n')
        filecreate.write('''                        <enabled>TRUE</enabled>''' + '\n')
        filecreate.write('''                        <in></in>''' + '\n')
        filecreate.write('''                        <out></out>''' + '\n')
        if NumsCount == 0:
            filecreate.write('''                        <file id="[{0}-{0}].png 2">'''.format(NameForNums[j]) + '\n')
            filecreate.write('''                            <duration>1</duration>''' + '\n')
            filecreate.write('''                            <rate>''' + '\n')
            filecreate.write('''                                <timebase>24</timebase>''' + '\n')
            filecreate.write('''                                <ntsc>FALSE</ntsc>''' + '\n')
            filecreate.write('''                            </rate>''' + '\n')
            filecreate.write('''                            <name>[{0}-{0}].png</name>'''.format(NameForNums[j]) + '\n')
            filecreate.write('''                            <pathurl>file://localhost/D:/proj/theVLproj/@1nums/[{0}-{0}].png</pathurl>'''.format(NameForNums[j]) + '\n')
            filecreate.write('''                            <timecode>''' + '\n')
            filecreate.write('''                                <string>00:00:00:00</string>''' + '\n')
            filecreate.write('''                                <displayformat>NDF</displayformat>''' + '\n')
            filecreate.write('''                                <rate>''' + '\n')
            filecreate.write('''                                    <timebase>24</timebase>''' + '\n')
            filecreate.write('''                                    <ntsc>FALSE</ntsc>''' + '\n')
            filecreate.write('''                                </rate>''' + '\n')
            filecreate.write('''                            </timecode>''' + '\n')
            filecreate.write('''                            <media>''' + '\n')
            filecreate.write('''                                <video>''' + '\n')
            filecreate.write('''                                    <duration>1</duration>''' + '\n')
            filecreate.write('''                                    <samplecharacteristics>''' + '\n')
            filecreate.write('''                                        <width>1920</width>''' + '\n')
            filecreate.write('''                                        <height>1080</height>''' + '\n')
            filecreate.write('''                                    </samplecharacteristics>''' + '\n')
            filecreate.write('''                                </video>''' + '\n')
            filecreate.write('''                            </media>''' + '\n')
            filecreate.write('''                        </file>''' + '\n')
        else:
            filecreate.write('''                        <file id="[{0}-{0}].png 2"/>'''.format(NameForNums[j]) + '\n')
        filecreate.write('''                        <compositemode>normal</compositemode>''' + '\n')
        filecreate.write('''                    </clipitem>''' + '\n')

    filecreate.write('                </track>' + '\n')

print('DONE - 2')
filecreate.close()
