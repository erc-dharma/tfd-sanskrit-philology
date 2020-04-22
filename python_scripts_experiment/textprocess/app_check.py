import re

def app_check(filename):
    appflag = False
    app2check = ""
    # msBod not included
    print("Which project? VSS (v) or NĀT (n)?")
    reply = input()
    if reply == "v":
        allmss = ['msCa', 'msCb', 'msCc', 'msNa', 'msNb', 'msNc', 'msL', 'Ed']
    else:
        allmss = ['msA', 'msB', 'msC', 'msD', 'msE', 'msF']
    mss = [""]
    print("Which MSS' presence to check:")
    for i in range(len(allmss)):
        print("Check this (ENTER or n)?", allmss[i])
        reply = input()
        if reply != "n":
            mss.append(allmss[int(i)]) 
    openfile = open(filename, "r")
    tempfile = 'temp.txt'
    writefile = open(tempfile, "w")
    # to tackle separate entries in same pāda
    for line in openfile:
        line = re.sub('\\\\oo', '</APP>\n<APP>', line)
        # when I put variants of both pādas in one <APP></APP>:
        if appflag == True and '<APP>' not in line:
            line = re.sub('\\\\v', '</APP>\n<APP>', line)
        # to restore signlum of group to sigla of mss:
        line = re.sub('mssCaCbCc', 'msCamsCbmsCc', line)
        writefile.write(line)
    writefile.close()
    openfile = open(tempfile, "r")
    for line in openfile:
        if '<APP>' in line or appflag == True:
            appflag = True
            app2check = app2check + line
            if '</APP>' in line:
                appflag = False
                check = True
                for ms in mss:
                    if ms not in app2check:
                        check = False
                        print("PROBLEM: MS", ms, "is missing!")
                if check == True:
                        print("OK!")
                print(app2check)
                print("-"*20)
                app2check = ''
    openfile.close()

