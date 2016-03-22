import os
from shutil import move

dir = "features_tuned/"

for file in os.listdir(dir):
    if "10" not in file and "DS" not in file:
        move(dir + file, dir + "0"+file)