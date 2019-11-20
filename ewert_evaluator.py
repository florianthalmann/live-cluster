import os, json
from eval_read_csv import ldict


class EwertEvaluator():
    
    def calculate_average_distance(self, dists, selection):
        avg_dist = 0
        for s1 in selection:
            for s2 in selection:
                if s1 < s2:
                    #print dists["distances"][0][0][s1][s2]
                    avg_dist += dists["distances"][0][0][s1][s2]
        avg_dist /= (pow(len(selection),2)-len(selection))/2
        return avg_dist
    
    def get_subset(self, thomas, type, filenames):
        sub = []
        for i in range(len(filenames)):
            archive_id = filenames[i].split("_")[0]
            if thomas[archive_id].recording == type:
                sub.append(i)
        return sub
    
    def recursively_evaluate_the_shit_out_of_this(self, basefolder, subfolder, audio_folder, avg_dists):
        files = os.listdir(basefolder+subfolder)
        thomas = ldict()
        
        for f in files:
            if f.endswith('dist.json'):
                with open(basefolder+subfolder+f) as file:
                    dists = json.load(file)
                    
                    filenames = dists["filenames"]
                    
                    tot = range(len(filenames))
                    sbd = self.get_subset(thomas, "SBD", filenames)
                    aud = self.get_subset(thomas, "AUD", filenames)
                    mat = self.get_subset(thomas, "MAT", filenames)
                    
                    avg_dists[subfolder] = {}
                    avg_dists[subfolder]["total"] = self.calculate_average_distance(dists, tot)
                    avg_dists[subfolder]["SBD"] = self.calculate_average_distance(dists, sbd)
                    avg_dists[subfolder]["AUD"] = self.calculate_average_distance(dists, aud)
                    avg_dists[subfolder]["MAT"] = self.calculate_average_distance(dists, mat)
        
        #recursively go through all subfolders
        for file in files:
            if os.path.isdir(basefolder+subfolder+file):
                self.recursively_evaluate_the_shit_out_of_this(basefolder, subfolder+file+"/", audio_folder, avg_dists)
        
        return avg_dists
    
    def annotate_distance_matrices(self, basefolder, subfolder, channel_feature_folder):
        files = os.listdir(basefolder+subfolder)
        
        for f in files:
            if f.endswith('dist.json'):
                with open(basefolder+subfolder+f) as file:
                    print basefolder+subfolder+f
                    dists = json.load(file)
                    channels = [ch for ch in os.listdir(channel_feature_folder+subfolder) if ch.endswith('chromagram.json')]
                    channel_filenames = []
                    for ch in channels:
                        with open(channel_feature_folder+subfolder+ch) as channel:
                            channel_json = json.load(channel)
                            channel_filenames.append(channel_json["file_metadata"]["identifiers"]["filename"])
                    dists["filenames"] = channel_filenames
                with open(basefolder+subfolder+f, 'w') as file:
                    json.dump(dists, file)
        
        #recursively go through all subfolders
        for file in files:
            if os.path.isdir(basefolder+subfolder+file):
                self.annotate_distance_matrices(basefolder, subfolder+file+"/", channel_feature_folder)

#channel_feature_folder = '/Volumes/gspeed1/thomasw/grateful_dead/AES_141/PAPER-audio/analysis2/features/channels/'
#analysis_folder = '/Volumes/gspeed1/thomasw/grateful_dead/AES_141/PAPER-audio/analysis2/results/'
channel_feature_folder = 'analysis/features/channels/'
analysis_folder = 'analysis/results/'
EwertEvaluator().annotate_distance_matrices(analysis_folder, '', channel_feature_folder)
avg_dists = EwertEvaluator().recursively_evaluate_the_shit_out_of_this(analysis_folder, '', channel_feature_folder, {})
tot = 0
sbd = 0
aud = 0
mat = 0
for d in avg_dists:
    tot += avg_dists[d]["total"]
    sbd += avg_dists[d]["SBD"]
    aud += avg_dists[d]["AUD"]
    mat += avg_dists[d]["MAT"]
    print avg_dists[d], d
print tot/len(avg_dists), sbd/len(avg_dists), aud/len(avg_dists), mat/len(avg_dists)

