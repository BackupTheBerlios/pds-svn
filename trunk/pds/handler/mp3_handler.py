import id3reader

mime_type = "audio/mpeg"

def keywords(datei):
    keys = []
    id3r = id3reader.Reader(datei)
    if id3r.getValue('album') != None:
        keys.append(str(id3r.getValue('album')))
    if id3r.getValue('title') != None:
        keys.append(str(id3r.getValue('title')))
    if id3r.getValue('performer') != None:
        keys.append(str(id3r.getValue('performer')))   
    return(keys)
    
if __name__ == "__main__":
    print keywords("/media/hda5/mp3/Dick Brave & The Backbeats/Dick This CD/09 Buona Sera.mp3")
