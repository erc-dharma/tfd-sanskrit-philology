import re

def trtex(filename):
    chapter = 0
    vsnum = 1
    vsnum_needed = True
    twodandas_just_passed = True
    textflag = False
    trflag = False
    noteflag = False
    note = ''
    openfile = open(filename, "r")
    print("\\documentclass{article}")
    print("\\usepackage[utf8x]{inputenx}")
    print("\\newcommand{\skt}[1]{\\textit{#1}}")
    print("\\input{/home/csaba/indology/dharma_project/vrsa_edition/sigla_for_tr_file.tex}")
    print("\\begin{document}")
    print("\\begin{center}{\Huge \\textbf{TITLE}}\\\\ {\Large (translation)}\\bigskip\\\\ {\large\\today}\end{center}")
    for line in openfile:
        chap_and_vsnum = (str(chapter) + "." + str(vsnum)) 
        if '<TEXT>' in line:
            if '||' in line:
                vsnum += 1
                vsnum_needed = True
                twodandas_just_passed = True
            elif '|' in line and twodandas_just_passed == True:
                print("\n\n\\textbf{" + chap_and_vsnum + "}\ ")
                twodandas_just_passed = False
        if '<TR>' in line or trflag == True:
            trflag = True
            if '</TR>' in line:
                trflag = False
            v01 = re.sub('.*<TR>', '', line[:-1])
            v01 = re.sub('</TR>.*', ' ', v01)
            # final white spaces
            v01 = v01.rstrip()
            print("\ " + v01 + "%")
        if '<NOTE>' in line or noteflag == True:
            noteflag = True
            v01 = re.sub('.*<NOTE>', '', line[:-1])
            v01 = re.sub('</NOTE>.*', ' ', v01)
            note = note + v01
            if '</NOTE>' in line:
                noteflag = False
                print("\\footnote{" + note + "}%")
                note = ""
        if '<NEWCHAPTER/>' in line:
                chapter += 1
                vsnum = 1
                print("\\vfill\pagebreak\\begin{center}{\large\\textbf{Chapter " + str(chapter) + "}}\\end{center}")
    print("\\end{document}")
    openfile.close()

