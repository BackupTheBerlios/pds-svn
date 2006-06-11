# -*- coding: utf-8 -*-

# Farben
BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'
RESET = '\033[0;0m'
BOLD = '\033[1m'
BLACKBG = '\033[40m'
REVERSE = '\033[2m'
# / Farben

import random, time, os

def cout(out, art="commandline", error="404"):
    if art != "commandline":
        if art == "hinweis":
            print RED+BOLD+" __________ ________________________________\n| Hinweis: |________________________________\\"
            count = 0
            text = "| \n| "
            for e in out.split():
                count += 1
                if count == 5:
                    e += "\n"+"| "
                    count = 0
                text = text + " "+e
            else:
                text += "\n| __________________________________________\n|"+"_"*43+"/"+RESET
            print text
        elif art == "info":
            print YELLOW+BLACKBG+"\n"+BOLD
            for e in out.split("\n"): 
                print e.center(50)
            print RESET
        elif art == "error":
            print RED+BLACKBG+BOLD+"ERROR: "+error+"\n"+out+RESET
        else:
            cout("Diese art >"+art+"< konnte nicht gefunden werden!", "error", "not found")    
    else:
        print out

def rest():
    # Diese Funktion lässt den Rechner was schlafen
    # er kann ja nicht immer arbeiten ;)
    zahl = random.randint(2,random.randint(4,5))
    cout("> warte "+str(zahl)+" Sekunden bis zur nächsten Aktion")
    time.sleep(zahl)


def liste2string(liste, blacklist=[""]):
    the_return = ""
    for e in liste:
        if e not in blacklist:
            the_return += e+" "
    return(the_return)


