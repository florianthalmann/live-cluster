import os, json

def create_dymo(clusterpath, audiofolder, outfolder, factor):
    parts = []
    renderingjson = {
        "@context": "https://tiny.cc/dymo-context",
        "@type": "Rendering",
        "dymo": {
            "@id":"dymo0",
            "@type":"Dymo",
            "cdt": "Conjunction",
            "parts":{"@list": parts},
            "parameters": {
                "@type": "Amplitude",
                "value": {
                "@type": "xsd:float",
                    "@value": "0.1"
                }
            }
        }
    }
    audiofiles = [elem for elem in os.listdir(audiofolder) if ".wav" in elem]
    
    for i in range(len(audiofiles)):
        with open(clusterpath) as clusterfile:
            clusterjson = json.load(clusterfile)
        
        create_subdymo(parts, "dymo"+str(i+1), audiofiles[i], clusterjson[i], factor)
        
    with open(outfolder+"save.json", 'w') as dymofile:
        json.dump(renderingjson, dymofile)

def create_subdymo(parts, name, audiopath, location, factor):
    parts.append({
        "@id":name,
        "@type":"Dymo",
        "source":"audio_trimmed/"+audiopath,
        "parameters": [
            {
                "@type": "Amplitude",
                "value": {
                "@type": "xsd:float",
                    "@value": "0.1"
                }
            },
            {
                "@type": "Pan",
                "value": {
                "@type": "xsd:float",
                    "@value": str(factor*location[0])
                }
            },
            {
                "@type": "Distance",
                "value": {
                "@type": "xsd:float",
                    "@value": str(factor*location[1])
                }
            }
        ]
    })