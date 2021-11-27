import re
from textprocess import devanagari_characters




def checkIfTagOrCommand(char, tagFlagOn, commandFlagOn, englishFlagOn):
            if char == '<':
               tagFlagOn = True
            elif char == '>':
               tagFlagOn = False
            elif char == '\\':
               commandFlagOn = True
            elif char == ' ':
               commandFlagOn = False   
            elif char == 'Ł':
               englishFlagOn = True   
            elif char == '$':
               englishFlagOn = False   
            return (tagFlagOn, commandFlagOn, englishFlagOn)
            
                            

def main(line):
    line = re.sub("{ }", "", line)
    #print("ITT:", line)
    tagFlagOn = False
    commandFlagOn = False
    englishFlagOn = False
    dic, vowels, consonants = devanagari_characters.devanagari_characters()
    def preprocessing(inputline,vowels,consonants):
            # print(inputword)
            # to make double letter one
            # trick : "|" becomes " |" to handle final virama
            preprocessingChars = [('ai', 'đ'), ('au', 'ő'), ('kh', 'K'), ('gh', 'G'), ('ṭh', 'Ṭ'), ('ḍh', 'Ḍ'), ('th', 'T'), ('dh', 'D'),('ph', 'P'), ('bh', 'B'), ('ch', 'C'), ('jh', 'J'), ('\|', ' |'), ('\| \|', '||'), (",", " ,")]
            # to handle final virama if there is no danda
            inputline = inputline + "  "
            # turning double characters such as 'ai' and 'gh' into single special characters:
            for p in preprocessingChars:
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
    #line = line.lower()
    # turning some Roman characters back from the Dharma compliant forms for Devanāgarī conversion:
    line = re.sub("ṁ", "ṃ", line)
    # first ṝ, then ṛ, to avoid a bug
    line = re.sub("r̥̄", "ṝ", line)
    line = re.sub("r̥", "ṛ", line)
    line = re.sub("l̥", "ḷ", line)
    # crux in main line
    line = re.sub("<crux>", "†", line)
    line = re.sub("</crux>", "‡", line)
    line = re.sub('\\\\csi', 'ि', line)    
    line = preprocessing(line,vowels,consonants)
    conj = False
    lineout = ''
    # putting the Devanagari characters together
    i = 0
    while i < len(line):
            tagFlagOn, commandFlagOn, englishFlagOn = checkIfTagOrCommand(line[i], tagFlagOn, commandFlagOn, englishFlagOn)
            if tagFlagOn == True or commandFlagOn == True or englishFlagOn == True:
                    lineout = lineout + line[i]
                    i += 1
                    continue
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
                    conj = True
                    lineout = lineout + line[i]
            # half consonant: put in a virāma
            elif conj == True and line[i] in consonants:
                    lineout = lineout + "V" + line[i]
            # non-initial vowel: nothing special to do
            elif conj == True and line[i] in vowels:
                    conj = False
                    lineout = lineout + line[i]
            # anything else:
            else:
                    #print(letter, end='')
                    lineout = lineout + line[i]
                    conj = False
            i += 1

    returnLine = ""
    for character in lineout:
            found = False
            tagFlagOn, commandFlagOn, englishFlagOn = checkIfTagOrCommand(character, tagFlagOn, commandFlagOn, englishFlagOn)
            if tagFlagOn == True or commandFlagOn == True or englishFlagOn == True:
                    returnLine = returnLine + character
                    continue         
            #check if it is a Devanāgarī character
            for d in dic:
                    if d == 'z':
                       assert False
                    if character == d[0] and tagFlagOn == False and commandFlagOn == False:
                            returnLine = returnLine + d[1]
                            found = True
                            break
            # if not in list of Devanāgarī characters:
            if found == False:
                    returnLine = returnLine + character
    return returnLine

