'''
making the index
Usage:
    textprocess.py -index filename.xml | sort | less
'''
import re

def index(filename):
    chapter = 0
    vsnum = 1
    textflag = False
    onflag = False
    afterendofsloka = False
    openfile = open(filename, "r")
    for line in openfile:
        # not yet used here:
        if '<START/>' in line:
            onflag = True
        if '<STOP/>' in line:
            onflag = False
        if '<startchapter-n="' in line:
            v01 = re.sub('.*<startchapter-n="', '', line)
            v01 = re.sub('".*', '', v01)
            chapter = int(v01) 
            vsnum = 1
        if '<TEXT>' in line or textflag == True:
            textflag = True
            afterendofsloka = False
            if '</TEXT>' in line:
                textflag = False
            if '||' in line:
                afterendofsloka = True 
                vsnum += 1
        if 'index_' in line:
            print(line.strip(), str(chapter) + "." + str(vsnum-afterendofsloka))
    openfile.close()

