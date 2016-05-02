import os
from shutil import copy
import xml.etree.ElementTree as etree

def simplify_title(title):
    title = title.lower()
    title = title.replace(' ','')
    title = title.replace('>','')
    title = title.replace('"','')
    title = title.replace("in'","ing")
    title = title.replace("st.","saint")
    return title

def get_files_by_songs_from_xml(folder):
    files_by_songs = {}
    for filename in os.listdir(folder):
        if filename.endswith('_files.xml'):
            tree = etree.parse(folder+filename)
            root = tree.getroot()
            for file_element in root:
                if file_element.get('source') == 'original':
                    title = file_element.find('title')
                    if title is not None:
                        title = simplify_title(title.text)
                        filename = file_element.get('name')
                        filename = filename[:filename.rfind('.')]+".wav"
                        files_by_songs[title] = filename
    return files_by_songs

def move_files_to_song_folders(infolder, rec_name, outfolder):
    files_by_songs = get_files_by_songs_from_xml(infolder)
    for songname in files_by_songs:
        #make song folder if it doesn't exist yet
        songfolder = outfolder+songname
        if not os.path.exists(songfolder):
            os.makedirs(songfolder)
        #print infolder+files_by_songs[songname], songfolder+'/'+rec_name+'.wav'
        copy(infolder+files_by_songs[songname], songfolder+'/'+rec_name+'.wav')

def sort_songs(infolder, outfolder):
    for date_folder in os.listdir(infolder):
        print infolder+date_folder
        if os.path.isdir(infolder+date_folder):
            for rec_folder in os.listdir(infolder+date_folder):
                print infolder+date_folder+'/'+rec_folder
                if os.path.isdir(infolder+date_folder+'/'+rec_folder):
                    move_files_to_song_folders(infolder+date_folder+'/'+rec_folder+'/', rec_folder, outfolder+date_folder+'/')

sort_songs('/Volumes/gspeed1/thomasw/grateful_dead/AES_141/download/WAV_44-16/', '/Volumes/gspeed1/thomasw/grateful_dead/AES_141/analysis/audio/original/')

#sort_songs('audio/', 'analysis/audio/original/')