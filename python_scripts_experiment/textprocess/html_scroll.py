# to clean up the results, open the html file in vim
# and say:
# %s/<div class=\"wrap-content.*\n*<\/div>//g


import re
from datetime import date
today = date.today()

from textprocess import xml_substitutions
from textprocess import line_to_dn
from textprocess import txt_output_line
from textprocess import simpletxtdn_line

def putin_text_line(line, chapter, vsnum, pada, indent, uvacaflag):
    '''
    Puts in all the required html stuff in the main text
    '''
    if uvacaflag != 0:
        uv = "<uvaca>"
    else:
        uv = ""
    if indent == True:
        ind = '&#160;&#160;&#160;&#160;'
    else:
        ind = ''
    return re.sub('<TEXT>', '<TEXT id="' + str(chapter) + '.' + str(vsnum+uvacaflag) + pada + '" class="sktvrs' + str(chapter) + '.' + str(vsnum+uvacaflag) + '" onclick="showApparatus(\'app' + str(chapter) + '.' + str(vsnum+ uvacaflag)  + pada + '\')" ondblclick="showNote(\'' + 'note' + str(chapter) + '.' + str(vsnum+uvacaflag) + '\')" '  + '>\n<RMTEXT>' + uv + ind, line)



def html_scroll(filename, apparatus_type):
    chapter = 0
    vsnum = 0
    prev_vsnum = 0
    textflag = False
    appflag = False
    paralflag = False
    anustubh = True
    hemistich = 0
    proseflag = False
    pvarflag = False
    uvacaflag = 0
    trflag = False
    noteflag = False
    onflag = False
    firstTEXT = True
    note = ''
    # pada = '<padaab>'
    collected_tr = ""
    collected_notes = ""
    appforthisline = "" 
    indent = False
    lastnotenum = "0.0"
    currentnotenum = "0.0"
    # header
    print('<!DOCTYPE html>\n <html lang="en">\n\n<head>\n <meta http-equiv="content-type" content="text/html; charset=UTF-8">\n <meta charset="utf-8">\n <title>Loading...</title>\n<rt id="realtitle">Title</rt>\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n <link rel="stylesheet" href="style_scroll.css">\n</head>\n\n<body onload="closeapp();">\n\n<div class="text" id="sanskrittext">\n\n<script xmlns="http://www.w3.org/1999/xhtml" src="showhide.js"></script>\n<script xmlns="http://www.w3.org/1999/xhtml" src="onlytext.js"></script>\n\n<span style="color:green">[Version of ' + str(today) + ']</span>\n\n<div class="header">&nbsp&nbsp&nbsp&nbsp\n&nbsp&nbsp&nbsp&nbsp\n&nbsp&nbsp&nbsp&nbsp\n\n\n<div class="wrap-main"></div>\n\n<div class="wrap-main"><TEXT onclick="showApparatus(\'instructions\')" >Click for instructions</TEXT>\n<div class="wrap-content" onclick="hideFunction(\'instructions\')" id="instructions">\n<APP> • Press keys \'s\', \'t\' and \'n\' to toggle the Sanskrit text, the translation and the notes; press \'a\' to open all four windows; press \'o\' to open/close all apparatus entries; press \'d\' to toggle Roman/Devanāgarī</APP> <APP> • You can also use these buttons for the same:</APP> <APP> &nbsp&nbsp&nbsp&nbsp <button onclick="showonlytext()" id="showonlytext">Only Skt</button></APP>\n <APP> &nbsp&nbsp&nbsp&nbsp <button onclick="showtextandtranslation()" id="showtextandtranslation">Skt & Tr</button></APP> <APP> &nbsp&nbsp&nbsp&nbsp <button onclick="showtexttrnotes()" id="txttrnotes">Skt & Tr & Notes</button></APP> <APP> &nbsp&nbsp&nbsp&nbsp <button onclick="showall()" id="all">All</button></APP> <APP> &nbsp&nbsp&nbsp&nbsp <button onclick="openallapp()" id="openallapp">Open all apparatus entries</button></APP> <APP>  &nbsp&nbsp&nbsp&nbsp <button onclick="turnItDevnag()" id="switchbutton">Switch to Devanāgarī</button></APP> <APP> • Click inside this box to close it</APP>\n<APP> • Single click on Sanskrit line to display apparatus and highlight translation of verse (if translation is visible)</APP>\n<APP> • Click inside apparatus box to close it</APP>\n<APP> • Double click on Sanskrit line to scroll to relevant note, if any and if notes are displayed</APP>\n<APP> • Click on translation to toggle highligting on relevant Sanskrit verse</APP><APP> • If your browser has problems rendering the Devanāgarī font, change your browser\'s default font (e.g. to \'Noto Sans Devanagari\' on Ubuntu) </APP>\n</div>\n</div>\n</div>\n\n<br/>\n<br/>\n\n')
    openfile = open(filename, "r")
    for line in openfile:
        # Dharma transliteration tricks
        line = re.sub("ṃ", "ṁ", line)
        line = re.sub("ṛ", "r̥", line)
        line = re.sub("ṝ", "r̥̄", line)
        line = re.sub("ḷ", "l̥", line)
        line = re.sub("Ṃ", "Ṁ", line)
        line = re.sub("Ṛ", "R̥", line)
        line = re.sub("Ṝ", "R̥̄", line)
        line = re.sub("Ḷ", "L̥", line)
        if '<START/>' in line:
            onflag = True
        if '<STOP/>' in line:
            onflag = False
        if onflag == True:
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
            if '</PROSE>' in line:
                proseflag = False
                anustubh = False
            if '<SETVSNUM' in line:
                v01 = re.sub('.*<SETVSNUM="', '', line)
                v01 = re.sub('".*', '', v01)
                vsnum = int(v01) - 1
            # the next to IF blocks function to get to the same; will get rid of <SETCHNUM at some point
            if '<SETCHNUM' in line:
                v01 = re.sub('.*<SETCHNUM="', '', line)
                v01 = re.sub('".*', '', v01)
                chapter = int(v01) - 1
            if '<startchapter-n="' in line:
                v01 = re.sub('.*<startchapter-n="', '', line)
                v01 = re.sub('".*', '', v01)
                chapter = int(v01) 
                vsnum = 0
                if firstTEXT == False:
                   print('\n</div>\n</div>\n<br/><br/><br/><NEWCHAPTER/>')
                else:
                   print('<NEWCHAPTER/>')
                firstTEXT = True
            # OBSOLETE
            if '<NEWCHAPTER/>' in line:
                #if text doesn't start with verse 1
                #vsnum = 72
                vsnum = 0
                print('<!-- chapter', chapter, '-->')
                if firstTEXT == False:
                   print('\n</div>\n</div>\n<br/><br/><br/><NEWCHAPTER/>')
                else:
                   print('<NEWCHAPTER/>')
                firstTEXT = True
            # hover trick
            if '<TEXT>' in line and firstTEXT == False:
                 line = re.sub('<TEXT>', '\n</div>\n</div>\n\n<mainwrap>\n<TEXT>', line)
            if '<TEXT>' in line and firstTEXT == True:
                 line = re.sub('<TEXT>', '\n<mainwrap>\n<TEXT>', line) 
                 firstTEXT = False
            # if it is the main text:        
            if '<TEXT>' in line or textflag == True:
                # deleting TeX-style \- (`can break line here')
                line = re.sub('\\\\-', '', line)
                # stripping line within <TEXT> mainly to produce the Devanāgarī version
                maintextrm = txt_output_line.txt_output_line(line, textflag)
                maintextrm = re.sub('<MNTR>', '', maintextrm)
                maintextrm = re.sub('</MNTR>', '', maintextrm)
                maintextrm = re.sub('<mainwrap>', '', maintextrm)
                maintextrm = re.sub('</mainwrap>', '', maintextrm)
                maintextrm = re.sub('<div>', '', maintextrm)
                maintextrm = re.sub('</div>', '', maintextrm)
                maintextrm = re.sub('{-}', '', maintextrm)
                if proseflag == False:
                    maintextrm = re.sub('\|\|.*', " ॥"+ str(chapter) + ":" + str(vsnum), maintextrm)
                else:
                    maintextrm = re.sub('\|\|', " ॥", maintextrm)
                maintextrm = re.sub('\|', " ।", maintextrm)
                # producing a Devanāgarī version of the line:
                maintextdn = simpletxtdn_line.simpletxtdn_line(maintextrm) 
                # <crux> has been turned into †, now turning back to <crux>
                # </crux> has been turned into ‡, now turning back to </crux>
                maintextdn = re.sub("†", "<crux>", maintextdn)
                maintextdn = re.sub("‡", "</crux>", maintextdn)
                maintextdn = re.sub("\n", "", maintextdn)

                textflag = True
                uvacaflag = 0
                if '</TEXT>' in line:
                    textflag = False
                # check if this is the end of a verse
                if '||' in line and proseflag == False:
                    chap_and_vsnum = ("<vsnum>" + str(chapter) + "." + str(vsnum) + "</vsnum>||") 
                    # We need a little extra vertical space between verses (amount controlled in the css file)
                    vspace = "<spaceaftersloka/>"
                else:
                    chap_and_vsnum = "" 
                    vspace = ""
                if '||' in line and anustubh == True and hemistich == 1 and proseflag == False:
                    outputline = re.sub('\|\|', ' ||' + chap_and_vsnum, line)
                    # main process to put in stuff
                    pada = "cd"
                    indent = False
                    outputline = putin_text_line(outputline, chapter, vsnum, pada, indent, uvacaflag)
                    appforthisline = "cd"
                    hemistich = 0
                elif '||' in line and anustubh == False and proseflag == False:
                    outputline = re.sub('\|\|', ' ||' + chap_and_vsnum, line)
                    outputline = "\n" + outputline + "\n" 
                    # main process to put in stuff
                    pada = "d"
                    indent = True
                    outputline = putin_text_line(outputline, chapter, vsnum, pada, indent, uvacaflag)
                    hemistich = 0
                    appforthisline = "d"
                # special danda: it does not increase verse number, e.g. after devy uvāca
                elif '|*' in line:
                    # main process to put in stuff
                    uvacaflag = 1
                    pada = "uvaca"
                    indent = False
                    outputline = re.sub('\|\*', ' | ', line)
                    outputline = putin_text_line(outputline, chapter, vsnum, pada, indent, uvacaflag)
                    outputline = re.sub('</TEXT>', '</uvaca></TEXT>', outputline)
                    hemistich = 0
                    appforthisline = "uvaca"
                # with anuṣṭubh, a danda increases verse number if it is the first single danda
                elif '|' in line and hemistich == 0 and anustubh == True and proseflag == False:
                    vsnum += 1
                    # main process to put in stuff
                    uvacaflag = 0
                    pada = "ab"
                    indent = False
                    outputline = putin_text_line(line, chapter, vsnum, pada, indent, uvacaflag)
                    appforthisline = "ab"
                    outputline = re.sub('\|', ' |', outputline)
                    # the next single danda not a first single danda
                    hemistich = 1 
                # check if this is a non-anuṣṭubh first line
                elif '|' not in line and hemistich == 0 and anustubh == False:
                    # no indent
                    vsnum += 1
                    # main process to put in stuff
                    uvacaflag = 0
                    pada = "a"
                    indent = False
                    outputline = putin_text_line(line, chapter, vsnum, pada, indent, uvacaflag)
                    hemistich = 1
                    appforthisline = "a"
                # check if this is a non-anuṣṭubh third line
                elif '|' not in line and hemistich == 2 and anustubh == False:
                    # no indent
                    # main process to put in stuff
                    uvacaflag = 0
                    pada = "c"
                    indent = False
                    outputline = putin_text_line(line, chapter, vsnum, pada, indent, uvacaflag)
                    hemistich = hemistich + 1
                    appforthisline = "c"
                # if this is a first single danda but it is not anuṣṭubh, don't increase verse number; it's pāda b
                elif '|' in line and anustubh == False and proseflag == False:
                    outputline = "\n" + line
                    # main process to put in stuff
                    uvacaflag = 0
                    pada = "b"
                    indent = True
                    outputline = putin_text_line(line, chapter, vsnum, pada, indent, uvacaflag)
                    outputline = re.sub('\|', ' |', outputline)
                    hemistich = hemistich + 1 
                    appforthisline = "b"
                # if it's a three-line anuṣṭubh, two ||s mean pāda ef
                elif '||' in line and hemistich == 2 and anustubh == True:
                    outputline = re.sub('\|\|', ' ||' + chap_and_vsnum, line)
                    # main process to put in stuff
                    uvacaflag = 0
                    pada = "ef"
                    indent = False
                    outputline = putin_text_line(outputline, chapter, vsnum, pada, indent, uvacaflag)
                    hemistich = 0 
                    appforthisline = "ef"
                # if it's a three-line anuṣṭubh, one | means pāda cd when it's hemistich 1
                elif '|' in line and hemistich == 1 and anustubh == True:
                    # main process to put in stuff
                    uvacaflag = 0
                    pada = "cd"
                    indent = False
                    outputline = putin_text_line(line, chapter, vsnum, pada, indent, uvacaflag)
                    outputline = re.sub('\|', ' |', outputline)
                    hemistich = 2 
                    appforthisline = "cd"
                else:
                    outputline = line 
                v01 = re.sub('{-}', "-", outputline)
                v01 = re.sub('{ }', " ", v01)
                v01 = re.sub('<COLOPHON>', "\n<colophon>\n<RMTEXT> ", v01)
                v01 = re.sub('</COLOPHON>', "", v01)
                # b and d lines non-anuṣṭubh verses with indentation
                if '&#160;&#160;&#160;&#160' in v01: 
                    v01 = re.sub('</TEXT>.*', '</RMTEXT>\n<DNTEXT>&#160;&#160;&#160;&#160' + maintextdn + ' </DNTEXT></TEXT>\n<apparatuswrap>', v01)
                else:
                    v01 = re.sub('</TEXT>.*', '</RMTEXT>\n<DNTEXT>' + maintextdn + ' </DNTEXT></TEXT>\n<apparatuswrap>', v01)
                if '</COLOPHON>' in line:
                    v01 = re.sub('</DNTEXT>', " </colophon></DNTEXT>", v01)
                v01 = re.sub('Ó', "oṃ", v01)
                #v01 = re.sub('<uvaca>', '', v01)
                #v01 = re.sub('</uvaca>', '', v01)
                v01 = re.sub('<ja>', ' ', v01)
                v01 = re.sub('</ja>', ' ', v01)
                #v01 = re.sub('<crux>', '†', v01)
                #v01 = re.sub('</crux>', '†', v01)
                v01 = re.sub('\\\\-', '', v01)
                v01 = re.sub('<mainwrap>', '<div class="wrap-main">', v01)
                v01 = re.sub('</mainwrap>', '</div>', v01)
                v01 = re.sub('<apparatuswrap>', vspace + '\n\n<div class="wrap-content" onclick="hideFunction(\'app' + str(chapter) + '.' + str(vsnum+uvacaflag) + appforthisline + '\')" id="app' + str(chapter) + '.' + str(vsnum+uvacaflag) + appforthisline + '">', v01)
                v01 = re.sub('</apparatuswrap>', '</div>', v01)
                # prose
                if proseflag == True:
                    v01 = re.sub('<TEXT>', '<TEXTPROSE>\n<RMTEXT>', v01)
                    v01 = re.sub('</TEXT>', '</TEXTPROSE>', v01)
                print(v01)
                # fill in the dn version

            # dealing with the apparatus
            if '<APP>' in line or appflag == True:
                appflag = True
                if '</APP>' in line:
                    appflag = False
                v01 = re.sub('{ }', " ", line)
                v01 = re.sub('\\\\vo', str(vsnum+uvacaflag), v01)
                v01 = re.sub('\\\\v', str(vsnum+uvacaflag), v01)
                v01 = re.sub('\\\\csa ', 'ā', v01)
                v01 = re.sub('\\\\csi ', 'i', v01)
                # delete everything around <LEM></LEM>
                lemma = re.sub('.*<LEM>', '', line)
                lemma = re.sub('</LEM>.*', ' ', lemma)
                lemma = re.sub("{ }", "", lemma)
                dnlemma = simpletxtdn_line.simpletxtdn_line(lemma.lower()) 
                #dnlemma = ""
                v01 = re.sub('</LEM>', '</LEM><DNLEM>' + dnlemma + '</DNLEM>', v01)
                v01 = xml_substitutions.xml_substitutions(v01)
                print(v01)
            if '<PARAL>' in line or paralflag == True:
                paralflag = True
                if '</PARAL>' in line:
                    paralflag = False
                v01 = re.sub('{ }', " ", line)
                v01 = re.sub('<PARAL> *\\\\vo', "<PARAL>" + str(vsnum+uvacaflag), v01)
                v01 = re.sub('<PARAL> *\\\\v', "<PARAL>" + str(vsnum+uvacaflag), v01)
                v01 = xml_substitutions.xml_substitutions(v01)
                print(v01)
            '''
            if '<PVAR>' in line or pvarflag == True:
                pvarflag = True
                if '</PVAR>' in line:
                    pvarflag = False
                v01 = re.sub('{ }', " ", line)
                v01 = re.sub('<PVAR>\\\\vo', "<PVAR>", v01)
                v01 = re.sub('<PVAR>\\\\v', "<PVAR>", v01)
                v01 = xml_substitutions.xml_substitutions(v01)
                print(v01)
            '''    
            if '<TRCHAPTER>' in line:
                trflag = True
                v01 = re.sub('<!-- <TRCHAPTER>', '<br/><br/><br/><trnslchapter>', line)
                v01 = re.sub('</TRCHAPTER> -->', '</trnslchapter>', v01)
                v01 = xml_substitutions.xml_substitutions(v01)
                if '</TRCHAPTER>' in line:
                    trflag = False
                    collected_tr = collected_tr  + v01
                else:
                    collected_tr = collected_tr + v01

            if '<TRSUBCHAPTER>' in line:
                trflag = True
                v01 = re.sub('<TRSUBCHAPTER>', '<br/><br/><trnslsubchapter>', line)
                v01 = re.sub('</TRSUBCHAPTER>', '</trnslsubchapter>', v01)
                v01 = xml_substitutions.xml_substitutions(v01)
                if '</TRSUBCHAPTER>' in line:
                    trflag = False
                    collected_tr = collected_tr  + v01
                else:
                    collected_tr = collected_tr + v01

            if '<TRSUBSUBCHAPTER>' in line:
                trflag = True
                v01 = re.sub('<TRSUBSUBCHAPTER>', '<br/><br/><trnslsubsubchapter>', line)
                v01 = re.sub('</TRSUBSUBCHAPTER>', '</trnslsubsubchapter>', v01)
                v01 = xml_substitutions.xml_substitutions(v01)
                if '</TRSUBSUBCHAPTER>' in line:
                    trflag = False
                    collected_tr = collected_tr  + v01
                else:
                    collected_tr = collected_tr + v01


            if '<TRCOLOPHON>' in line:
                trflag = True
                v01 = re.sub('<TRCOLOPHON>', '<br/><br/><trnslcolophon>', line)
                v01 = re.sub('</TRCOLOPHON>', '</trnslcolophon>', v01)
                v01 = xml_substitutions.xml_substitutions(v01)
                if '</TRCOLOPHON>' in line:
                    trflag = False
                    collected_tr = collected_tr  + v01 + "<br/><br/><br/><br/>"
                else:
                    collected_tr = collected_tr + v01
            if '<TR>' in line or trflag == True:
                trflag = True
                # &#39 is a single quote, needed because of a bug...?
                strng = "sktvrs" + str(chapter) +  "." + str(vsnum+uvacaflag)
                v01 = re.sub("<!-- <TR>", "\n<trnsl class=\"trnsl" + str(chapter) +  '.' + str(vsnum+uvacaflag) + '" ' + "onclick=\"showSkt(&#39" + strng + "&#39)\">", line)
                v01 = re.sub('</TR> -->', '</trnsl>', v01)
                if '<TR>' in line and (prev_vsnum != vsnum and uvacaflag != 1):
                    collected_tr = collected_tr + "\n<br/><br/>\n" + "|" + '<vsnum id="tr' + str(chapter) + '.' + str(vsnum) + '">' + str(chapter) + "." + str(vsnum) + "</vsnum>" + "| "
                if '<TR>' in line and uvacaflag == 1:
                    collected_tr = collected_tr + "<br/><br/>"
                if '</TR>' in line:
                    prev_vsnum = vsnum
                    trflag = False
                    collected_tr = collected_tr  + v01
                    # handling the sign |F| meaning 'and the following verse'; output e.g. --|1.8| after |1.7|
                    collected_tr = re.sub('\|F\|', '-- |' + '<vsnum>' + str(chapter) + "." + str(vsnum+1) + "</vsnum>" + "| ", collected_tr)
                    collected_tr = xml_substitutions.xml_substitutions(collected_tr)
                    collected_tr = re.sub("`", "‘", collected_tr)
                    collected_tr = re.sub("'", "’", collected_tr)
                else:
                    collected_tr = collected_tr + v01
            if '<NOTE>' in line or noteflag == True:
                currentnotenum = str(chapter) + "." + str(vsnum)
                noteflag = True
                v01 = xml_substitutions.xml_substitutions(line)
                v01 = re.sub("`", "‘", v01)
                v01 = re.sub("'", "’", v01)
                if '<NOTE>' in line and lastnotenum != currentnotenum:
                    collected_notes = collected_notes + "<br/><br/>" + "|" + '<vsnum id="note' + str(chapter) + "." + str(vsnum) + '">' + str(chapter) + "." + str(vsnum) + "</vsnum>" + "| "
                    lastnotenum = currentnotenum
                if '</NOTE>' in line:
                    noteflag = False
                    collected_notes = collected_notes  + v01
                else:
                    collected_notes = collected_notes + v01
            '''    
            if '<NOTE>' in line or noteflag == True:
                noteflag = True
                note = note + line
                if '</NOTE>' in line:
                    noteflag = False
                    note = xml_substitutions.xml_substitutions(note)
                    print(note)
                    note = '' 
            '''
            if '<TITLE>' in line:
                size = "h1"
            if '<CHAPTER>' in line:
                size = "chapter"
            if '<SUBCHAPTER>' in line:
                size = "subchapter"
            if '<SUBSUBCHAPTER>' in line:
                size = "subsubchapter"
            if '<SUBSUBCHAPTER>' in line or '<SUBCHAPTER>' in line or '<CHAPTER>' in line or '<TITLE>' in line:
                v01 = re.sub('{ }', " ", line)
                # the spaces also make sure that final consonants will
                # will come out properly in Devanagari
                v01 = re.sub('<.?TITLE>', " ", v01)
                v01 = re.sub('<.?SUBSUBCHAPTER>', " ", v01)
                v01 = re.sub('<.?SUBCHAPTER>', " ", v01)
                v01 = re.sub('<.?CHAPTER>', " ", v01)
                # turn it into Devanāgarī
                textdn = simpletxtdn_line.simpletxtdn_line(v01.lower()) 
                if firstTEXT == False:
                   print('\n</div>\n</div>')
                print("<" + size + ">\n<RMTEXT>" + v01 + "</RMTEXT>\n<DNTEXT>" + textdn + "</DNTEXT></" + size + ">")
                firstTEXT = True

    # close text box
    print("</div></div><br/><br/><br/><br/></div>\n")        
    # print translation box
    print('<div class="translation" id="translation">\n<h2>Translation</h2>')
    print(collected_tr)
    print("\n<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/></div>\n")        
    # print notes box
    print('<div class="notes" id="notes">\n<h2>Notes</h2>\n')
    print(collected_notes)
    print("\n<br/>\n<br/></div>\n")        
    # print mss box
    print('<div class="msimage" id="mssimages">\n<h2>Sources</h2>\n')
    open_mssdata_file = open("/home/csaba/indology/dharma_project/vrsa_edition/vss_mss_data.html", "r")
    for l in open_mssdata_file:
        print(l[:-1], end=" ")        
    print("\n<br/>\n</div>\n</body></html>")        
    quit()
    openfile.close()

