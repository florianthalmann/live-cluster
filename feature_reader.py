import os, rdflib, json
import numpy as np

class JamsFeatureReader():
    
    def __init__(self, folder):
        self.folder = folder
        self.features = {}
    
    def getFeatureMatrixSegmentAvgAndVar(self, feature, from_time, to_time):
        times = self.getFeatureMatrix("match")
        featureMatrix = []
        for i in range(len(times)):
            ft = self.getBTime(from_time, times[i])
            tt = self.getBTime(to_time, times[i])
            matrix = self.getMatrixSegment(feature, ft, tt, i)
            if len(matrix) > 0:
                #NORMALIZE MEANS AND VARIANCES SEPARATELY!!!!!!!
                means = self.normalize(matrix.mean(0))
                varis = self.normalize(matrix.var(0))
                featureMatrix.append(np.concatenate([means, varis]))
        if len(featureMatrix) == len(self.getFeatureMatrix("match")):
            return np.array(featureMatrix)
    
    def normalize(self, matrix):
        min = matrix.min()
        matrix -= min
        max = matrix.max()
        if max != 0:
            matrix /= max
        return matrix
    
    def getLabels(self):
        labels = []
        for filename in os.listdir(self.folder):
            if "json" in filename and "match" in filename:
                labels.append(filename.replace('_','',1).split('_')[0].replace('10','1x').replace('00','x').replace('0','').replace('x','0'))
        return labels
    
    def getBTime(self, atime, times):
        index = 0
        while True:
            if times[index][0] >= atime or index >= len(times)-1:
                return times[index][1]
            index += 1
    
    def getMatrixSegment(self, feature, from_time, to_time, index):
        matrix = self.getFeatureMatrix(feature)[index]
        time_increment = matrix["time_increment"]
        segment = matrix["data"][int(float(from_time)/time_increment):int(float(to_time)/time_increment)]
        return np.array(segment)
    
    def getFeatureMatrix(self, feature):
        if feature not in self.features:
            featureMatrix = []
            for filename in os.listdir(self.folder):
                if "json" in filename and feature in filename:
                    with open(self.folder+filename) as file:
                        featurejson = json.load(file)
                    if "match" in filename:
                        featureMatrix.append(self.loadABTimeline(featurejson))
                    else:
                        featureMatrix.append(self.loadMatrix(featurejson))
            self.features[feature] = np.array(featureMatrix)
        return self.features[feature]
    
    def loadMatrix(self, featurejson):
        matrix = {}
        annotation = featurejson["annotations"][0]
        sampleRate = annotation["annotation_metadata"]["annotator"]["sample_rate"]
        stepSize = annotation["annotation_metadata"]["annotator"]["step_size"]
        matrix["time_increment"] = float(stepSize)/sampleRate
        data = []
        for row in annotation["data"]:
            data.append(row["value"][2:])
        matrix["data"] = np.array(data)
        return matrix
    
    def loadABTimeline(self, featurejson):
        abTimes = []
        for row in featurejson["annotations"][0]["data"]:
            abTimes.append([float(row["value"]), float(row["time"])])
        return abTimes

class RDFFeatureReader():
    
    def getFeatureMatrix(self, folder, feature):
        featureMatrix = []
        for filename in os.listdir(folder):
            if "n3" in filename:
                if feature in filename:
                    g = rdflib.Graph()
                    g.load(folder+filename, format="n3")
                    if "match" in filename:
                        self.loadABTimeline(g)
                    else:
                        featureMatrix.append(self.loadMatrix(g).mean(0))
        return np.array(featureMatrix)
    
    def loadMatrix(self, graph):
        result = graph.query(
            """SELECT DISTINCT ?dim ?sig
                WHERE {
                    ?a af:dimensions ?dim .
                    ?a af:value ?sig .
                }""")
        for row in result:
            dim = int(row[0].split(" ")[0])
            matrix = np.fromstring(row[1], sep=" ")
            return matrix.reshape(-1, dim)
    
    def loadEvents(self, graph):
        result = graph.query(
            """SELECT DISTINCT ?dur
               WHERE {
                  ?a tl:at ?dur .
               }""")
        durations = []
        for row in result:
            durations.append(self.parseXSDDuration(row[0]))
        durations.sort()
        return durations
    
    def loadABTimeline(self, graph):
        result = graph.query(
            """SELECT DISTINCT ?atime ?btime
               WHERE {
                  ?e af:feature ?atime .
                  ?e event:time ?t .
                  ?t tl:at ?btime .
               }""")
        abTimes = []
        for row in result:
            abTimes.append([float(row[0]), self.parseXSDDuration(row[1])])
        return abTimes
    
    def parseXSDDuration(self, duration):
        return float(duration[2:-1])