import os
import scipy.io.wavfile as wf
import numpy as np
from feature_reader import JamsFeatureReader

infolder = "audio_tuned/"
outfolder = "audio_trimmed_short/"

#returns the first time value larger or equal the given time
def get_first_time_value(time, times):
    index = 0
    while True:
        if (times[index][0] >= time):
            return times[index][1]
        index += 1

def trim_wavs(from_sec, to_sec):
    files = os.listdir(infolder)[1:]
    times = JamsFeatureReader("features_tuned/").getFeatureMatrix("match")
    
    for index in range(len(files)):
        current_file = files[index]
        current_times = times[index]
        print "trimming " + outfolder+current_file
        current_from = get_first_time_value(from_sec, current_times)
        current_to = get_first_time_value(to_sec, current_times)
        rate, data = wf.read(infolder+current_file)
        print rate, current_from, current_to
        data = data[int(rate*current_from):int(rate*current_to)]
        wf.write(outfolder+current_file, rate, data)

trim_wavs(330,405)