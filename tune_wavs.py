import os
import scipy.io.wavfile as wf
import numpy as np
from shutil import move
from feature_reader import JamsFeatureReader

#returns the first time value larger or equal the given time
def get_first_time_value(time, times):
    index = 0
    while True:
        if (times[index][0] >= time):
            return times[index][1]
        index += 1

def resample_wavs(folder):
    files = os.listdir(folder)[1:]
    for file in [f for f in os.listdir(folder) if ".wav" in f]:
        print "resampling " + folder+file
        os.system("sox " + folder+file + " -r 44100 " + folder+"r"+file)
        move(folder+"r"+file, folder+file)

def adjust_wavs_rate(infolder, outfolder, featurefolder):
    from_sec = 50
    to_sec = 350
    files = [f for f in os.listdir(infolder) if ".wav" in f]
    times = JamsFeatureReader(featurefolder).getFeatureMatrix("match")
    
    for index in range(len(files)):
        current_file = files[index]
        current_times = times[index]
        print "tuning " + outfolder+current_file
        current_from = get_first_time_value(from_sec, current_times)
        current_to = get_first_time_value(to_sec, current_times)
        rate, data = wf.read(infolder+current_file)
        num_samples = len(data[int(rate*current_from):int(rate*current_to)])
        rate_factor = (float(num_samples)/rate)/(to_sec-from_sec)
        print rate, current_from, current_to, rate_factor
        rate *= rate_factor
        wf.write(outfolder+current_file, rate, data)

def tune_wavs(infolder, outfolder, featurefolder):
    adjust_wavs_rate(infolder, outfolder, featurefolder)
    resample_wavs(outfolder)