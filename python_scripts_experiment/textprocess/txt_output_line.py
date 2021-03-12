import re 

# only simple text LINE 
def txt_output_line(line, textflag):
    chapter = 0
    vsnum = 0
    #textflag = False
    # this was problematic:
    #if '%' == line[0]:
     #   textflag = False
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
        v01 = re.sub('<TEXT> ?', '', line[:-1])
        v01 = re.sub('\|\*', '|', v01)
        v01 = re.sub('\\\\-', '', v01)
        v01 = re.sub('</TEXT>.*', '', v01)
        v01 = re.sub('{ }', " ", v01)
        v01 = re.sub('<COLOPHON>', " ", v01)
        v01 = re.sub('</COLOPHON>', " ", v01)
        v01 = re.sub('<uvaca>', '', v01)
        v01 = re.sub('</uvaca>', '', v01)
        return v01 
    if '<SUBCHAPTER>' in line:
        v01 = re.sub('<SUBCHAPTER>', '\n---- ', line)
        v01 = re.sub('</SUBCHAPTER>', ' ----', v01)
        return v01 
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


