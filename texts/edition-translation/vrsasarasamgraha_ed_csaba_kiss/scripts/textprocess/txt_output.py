# only simple text file
import re

def txt_output(filename):
    chapter = 0
    vsnum = 0
    textflag = False
    onflag = False
    openfile = open(filename, "r")
    for line in openfile:
        # not yet used here:
        if '<START/>' in line:
            onflag = True
        if '<STOP/>' in line:
            onflag = False
        if '%' == line[0]:
            textflag = False
        if '<startchapter-n="' in line:
            v01 = re.sub('.*<startchapter-n="', '', line)
            v01 = re.sub('".*', '', v01)
            chapter = int(v01) 
            vsnum = 0
            print("\n\n\n")
            # hemistich = 0
        # OBSOLETE
        if '<NEWCHAPTER/>' in line:
                chapter += 1
                vsnum = 0
                print("\n\n\n")
        if '<TEXT>' in line or textflag == True:
            textflag = True
            if '</TEXT>' in line:
                textflag = False
            if '||' in line:
                vsnum += 1
                chap_and_vsnum = (str(chapter) + "." + str(vsnum) + "||") 
            else:
                chap_and_vsnum = "" 
            v01 = re.sub('.*<TEXT> ?', '', line[:-1])
            v01 = re.sub('\|\*', '|', v01)
            v01 = re.sub('\-', '|', v01)
            v01 = re.sub('</TEXT>.*', chap_and_vsnum, v01)
            v01 = re.sub('{ }', " ", v01)
            v01 = re.sub('<COLOPHON>', "\n||", v01)
            v01 = re.sub('</COLOPHON>', "||", v01)
            v01 = re.sub('<uvaca>', '', v01)
            v01 = re.sub('</uvaca>', '', v01)
            v01 = re.sub('<MNTR>', '', v01)
            v01 = re.sub('</MNTR>', '', v01)
            print(v01)
        if '<SUBCHAPTER>' in line:
            v01 = re.sub('<SUBCHAPTER>', '\n---- ', line)
            v01 = re.sub('</SUBCHAPTER>', ' ----', v01)
            print(v01)
        '''    
        if '<APP>' in line:
            v01 = re.sub('<APP> ?', '     ', line[:-1])
            v01 = re.sub('</APP>', '', v01)
            v01 = re.sub('{ }', " ", v01)
            v01 = re.sub('\\\\va', str(vsnum) + "a", v01)
            v01 = re.sub('\\\\vb', str(vsnum) + "b", v01)
            v01 = re.sub('\\\\vc', str(vsnum) + "c", v01)
            v01 = re.sub('\\\\vd', str(vsnum) + "d", v01)
            v01 = re.sub('\\\\vo', str(vsnum), v01)
            v01 = re.sub('\\\\oo', "¤", v01)
            v01 = re.sub('\\\\lem', "]", v01)
            v01 = re.sub('\\\\Ja', "msJa", v01)
            v01 = re.sub('\\\\om\\\\?', "omitted in", v01)
            print(v01)
    '''        
    openfile.close()

