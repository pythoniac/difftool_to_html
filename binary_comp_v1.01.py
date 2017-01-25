#!/usr/bin/env python3

import sys
import webbrowser
import os
import time
import glob

# GLOBALS:
TEMPLATENAME = 'html_template.htm'
OUTFILENAME = 'result.htm'

def init():
    files = []
    if len(sys.argv) == 3:
        try:
            files.append(sys.argv[1])
            files.append(sys.argv[2])
        except:
            print('\nWe encountered an error while processing: ')
            e = sys.exc_info()[0]
            print('The error message reads: ', e, '\n')
            input('<ok> - EXIT')
            sys.exit(-999)
    else:
        files = 0
        while not files:
            files = fileDialog()
    return files

def fileDialog():
    print()
    files = glob.glob('*.*')
    self = os.path.basename(__file__)
    exclude = [self, OUTFILENAME, TEMPLATENAME]
    files.sort(key=lambda f: os.path.splitext(f)[1])
    for excludeFile in exclude:
        try:
            files.remove(excludeFile)
        except:
            pass
    for index, file in enumerate(files):
        print(index, file)

    first = input('\nfirst file number?')
    second = input('second file number?')
    try:
        first = int(first)
        second = int(second)
    except:
        return 0
    if not first == second and first < len(files) and second < len(files):
        first = files[first]
        second =files[second]
        return [first, second]
    else:
        return 0
    return

def readFiles(files):
    content = []
    for file in files:
        with open(file, 'rb') as f:
            content.append(f.read())
    return content

def chunker(sequence, size):
    return [sequence[pos:pos + size] for pos in range(0, len(sequence), size)]

def compare(data1, data2):
    diffList = []
    chunkCount = 0
    for chunk1, chunk2 in zip(data1, data2):
        if not chunk1 == chunk2:
            elementCount = 0
            diffList.append(chunkCount)
            temp =[]
            for binary1, binary2 in zip(chunk1, chunk2):
                if not binary1 == binary2:
                    temp.append(elementCount)
                elementCount += 1
            diffList.append(temp)
        chunkCount += 1
    return diffList

def generateHTMLdiff(diffList, data1, data2, firstFile):
    diffHTML = []
    strTemp = ''
    strTemp += '<p>'+str(firstFile)+' - is displayed on top</p><br>'
    diffHTML.append(strTemp)
    strTemp = ''
    i = iter(diffList)
    for chunk, elements in zip(i,i):

        #add leading position of chunk
        positionInt = chunk*16
        positionHex = hex(positionInt)
        strTemp += '<p>'
        strTemp += str(positionInt)+' / '+str(positionHex)+': '
        for number in elements:
            strTemp += ' '+str(positionInt+number)
            if not number == elements[-1]:
                strTemp +=','
        strTemp += '</p>'
        diffHTML.append(strTemp)
        strTemp=''

        # add chunk from data1 which differs from data2
        strTemp += '<p>'
        counterEMSP = 0
        for binary in data1[chunk]:
            if counterEMSP and counterEMSP % 4 == 0:
                strTemp += '&emsp; '
            strTemp += str(format(binary, '02X'))+' '
            counterEMSP += 1
        strTemp += '</p>'
        diffHTML.append(strTemp)
        strTemp = ''

        # add chunk from data2 with format highlighting defined in html document template
        strTemp += '<p>'
        counterEMSP = 0
        counterPosition = 0
        for binary in data2[chunk]:
            if counterEMSP and counterEMSP % 4 == 0:
                strTemp += '&emsp; '
            if counterPosition in elements:
                strTemp += '<d>'
                strTemp += str(format(binary, '02X')) + ' '
                strTemp += '</d>'
            else:
                strTemp += str(format(binary, '02X'))+' '
            counterEMSP += 1
            counterPosition +=1
        strTemp += '</p>'
        diffHTML.append(strTemp)
        diffHTML.append('<br>')
        strTemp = ''

    # finally include information on file sizes
    # BUGGY CONCERNING FILE SIZE
    if len(data1) > len(data2):
        strTemp += '<p>file1 > file2 - file2 ends at: '
        strTemp += str(len(data2))+' / '
        strTemp += str(hex(len(data2)))+'</p>'
    elif len(data1) < len(data2):
        strTemp += '<p>file1 < file2 - file1 ends at: '
        strTemp += str(len(data1))+' / '
        strTemp += str(hex(len(data1)))+'</p>'
    else:
        strTemp += '<p>files are of identical size</p>'
    diffHTML.append(strTemp)
    return diffHTML

def injectHTML(diffHTML):
    out = []
    with open(TEMPLATENAME, 'r') as f:
        template = f.readlines()
    for line in template:
        if not line.startswith('~inject_HTML_here~'):
            out.append(line)
        else:
            break
    for line in diffHTML:
        line += '\n'
        out.append(line)
    out.append('</body>\n</html>\n')
    with open(OUTFILENAME, 'w') as f:
        f.writelines(out)

def main():
    files = init()
    content = readFiles(files)
    data1 = chunker(content[0], 16)
    data2 = chunker(content[1], 16)
    diffList = compare(data1, data2)
    diffHTML = generateHTMLdiff(diffList, data1, data2, files[0])
    injectHTML(diffHTML)
    try:
        print('opening webbrowser')
        webbrowser.open('file://'+os.path.realpath(OUTFILENAME))
        print('OK, exiting in 3 seconds')
        time.sleep(3)
    except:
        print('something went wront while trying to open results in webbrowser')
        print('please open',OUTFILENAME,'manually')
        input('EXIT!')

if __name__ == '__main__':
    main()