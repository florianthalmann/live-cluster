import os

def normalize_audio(audiodir):
    for file in os.listdir(audiodir):
        if ".wav" in file:
            os.system("sox –norm "+audiodir+file+" "+audiodir+file)