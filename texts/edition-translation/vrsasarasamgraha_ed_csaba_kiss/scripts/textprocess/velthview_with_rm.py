def velthview_with_rm(line, romanflag):
        #Now it works even if Ł and $ are not in the same line
        #romanflag = False 
        return_line = ""
        new_c = ""
        dharma_trans_dict = {"ṃ": "ṁ", 
                             "ṛ": "r̥", 
                             "ṝ": "r̥̄", 
                             "ḷ": "l̥",} 
        subdict ={'ā': 'aa', 
                    "'": '.a', 
                    'ī': 'ii', 
                    'ū': 'uu', 
                    'ṛ': '.r', 
                    'r̥': '.r', 
                    'ṝ': '.R',
                    'r̥̄': '.R',
                    'ḷ': '.l', 
                    'l̥': '.l', 
                    'ḹ': '.L', 
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
        for c in line:
            new_c = c
            if c == "Ł":
                romanflag = True
                new_c = "Ł"
            elif c == "$":
                romanflag = False
                new_c = "$"
            elif romanflag == False:
                if c in subdict:
                    new_c = subdict[c]
            elif romanflag == True:
                # Dharma transliteration tricks (XeLaTeX)
                if c in dharma_trans_dict:
                    new_c = dharma_trans_dict[c]
            return_line = return_line + new_c    
        return return_line, romanflag

