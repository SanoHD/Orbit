from glob import glob
import sys, os, shlex
from time import sleep


#################### Packages

_packages = glob("packages\\*.orb")
packages = []

for _p in _packages:
    packages.append(_p[9:-4])

#print(packages)

#################### Stuff

max_args = 32 # -> print &1 &5 &23
var = {}
clear = lambda: os.system("cls")

#################### Main

def parser(x):
    if x == "packs":
        for p in packages:
            print(p)

    elif x == "clear":
        clear()

    elif x == "showvars":
        for v in var:
            print(v,"=",var[v])

    elif x == "help":
        clear()
        hfile = open("Dev\\help.txt")
        print(hfile.read())
        hfile.close()


    elif not x.split()[0] in packages:
        print("Invalid Command.")




############## TEST #############################

def packparser(line):
    global ofile, filename
    
    line = line.strip().replace("\\n","\n")
   
    for ac in range(max_args): # argument count
        if "&"+str(ac+1) in line:
            try:
                line = line.replace("&"+str(ac+1),ss[ac+1])
            except:
                line = line.replace("&"+str(ac+1),"")

    for v in var:
        if "~"+v in line:
            line = line.replace("~"+v,var[v])
            
    sline = line.split()
    aline = line.split("+")
    shsplit = shlex.split(line)
    
    if line[:4] == "$pl ":
        aline[0] = aline[0][4:]
        #print(aline)
        for arg in aline:
            print(arg,end="")
        print()
    
    elif line[:6] == "$file ":
        filename = line[6:]
        ofile = open(filename,"r+")
    
    elif line[:7] == "$filec ":
        ofile = open(line[7:],"w+")
        ofile.close()

    elif line[:4] == "$fw ":
        ofile.write(line[4:])

    elif line == "$fc":
        ofile.close()
    
    elif line == "$fd":
        os.remove(filename)
        

    elif "/" in line:
        slashline = line.split("/")
        if slashline[1] == "#input":
            try:
                var[slashline[0]] = input(slashline[2])
            except:
                var[slashline[0]] = input()
                
        elif slashline[1] == "#file":
            var[slashline[0]] = ofile.read()
            
        elif slashline[1][:6] == "#file:":
            for oline in ofile: # mc1
                ovn = oline.strip().split(":")[0]
                oelse = oline.strip()[len(ovn)+1:]
                if slashline[1][6:] == ovn:
                    var[slashline[0]] = oelse
                    
        elif slashline[1][0] == "[" and slashline[1][-1] == "]":
            if ":" in slashline[1]:
                s = slashline[1].split(":")
                try: a = int(s[0][1:])
                except: a = None
                try: b = int(s[1][:-1])
                except: b = None
                var[slashline[0]] = var[slashline[0]][a:b]
            else:
                var[slashline[0]] = var[slashline[0]][int(slashline[1][1:-1])]
        else:
            vn = slashline[0]
            slashline = slashline[1:]
            e = ""
            for s in slashline:
                e += s
            var[vn] = e

    if line[:2] == ".{" and line[-1] == "}":
        parser(line[2:-1])
        
    if line[:2] == "!{" and line[-1] == "}":
        packparser(line[2:-1])
    

    elif line[:5] == "stop ":
        t = line[5:]
        if t in var:
            t = var[t]
        sleep(float(t))


while True:
    x = input(" > ")
    xs = x.split()
    ss = shlex.split(x)

    if x != "":
        parser(x)  

    try:
        xorb = "packages\\"+xs[0]+".orb"
        if xs[0] in packages:
            file = open(xorb)
            for line in file:
                if not line.strip() == "" and not line.strip()[0] == ";":
                    packparser(line)
                else:
                    continue
            file.close()
    except:
        print("An Error occurred.")


    #print("VAR:",var)

