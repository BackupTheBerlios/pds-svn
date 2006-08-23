import os,re

def keywords(datei):
    keys = []
    filename = "tmp_pdf_file.html"
    os.system("pdftotext -htmlmeta "+datei+" "+filename)
    f = open(filename, "r")
    search = ['<title>']
    for i in f:
        i = i.lower()
        if i.find(search[0]) > -1:
            i = i.replace(search[0],"").replace("</title>","").replace("\n","").replace("\r","")
            keys.extend(i.split())
    f.close()
    os.system("rm "+filename)
    return(keys)
    return(keys)
    
if __name__ == "__main__":
    print keywords("/home/sigma/m@rie.pdf")
