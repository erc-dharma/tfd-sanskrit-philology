#!/usr/bin/python3
# regex:
import re
# for the commandline arguments:
import sys
import numpy as np
import pandas as pd
# for excel
import xlrd 

class bcolors:
	MAIN = '\033[0m'
	LEMMA = '\033[93m'
	MSS = '\033[89m'
	NEUT = '\033[94m'
	TR = '\033[91m'
	VEG = '\033[90m'
	CH = '\033[90m'
	SCH = '\033[90m'
	VAR = '\033[90m'
	'''
	FAIL = '\033[91m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	'''

def txt_output(vd):
    for i in range(len(vd)):
            vsnum = "||" + str(int(vd.Chapter[i])) + "." + str(int(vd['Verse number'][i])) + "||"
            if vd.Structure[i] == 'cd' or vd.Structure[i] == 'ef' or vd.Structure[i] == 'd':
                print(vd['Main text'][i], vsnum)
            elif vd.Structure[i] == 'Ch':
                print('----', vd['Main text'][i], '----')
            elif vd.Structure[i] == 'Subch':
                print('--', vd['Main text'][i], '--')
            elif vd.Structure[i] == 'Col':
                print('||', vd['Main text'][i], '||')
            else:
                print(vd['Main text'][i])


def txt_output_with_app(vd):
    def print_variants(i):
            if vd['In pada'][i] != '':
                padas = vd['In pada'][i].split(":")
                lemmata = vd['Lemmata'][i].split(":")
                variants = vd['Variants'][i].split(":")
                mss = vd['MSS'][i].split(":")
                for l in range(len(lemmata)):
                    print('       ' + padas[l], bcolors.LEMMA + lemmata[l] + bcolors.NEUT + ']', 
                            bcolors.MSS +   mss[l] + '; ' + bcolors.VAR + variants[l], bcolors.NEUT)

    def print_transl(i):
            if vd['Translation'][i] != '':
                print('     ', bcolors.TR, vd['Translation'][i])

    for i in range(len(vd)):
            if vd['Verse number'][i] != '':
                vsnum = "||" + str(int(vd.Chapter[i])) + "." + str(int(vd['Verse number'][i])) + "||"
            # end of verse
            if vd.Structure[i] == 'cd' or vd.Structure[i] == 'ef' or vd.Structure[i] == 'd':
                print(bcolors.MAIN + vd['Main text'][i] + bcolors.VEG, vsnum, bcolors.NEUT)
                print_variants(i)
                print_transl(i)
            elif vd.Structure[i] == 'Ch':
                print(bcolors.CH + '[', vd['Main text'][i].upper(), ']', bcolors.NEUT)
            elif vd.Structure[i] == 'Subch':
                print(bcolors.SCH + '[', vd['Main text'][i], ']', bcolors.NEUT)
            elif vd.Structure[i] == 'Col':
                print('||', vd['Main text'][i], '||')
            else:
                print(bcolors.MAIN + vd['Main text'][i], bcolors.VEG, '|')
                print_variants(i)
                print_transl(i)


def tex_output(vd):

    def print_header():
        print("\\newcommand{\\dnapp}[1]{}\\newcommand{\\rmapp}[1]{#1} \\fejno=0\\versno=0 \\ujfej\\szam\\bek")

    def print_variants(i):
            if vd['In pada'][i] != '':
                padas = vd['In pada'][i].split(":")
                #lemmata = vd['Lemmata'][i].split(":")
                variants = vd['Apparatus'][i].split(":")
                #mss = vd['MSS'][i].split(":")
                print('     \\var{', variants, '}%')

    def print_parallels(i):
            if vd['Parallels'][i] != '':
                print('     \\paral{\\v' + vd['Parallel for pada'][i], vd['Parallels'][i] + '}%')

    print_header()
    for i in range(len(vd)):
            if vd['Verse number'][i] != '':
                vsnum = "||" + str(int(vd.Chapter[i])) + "." + str(int(vd['Verse number'][i])) + "||"
            # end of verse
            if vd.Structure[i] == 'cd' or vd.Structure[i] == 'ef':
                print(vd['Main text'][i], '\\veg \\dontdisplaylinenum\n')
            if vd.Structure[i] == 'd':
                print('\ \ ', vd['Main text'][i], '\\veg \\dontdisplaylinenum\n')
            elif vd.Structure[i] == 'Ch':
                print('\\alfejezet{', vd['Main text'][i], '}\n')
            elif vd.Structure[i] == 'Subch':
                print('\\alalfejezet{', vd['Main text'][i], '}\n')
            elif vd.Structure[i] == 'uv' or vd.Structure[i] == 'cd*':
                print(vd['Main text'][i] + '{\\danda}\\dontdisplaylinenum\n' )
            elif vd.Structure[i] == 'Col':
                print('||', vd['Main text'][i], '||\n')
            elif vd.Structure[i] == 'ab':
                print(vd['Main text'][i], '\\thinspace{\\dandab} \dontdisplaylinenum\n')
            elif vd.Structure[i] == 'b':
                print('\ \ ', vd['Main text'][i], '\\thinspace{\\dandab} \dontdisplaylinenum\n')
            elif vd.Structure[i] == 'a' or vd.Structure[i] == 'c':
                print(vd['Main text'][i], '\n')
            print_variants(i)
            print_parallels(i)

def sandhi(vd):
    def apply_sandhi(text):
        for i in range(len(cons_clusters)):
            text = re.sub(cons_clusters[i][0] + " " + cons_clusters[i][1], cons_clusters[i], text) 
        for i in range(len(cons_vowel_comb)):
            text = re.sub(cons_vowel_comb[i][0] + " " + cons_vowel_comb[i][1], cons_vowel_comb[i], text) 
        print(text)

    vowels = ['a', 'i', 'u', 'ṛ', 'e', 'o']
    consonants =['k', 'g', 'ṅ', 'c', 'j', 'ñ', 'ṭ', 'ḍ', 'ṇ', 't', 'd', 'n', 'p', 'b', 'm',
                    'y', 'r', 'l', 'v', 'ś', 'ṣ', 's', 'h']
    cons_clusters = []
    cons_vowel_comb = []
    for i in range(len(consonants)):
        for j in range(len(consonants)):
            cons_clusters.append(consonants[i] + consonants[j])
    for i in range(len(consonants)):
        for j in range(len(vowels)):
            cons_vowel_comb.append(consonants[i] + vowels[j])

    for i in range(len(vd)):
        apply_sandhi(vd['Main text'][i])



def tex_dn_output(vd):

    #print(vd['Main text'])
    vd['Main text'] = vd['Main text'].apply(lambda x: "{\\dn " + velthview(sandhi(x)) + "}")

    def print_header():
        print("\\renewcommand{\\rmapp}[1]{}\\renewcommand{\\dnapp}[1]{#1}")
        print("\\renewcommand{\\mntr}[1]{\mntrdn{#1}}")
        print("\\fejno=0\\versno=0 \\ujfej\\szam\\bek")

    def print_variants(i):
            if vd['In pada'][i] != '':
                padas = vd['In pada'][i].split(":")
                lemmata = vd['Lemmata'][i].split(":")
                variants = vd['Variants'][i].split(":")
                mss = vd['MSS'][i].split(":")
                for l in range(len(lemmata)):
                    print('     \\var{\\v' + padas[l], lemmata[l] + '\lem', 
                                mss[l] + ';', variants[l] + '}%')

    def print_parallels(i):
            if vd['Parallels'][i] != '':
                print('     \\paral{\\v' + vd['Parallel for pada'][i], vd['Parallels'][i] + '}%')

    print_header()
    for i in range(len(vd)):
            if vd['Verse number'][i] != '':
                vsnum = "||" + str(int(vd.Chapter[i])) + "." + str(int(vd['Verse number'][i])) + "||"
            # end of verse
            if vd.Structure[i] == 'cd' or vd.Structure[i] == 'ef':
                print(vd['Main text'][i], '\\vegdn \\dontdisplaylinenum\n')
            if vd.Structure[i] == 'd':
                print('\ \ ', vd['Main text'][i], '\\vegdn \\dontdisplaylinenum\n')
            elif vd.Structure[i] == 'Ch':
                print('\\alfejezet{', vd['Main text'][i], '}\n')
            elif vd.Structure[i] == 'Subch':
                print('\\alalfejezet{', vd['Main text'][i], '}\n')
            elif vd.Structure[i] == 'uv' or vd.Structure[i] == 'cd*':
                print(vd['Main text'][i] + '{\\dandadn}\\dontdisplaylinenum\n' )
            elif vd.Structure[i] == 'Col':
                print('{\dn ||}', vd['Main text'][i], '{\dn ||}\n')
            elif vd.Structure[i] == 'ab':
                print(vd['Main text'][i], '\\thinspace{\\dandabdn} \dontdisplaylinenum\n')
            elif vd.Structure[i] == 'b':
                print('\ \ ', vd['Main text'][i], '\\thinspace{\\dandabdn} \dontdisplaylinenum\n')
            elif vd.Structure[i] == 'a' or vd.Structure[i] == 'c':
                print(vd['Main text'][i], '\n')
            print_variants(i)
            print_parallels(i)

def sandhi(line):
    def apply_sandhi(text):
        for i in range(len(cons_clusters)):
            text = re.sub(cons_clusters[i][0] + " " + cons_clusters[i][1], cons_clusters[i], text) 
        for i in range(len(cons_vowel_comb)):
            text = re.sub(cons_vowel_comb[i][0] + " " + cons_vowel_comb[i][1], cons_vowel_comb[i], text) 
        return text

    vowels = ['a', 'ā', 'i', 'ī', 'u', 'ū', 'ṛ', 'ṝ', 'e', 'o']
    consonants =['k', 'g', 'ṅ', 'c', 'j', 'ñ', 'ṭ', 'ḍ', 'ṇ', 't', 'd', 'n', 'p', 'b', 'm',
                    'y', 'r', 'l', 'v', 'ś', 'ṣ', 's', 'h']
    cons_clusters = []
    cons_vowel_comb = []
    for i in range(len(consonants)):
        for j in range(len(consonants)):
            cons_clusters.append(consonants[i] + consonants[j])
    for i in range(len(consonants)):
        for j in range(len(vowels)):
            cons_vowel_comb.append(consonants[i] + vowels[j])

    return apply_sandhi(line)


def velthview(line):
	# convert Unicode line to Velthuis
        subdict ={'ā': 'aa', 
                    "'": '.a', 
                    'ī': 'ii', 
                    'ū': 'uu', 
                    'ṛ': '.r', 
                    'r̥': '.r', 
                    'ṝ': '.R',
                    '\\\d{\\\=r}': '.R', 
                    'ḷ': '.l', 
                    'l̥': '.l', 
                    'ḹ': '.L', 
                    '\\\d{\\\=l}': '.L', 
                    'ṅ': '\"n',
                    'ñ': '~n', 
                    'ṭ': '.t', 
                    'ḍ': '.d', 
                    'ṇ': '.n', 
                    'ś': '\"s',
                    'ṣ': '.s', 
                    'ṃ': '.m', 
                    'ṁ': '.m', 
                    'ḥ': '.h',
                    'Ó': '.o',
                    '°': '@'} 
        for c in subdict:
            line = re.sub(c, subdict[c], line)
        return line


def putmyfile_into_pandas(filename):
    loc = -1
    # the pandas dataframe for the text
    vd = pd.DataFrame(columns=('Chapter', 'Verse number', 'Structure', 'Verse form', 'Main text', 'Apparatus', 'Parallels', 'Translation'))
    chapter = 0
    vsnum = 0
    pdvsnum = 0
    anustubh = False
    hemistich = 0
    textflag = False
    appflag = False
    paralflag = False
    proseflag = False
    trflag = False
    vsform = ''
    openfile = open(filename, "r")
    for line in openfile:
        if '%' == line[0]:
            textflag = False
        if '<NEWCHAPTER/>' in line:
                chapter += 1
                vsnum = 1
                pdvsnum = 1
        if '<NOTANUSTUBH/>' in line:
            anustubh = False 
            proseflag = False
            hemistich = 0
            vsform = 'non-anuṣṭubh'
        if '<ANUSTUBH/>' in line:
            anustubh = True
            proseflag = False
            hemistich = 0
            vsform = 'anuṣṭubh'
        if '<PROSE>' in line:
            proseflag = True
            vsform = 'prose'
        if '</PROSE>' in line:
            proseflag = False
            vsform = ''
        if '<TEXT>' in line or textflag == True:
            loc += 1
            pdvsnum = vsnum 
            textflag = True
            if '<COLOPHON>' in line:
                vsform = ''
            if '</TEXT>' in line:
                textflag = False
            if '||' in line:
                pdvsnum = vsnum
                chap_and_vsnum = (str(chapter) + "." + str(vsnum) + "||") 
                vsnum += 1
            else:
                chap_and_vsnum = "" 
            v01 = re.sub('<TEXT> ?', '', line[:-1])
            v01 = re.sub('\|\*', '|', v01)
            #v01 = re.sub('\-', '|', v01)
            v01 = re.sub('</TEXT>.*', chap_and_vsnum, v01)
            v01 = re.sub('{ }', " ", v01)
            v01 = re.sub('<COLOPHON>', "\n||", v01)
            v01 = re.sub('</COLOPHON>', "||", v01)
            v01 = re.sub('<uvaca>', '', v01)
            v01 = re.sub('</uvaca>', '', v01)
            #print(v01)
            # Structure
            struc = ''
            # end of normal śloka
            if '||' in line and anustubh == True and proseflag == False and hemistich == 1:
                hemistich = 0
                struc = 'cd'
            elif '||' in line and anustubh == True and proseflag == False and hemistich == 2:
                hemistich = 0
                struc = 'ef'
            elif '||' in line and anustubh == False and proseflag == False:
                hemistich = 0
                struc = 'd'
            # special danda: it does not increase verse number, e.g. after devy uvāca
            elif '|*' in line and proseflag == False:
                struc = 'uvaca'
                vsform = 'uvāca-line'
            # with anuṣṭubh, a danda increases verse number if it is the first single danda
            elif '|' in line and hemistich == 0 and anustubh == True and proseflag == False:
                hemistich = 1 
                struc = 'ab'
            # if this is a first single danda but it is not anuṣṭubh, don't increase verse number    
            elif '|' in line and anustubh == False and proseflag == False and hemistich == 1:
                hemistich = hemistich + 1 
                struc = 'b'
            elif '|' in line and hemistich > 0 and anustubh == True and proseflag == False:
                hemistich = hemistich + 1 
                struc = 'cd'
            # check if this is a non-anuṣṭubh first line
            elif '|' not in line and hemistich == 0 and anustubh == False and proseflag == False:
                # no indent
                hemistich = 1
                struc = 'a'
            elif '|' not in line and hemistich == 2 and anustubh == False and proseflag == False:
                # no indent
                hemistich = hemistich + 1
                struc = 'c'
            elif '<COLOPHON>' in line:
                struc = 'colophon'
            # put it into dataframe
            if proseflag == True:
                vd.loc[loc] = [str(chapter)] + [''] + [struc] + [vsform] + [v01] + [''] + [''] + ['']
            else:
                vd.loc[loc] = [str(chapter)] + [str(pdvsnum)] + [struc] + [vsform] + [v01] + [''] + [''] + ['']
            print('Verse', str(chapter) + '.' + str(pdvsnum), 'processed')
            if struc  == 'uvaca':
                # back to default
                vsform = '' 
        if '<APP>' in line or '<PVAR>' in line or appflag == True:
            appflag = True
            v01 = re.sub('<APP> ?', '[', line[:-1])
            v01 = re.sub('<PVAR> ?', '[', v01)
            if '</APP>' in line or '</PVAR>' in line:
                appflag = False
            v01 = re.sub(' ?</APP>', '', v01)
            v01 = re.sub(' ?</PVAR>', '', v01)
            v01 = re.sub('{ }', " ", v01)
            v01 = re.sub('<LEM>', '', v01)
            v01 = re.sub('</LEM>', ']', v01)
            v01 = re.sub('ṝ', '\\\d{\\\=r}', v01)
            v01 = re.sub('ḹ', '\\\d{\\\=l}', v01)
            v01 = re.sub('\\Ł', '', v01)
            v01 = re.sub('\\$', '', v01)
            v01 = re.sub('\\\\csa', '{ā}', v01)
            #v01 = re.sub('\|', '{\\\\danda}', v01)
            #print(v01)
            amivan = vd.loc[[loc], ['Apparatus']] 
            vd.loc[[loc], ['Apparatus']] = amivan + v01
        if '<PARAL>' in line or paralflag == True:
            paralflag = True
            if '</PARAL>' in line:
                paralflag = False
            v01 = re.sub('{ }', " ", line)
            v01 = re.sub('<PARAL>', '', v01[:-1])
            v01 = re.sub('</PARAL>', '', v01)
            v01 = re.sub('{ }', " ", v01)
            v01 = re.sub('\\Ł', '', v01)
            v01 = re.sub('\\$', '', v01)
            #v01 = re.sub('\|\|', '{\\\\thinspace\ketdanda}', v01)
            #v01 = re.sub('\|', '{\\\\thinspace\danda}', v01)
            #print(v01)
            amivan = vd.loc[[loc], ['Parallels']] 
            vd.loc[[loc], ['Parallels']] = amivan + v01
        if '<TR>' in line or trflag == True:
            trflag = True
            if '</TR>' in line:
                trflag = False
            v01 = re.sub('{ }', " ", line[:-1])
            v01 = re.sub('<TR>', '', v01)
            v01 = re.sub('</TR>', '', v01)
            v01 = re.sub('{ }', " ", v01)
        #    v01 = re.sub('\\Ł', '', v01)
        #    v01 = re.sub('\\$', '', v01)
        #    #v01 = re.sub('\|\|', '{\\\\thinspace\ketdanda}', v01)
        #    #v01 = re.sub('\|', '{\\\\thinspace\danda}', v01)
            #print(v01)
            amivan = vd.loc[[loc], ['Translation']] 
            vd.loc[[loc], ['Translation']] = amivan + v01
        if '<SUBCHAPTER>' in line:
            vsform = ''
            v01 = re.sub('<SUBCHAPTER>', '', line[:-1])
            v01 = re.sub('</SUBCHAPTER>', '', v01)
            v01 = re.sub('{ }', " ", v01)
            loc += 1
            vd.loc[loc] = [str(chapter)] + [''] + ['subchapter'] + [vsform] + ["[" + v01 + "]"] + [''] + [''] + ['']
            vsform = 'anuṣṭubh'
        if '<CHAPTER>' in line:
            vsform = ''
            v01 = re.sub('<CHAPTER>', '', line[:-1])
            v01 = re.sub('</CHAPTER>', '', v01)
            v01 = re.sub('{ }', " ", v01)
            loc += 1
            vd.loc[loc] = [str(chapter)] + [''] + ['chapter'] + [vsform] + [v01] + [''] + [''] + ['']
            vsform = 'anuṣṭubh'
        if 'metre=' in line:
            v01 = re.sub('.*metre=', '', line[:-1])
            v01 = re.sub(' .*', '', v01)
            vsform = v01
    openfile.close()
    vd.to_csv(outputfilename, sep="Đ")
#    vd.to_csv("/home/csaba/indology/dharma_project/vrsa_edition/sivadharmottara_written.csv", sep="Đ")


#vd = pd.read_excel("/home/csaba/indology/dharma_project/vrsa_edition/vrsa_written.xlsx", 
                    #sheet_name="Ch11", skiprows=range(0), skip_footer=0) 
#vd = vd.replace(np.nan, '', regex=True)
#txt_output_with_app(vd)
#tex_output(vd)
#sandhi(vd)
#tex_dn_output(vd)

#filename = "/home/csaba/indology/dharma_project/sivadharma/vrsasarasamgraha.xml"
#filename = "/home/csaba/indology/dharma_project/readings/dominic/sivadharmottara10.xml"
#filename = "/home/csaba/indology/dharma_project/nat_edition/nat2019.xml"

inputfilename = sys.argv[1]
outputfilename = sys.argv[2]
putmyfile_into_pandas(inputfilename)









