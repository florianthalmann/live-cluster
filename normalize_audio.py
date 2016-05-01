import os

def normalize_audio(audiodir):
    for file in os.listdir(audiodir):
        if file.endswith(".wav"):
            os.system("sox -norm "+audiodir+file+" "+audiodir+file)
