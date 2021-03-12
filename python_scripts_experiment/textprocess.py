#!/usr/bin/python3
# to allow local xml - xsl files display in firefox:
# about:config -->
# set security.fileuri.strict_origin_policy to False

# regex:
import re
# for the commandline arguments:
import sys
# Tamil modules
#import tamil.txt2unicode

# my modules:
from textprocess import txt_output
from textprocess import tex_output
from textprocess import tex_dn_output
#from textprocess import velthview_with_rm
from textprocess import translation
from textprocess import xml_output
from textprocess import xml_output_wrap
from textprocess import xml_output_dn
from textprocess import onlytranslation
from textprocess import simpletxtdn
from textprocess import app_check
from textprocess import velth
from textprocess import uni
from textprocess import line_to_dn
from textprocess import trtex
from textprocess import change_sigla 
from textprocess import html_scroll 


# do I use this?
def sandhi(text, cons_clusters, cons_vowel_comb):
    for i in range(len(cons_clusters)):
            text = re.sub(cons_clusters[i][0] + " " + cons_clusters[i][1], cons_clusters[i], text) 
    for i in range(len(cons_vowel_comb)):
            text = re.sub(cons_vowel_comb[i][0] + " " + cons_vowel_comb[i][1], cons_vowel_comb[i], text) 
    return text

# do I use this?
def generate_sandhi_rules():
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
    return (cons_clusters, cons_vowel_comb)

# not yet tested
def text_output02(filename):
    import xml.dom.minidom
    DOMTree = xml.dom.minidom.parse("output01.xml")
    collection = DOMTree.documentElement
    texts = collection.getElementsByTagName("TEXT")
    for text in texts:
        print(text.childNodes[0].data, end="")
        num = text.getElementsByTagName('vsnum')
        if not num:
                print()
        else:		
                for n in num:
                    print(n.childNodes[0].data + "||")
    '''
    for a in apps:
	print(a.childNodes[0].data, end="")
	lems = a.getElementsByTagName("LEM")
	for l in lems:
		print(l.childNodes[0].data)
    '''



#filename = '/home/csaba/indology/skt/saiva/sivadharma/vrsasarasamgraha.txt'
#filename = '/home/csaba/indology/dharma_project/nat2019.txt'

if len(sys.argv) == 2 and sys.argv[1] == '-help':
    print("Usage:\n python3 textprocess.py -argument filename\nor\n textprocess.py -argument filename\nor rather\n python3 textprocess.py -argument filename > outputfilename.xml/pdf/whatever \n\nArguments:\n-help: print this list\n-txt: print main text as plain text\n-txtdn: print main text in Devanagari as plain text\n-velth: print main text in Velthuis\n-scroll: produce a html version (CURRENT)\n-xml1: produce an xml file in Roman with the apparatus entries closed\n-xml2: produce an xml file in Roman with the apparatus entries open\n-xml3: produce an xml file with the apparatus entries appearing when mouse is over text\n-xmldn1: produce an xml file in Devanagari with the apparatus entries closed\n-xmldn2: produce an xml file in Devanagari with the apparatus entries open\n-texdn: TeX output in Devanagari\n-texrm: TeX output in Roman\n-tr: print translation as plain text\n-sktandtr: print Sanskrit text and translation as plain text\n-trtex: produce a TeX file containing the translation and notes\n-appcheck: check if there are missing sigla")
    print()
    print("Required input format:")
    print("<START/>")
    print("<NEWCHAPTER/>")
    print("<TEXT> dhṛtarāṣṭra uvāca|*</TEXT>")
    print("<TEXT> dharmakṣetre kurukṣetre samavetā yuyutsavaḥ|</TEXT>")
    print("<TEXT> māmakāḥ pāṇḍavāś{ }caiva kim{ }akurvata sañjaya||</TEXT>")
    print("    <APP>\\vc <LEM>māmakāḥ</LEM> \msA; māmaka \msB, mamakāḥ \msC\oo")
    print("              <LEM>pāṇḍa°<LEM> \msA; pāṇḍu° \msB\msC</APP>")
    print("    <TR>This is the place for the translation...</TR>")
    print("    <NOTE>This is the place for the notes...</NOTE>")
    print()
    print("Use |* for lines with `uvāca' for correct line numbering. For the correct TeX output, the MSS sigla should be defined in the macro file. \oo in the input is just for a dot dividing entries in the same pāda. { } are just to facilitate sandhi in Devanāgarī output.")
    print()
    print("To capture the output of this program, use this format e.g.: ")
    print("textprocess -texrm inputfilename > filenametosaveoutput.tex")
    quit()
elif len(sys.argv) != 3:
    print("Too few or too many arguments!")
    quit()

filename = sys.argv[2]


if sys.argv[1] == '-texdn': 
    tex_dn_output.tex_dn_output(filename)
elif sys.argv[1] == '-texrm': 
    tex_output.tex_output(filename)
elif sys.argv[1] == '-txt': 
    txt_output.txt_output(filename)
elif sys.argv[1] == '-txtdn': 
    simpletxtdn.simpletxtdn(filename)
elif sys.argv[1] == '-sktandtr': 
    translation.translation(filename)
elif sys.argv[1] == '-tr': 
    onlytranslation.onlytranslation(filename)
elif sys.argv[1] == '-velth': 
    velth.velth(filename)
elif sys.argv[1] == '-xml1': 
    xml_output.xml_output(filename, 1)
elif sys.argv[1] == '-xml2': 
    xml_output.xml_output(filename, 2)
elif sys.argv[1] == '-xml3': 
    xml_output_wrap.xml_output(filename, 1)
elif sys.argv[1] == '-xml4': 
    xml_output_wrap.xml_output(filename, 2)
elif sys.argv[1] == '-scroll': 
    html_scroll.html_scroll(filename, 1)
elif sys.argv[1] == '-xmldn': 
    xml_output_dn.xml_output_dn(filename,1)
elif sys.argv[1] == '-xmldn1': 
    xml_output_dn.xml_output_dn(filename,1)
elif sys.argv[1] == '-xmldn2': 
    xml_output_dn.xml_output_dn(filename,2)
elif sys.argv[1] == '-uni': 
    uni.uni(sys.argv[2])
elif sys.argv[1] == '-appcheck': 
    app_check.app_check(filename)
elif sys.argv[1] == '-trtex': 
    trtex.trtex(filename)
# mainly for vim and command line:
elif sys.argv[1] == '-line2dn': 
    line_to_dn.line_to_dn(sys.argv[2])
else:
    print("Usage: textprocess.py [-help|-txt|-txtdn|-texrm|-texdn|-velth|-scroll|-tr|-sktandtr|-trtex|-xml1|-xml2|-xml3|-xmldn1|xmldn2|-appcheck]")
