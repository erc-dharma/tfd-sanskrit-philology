#!/usr/bin/python3
# By Csaba Kiss

# regex:
import re
# for the commandline arguments:
import sys


def tei_output(filename):
    '''
    Usage: 
        python3 teioutput.py test_file.xml > anyfilenameyouwanttosavetheTEI.xml
    Lot of stuff to be deleted/reworked
    Expected input format:
    <TEXT> śatasāhasrikaṃ granthaṃ sahasrādhyāyam uttamam|</TEXT>
        <APP>\vb <LEM>sahasrādhyāyam</LEM> \A\B; sahaśradhyāyam \C,sahasrādhyāyar \D</APP>
        % satasāhaśrikaṃ \msCc
    <TEXT> pūrvam asya śataṃ pūrṇaṃ śrutvā bhāratasaṃhitām||</TEXT>
        <APP>\vc <LEM>pūrvam asya</LEM> \D; pūrva cāsya \A\B, purva casya \C</APP>
        <APP>\vd <LEM>bhārata°</LEM> \A\B; nārāda° \C\D</APP>
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Expected TEI output (plus header and footer are added on the fly):
    <lb n="1"/>
    <lg n="1" met="anuṣṭubh">
    <lg type="halfverse" n="ab">
    <l> śatasāhasrikaṃ granthaṃ sahasrādhyāyam uttamam|</l>
    </lg>

    <app loc="1.1ab">
         <lem wit="#A #B">sahasrādhyāyam</lem>
         <rdg wit="#C"> sahaśradhyāyam</rdg>
         <rdg wit="#D">sahasrādhyāyar</rdg>
    </app>

    <lb n="2"/>
    <lg type="halfverse" n="cd">
    <l> pūrvam asya śataṃ pūrṇaṃ śrutvā bhāratasaṃhitām||1.1||</l>
    </lg>
    </lg>

    <app loc="1.1cd">
         <lem wit="#D">pūrvam asya</lem>
         <rdg wit="A# B#"> pūrva cāsya </rdg>
         <rdg wit="#C"> purva casya </rdg>
    </app>
    <app loc="1.1.cd">
         <lem wit="#A #B">bhārata°</lem>
         <rdg wit="#C #D"> nārāda° </rdg>
    </app>
    '''
    chapter = 0
    vsnum = 1
    textflag = False
    appflag = False
    proseflag = False
    chap_and_vsnum = "" 
    anustubh = True
    hemistich = 0
    lemma_done = False
    finalvarlist = []
    # for TEI linebreak <lb>
    lb = 1
    print(header)
    # preparation: delete \n-s in apparatus lines
    openfile = open(filename, "r")
    tempfile = open("tempfile.txt","w") 
    for line in openfile:
        if '<APP>' in line and '</APP>' not in line:
            appflag = True
            mod_line = re.sub('\n', '', line)
            mod_line = mod_line.strip()
            tempfile.write(mod_line)
        elif appflag == True and '</APP>' not in line:
            mod_line = re.sub('\n', '', line)
            mod_line = mod_line.strip()
            tempfile.write(mod_line)
        else:
            tempfile.write(line)
            appflag = False
    tempfile.close()
    openfile = open("tempfile.txt", "r")
    appflag = False
    for line in openfile:
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
            line = re.sub('<PROSE>', '', line)
        if '</PROSE>' in line:
            proseflag = False
            line = re.sub('</PROSE>', '', line)
        if '<NEWCHAPTER/>' in line:
            chapter += 1
            vsnum = 0
            print('<!-- chapter', chapter, '-->')
            print('<NEWCHAPTER/>')
        # if it is the main text:        
        if ('<TEXT>' in line or textflag == True) and proseflag == False:
	    # call Devanagari converter?
	    #line = convert2dn(line)
            #print('\n<lb n="' + str(lb) + '"/>')
            textflag = True
            uvacaflag = 0
            if '</TEXT>' in line:
                textflag = False
            # check if this is the end of a verse
            #if '||' in line:
            #else:
                #chap_and_vsnum = "" 
            # end of a regular anuṣṭubh
            if '||' in line and anustubh == True and hemistich == 1:
#                outputline = re.sub('\|\|', '||' + chap_and_vsnum, line)
                outputline = re.sub('\|\|', '', line)
                outputline = re.sub('<TEXT>', '<l n="cd">', outputline)
                #outputline = re.sub('</TEXT>', '</l><lb n="' + str(lb) + '"/>\n</lg>', outputline)
                outputline = re.sub('</TEXT>', '</l>\n</lg>', outputline)
                hemistich = 0
                app_pada = "cd"
                lb += 1
            elif '||' in line and anustubh == False:
                outputline = re.sub('\|\|', '', line)
                outputline = re.sub('<TEXT>', '<l n="d">', outputline)
                #print('<lg type="halfverse" n="d">')
                outputline = re.sub('</TEXT>', '</l>\n</lg>', outputline)
                #outputline = re.sub('\|\|', '||' + chap_and_vsnum, outputline)
                hemistich = 0
                app_pada = "d"
                lb += 1
            # special danda: it does not increase verse number, e.g. after devy uvāca
            elif '|*' in line:
                uvacaflag = 1
                outputline = re.sub('\|\*', '', line)
                outputline = re.sub('<TEXT>', '<l n="uvaca">', outputline)
                outputline = re.sub('</TEXT>', '</l>', outputline)
                app_pada = "uvaca"
                hemistich = 0
            # with anuṣṭubh, a danda increases verse number if it is the first single danda
            elif '|' in line and hemistich == 0 and anustubh == True:
                vsnum += 1
                chap_and_vsnum = (str(chapter) + "." + str(vsnum)) 
                print('<lg n="' + str(chap_and_vsnum)+  '" met="anuṣṭubh">')
                outputline = re.sub('\|', '', line)
                #print('<lg type="halfverse" n="ab">')
                #outputline = '\n\n<verse verseno="' + str(chapter) + "." + str(vsnum) + '"/>' + line  
                #outputline = re.sub('<TEXT>', '<l>', line)
                outputline = re.sub('<TEXT>', '<l n="ab">', outputline)
                outputline = re.sub('</TEXT>', '</l>', outputline)
                app_pada = "ab"
                lb += 1
                # the next single danda not a first single danda
                hemistich = 1 
            # check if this is a non-anuṣṭubh first line
            elif '|' not in line and hemistich == 0 and anustubh == False:
                # no indent
                vsnum += 1
                chap_and_vsnum = (str(chapter) + "." + str(vsnum)) 
                outputline = line
                print('<lg n="' + str(chap_and_vsnum)+  '" met="non-anuṣṭubh">')
                #print('<lg type="halfverse" n="a">')
                #outputline = re.sub('<TEXT>', '<TEXT pada="a">', outputline)
                outputline = re.sub('<TEXT>', '<l n="a">', line)
                outputline = re.sub('</TEXT>', '</l>', outputline)
                hemistich = 1
                app_pada = "a"
                lb += 1
            # check if this is a non-anuṣṭubh third line
            elif '|' not in line and hemistich == 2 and anustubh == False:
                # no indent
                #print('<lg type="halfverse" n="c">')
                outputline = re.sub('<TEXT>', '<l n="c">', line)
                outputline = re.sub('</TEXT>', '</l>', outputline)
                lb += 1
                hemistich = hemistich + 1
                app_pada = "c"
            # if this is a first single danda but it is not anuṣṭubh, don't increase verse number    
            elif '|' in line and anustubh == False:
                #print('<lg type="halfverse" n="b">')
                outputline = re.sub('\|', '', line)
                outputline = re.sub('<TEXT>', '<l n="b">', outputline)
                outputline = re.sub('</TEXT>', '</l>', outputline)
                lb += 1
                app_pada = "b"
                hemistich = hemistich + 1 
            elif '||' in line and hemistich == 2 and anustubh == True:
#                print('<lg n="' + str(vsnum)+  '" met="anuṣṭubh">')
                #print('<lg type="halfverse" n="ef">')
#                outputline = re.sub('<TEXT>', '<TEXT pada="ef">', line)
                outputline = re.sub('\|', '', line)
                outputline = re.sub('<TEXT>', '<l n="ef">', outputline)
                outputline = re.sub('</TEXT>', '</l>\n</lg>', outputline)
                hemistich = 0 
                app_pada = "ef"
                lb += 1
            # second line of anuṣṭubh in a 3 line śloka
            elif '|' in line and hemistich == 1 and anustubh == True:
                #print('<lg n="' + str(vsnum)+  '" met="anuṣṭubh">')
                outputline = re.sub('\|', '', line)
                #print('<lg type="halfverse" n="cd">')
                outputline = re.sub('<TEXT>', '<l n="cd">', outputline)
                outputline = re.sub('</TEXT>', '</l>', outputline)
                hemistich = 2 
                app_pada = "cd"
                lb += 1
		
            else:
                outputline = line
            v01 = re.sub('{ }', " ", outputline)
            v01 = re.sub('.*<COLOPHON>', "<l>", v01)
            v01 = re.sub('</COLOPHON>.*', "</l>", v01)
            v01 = re.sub('Ó', "oṃ", v01)
            #v01 = re.sub('<uvaca>', '', v01)
            #v01 = re.sub('</uvaca>', '', v01)
            v01 = re.sub('<ja>', ' ', v01)
            v01 = re.sub('</ja>', ' ', v01)
            print(v01)
        outputline = line
        if '<TEXT>' in line and proseflag == True:
            outputline = re.sub('<TEXT>', '<div type="prose">', outputline)
        if '</TEXT>' in line and proseflag == True:
            v01 = re.sub('</TEXT>', '</div>', outputline)
            print(v01)
        if '<APP>' in line or appflag == True:
            appflag = True
            line = re.sub('\\\\oo', '</APP><APP>', line)
            line = re.sub('<APP>\ ?\ ?\n', '<APP>', line)
            # LEMMA
            lem_wit = '' 
            # find pada if it is a, b, c or d in a śloka
            if '\\va ' in line:
                app_pada = "a"
            if '\\vb ' in line:
                app_pada = "b"
            if '\\vc ' in line:
                app_pada = "c"
            if '\\vd ' in line:
                app_pada = "d"
            if '\\ve ' in line:
                app_pada = "e"
            if '\\vf ' in line:
                app_pada = "f"
            if '\\vab ' in line:
                app_pada = "ab"
            if '\\vcd ' in line:
                app_pada = "cd"
            # find lemma witness sigla
            lem_wit = re.sub('.*</LEM> ', '', line)
            lem_wit = re.sub(';.*', '', lem_wit)
            if '\eme' in lem_wit or '\corr' in lem_wit or '\conj' in lem_wit:
                lem_wit = re.sub('\\\\', '', lem_wit)[:-1]
                not_a_witness = True
            else:
                lem_wit = re.sub('\\\\', ' #', lem_wit)[:-1]
                not_a_witness = False
            lem_wit = re.sub('^ ', '', lem_wit)
            v01 = re.sub('^.*<APP>', '', line)
            # you have to have 'type' and not 'wit' if it is eme, corr or conj
            if not_a_witness == False:
                v01 = re.sub('.*<LEM>', '<lem wit="' + lem_wit + '">', v01)
            else:
                v01 = re.sub('.*<LEM>', '<lem type="' + lem_wit + '">', v01)
            v01 = re.sub('</LEM>.*', '</lem>\n', v01)
            finallemma = xml_substitutions(v01)
            # variants
            if '<LEM>' in line:
                variants = re.sub('.*;', '', line)
            else:
                variants = line
            variants = re.sub('</APP>', '', variants)
            variants = re.sub('\n', '', variants)
            variants_list = variants.split(",")
            for var in variants_list:
                sigla = re.sub('.* \\\\', '\\\\', var)
                sigla = re.sub(' *', '', sigla)
                sigla = re.sub('\\\\', ' #', sigla)
                # strip is to get rid of some trailing spaces
                skt = re.sub('\\\\om', 'omitted', var.strip())
                skt = re.sub('\\\\.*', '', skt)
                skt = xml_substitutions(skt) 
                finalvarlist.append('<rdg wit="' + sigla + '">' + skt + "</rdg>")
            v01 = re.sub('{ }', " ", v01)
            # PRINT OUT APPARATUS when there is an </APP> in the line
            if '</APP>' in line:
                print('<app loc="' + str(chap_and_vsnum) + app_pada + '"> <!-- app sections are to be cut and pasted to the end of the file.  -->')
                print("    ", finallemma[:-1], end="")
                appflag = False
                for v in finalvarlist:
                    fv = re.sub('\\\\', '', v)
                    fv = re.sub('wit=" ', 'wit="', fv)
                    print("    ", fv)
                print("</app>\n")
                finalvarlist = []
    print(footer)        
    openfile.close()


def xml_substitutions(line):
        subdict ={'\\\\A': '',
                '\\\\B': '',
                '\\\\C': '',
                '\\\\D': '',
                '\\\\Ed': '',
                '\\\\verseomitted': '<LEM>this verse omitted</LEM>',
                '\\\\om': 'omitted in',
                #'acorr': '<corr>acorr</corr>',
                #'pcorr': '<corr>pcorr</corr>',
                '\\\\oo': " •", 
                '\\\\uncl': "",
                '\\\\': " ", 
                '\\Ł': '<SKT>', 
                '\\$': '</SKT>',
                '--': '–',
                'Ó': 'oṃ',
		'\\\\lac': 'lacuna'
                } 
        for c in subdict:
            line = re.sub(c, subdict[c], line)
        return line

header = '<?xml version="1.0" encoding="UTF-8"?>\n<?xml-model href="tei-epidoc.rng" schematypens="http://relaxng.org/ns/structure/1.0"?>\n<?xml-model href="tei-epidoc.rng" schematypens="http://purl.oclc.org/dsdl/schematron"?>\n<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:space="preserve" xml:lang="en">\n<teiHeader>\n<fileDesc>\n<titleStmt>\n<title xml:lang="eng-Latn">Test File</title>\n</titleStmt>\n<publicationStmt>\n<authority/>\n<idno type="filename">0001</idno>\n</publicationStmt>\n<sourceDesc>\n<msDesc><msIdentifier><repository>Repo</repository></msIdentifier></msDesc>\n</sourceDesc>\n</fileDesc>\n</teiHeader>\n<text>\n<body>\n<div type="edition" xml:lang="san-Latn">\n\n' 

footer = '</div>\n</body>\n</text>\n</TEI>'




filename = sys.argv[1]
tei_output(filename)
