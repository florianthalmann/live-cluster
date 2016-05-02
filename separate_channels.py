import os
import scipy.io.wavfile as wf
from shutil import copy

def separate_channels(infolder, outfolder):
    if len(os.listdir(outfolder)) != 2*len(os.listdir(infolder)):
        files = [f for f in os.listdir(infolder) if ".wav" in f]
    
        for file in files:
            print "separating " + infolder+file
            name = file.replace('.wav', '')
            rate, data = wf.read(infolder+file)
            left = data[:,0]
            right = data[:,1]
            wf.write(outfolder+name+"_l.wav", rate, left)
            wf.write(outfolder+name+"_r.wav", rate, right)

#copies the common features of separated channels to the given outfolder
def copy_features_of_separated_channels(infolder, outfolder):
    if len(os.listdir(outfolder)) < 2*len(os.listdir(infolder)):
        files = [f for f in os.listdir(infolder) if ".json" in f]
    
        for file in files:
            print "copying " + infolder+file
            name = file.split('_')[0]
            copy(infolder+file, outfolder+file.replace(name, name+"_l"))
            copy(infolder+file, outfolder+file.replace(name, name+"_r"))