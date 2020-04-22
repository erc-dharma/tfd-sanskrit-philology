import re

def onlytranslation(filename):
    chapter = 0
    vsnum = 1
    vsnum_needed = True
    twodandas_just_passed = False
    textflag = False
    trflag = False
    openfile = open(filename, "r")
    for line in openfile:
        chap_and_vsnum = (str(chapter) + "." + str(vsnum)) 
        if '<TEXT>' in line:
            if '||' in line:
                vsnum += 1
                vsnum_needed = True
                twodandas_just_passed = True
            else:
                twodandas_just_passed = False
        if '<TR>' in line or trflag == True:
            trflag = True
            if '</TR>' in line:
                trflag = False
            v01 = re.sub('.*<TR>', '', line[:-1])
            v01 = re.sub('</TR>.*', ' ', v01)
            v01 = re.sub('^ *', '', v01)
            v01 = re.sub('\\\\', '', v01)
            # final white spaces
            v01 = v01.rstrip()
            if vsnum_needed == True and twodandas_just_passed == False:
                print("\n" + chap_and_vsnum, v01 )
                vsnum_needed = False
            else:
                    print(v01)
        if '<NEWCHAPTER/>' in line:
                chapter += 1
                vsnum = 1
    openfile.close()

