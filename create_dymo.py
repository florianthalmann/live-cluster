import os, json

def create_dymo(clusterpath, audiofolder, outfolder, factor):
    dymojson = {"@id":"dymo0","@type":"Dymo","ct":"parallel","parts":[],"Amplitude":{"value":0.1,"type":"Parameter"}}
    audiofiles = [elem for elem in os.listdir(audiofolder) if ".wav" in elem]
    
    for i in range(len(audiofiles)):
        with open(clusterpath) as clusterfile:
            clusterjson = json.load(clusterfile)
        
        create_subdymo(dymojson, "dymo"+str(i), audiofiles[i], clusterjson[i], factor)
        
    with open(outfolder+"dymo.json", 'w') as dymofile:
        json.dump(dymojson, dymofile)

def create_subdymo(dymojson, name, audiopath, location, factor):
    dymojson["parts"].append({"@id":name,"@type":"Dymo","parts":[],"source":"audio_trimmed/"+audiopath,"Amplitude":{"value":0.1,"type":"Parameter"},"Pan":{"value":factor*location[0],"type":"Parameter"},"Distance":{"value":factor*location[1],"type":"Parameter"}})