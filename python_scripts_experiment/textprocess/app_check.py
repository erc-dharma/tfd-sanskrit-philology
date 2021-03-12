import re
from matplotlib import pyplot as plt

def app_check(filename):
    appflag = False
    onflag = False
    app2check = ""
    # msBod not included
    print("Which project? VSS (v) or NĀT (n)?")
    reply = input()
    if reply == "v":
        #allmss = ['msCa', 'msCb', 'msCc', 'msNa', 'msNb', 'msNc', 'msL', 'Ed']
        allmss = ['msCa', 'msCb', 'msCc', 'msNa', 'msNb', 'msNc', 'Ed']
    else:
        allmss = ['msA', 'msB', 'msC', 'msD', 'msE', 'msF']
    mss = [""]
    print("Which MSS' presence to check:")
    for i in range(len(allmss)):
        print("Check this (ENTER or n)?", allmss[i])
        reply = input()
        if reply != "n":
            mss.append(allmss[int(i)]) 
            print(allmss[i], "will be checked")
        else:
            print(allmss[i], "will NOT be checked")        
    openfile = open(filename, "r")
    tempfile = 'temp.txt'
    writefile = open(tempfile, "w")
    # to tackle separate entries in same pāda
    for line in openfile:
        line = re.sub('\\\\oo', '</APP>\n<APP>', line)
        # when I put variants of both pādas in one <APP></APP>:
        if appflag == True and '<APP>' not in line:
            line = re.sub('\\\\v', '</APP>\n<APP>', line)
        # to restore siglum of group to sigla of mss:
        line = re.sub('mssCaCbCc', 'msCamsCbmsCc', line)
        writefile.write(line)
    writefile.close()
    chart_data = {}
    num = 0
    openfile = open(tempfile, "r")
    for line in openfile:
        if "<NEWCHAPTER/>" in line or "<startchapter-n=" in line:
            num += 1
            for i in range(50):
                chart_data[num+i] = [] 
            num = num + 49
        if '<START/>' in line:
            onflag = True
        if '<STOP/>' in line:
            onflag = False
        if '<APP>' in line or appflag == True:
            appflag = True
            app2check = app2check + line
            if '</APP>' in line:
                num += 1
                chart_data[num] = [] 
                appflag = False
                check = True
                for ms in mss:
                    if ms not in app2check:
                        check = False
                        if onflag == True:
                            print("PROBLEM: MS", ms, "is missing!")
                    else:
                        chart_data[num].append(ms)
                if check == True:
                        if onflag == True:
                             print("OK!")
                if onflag == True:
                    print(app2check)
                    print("-"*20)
                app2check = ''
    openfile.close()

    print("Want to see visual data? (y or ENTER [no])")
    inp = input()
    if inp == "y":
        visual_data = []
        for app in chart_data:
            if len(chart_data[app]) == 0:
                visual_data.append(len(chart_data[app]))
            else:
                visual_data.append(len(chart_data[app])-1)
        #plt.plot(range(1,len(visual_data)+1), visual_data, color = "red")
        plt.bar(range(1,len(visual_data)+1), visual_data)
        plt.xlabel("Apparatus entry no.")
        plt.ylabel("No. of collated sources")
        plt.title("Vṛṣasārasaṃgraha: the state of collation")
        plt.show()


