import re

def trtex(filename):
    chapter = 0
    vsnum = 1
    vsnum_needed = True
    twodandas_just_passed = True
    textflag = False
    trflag = False
    noteflag = False
    noanustubh = False
    note = ''
    openfile = open(filename, "r")
    print("\\documentclass{article}")
    print("\\usepackage[utf8x]{inputenx}")
    print("\\newcommand{\skt}[1]{\\textit{#1}}")
    print("\\newcommand{\danda}{\\thinspace$\cal j$ }")
    print("\\newcommand{\\twodanda}{\\thinspace$\cal k$ }")
    print("\\input{/home/csaba/indology/dharma_project/vrsa_edition/sigla_for_tr_file.tex}")
    print("\\begin{document}")
    print("\\begin{center}{\Huge \\textbf{Vṛṣasārasaṃgraha}}\\\\ {\Large (translation)}\\bigskip\\\\ {\large\\today}\end{center}")
    for line in openfile:
        chap_and_vsnum = (str(chapter) + "." + str(vsnum)) 
        if '<NOTANUSTUBH/>' in line:
            notanustubh = True
        if '<ANUSTUBH/>' in line:
            notanustubh = False
        if '<TEXT>' in line:
            if '||' in line:
                vsnum += 1
                vsnum_needed = True
                twodandas_just_passed = True
            elif ('|' in line or notanustubh == True) and ( vsnum_needed == True or twodandas_just_passed == True):
                print("\n\n\\textbf{" + chap_and_vsnum + "}%")
                vsnum_needed = False
                twodandas_just_passed = False
        if '<TR>' in line or trflag == True:
            trflag = True
            if '</TR>' in line:
                trflag = False
            v01 = re.sub('.*<TR>', '', line[:-1])
            v01 = re.sub('\|F\|', '--\\\\textbf{' + str(chapter) + "." + str(vsnum) + '}', v01)
            v01 = re.sub('</TR>.*', ' ', v01)
            v01 = re.sub('Ł', '\\\\skt{', v01)
            v01 = re.sub('\$', '}', v01)
            v01 = re.sub('\^', '${\\\\uparrow}$', v01)
            # final white spaces
            v01 = v01.rstrip()
            print("\ " + v01 + "%")
        if '<NOTE>' in line or noteflag == True:
            noteflag = True
            v01 = re.sub('.*<NOTE>', '', line[:-1])
            v01 = re.sub('</NOTE>.*', ' ', v01)
            v01 = re.sub('\\|\\|', '\\\\twodanda', v01)
            v01 = re.sub('\\|', '\\\\danda', v01)
            v01 = re.sub('<sep/>', '\n\n', v01)
            v01 = re.sub('<br/>', '\n', v01)
            v01 = re.sub('Ł', '\\\\skt{', v01)
            v01 = re.sub('\$', '}', v01)
            note = note + v01
            if '</NOTE>' in line:
                noteflag = False
                print("\\footnote{" + note + "}%")
                note = ""
        if '<startchapter-n="' in line:
            v01 = re.sub('.*<startchapter-n="', '', line)
            v01 = re.sub('".*', '', v01)
            chapter = int(v01) 
            vsnum = 1
        if '<NEWCHAPTER/>' in line:
                chapter += 1
                vsnum = 1
                print("\\vfill\pagebreak\\begin{center}{\large\\textbf{Chapter " + str(chapter) + "}}\\end{center}")
        if '<TRCHAPTER>' in line:
            v01 = re.sub('.*<TRCHAPTER>', '', line)
            v01 = re.sub('</TRCHAPTER>.*', '', v01)
            print("\\vfill\pagebreak\\begin{center}{\large\\textbf{" + v01 + "}}\\end{center}")
    print("\\end{document}")
    openfile.close()

