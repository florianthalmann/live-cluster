import os
from separate_channels import separate_channels
from separate_channels import copy_features_of_separated_channels
from extract_features import extract_features
from tune_wavs import tune_wavs
from normalize_audio import normalize_audio
from cluster_features import ClusterPlotter

audio_folder = '/Volumes/gspeed1/thomasw/grateful_dead/AES_141/download/WAV_44-16/'
analysis_folder = '/Volumes/gspeed1/thomasw/grateful_dead/AES_141/analysis/'

features = ["vamp:match-vamp-plugin:match:a_b", "vamp:qm-vamp-plugins:qm-mfcc:coefficients", "vamp:qm-vamp-plugins:qm-chromagram:chromagram"]

original_features_folder, tuned_audio_folder, tuned_features_folder

def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path

#create all current folders
def create_current_folders(basefolder, subfolder, outfolder):
    original_features_folder = create_folder(outfolder+"features/original/"+subfolder)
    tuned_audio_folder = create_folder(basefolder+"tuned/"+subfolder)
    tuned_features_folder = create_folder(outfolder+"features/tuned/"+subfolder)
    channels_audio_folder = create_folder(basefolder+"channels/"+subfolder)
    channels_features_folder = create_folder(outfolder+"features/channels/"+subfolder)
    results_folder = create_folder(outfolder+"results/"+subfolder)

#create alignment features and tune wavs
def align_and_tune():
    extract_features(basefolder+subfolder, original_features_folder, [features[0]], "jams", "00")
    tune_wavs(basefolder+subfolder, tuned_audio_folder, original_features_folder)
    normalize_audio(tuned_audio_folder)

#recreate alignment features for tuned wavs, separate channels and extract features for separate channels
def realign_and_separate_and_analyze():
    extract_features(tuned_audio_folder, tuned_features_folder, [features[0]], "jams", "00")
    separate_channels(tuned_audio_folder, channels_audio_folder)
    copy_features_of_separated_channels(tuned_features_folder, channels_features_folder)
    extract_features(channels_audio_folder, channels_features_folder, features[1:], "jams")

def create_clustering_and_plots():
    ClusterPlotter().saveSegmentAnalysis("mfcc", channels_features_folder, results_folder)
    ClusterPlotter().saveSegmentAnalysis("chroma", channels_features_folder, results_folder)

def recursively_analyze_the_shit_out_of_this(basefolder, subfolder, outfolder):
    #analyze current folder
    create_current_folders(basefolder, subfolder, outfolder)
    align_and_tune()
    realign_and_separate_and_analyze()
    create_clustering_and_plots()
    
    #recursively go through all subfolders
    files = os.listdir(basefolder+subfolder)
    for file in files:
        if os.path.isdir(file):
            recursively_analyze_the_shit_out_of_this(basefolder, subfolder+file+"/", outfolder)


recursively_analyze_the_shit_out_of_this(audio_folder, "", analysis_folder)

#ClusterPlotter().createStridePlot(100, "chroma", "features/", "plots/stride(50,450)->(100,500)/")
#ClusterPlotter().createMultilevelAveragePlot(50, 1, "mfcc", "features/channels/", "plots/test3/mfcc-5_mds_50_1")
#ClusterPlotter().createSingleLevelPlot(256, 32, "mfcc", "features/channels/", "results/eval5/mfcc_mds_256*32sec")

#ClusterPlotter().saveSegmentAnalysis("mfcc", "features/channels/", "results/eval4/")
ClusterPlotter().saveParameterAnalysis("results/eval4/dist.json", "results/eval4/tril/")

#ClusterPlotter().plotDistanceDistributions("results/eval4/dist.json", "results/eval4/dist_distribs/")
#ClusterPlotter().plotDistanceDistributions2("results/eval4/dist.json", "results/eval5/*distribs2/")

#create a dymo based on the plots
#create_dymo("plots/multilevel/chroma_mds_tu_avg20.json", "audio_trimmed/", "dymos/", 100)



#ClusterPlotter().testLinearity()
