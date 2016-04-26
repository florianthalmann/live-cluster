import os, rdflib, json
import numpy as np

class JamsFeatureReader():
    
    def __init__(self, folder):
        self.folder = folder
        self.features = {}
    
    def getFeatureMatrixSegmentAvgAndVar(self, feature, from_time, to_time):
        times = self.getFeatureMatrix("match")
        featureMatrix = []
        for t in times:
            ft = self.getBTime(from_time, t)
            tt = self.getBTime(to_time, t)
            matrix = self.getMatrixSegment(feature, ft, tt)
            if len(matrix) > 0:
                featureMatrix.append(np.concatenate([matrix.mean(0), matrix.var(0)]))
        if len(featureMatrix) == len(self.getFeatureMatrix("match")):
            return np.array(featureMatrix)
    
    def getLabels(self):
        labels = []
        for filename in os.listdir(self.folder):
            if "json" in filename and "match" in filename:
                labels.append(filename.split('_')[0])
        return labels
    
    def getBTime(self, atime, times):
        index = 0
        while True:
            if times[index][0] >= atime or index >= len(times)-1:
                return times[index][1]
            index += 1
    
    def getMatrixSegment(self, feature, from_time, to_time):
        matrix = []
        for features in self.getFeatureMatrix(feature):
            for row in features:
                if from_time <= float(row[0]) and float(row[0]) < to_time:
                    matrix.append(row[1])
        return np.array(matrix)
    
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
        matrix = []
        for row in featurejson["annotations"][0]["data"]:
            matrix.append([float(row["time"]), row["value"][1:]])
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