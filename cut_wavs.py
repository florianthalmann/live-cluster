import os, scipy.io.wavfile as wf
import numpy as np

infolder = "audio2/"
outfolder = "audio3/"
files = os.listdir(infolder)[1:]
rate, l = wf.read(infolder+files[0])

for file in files:
    print "writing " + outfolder+file
    rate, r = wf.read(infolder+file)
    lr = np.hstack((l, r))
    print lr
    wf.write(outfolder+file, rate, lr)