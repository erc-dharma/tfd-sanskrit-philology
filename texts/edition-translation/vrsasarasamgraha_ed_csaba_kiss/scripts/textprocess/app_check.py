import re
import sys



def checkAcorrPcorr(app2check, mss2check, lineNum):
    corrProblem = 0
    for ms in mss2check:
        if (ms + 'acorr' in app2check and ms + 'pcorr' not in app2check) or (ms + 'pcorr' in app2check and ms + 'acorr' not in app2check):
               print("PROBLEM in line", str(lineNum) + ", " + ms + "acorr or pcorr is missing:")
               print(app2check)
               corrProblem += 1
    return corrProblem
    


def app_check(filename):
    print('[Usage: textprocess.py -appcheck filename "msA, msB, msC"]\n')
    appflag = False
    onflag = False
    if len(sys.argv) > 3:
        mss2check = re.sub(" ", "", sys.argv[3]).split(',') 
    else:
        mss2check = ['msCa', 'msCb', 'msCc', 'Ed']
    print("\nChecking the presence of these mss:", mss2check, "\n")
    app2check = ""
    openfile = open(filename, "r")
    tempfl = ""
    for line in openfile:
        line = re.sub('\\\\oo', '</APP>\nEXTRALINE<APP>', line)
        # when I put variants of both pādas in one <APP></APP>:
        if appflag == True and '<APP>' not in line:
            line = re.sub('\\\\v', '</APP>\nEXTRALINE<APP>', line)
        # to restore siglum of group to sigla of mss:
        line = re.sub('mssCaCbCc', 'msCamsCbmsCc', line)
        tempfl = tempfl + line
    problem = 0
    lineNum = 0
    for line in tempfl.split("\n"):
        lineNum += 1
        if 'EXTRALINE' in line:
            line = re.sub('EXTRALINE', '', line)
            lineNum -= 1
        if '<START/>' in line:
            onflag = True
        if '<STOP/>' in line:
            onflag = False
        if '<APP>' in line or appflag == True:
            appflag = True
            app2check = app2check + line
            if '</APP>' in line:
                appflag = False
                for ms in mss2check:
                    if ms not in app2check:
                        check = False
                        if onflag == True:
                            print("PROBLEM in line", str(lineNum) + ", " + ms, "is missing:")
                            print(app2check)
                            problem += 1
                problem = problem + checkAcorrPcorr(app2check, mss2check, lineNum)
                app2check = ''

    print("\nWe have been checking the presence of these mss:", mss2check)
    if problem == 0:
        print("There were no problems. Congratulations! \n")
    elif problem == 1:
        print("There was only one problem.\n")
    else:
        print("There were", problem, "problems.\n")
