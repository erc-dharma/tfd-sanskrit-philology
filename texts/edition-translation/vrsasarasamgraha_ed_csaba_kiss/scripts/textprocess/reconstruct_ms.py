# reconstruct the readings of a given ms 
import re
import sys

class bcolors:
	VAR = '\033[91m'
	YELLOW = '\033[93m'
	WHITE = '\033[0m'
	LEMCOLOR = '\033[92m'
	'''
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	'''

chapter = 0
vsnum = 0
counter = 0
textflag = False
onflag = False
appflag = False
full_variant_line = ""
highlighted_ed_text = ""
printout_last_line = False

# CHANGE THIS AS YOU LIKE
mss_2_reconstruct = "#msCb"



filename = sys.argv[1] 
if filename != "-help":
    if len(sys.argv) == 3:
        mss_2_reconstruct = sys.argv[2]
    openfile = open(filename, "r")
else:
    print("Usage: python3 reconstruct_mss.py filename ['#msSiglum']\nor:    python3 reconstruct_mss.py filename ['#msSiglum'] | less -R")
    quit()

print("Reconstructing", mss_2_reconstruct)
print()

# preprocess
tempfile = open("tempfile.txt","w") 
for line in openfile:
    # unfold abbreviated/groupped MS sigla
    re.sub("\\\\mssCaCbCc", "\\\\msCa\\\\msCb\\\\msCc", line)

    '''
    # Dharma transliteration tricks
    line = re.sub("ṃ", "ṁ", line)
    line = re.sub("ṛ", "r̥", line)
    line = re.sub("ṝ", "r̥̄", line)
    line = re.sub("ḷ", "l̥", line)
    line = re.sub("Ṃ", "Ṁ", line)
    line = re.sub("Ṛ", "R̥", line)
    line = re.sub("Ṝ", "R̥̄", line)
    line = re.sub("Ḷ", "L̥", line)
    '''
    line = re.sub("<crux>", "†", line)
    line = re.sub("</crux>", "†", line)

    if ('<APP>' in line or appflag == True) and '</APP>' not in line:
        appflag = True
        # make separate entries from bits divided with \oo
        mod_line = re.sub('\\\\oo', '</APP><APP>', line)
        mod_line = re.sub('\n', '', mod_line)
        mod_line = re.sub('</APP><APP>', '</APP>\n<APP>', mod_line)
        mod_line = mod_line.strip()
        tempfile.write(mod_line)
    else:
        # if not APP entry at all
        tempfile.write(line)
        appflag = False
tempfile.close()



openfile = open("tempfile.txt", "r")
justStarted = True
for line in openfile:
    if '<START/>' in line:
        onflag = True
    if '<STOP/>' in line:
        onflag = False
        printout_last_line = True
    # TeX-type comments
    if '%' == re.sub('^ *', '', line)[0]:
        textflag = False
        line = ''
    if '<startchapter-n="' in line:
        c = re.sub('.*<startchapter-n="', '', line)
        c = re.sub('".*', '', c)
        chapter = int(c) 
        vsnum = 0
        # hemistich = 0
    if ('<TEXT>' in line or textflag == True) and (onflag == True or printout_last_line == True):
        textflag = True
        printout_last_line = False
        if '</TEXT>' in line:
            textflag = False
        if '||' in line:
            vsnum += 1
            chap_and_vsnum = (str(chapter) + "." + str(vsnum) + "||") 
        else:
            chap_and_vsnum = "" 
        v01 = re.sub('<TEXT> ?', '', line[:-1])
        v01 = re.sub('\|\*', '|', v01)
        v01 = re.sub('\-', '|', v01)
        v01 = re.sub('</TEXT>.*', chap_and_vsnum, v01)
        v01 = re.sub('{ }', " ", v01)
        v01 = re.sub('{-}', " ", v01)
        v01 = re.sub('<COLOPHON>', "\n||", v01)
        v01 = re.sub('</COLOPHON>', "||", v01)
        v01 = re.sub('<uvaca>', '', v01)
        v01 = re.sub('</uvaca>', '', v01)
        v01 = re.sub('<MNTR>', '', v01)
        v01 = re.sub('</MNTR>', '', v01)
        storeLine = v01
        # variant previous line, if any, of given MS
        print(highlighted_ed_text) # comment this out to hide readings of the crit. ed.
        if justStarted != True:
            print(full_variant_line, "  in:", mss_2_reconstruct)
        highlighted_ed_text = storeLine
        justStarted = False
        # first the MS line looks like the crit. edited line; we'll modify it later
        full_variant_line = v01
    if '<SUBCHAPTER>' in line and onflag == True:
        v01 = re.sub('<SUBCHAPTER>', '\n---- ', line)
        v01 = re.sub('</SUBCHAPTER>', ' ----', v01)
        print(v01)

    if ('<APP>' in line or appflag == True) and onflag == True:
        appflag = True
        #line = re.sub('\\\\oo', '</APP><APP>', line)
        line = re.sub('<APP>\ ?\ ?\n', '<APP>', line)

        # LEMMA
        lem_wit = '' 
        # find pada if it is a, b, c or d in a śloka
        if '\\vo ' in line:
            app_pada = ""
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
        # you have to have 'type' and not 'wit' if it is eme, corr or conj
        if '\eme' in lem_wit or '\corr' in lem_wit or '\conj' in lem_wit:
            lem_wit = re.sub('\\\\', '', lem_wit)[:-1]
            not_a_witness = True
        else:
            lem_wit = re.sub('\\\\', ' #', lem_wit)[:-1]
            not_a_witness = False
        lem_wit = re.sub('^ ', '', lem_wit)

        v01 = re.sub('^.*<APP>', '', line)
        v01 = re.sub('.*<LEM>', '', v01)
        v01 = re.sub('</LEM>.*', '', v01)
        v01 = re.sub("{ }", " ",  v01)
        v01 = re.sub("{-}", " ",  v01)
        finallemma = re.sub("°", "",  v01).strip()

        # variants, already in one line, see above
        if '<LEM>' in line:
            variants = re.sub('.*;', '', line)
        else:
            variants = line
        variants = re.sub('</APP>', '', variants)
        variants = re.sub('\n', '', variants)
        variants_list = variants.split(",")
        # in order to print out last line
        for var in variants_list:
            sigla = re.sub('.* \\\\', '\\\\', var)
            sigla = re.sub(' *', '', sigla)
            sigla = re.sub('\\\\', ' #', sigla)
            # strip to get rid of some trailing spaces
            skt = re.sub('\\\\om', '[omitted]', var.strip())
            skt = re.sub('\\\\.*', '', skt).strip()
            #skt = xml_substitutions(skt) 
            skt = re.sub('{ }', " ", skt)
            skt = re.sub('°', "", skt)
            skt = re.sub("<UNCL>", "≀", skt)
            skt = re.sub("</UNCL>", "≀", skt)


            if mss_2_reconstruct in sigla and mss_2_reconstruct not in lem_wit:
                counter += 1
                # if we have the lemma string twice in one line (special case)
                if highlighted_ed_text.count(finallemma) > 1:
                    offset = highlighted_ed_text.index(finallemma) + len(finallemma) + 1
                    # if we are in the first half of the line
                    if app_pada == 'a' or app_pada == 'c' or app_pada == 'e':
                        highlighted_ed_text = re.sub(finallemma, bcolors.LEMCOLOR + finallemma.strip() + bcolors.WHITE, highlighted_ed_text[:offset]) + highlighted_ed_text[offset:]
                        full_variant_line = re.sub(finallemma, bcolors.VAR + skt + bcolors.WHITE, full_variant_line[:offset]) + full_variant_line[offset:] 
                    elif app_pada == 'b' or app_pada == 'd' or app_pada == 'f':
                        highlighted_ed_text = highlighted_ed_text[:offset] + re.sub(finallemma, bcolors.LEMCOLOR + finallemma.strip() + bcolors.WHITE, highlighted_ed_text[offset:])
                        full_variant_line = full_variant_line[:offset] + re.sub(finallemma, bcolors.VAR + skt + bcolors.WHITE, full_variant_line[offset:])
                        
                else:
                    #print("H: ", highlighted_ed_text)
                    highlighted_ed_text = re.sub(finallemma, bcolors.LEMCOLOR + finallemma + bcolors.WHITE, highlighted_ed_text) 
                    full_variant_line = re.sub(finallemma, bcolors.VAR + skt + bcolors.WHITE, full_variant_line) 
                    break
        

print()
print("[", counter, "differences between the critical edition and", mss_2_reconstruct, "]")
openfile.close()
