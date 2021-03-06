import os
import scipy.io.wavfile as wf
import numpy as np
from shutil import move
from feature_reader import JamsFeatureReader

#returns the first time value larger or equal the given time
def get_first_time_value(time, times):
    index = 0
    while True:
        if index < len(times):
            if times[index][0] >= time:
                return times[index][1]
            index += 1
        else:
            return None

def resample_wavs(folder):
    for file in [f for f in os.listdir(folder) if ".wav" in f]:
        print "resampling " + folder+file
        os.system("sox " + folder+file + " -r 44100 " + folder+"r"+file)
        move(folder+"r"+file, folder+file)

def adjust_wavs_rate(infolder, outfolder, featurefolder):
    files = [f for f in os.listdir(infolder) if ".wav" in f]
    times = JamsFeatureReader(featurefolder).getFeatureMatrix("match")
    #get the right window
    rate, data = wf.read(infolder+files[0])
    length = int(float(len(data))/rate)
    from_sec = 20
    to_sec = length-20
    
    for index in range(len(files)):
        current_file = files[index]
        current_times = times[index]
        print "tuning " + outfolder+current_file
        current_from = get_first_time_value(from_sec, current_times)
        current_to = get_first_time_value(to_sec, current_times)
        if current_from != None and current_to != None:
            rate, data = wf.read(infolder+current_file)
            num_samples = len(data[int(rate*current_from):int(rate*current_to)])
            rate_factor = (float(num_samples)/rate)/(to_sec-from_sec)
            print rate, current_from, current_to, rate_factor
            rate *= rate_factor
            wf.write(outfolder+current_file, rate, data)

def tune_wavs(infolder, outfolder, featurefolder):
    if len(os.listdir(outfolder)) != len(os.listdir(infolder)):
        adjust_wavs_rate(infolder, outfolder, featurefolder)
        resample_wavs(outfolder)