from separate_channels import separate_channels
from separate_channels import copy_features_of_separated_channels
from extract_features import extract_features
from tune_wavs import tune_wavs
from normalize_audio import normalize_audio
from cluster_features import ClusterPlotter

features = ["vamp:match-vamp-plugin:match:a_b", "vamp:qm-vamp-plugins:qm-mfcc:coefficients", "vamp:qm-vamp-plugins:qm-chromagram:chromagram"]

#FIRST RUN ALL THIS

#create alignment features and tune wavs
#extract_features("audio/original/", "features/original/", [features[0]], "jams", "00")
#tune_wavs("audio/original/", "audio/tuned/", "features/original/")
#normalize_audio("audio/tuned/")

#recreate alignment features for tuned wavs, separate channels and extract features for separate channels
#extract_features("audio/tuned/", "features/tuned/", [features[0]], "jams", "00")
#separate_channels("audio/tuned/", "audio/channels/")
#copy_features_of_separated_channels("features/tuned/", "features/channels/")
#extract_features("audio/channels/", "features/channels/", features[1:], "jams")

#ClusterPlotter().createStridePlot(100, "chroma", "features/", "plots/stride(50,450)->(100,500)/")
#ClusterPlotter().createMultilevelAveragePlot(50, 1, "mfcc", "features/channels/", "plots/test3/mfcc-5_mds_50_1")
#ClusterPlotter().createSingleLevelPlot(256, 0.0625, "mfcc", "features/channels/", "results/eval4/mfcc_mds_256*0.0625sec")
#ClusterPlotter().saveSegmentAnalysis("mfcc", "features/channels/", "results/eval4/")
ClusterPlotter().saveParameterAnalysis("results/eval4/dist.json", "results/eval4/")
ClusterPlotter().plotMeasures('results/eval4/', ['close'], 0, 'close0.png')
ClusterPlotter().plotMeasures('results/eval4/', ['close'], 1, 'close1.png')
ClusterPlotter().plotMeasures('results/eval4/', ['fitness'], 0, 'fitness0.png')
ClusterPlotter().plotMeasures('results/eval4/', ['fitness'], 1, 'fitness1.png')

#create a dymo based on the plots
#create_dymo("plots/multilevel/chroma_mds_tu_avg20.json", "audio_trimmed/", "dymos/", 100)



#ClusterPlotter().testLinearity()
