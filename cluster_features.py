import os, rdflib
import numpy as np
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.manifold import MDS
import pandas as pd

class RdfReader():
    
    def getFeatureMatrix(self, folder, feature):
        featureMatrix = []
        for filename in os.listdir(folder):
            if "n3" in filename:
                objectname = filename.split("_")[0]
                g = rdflib.Graph()
                g.load(folder+filename, format="n3")
                #if ("barbeattracker" in filename):
                    #self.loadEvents(g)
                if (feature in filename):
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
    
    def parseXSDDuration(self, duration):
        return float(duration[2:-1])

class ClusterPlotter():
    
    def plotDendrogram(self, featureMatrix, title, saveFile):
        Z = linkage(features, 'ward')
        fig = plt.figure()
        plt.title(title)
        plt.xlabel('version')
        plt.ylabel('distance')
        fig.patch.set_facecolor('white')
        dendrogram(Z)
        plt.savefig(saveFile, facecolor='white', edgecolor='none')
        #plt.show()
    
    def plotMDS(self, featureMatrix, title, saveFile):
        dist = 1 - cosine_similarity(features)
        mds = MDS(n_components=2, dissimilarity="precomputed", random_state=6)
        results = mds.fit(dist)
        coords = results.embedding_
        
        fig = plt.figure()
        plt.title(title)
        plt.scatter(coords[:, 0], coords[:, 1], marker = 'o')
        fig.patch.set_facecolor('white')
        for label, x, y in zip(range(len(features)), coords[:, 0], coords[:, 1]):
            plt.annotate(label, (x, y))
        plt.savefig(saveFile, facecolor='white', edgecolor='none')
        #plt.show()


features = RdfReader().getFeatureMatrix("features/", "mfcc")
title = "MFCCs of Looks Like Rain on 1982-10-10"
ClusterPlotter().plotDendrogram(features, title, "plots/mfcc_dendro.png")
ClusterPlotter().plotMDS(features, title, "plots/mfcc_mds.png")
