import os
from shutil import move

formats = {"jams": ".json", "rdf": ".n3"}

def extract_simple_feature(audiodir, featuresdir, outformat, feature, file):
    name = file.replace('.wav', '')
    os.system("sonic-annotator -d " + feature + " " + audiodir+file + " -w " + outformat)
    move(audiodir + name + formats[outformat], featuresdir + name + '_' + feature.replace(':', '_') + formats[outformat])

def extract_multiplex_feature(audiodir, featuresdir, outformat, feature, file, reffile):
    name = file.replace('.wav', '')
    os.system("sonic-annotator -d " + feature + " -m " + audiodir+reffile+".wav " + audiodir+file + " -w " + outformat)
    move(audiodir + reffile+formats[outformat], featuresdir + name + '_' + feature.replace(':', '_') + formats[outformat])

def extract_features(audiodir, featuresdir, features, outformat, reference="00"):
    for file in os.listdir(audiodir):
        if ".wav" in file:
            for feature in features:
                if "match" in feature or "similarity" in feature:
                    extract_multiplex_feature(audiodir, featuresdir, outformat, feature, file, reference)
                else:
                    extract_simple_feature(audiodir, featuresdir, outformat, feature, file)