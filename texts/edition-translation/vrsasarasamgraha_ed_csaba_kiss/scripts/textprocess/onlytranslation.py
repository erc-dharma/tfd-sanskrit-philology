import re

def onlytranslation(filename):
    chapter = 0
    vsnum = 0
    printverse = False
    colophon = False
    finalverse = ""
    finalnote = ""
    trflag = False
    noteflag = False
    openfile = open(filename, "r")
    for line in openfile:
        if '<TEXT>' in line:
            if '||' in line:
                vsnum += 1
                printverse = True
            else:
                printverse = False
        if '<TRCHAPTER>' in line:
            line = re.sub('.*<TRCHAPTER> *', '', line)
            line = re.sub(' *</TRCHAPTER>.*', '', line[:-1])
            print("\n\n")
            print("------", line.upper(), "------")
        if '<TRSUBCHAPTER>' in line:
            line = re.sub('.*<TRSUBCHAPTER> *', '', line)
            line = re.sub(' *</TRSUBCHAPTER>.*', '', line[:-1])
            print("\n\n\n")
            print("[---", line, "---]")
        if '<TRCOLOPHON>' in line or colophon == True:
            colophon = True
            if '</TRCOLOPHON>' in line:
                colophon = False
            line = re.sub('.*<TRCOLOPHON>', '', line)
            line = re.sub('</TRCOLOPHON>.*', '', line)
            print()
            print(line)
            print()
        if ('<TR>' in line or trflag == True) and colophon == False:
            trflag = True
            if '</TR>' in line:
                trflag = False
            v01 = re.sub('.*<TR>', '', line[:-1])
            v01 = re.sub('</TR>.*', '', v01)
            v01 = re.sub(' +', ' ', v01)
            v01 = re.sub('^ +', '', v01)
            v01 = re.sub('\\\\', '', v01)
            # final white spaces
            v01 = v01.rstrip()
            finalverse = finalverse +  v01 + ' '
            if printverse == True and trflag == False and colophon == False:
                chap_and_vsnum = (str(chapter) + "." + str(vsnum)) 
                print("\n\033[0;33;40m" + chap_and_vsnum)
                print(finalverse)
                finalverse = ""
            if printverse == True and trflag == False and colophon == True:
                print(finalverse)
                colophon = False
                finalverse = ""
                printverse = False
        '''
        # uncomment for notes
        if ('<NOTE>' in line or noteflag == True) and colophon == False:
            noteflag = True
            if '</NOTE>' in line:
                noteflag = False
            v01 = re.sub('.*<NOTE>', '', line[:-1])
            v01 = re.sub('</NOTE>.*', ' ', v01)
            v01 = re.sub(' +', ' ', v01)
            v01 = re.sub('^ +', '', v01)
            v01 = re.sub('\\\\', '', v01)
            v01 = re.sub('Ł', '\033[3m', v01)
            v01 = re.sub('\$', '\033[0m', v01)
            v01 = re.sub('<br/>', '\n', v01)
            # final white spaces
            # v01 = v01.rstrip()
            finalnote = finalnote +  "   " + v01
            if printverse == True and noteflag == False and colophon == False:
                chap_and_vsnum = ("   ---Notes for verse " + str(chapter) + "." + str(vsnum) + "---") 
                print("\n" + chap_and_vsnum)
                print(finalnote)
                print("--------")
                finalnote = ""
        '''
        # OBSOLETE
        if '<NEWCHAPTER/>' in line:
                chapter += 1
                vsnum = 1
        if '<startchapter-n="' in line:
            v01 = re.sub('.*<startchapter-n="', '', line)
            v01 = re.sub('".*', '', v01)
            chapter = int(v01)
            vsnum = 0
            trflag = False
            printverse = False

    openfile.close()

