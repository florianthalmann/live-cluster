import os
import scipy.io.wavfile as wf
import numpy as np

def separate_channels(infolder, outfolder):
    files = [elem for elem in os.listdir(infolder) if ".wav" in elem]
    
    for file in files:
        print "separating " + infolder+file
        name = file.replace('.wav', '')
        rate, data = wf.read(infolder+file)
        left = data[:,0]
        right = data[:,1]
        wf.write(outfolder+name+"l.wav", rate, left)
        wf.write(outfolder+name+"r.wav", rate, right)