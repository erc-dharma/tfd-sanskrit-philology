import re

class bcolors:
	IT = '\033[94m'
	YELLOW = '\033[93m'
	WHITE = '\033[0m'
	TR = '\033[92m'
	'''
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	'''

def translation(filename):
    onflag = False
    chapter = 0
    vsnum = 0
    textflag = False
    trflag = False
    openfile = open(filename, "r")
    for line in openfile:
        if '<START/>' in line:
            onflag = True
        if '<STOP/>' in line:
            onflag = False
        #chap_and_vsnum = (str(chapter) + "." + str(vsnum)) 
        if ('<TR>' in line or trflag == True) and onflag == True:
            trflag = True
            if '</TR>' in line:
                trflag = False
            v01 = re.sub('.*<TR>', '', line[:-1])
            v01 = re.sub('</TR>.*', ' ', v01)
            v01 = re.sub('^ *', '', v01)
            # final white spaces
            v01 = v01.rstrip()
            if '<TR>' in line or trflag == True: 
                if '</TR>' in line:
                    trflag == False
                print("    ", bcolors.TR, v01, bcolors.WHITE)
            else:
                print(bcolors.TR, v01, bcolors.WHITE)
        if '<startchapter-n="' in line and onflag == True:
            v01 = re.sub('.*<startchapter-n="', '', line)
            v01 = re.sub('".*', '', v01)
            chapter = int(v01) 
        # OBSOLETE
        if '<NEWCHAPTER/>' in line:
                chapter += 1
                vsnum = 0
        if ('<TEXT>' in line or textflag == True) and onflag == True:
            textflag = True
            if '</TEXT>' in line:
                textflag = False
            if '||' in line:
                vsnum += 1
                chap_and_vsnum = (str(chapter) + "." + str(vsnum) + "||") 
            else:
                chap_and_vsnum = "" 
            v01 = re.sub('<TEXT> ?', '', line[:-1])
            v01 = re.sub('\|\*', '|', v01)
            v01 = re.sub('\-', '|', v01)
            v01 = re.sub('</TEXT>.*', chap_and_vsnum, v01)
            v01 = re.sub('{ }', " ", v01)
            v01 = re.sub('<COLOPHON>', "\n||", v01)
            v01 = re.sub('</COLOPHON>', "||\n", v01)
            v01 = re.sub('<uvaca>', '', v01)
            v01 = re.sub('</uvaca>', '', v01)
            print(v01)
        '''if '<TEXT>' in line:
            if '||' in line:
                vsnum += 1
        '''        
    openfile.close()



