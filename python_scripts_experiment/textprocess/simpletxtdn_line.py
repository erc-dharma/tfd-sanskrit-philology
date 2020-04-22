import re
from textprocess import devanagari_characters

def simpletxtdn_line(line):
    dic, vowels, consonants = devanagari_characters.devanagari_characters()
    def preprocessing(inputline,vowels,consonants):
            # print(inputword)
            # to make double letter one
            # trick : "|" becomes " |" to handle final virama
            preprocessing = [('ai', 'đ'), ('au', 'ő'), ('kh', 'K'), ('gh', 'G'), ('ṭh', 'Ṭ'), ('ḍh', 'Ḍ'), ('th', 'T'), ('dh', 'D'),('ph', 'P'), ('bh', 'B'), ('ch', 'C'), ('jh', 'J'), ('\|', ' |'), ('\| \|', '||'), (",", " ,")]
            # to handle final virama if there is no danda
            inputline = inputline + "  "
            for p in preprocessing:
                    inputline = re.sub(p[0], p[1], inputline)
            # spaces, sandhi
            # list of characters separated
            s = list(inputline)
            i = 0
            # C + V should be written as conjunct 
            while i < len(s)-2:
                    if s[i] in consonants and s[i+1] == ' ' and s[i+2] in vowels:
                            s[i+1] = ''	
                    elif s[i] in consonants and s[i+1] == ' ' and s[i+2] in consonants:
                            s[i+1] = ''
                    i += 1
            # put them back together
            "".join(s)
            return s

    # first preprocess
    line = preprocessing(line,vowels,consonants)
    conj = False
    lineout = ''
    # putting the Devanagari characters together
    i = 0
    while i < len(line):
            # init vowel
            if conj == False and line[i] in vowels:
                    #print(letter.upper(), end='')
                    # if it is initial, make it capital
                    lineout = lineout + line[i].upper()
            # last consonant, put in virāma
            elif i < len(line)-2 and line[i] in consonants and line[i+1] == " ":
                    lineout = lineout + line[i] + "V"
            # syllable initial consonant, nothing special to do
            elif conj == False and line[i] in consonants:
                    #print(letter, end='')
                    conj = True
                    lineout = lineout + line[i]
            # half consonant: put in a virāma
            elif conj == True and line[i] in consonants:
                    #print("V" + letter, end='')
                    lineout = lineout + "V" + line[i]
            # non-initial vowel: nothing special to do
            elif conj == True and line[i] in vowels:
                    #print(letter, end='')
                    conj = False
                    lineout = lineout + line[i]
            # anything else:
            else:
                    #print(letter, end='')
                    lineout = lineout + line[i]
            i += 1
    ret_line = ""
    for character in lineout:
            found = False
            #check if it is a Devanāgarī character
            for d in dic:
                    if character == d[0]:
                            ret_line = ret_line + d[1]
                            found = True
                            break
            # if not in list of Devanāgarī characters:
            if found == False:
                    ret_line = ret_line + character
    return ret_line

