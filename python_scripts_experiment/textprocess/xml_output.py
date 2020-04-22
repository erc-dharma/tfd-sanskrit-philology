import re
from textprocess import xml_substitutions

def xml_output(filename, apparatus_type):
    chapter = 0
    vsnum = 0
    textflag = False
    appflag = False
    paralflag = False
    anustubh = True
    hemistich = 0
    proseflag = False
    pvarflag = False
    trflag = False
    noteflag = False
    onflag = False
    note = ''
    pada = '<padaab>'
    # header
    print('<?xml version="1.0" encoding="UTF-8"?>')
    # closed apparatus
    if apparatus_type == 1:
        print('<?xml-stylesheet type="text/xsl" href="vrsa_critical01.xsl"?>\n<body>')
        print('<a href="output02.xml">Make all apparatus entries and the translation visible</a><br/><br/>')
    # opened apparatus
    if apparatus_type == 2:
        print('<?xml-stylesheet type="text/xsl" href="vrsa_critical02.xsl"?>\n<body>')
        print('<a href="output01.xml">Make all apparatus entries and the translation invisible</a><br/><br/>')
    # with no apparatus
    if apparatus_type == 3:
        print('<?xml-stylesheet type="text/xsl" href="vrsa_critical03.xsl"?>\n<body>')
    if apparatus_type == 4:
        print('<?xml-stylesheet type="text/xsl" href="vrsa_critical04.xsl"?>\n<body>')
    openfile = open(filename, "r")
    for line in openfile:
        if '<START/>' in line:
            onflag = True
        if '<STOP/>' in line:
            print("</body>")        
            onflag = False
            quit()
        if '<NOTANUSTUBH/>' in line:
            anustubh = False 
            proseflag = False
            hemistich = 0
        if '<ANUSTUBH/>' in line:
            anustubh = True
            proseflag = False
            #hemistich = 0
        if '<PROSE>' in line:
            proseflag = True
            anustubh = False
            print("<PROSE>")
        if '</PROSE>' in line:
            proseflag = False
            anustubh = False
            print("</PROSE>")
        if '<NEWCHAPTER/>' in line:
            chapter += 1
            #if text doesn't start with verse 1
            #vsnum = 83
            vsnum = 0
            print('<!-- chapter', chapter, '-->')
            print('<NEWCHAPTER/>')
        if '<SETVSNUM' in line:
            v01 = re.sub('.*<SETVSNUM="', '', line)
            v01 = re.sub('".*', '', v01)
            vsnum = int(v01) - 1
        # if it is the main text:        
        if '<TEXT>' in line or textflag == True:
            textflag = True
            uvacaflag = 0
            if '</TEXT>' in line:
                textflag = False
            # check if this is the end of a verse
            if '||' in line and proseflag == False:
                chap_and_vsnum = ("<vsnum>" + str(chapter) + "." + str(vsnum) + "</vsnum>||") 
            else:
                chap_and_vsnum = "" 
            if '||' in line and anustubh == True and hemistich == 1 and proseflag == False:
                outputline = re.sub('\|\|', '||' + chap_and_vsnum, line)
                outputline = re.sub('<TEXT>', '<TEXT pada="cd">', outputline)
                hemistich = 0
            elif '||' in line and anustubh == False and proseflag == False:
                outputline = re.sub('\|\|', '||' + chap_and_vsnum, line)
                outputline = "\n &#160;&#160;&#160;&#160;" + outputline + "\n" 
                outputline = re.sub('<TEXT>', '<TEXT pada="d">', outputline)
                hemistich = 0
            # special danda: it does not increase verse number, e.g. after devy uvāca
            elif '|*' in line:
                uvacaflag = 1
                outputline = re.sub('\|\*', '| ', line)
                outputline = re.sub('<TEXT>', '<TEXT><uvaca>', outputline)
                outputline = re.sub('</TEXT>', '</uvaca></TEXT>', outputline)
                hemistich = 0
            # with anuṣṭubh, a danda increases verse number if it is the first single danda
            elif '|' in line and hemistich == 0 and anustubh == True and proseflag == False:
                vsnum += 1
                outputline = '\n\n<verse verseno="' + str(chapter) + "." + str(vsnum) + '"/>' + line  
                outputline = re.sub('<TEXT>', '<TEXT pada="ab">', outputline)
                # the next single danda not a first single danda
                hemistich = 1 
            # check if this is a non-anuṣṭubh first line
            elif '|' not in line and hemistich == 0 and anustubh == False:
                # no indent
                vsnum += 1
                outputline = '\n\n<verse verseno="' + str(chapter) + "." + str(vsnum) + '"/>' + line  
                outputline = re.sub('<TEXT>', '<TEXT pada="a">', outputline)
                hemistich = 1
            # check if this is a non-anuṣṭubh third line
            elif '|' not in line and hemistich == 2 and anustubh == False:
                # no indent
                outputline = re.sub('<TEXT>', '<TEXT pada="c">', line)
                hemistich = hemistich + 1
            # if this is a first single danda but it is not anuṣṭubh, don't increase verse number    
            elif '|' in line and anustubh == False and proseflag == False:
                outputline = "\n &#160;&#160;&#160;&#160;" + line
                outputline = re.sub('<TEXT>', '<TEXT pada="b">', outputline)
                hemistich = hemistich + 1 
            elif '||' in line and hemistich == 2 and anustubh == True:
                outputline = re.sub('\|\|', '||' + chap_and_vsnum, line)
                outputline = re.sub('<TEXT>', '<TEXT pada="ef">', line)
                hemistich = 0 
            elif '|' in line and hemistich == 1 and anustubh == True:
                outputline = re.sub('<TEXT>', '<TEXT pada="cd">', line)
                hemistich = 2 
            else:
                outputline = line 
            v01 = re.sub('{ }', " ", outputline)
            v01 = re.sub('<COLOPHON>', "\n||", v01)
            v01 = re.sub('</COLOPHON>', "||\n <ANUSTUBH/> ", v01)
            v01 = re.sub('</TEXT>.*', '</TEXT>', v01)
            v01 = re.sub('Ó', "oṃ", v01)
            #v01 = re.sub('<uvaca>', '', v01)
            #v01 = re.sub('</uvaca>', '', v01)
            v01 = re.sub('<ja>', ' ', v01)
            v01 = re.sub('</ja>', ' ', v01)
            v01 = re.sub('\\\\-', '', v01)
            print(v01)
        if '<APP>' in line or appflag == True:
            appflag = True
            if '</APP>' in line:
                appflag = False
            v01 = re.sub('{ }', " ", line)
            v01 = re.sub('\\\\vo', str(vsnum+uvacaflag), v01)
            v01 = re.sub('\\\\v', str(vsnum+uvacaflag), v01)
            v01 = re.sub('\\\\csa', 'ā', v01)
            v01 = re.sub('\\\\csi', 'i', v01)
            v01 = xml_substitutions.xml_substitutions(v01)
            print(v01)
        if '<PARAL>' in line or paralflag == True:
            paralflag = True
            if '</PARAL>' in line:
                paralflag = False
            v01 = re.sub('{ }', " ", line)
            v01 = re.sub('<PARAL>\\\\vo', "<PARAL>" + str(vsnum+uvacaflag), v01)
            v01 = re.sub('<PARAL>\\\\v', "<PARAL>" + str(vsnum+uvacaflag), v01)
            v01 = xml_substitutions.xml_substitutions(v01)
            print(v01)
        if '<PVAR>' in line or pvarflag == True:
            pvarflag = True
            if '</PVAR>' in line:
                pvarflag = False
            v01 = re.sub('{ }', " ", line)
            v01 = re.sub('<PVAR>\\\\vo', "<PVAR>", v01)
            v01 = re.sub('<PVAR>\\\\v', "<PVAR>", v01)
            v01 = xml_substitutions.xml_substitutions(v01)
            print(v01)
        if '<TR>' in line or trflag == True:
            trflag = True
            if '</TR>' in line:
                trflag = False
            v01 = re.sub('<!-- <TR>', '<TR>', line)
            v01 = re.sub('</TR> -->', '</TR>', v01)
            v01 = xml_substitutions.xml_substitutions(v01)
            print(v01)
        if '<NOTE>' in line or noteflag == True:
            noteflag = True
            note = note + line
            if '</NOTE>' in line:
                noteflag = False
                print(note)
                note = '' 
        if '<SUBCHAPTER>' in line or '<CHAPTER>' in line or '<TITLE>' in line:
            v01 = re.sub('{ }', " ", line)
            print(v01)
        if '<TAMIL>' in line:
            v01 = re.sub('<TAMIL>', '', line)
            v01 = re.sub('</TAMIL>', '', v01)
            #v01 = tamil.txt2unicode.diacritic2unicode(v01)
            print(v01, "<br/>")
    print("</body>")        
    openfile.close()

