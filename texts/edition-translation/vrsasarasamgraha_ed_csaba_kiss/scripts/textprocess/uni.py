import re

def uni(line):
	# convert Velthuis to Unicode
        subdict ={'aa': 'ā', 
            '\.a':  "'", 
            'ii':   'ī', 
            'uu':   'ū', 
            '\.r':   'ṛ', 
            '\.R':   'ṝ',
            '\.l':   'ḷ', 
            '\.L':   'ḹ', 
            '\"n':   'ṅ',
            '\~n':  'ñ', 
            '\.t':  'ṭ', 
            '\.d':  'ḍ', 
            '\.n':  'ṇ', 
            '\"s':  'ś',
            '\.s':  'ṣ', 
            '\.m':  'ṃ', 
            '\.h':  'ḥ'
                    } 
        for c in subdict:
            line = re.sub(c, subdict[c], line)
        print(line)
        return line

