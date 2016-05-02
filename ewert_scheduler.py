import os
from separate_channels import separate_channels
from separate_channels import copy_features_of_separated_channels
from extract_features import extract_features
from tune_wavs import tune_wavs
from normalize_audio import normalize_audio
from cluster_features import ClusterPlotter


features = ["vamp:match-vamp-plugin:match:a_b", "vamp:qm-vamp-plugins:qm-mfcc:coefficients", "vamp:qm-vamp-plugins:qm-chromagram:chromagram"]

class EwertScheduler():
    
    def create_folder(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    #create all current folders
    def create_current_folders(self, basefolder, subfolder, outfolder):
        self.original_audio_folder = self.create_folder(basefolder+subfolder)
        self.original_features_folder = self.create_folder(outfolder+"features/original/"+subfolder)
        self.tuned_audio_folder = self.create_folder(outfolder+"audio/tuned/"+subfolder)
        self.tuned_features_folder = self.create_folder(outfolder+"features/tuned/"+subfolder)
        self.channels_audio_folder = self.create_folder(outfolder+"audio/channels/"+subfolder)
        self.channels_features_folder = self.create_folder(outfolder+"features/channels/"+subfolder)
        self.results_folder = self.create_folder(outfolder+"results/"+subfolder)

    #create alignment features and tune wavs
    def align_and_tune(self):
        extract_features(self.original_audio_folder, self.original_features_folder, [features[0]], "jams")
        tune_wavs(self.original_audio_folder, self.tuned_audio_folder, self.original_features_folder)
        #normalize_audio(self.tuned_audio_folder)

    #recreate alignment features for tuned wavs, separate channels and extract features for separate channels
    def realign_and_separate_and_analyze(self):
        extract_features(self.tuned_audio_folder, self.tuned_features_folder, [features[0]], "jams")
        separate_channels(self.tuned_audio_folder, self.channels_audio_folder)
        copy_features_of_separated_channels(self.tuned_features_folder, self.channels_features_folder)
        extract_features(self.channels_audio_folder, self.channels_features_folder, features[1:], "jams")

    def create_clustering_and_plots(self):
        ClusterPlotter().saveSegmentAnalysisAndPlots("mfcc", self.channels_features_folder, self.results_folder)
        ClusterPlotter().saveSegmentAnalysisAndPlots("chroma", self.channels_features_folder, self.results_folder)

    def recursively_analyze_the_shit_out_of_this(self, basefolder, subfolder, outfolder):
        files = os.listdir(basefolder+subfolder)
        print basefolder+subfolder, files
        
        if any(f.endswith('.wav') for f in files):
            #analyze current folder
            self.create_current_folders(basefolder, subfolder, outfolder)
            self.align_and_tune()
            self.realign_and_separate_and_analyze()
            self.create_clustering_and_plots()
        
        #recursively go through all subfolders
        for file in files:
            print "  ", basefolder+subfolder+file, os.path.isdir(basefolder+subfolder+file)
            if os.path.isdir(basefolder+subfolder+file):
                self.recursively_analyze_the_shit_out_of_this(basefolder, subfolder+file+"/", outfolder)

audio_folder = '/Volumes/gspeed1/thomasw/grateful_dead/AES_141/analysis/audio/original/'
analysis_folder = '/Volumes/gspeed1/thomasw/grateful_dead/AES_141/analysis/'
#audio_folder = 'audio/'
#analysis_folder = 'analysis/'
EwertScheduler().recursively_analyze_the_shit_out_of_this(audio_folder, '', analysis_folder)
