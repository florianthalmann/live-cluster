import os, wave
import numpy as np

infolder = "audio2/"
outfolder = "audio3/"
files = os.listdir(infolder)[1:]
reffile = wave.open(infolder+files[0], 'rb')
l = reffile.readframes(reffile.getnframes())
nchannels, sampwidth, framerate, nframes, comptype, compname =  reffile.getparams()

for file in files:
    print "writing " + outfolder+file
    infile = wave.open(infolder+file, 'rb')
    r = infile.readframes(infile.getnframes())
    print infile.getparams()
    lr = ''
    for i in range(88200):
        lr += l[i]
        lr += r[i]
    outfile = wave.open(outfolder+file, 'wb')
    outfile.setparams((2,sampwidth,framerate,nframes,comptype,compname))
    outfile.writeframes(lr)
    outfile.close()