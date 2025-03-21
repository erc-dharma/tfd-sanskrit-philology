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


