import os
from shutil import move

#features = ["vamp:qm-vamp-plugins:qm-barbeattracker", "vamp:qm-vamp-plugins:qm-mfcc:coefficients", "vamp:qm-vamp-plugins:qm-chromagram:chromagram"]
features = ["vamp:match-vamp-plugin:match:a_b"]
audiodir = 'audio2/'

for file in os.listdir(audiodir):
    if ".wav" in file:
        currentName = file.replace('.wav', '')
        for feature in features:
            #os.system("sonic-annotator -d " + feature + " " + audiodir+file + " -w rdf")
            #move(audiodir + currentName + '.n3', 'features/' + currentName + '_' + feature.replace(':', '_') + '.n3')
            os.system("sonic-annotator -d " + feature + " -m " + audiodir+"0.wav " + audiodir+file + " -w rdf")
            move(audiodir + '0.n3', 'features/' + currentName + '_' + feature.replace(':', '_') + '.n3')