import re

def change_sigla(line):
    subdict ={'\\\\msNC45': '\\\\msNCfortyfive',
              '\\\\msNK82':  '\\\\msNKeightytwo',
              '\\\\msNCA12':  '\\\\msNCAtwelve',
              '\\\\msNK28':  '\\\\msNktwentyeight',
              '\\\\msNKo77':  '\\\\msNKoseventyseven',
              '\\\\msNKA12':  '\\\\msNKAtwelve',
              '\\\\msGP43':  '\\\\msGPfortythree',
              '\\\\msGP74':  '\\\\msGPseventyfour'}
    for c in subdict:
        line = re.sub(c, subdict[c], line)
    return line
