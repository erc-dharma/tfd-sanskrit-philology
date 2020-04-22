import re
from textprocess import velthview_with_rm

def tex_dn_output(filename):
    chapter = 0
    vsnum = 0
    onflag = False
    textflag = False
    appflag = False
    paralflag = False
    anustubh = True
    proseflag = False
    pvarflag = False
    hemistich = 0
    just_uvaca = False
    romanflag = False
    print("\\renewcommand{\\rmapp}[1]{}\\renewcommand{\\dnapp}[1]{#1}")
    print("\\renewcommand{\\mntr}[1]{\mntrdn{#1}}")
    print("\\fejno=0\\versno=0")
    openfile = open(filename, "r")
    for line in openfile:
        if '<START/>' in line:
            onflag = True
        if '<STOP/>' in line:
            onflag = False
        lin, romanflag = velthview_with_rm.velthview_with_rm(line, romanflag)
        if '<NOTANUSTUBH/>' in lin:
            print("\n\\nemsloka")
            anustubh = False 
            hemistich = 0
        if '<ANUSTUBH/>' in lin:
            print("\n\\dnvers")
            anustubh = True 
            hemistich = 0
        if '<LONGVERSELINES/>' in line:
            print("\n\\nemslokalong\n")
        if '<NORMALVERSELINES/>' in line:
            print("\n\\nemslokanormal\n")
        if '<LITEM/>' in line:
            print("\n")
        if '<SETVSNUM' in line:
            v01 = re.sub('.*<SETVSNUM="', '', line)
            v01 = re.sub('".*', '', v01)
            vsnum = int(v01) - 1
            print("\\versno=" + str(vsnum))
        if '<NEWCHAPTER/>' in lin and onflag == True:
            if chapter > 0:
                #print("\\bekveg\\szamveg\\vfill\\phpspagebreak\\ujfej\\szam\\bek\n")
                v01 = "\nBACKSLASHugrasBACKSLASHujfej"
            else:
                v01 = "BACKSLASHujfejBACKSLASHszamBACKSLASHbek\n"
            v01 = re.sub('BACKSLASH', '\\\\', v01)
            print(v01)
            chapter += 1
            vsnum = 0
        if '<PROSE>' in lin and onflag == True:
            proseflag = True
            print("\n\\prose ", end="")
        if '</PROSE>' in lin:
            proseflag = False
            print("\n\\vers")
        if ('<TEXT>' in lin or textflag == True) and onflag == True:
            textflag = True
            if '</TEXT>' in line:
                textflag = False
            if '||' in lin and anustubh == True and proseflag == False:
                outputline = re.sub('\|\|', ' \\\\vegdnBACKSLASHdontdisplaylinenum', lin)
                hemistich = 0
            elif '||' in lin and anustubh == False and proseflag == False:
                outputline = re.sub('\|\|', ' \\\\vegdnBACKSLASHdontdisplaylinenum', lin)
                outputline = "\n\\dnnemslokad " + outputline + "\n" 
                hemistich = 0
            elif '|*' in line and proseflag == False:
                outputline = re.sub('\|\*', '{\\\\dandabdn}BACKSLASHdontdisplaylinenum ', lin)
                just_uvaca = True
            elif '|' in line and hemistich == 0 and anustubh == True and proseflag == False:
                if just_uvaca == False:
                    outputline = re.sub('\|', '{\\\\dandabdn} BACKSLASHdontdisplaylinenum', lin)
                else:
                    outputline = re.sub('\|', '{\\\\dandadn} BACKSLASHdontdisplaylinenum', lin)
                hemistich = 1 
                just_uvaca = False
            elif '|' not in lin and hemistich == 0 and anustubh == False and proseflag == False:
                if just_uvaca == False:
                    # no indent
                    outputline = "\nBACKSLASHujversBACKSLASHdnnemsloka " + lin + "BACKSLASHdontdisplaylinenum " 
                else:
                    outputline = "\nBACKSLASHdnnemsloka " + lin + "BACKSLASHdontdisplaylinenum " 
                hemistich = 1
                just_uvaca = False
            elif '|' not in lin and hemistich == 2 and anustubh == False and proseflag == False:
                # no indent
                outputline = "\nBACKSLASHdnnemslokac " + lin + "BACKSLASHdontdisplaylinenum "
                hemistich = hemistich + 1
            elif '|' in lin and anustubh == False and proseflag == False:
                outputline = re.sub('\|', ' \\\\dandadnBACKSLASHdontdisplaylinenum', lin)
                outputline = "\nBACKSLASHdnnemslokab " + outputline
                hemistich = hemistich + 1 
            elif '|' in lin and hemistich > 0 and anustubh == True and proseflag == False:
                outputline = re.sub('\|', '{\\\\dandadn}BACKSLASHdontdisplaylinenum ', lin)
                hemistich = hemistich + 1 
            else:
                outputline = lin
            # simple substitutions
            if proseflag == False:
                v01 = re.sub('<TEXT> ?', '\n{\\\\dn ', outputline[:-1])
            if proseflag == True:
                v01 = re.sub('<TEXT> ?', '{\\\\dn ', outputline[:-1])
            # to eliminate spaces in prose passages    
            if proseflag == False:
                v01 = re.sub('</TEXT>.*', '}', v01)
            else:
                v01 = re.sub('</TEXT>.*', '}%', v01)
            v01 = re.sub('<MNTR>', '\\\\mntr{', v01)
            v01 = re.sub('</MNTR>', '}', v01)
            v01 = re.sub('<LITEM/>', '', v01)
            v01 = re.sub('{ }', "", v01)
            v01 = re.sub('<COLOPHON>', "\n\\ugras\n\\\\begin{center}\n{||} ", v01)
            v01 = re.sub('</COLOPHON>', "{||}\n\\\\end{center}\\\\vers", v01)
            v01 = re.sub('<PROSE> ?', '', v01)
            v01 = re.sub('</PROSE>', '', v01)
            v01 = re.sub('<uvaca>', '', v01)
            v01 = re.sub('</uvaca>', '', v01)
            v01 = re.sub('BACKSLASH', '\\\\', v01)
            print(v01)
        if ('<APP>' in lin or appflag == True) and onflag == True:
            appflag = True
            v01 = re.sub('<APP> ?', '    \\\\var{{\dn ', lin[:-1])
            if '</APP>' in lin:
                appflag = False
            v01 = re.sub('</APP>', '}}', v01)
            v01 = re.sub('{ }', "", v01)
            v01 = re.sub('°', "@", v01)
            v01 = re.sub('<LEM>', '', v01)
            v01 = re.sub('</LEM>', '\lem ', v01)
            v01 = re.sub('<UNCL>', '\\\\uncl{', v01)
            v01 = re.sub('</UNCL>', '}', v01)
            v01 = re.sub('<MNTR>', '\\\\mntr{', v01)
            v01 = re.sub('</MNTR>', '}', v01)
            v01 = re.sub('<EYESKIPTO>', '}\\\\eyeskipto{', v01)
            v01 = re.sub('</EYESKIPTO>', '}{\dn', v01)
            v01 = re.sub('\\Ł', '} ', v01)
            v01 = re.sub('\\$', ' {\dn ', v01)
            v01 = re.sub('\\;', '{\\\\normalfont\\\\thinspace ;}', v01)
            v01 = re.sub('\*', '{\il}', v01)
            v01 = re.sub('×', '{\lost}', v01)
            v01 = re.sub('{\\\\lost}\\\\csi', '{\\\\csi{}\\\\lost}', v01)
            v01 = re.sub('<ja>', ' ', v01)
            v01 = re.sub('</ja>', ' ', v01)
            print(v01)
        if ('<PARAL>' in lin or paralflag == True) and onflag == True:
            paralflag = True
            if '</PARAL>' in lin:
                paralflag = False
            v01 = re.sub('{ }', "", lin[:-1])
            v01 = re.sub('°', "@", v01)
            v01 = re.sub('<LEM>', '', v01)
            v01 = re.sub('</LEM>', '\lem ', v01)
            v01 = re.sub('<PARAL>', '    \\\\paral{{\dn', v01)
            v01 = re.sub('</PARAL>', '}}', v01)
            v01 = re.sub('{ }', " ", v01)
            v01 = re.sub('\\Ł', '}', v01)
            v01 = re.sub('\\$', '{\dn ', v01)
            print(v01)
        if ('<PVAR>' in lin or pvarflag == True) and onflag == True:
            pvarflag = True
            if '</PVAR>' in lin:
                pvarflag = False
            v01 = re.sub('{ }', "", lin)
            v01 = re.sub('<PVAR>', '    \\\\prosevar{{\dn ', v01[:-1])
            v01 = re.sub('</PVAR>', '}}', v01)
            v01 = re.sub('<LEM>', '', v01)
            v01 = re.sub('</LEM>', '\lem ', v01)
            v01 = re.sub('\\Ł', '} ', v01)
            v01 = re.sub('\\$', ' {\dn ', v01)
            v01 = re.sub('\\;', '{\\\\normalfont\\\\thinspace ;}', v01)
            v01 = re.sub('\*', '{\il}', v01)
            v01 = re.sub('×', '{\lost}', v01)
            v01 = re.sub('{\\\\lost}\\\\csi', '{\\\\csi{}\\\\lost}', v01)
            print(v01)
        if '<SUBCHAPTER>' in line and onflag == True:
            v01 = re.sub('<SUBCHAPTER>', '\n\n\\\\alalfejezet{\dn ', lin[:-1])
            v01 = re.sub('</SUBCHAPTER>', '}', v01)
            v01 = re.sub('{ }', "", v01)
            print(v01)
        if '<CHAPTER>' in line and onflag == True:
            v01 = re.sub('<CHAPTER>', '\n\n\\\\alfejezetdn{{\dn\Large\dnnum ', lin[:-1])
            v01 = re.sub('</CHAPTER>', '}}', v01)
            v01 = re.sub('{ }', "", v01)
            print(v01, end="")
        if '<TITLE>' in line and onflag == True:
            v01 = re.sub('<TITLE>', '\\\\begin{center}{{\dn\Huge  ', lin[:-1])
            v01 = re.sub('</TITLE>', '}}\\\\end{center}', v01)
            v01 = re.sub('{ }', "", v01)
            print(v01, end="")
        if '<TAMIL>' in line and onflag == True:
            v01 = re.sub('<TAMIL>', '', line[:-1])
            v01 = re.sub('</TAMIL>', '', v01)
            v01 = tamil.txt2unicode.diacritic2unicode(v01)
            print('{\\tamilfont ', v01, '}\n')
    openfile.close()


