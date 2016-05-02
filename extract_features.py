import os
from shutil import move

formats = {"jams": ".json", "rdf": ".n3"}

def extract_simple_feature(audiodir, featuresdir, outformat, feature, file):
    name = file.replace('.wav', '')
    outfile = featuresdir + name + '_' + feature.replace(':', '_') + formats[outformat]
    if not os.path.isfile(outfile):
        os.system("sonic-annotator -d " + feature + " " + audiodir+file + " -w " + outformat)
        move(audiodir + name + formats[outformat], outfile)

def extract_multiplex_feature(audiodir, featuresdir, outformat, feature, file, reffile):
    name = file.replace('.wav', '')
    outfile = featuresdir + name + '_' + feature.replace(':', '_') + formats[outformat]
    if not os.path.isfile(outfile):
        os.system("sonic-annotator -d " + feature + " -m " + audiodir+reffile+" " + audiodir+file + " -w " + outformat)
        move(audiodir + reffile.replace('.wav','')+formats[outformat], outfile)

def extract_features(audiodir, featuresdir, features, outformat, reference=None):
    for file in os.listdir(audiodir):
        if file.endswith(".wav"):
            if not reference:
                reference = file
            for feature in features:
                if "match" in feature or "similarity" in feature:
                    extract_multiplex_feature(audiodir, featuresdir, outformat, feature, file, reference)
                else:
                    extract_simple_feature(audiodir, featuresdir, outformat, feature, file)