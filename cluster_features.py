import os, json
import numpy as np
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.manifold import MDS
import pandas as pd
import seaborn as sns
from feature_reader import JamsFeatureReader

class ClusterPlotter():
    
    def plotDendrogram(self, featureMatrix, title, saveFile):
        Z = linkage(featureMatrix, 'ward')
        fig = plt.figure()
        plt.title(title)
        plt.xlabel('version')
        plt.ylabel('distance')
        fig.patch.set_facecolor('white')
        dendrogram(Z)
        plt.savefig(saveFile, facecolor='white', edgecolor='none')
        #plt.show()
    
    def plotMDSScatter(self, featureMatrix, title, saveFile):
        coords = self.getMDS(featureMatrix)
        fig = plt.figure()
        plt.title(title)
        plt.scatter(coords[:, 0], coords[:, 1], marker = 'o')
        fig.patch.set_facecolor('white')
        for label, x, y in zip(range(len(featureMatrix)), coords[:, 0], coords[:, 1]):
            plt.annotate(label, (x, y))
        plt.savefig(saveFile, facecolor='white', edgecolor='none')
        #plt.show()
    
    def plotMDSLines(self, featureMatrices, title, saveFile):
        lines = np.empty([featureMatrices.shape[1], featureMatrices.shape[0], 2])
        for i in range(len(featureMatrices)):
            coords = self.getMDS(featureMatrices[i])
            for j in range(len(coords)):
                lines[j][i] = coords[j]
        fig = plt.figure()
        plt.title(title)
        for line in lines:
            plt.plot(line[:, 0], line[:, 1])
        fig.patch.set_facecolor('white')
        #for label, x, y in zip(range(len(features)), coords[:, 0], coords[:, 1]):
            #plt.annotate(label, (x, y))
        plt.savefig(saveFile, facecolor='white', edgecolor='none')
        #plt.show()
    
    def getFeatures(self, feature, featuresfolder, starts, ends):
        if not hasattr(self,'reader') or self.reader.folder != featuresfolder:
            self.reader = JamsFeatureReader(featuresfolder)
        features = []
        for i in range(len(starts)):
            #print starts[i], ends[i]
            matrix = self.reader.getFeatureMatrixSegmentAvgAndVar(feature, starts[i], ends[i])
            if matrix is not None and len(matrix) > 0:
                features.append(matrix)
        return np.array(features)
    
    def getMDS(self, featureMatrix, dist=None):
        if dist is None:
            dist = 1-cosine_similarity(featureMatrix)
        mds = MDS(n_components=2, dissimilarity="precomputed", random_state=6)
        results = mds.fit(dist)
        return results.embedding_
    
    def normalize(self, features):
        for i in range(len(features)):
            for j in range(len(features[i])):
                features[i][j] = features[i][j] / features[i][j].max()
        return features
    
    def plotMatrixHeat(self, matrix, path):
        f, ax = plt.subplots(figsize=(11, 9))
        
        # Generate a custom diverging colormap
        cmap = sns.diverging_palette(220, 10, as_cmap=True)
        
        # Draw the heatmap with the mask and correct aspect ratio
        sns.heatmap(matrix, cmap=cmap, vmax=matrix.max(),
                    square=True, xticklabels=5, yticklabels=5,
                    linewidths=.5, cbar_kws={"shrink": .5}, ax=ax)
        
        plt.savefig(path)
    
    def getAvgDistances(self, feature, featuresfolder, starts, ends, outfile=None):
        features = self.getFeatures(feature, featuresfolder, starts, ends)
        if outfile:
            self.plotMatrixHeat(features[0], outfile+"_ex_features.png")
        dist = np.zeros([features.shape[1], features.shape[1]])
        for matrix in features:
            dist += 1 - cosine_similarity(matrix)
        dist /= features.shape[0]
        if outfile:
            self.plotMatrixHeat(dist, outfile+"_distances.png")
        return dist
    
    def createLinesWithScatters(self, feature, featuresfolder, outfolder, starts, ends):
        features = self.getFeatures(feature, featuresfolder, starts, ends)
        title = feature+" of Looks Like Rain on 1982-10-10"
        self.plotMDSLines(features, title, outfolder+feature+"_mds_mul.png")
        self.plotMDSScatter(reader.getFeatureMatrixSegment(feature, starts[0], ends[0]), title, outfolder+feature+"_mds_early.png")
        self.plotMDSScatter(reader.getFeatureMatrixSegment(feature, starts[int(features.shape[0]/2)], ends[int(features.shape[0]/2)]), title, outfolder+feature+"_mds_medium.png")
        self.plotMDSScatter(reader.getFeatureMatrixSegment(feature, starts[features.shape[0]-1], ends[features.shape[0]-1]), title, outfolder+feature+"_mds_late.png")
    
    def plotAverageMDS(self, feature, featuresfolder, outfile, starts, ends):
        title = feature+" of Looks Like Rain on 1982-10-10"
        labels = JamsFeatureReader(featuresfolder).getLabels()
        
        dists = self.getAvgDistances(feature, featuresfolder, starts, ends, outfile)
        coords = self.getMDS(feature, dists)
        with open(outfile+".json", 'w') as distfile:
            json.dump(coords.tolist(), distfile)
        
        
        fig = plt.figure(figsize=(16.0, 12.0))
        plt.title(title)
        plt.plot(coords[:, 0], coords[:, 1], marker = 'o', lw=0)
        fig.patch.set_facecolor('white')
        for label, x, y in zip(labels, coords[:, 0], coords[:, 1]):
            plt.annotate(label, (x, y))
        plt.savefig(outfile+".png", facecolor='white', edgecolor='none')
    
    def plotAvgMDSLines(self, features):
        return
    
    def createStridePlot(self, pointcount, feature, outfolder):
        starts = np.linspace(50, 100, num=pointcount, endpoint=False)
        ends = starts+400
        self.createLinesWithScatters(feature, outfolder, starts, ends)
    
    def createZoomPlot(self, pointcount, feature, outfolder):
        starts = np.linspace(50, 250, num=pointcount, endpoint=False)
        ends = np.full((pointcount), 250)
        self.createLinesWithScatters(feature, outfolder, starts, ends)
    
    def createSingleLevelPlot(self, numsegments, segmentlength, feature, featurefolder, outfile):
        starts = []
        ends = []
        starts = np.linspace(50, 450, num=numsegments, endpoint=True)
        ends = starts+segmentlength
        self.plotAverageMDS(feature, featurefolder, outfile, starts, ends)
    
    def createMultilevelAveragePlot(self, pointsperlevel, numlevels, feature, featurefolder, outfile):
        starts = []
        ends = []
        levels = np.logspace(-1, 8, num=numlevels, base=2, endpoint=True)
        for level in levels:
            s = np.linspace(50, 450, num=pointsperlevel, endpoint=True)
            starts.append(s)
            ends.append(s+level)
        starts = np.resize(starts, (pointsperlevel*numlevels))
        ends = np.resize(ends, (pointsperlevel*numlevels))
        self.plotAverageMDS(feature, featurefolder, outfile, starts, ends)
    
    def writeJson(self, list, path):
        with open(path, 'w') as file:
            json.dump(list, file)
    
    def saveSegmentAnalysis(self, feature, featuresfolder, outfolder):
        numsegments = np.logspace(0, 9, base=2, num=10, endpoint=True)
        segmentlengths = np.logspace(-5, 7, base=2, num=13, endpoint=True)
        dist = {"numsegments":numsegments.tolist(),"segmentlengths":segmentlengths.tolist(),"distances":[]}
        for i in range(len(numsegments)):
            current_dist = []
            for j in range(len(segmentlengths)):
                starts = np.linspace(50, 450, num=numsegments[i], endpoint=True)
                ends = starts+segmentlengths[j]
                distances = self.getAvgDistances(feature, featuresfolder, starts, ends)
                current_dist.append(distances.tolist())
                print "segments:", numsegments[i], "lengths (sec):", segmentlengths[j]
            dist["distances"].append(current_dist)
        self.writeJson(dist, outfolder+"dist.json")
    
    def saveParameterAnalysis(self, distfile, outfolder):
        with open(distfile) as file:
            distjson = json.load(file)
        numsegments = distjson["numsegments"]
        segmentlengths = distjson["segmentlengths"]
        totalchannels = len(distjson["distances"][0][0])
        shape = [len(numsegments), len(segmentlengths)]
        means = np.empty(shape)
        varis = np.empty(shape)
        close = np.empty(shape)
        fit = np.empty(shape)
        for i in range(len(numsegments)):
            current_dist = []
            for j in range(len(segmentlengths)):
                distances = np.array(distjson["distances"][i][j])
                means[i][j] = distances.mean()
                varis[i][j] = distances.var()
                #extrm[i][j] = np.minimum(distances.max()-distances, distances).mean()
                close[i][j] = (distances < means[i][j]/3).sum()-totalchannels
                fit[i][j] = means[i][j]*close[i][j]
                #print "segments:", numsegments[i], "lengths (sec):", segmentlengths[j], "avg dist:", means[i][j], "var dist:", varis[i][j], "closest:", close[i][j], "fit:", fit[i][j]
        self.plotMatrixHeat(np.array(means), outfolder+"means.png")
        self.plotMatrixHeat(np.array(varis), outfolder+"vars.png")
        self.plotMatrixHeat(np.array(close), outfolder+"close.png")
        self.plotMatrixHeat(np.array(fit), outfolder+"fitness.png")
        self.writeJson(means.tolist(), outfolder+"means.json")
        self.writeJson(varis.tolist(), outfolder+"vars.json")
        self.writeJson(close.tolist(), outfolder+"close.json")
        self.writeJson(fit.tolist(), outfolder+"fitness.json")
    
    def plotMeasures(self, path, names, dim, outfile):
        fig = plt.figure()
        for name in names:
            with open(path+name+'.json') as file:
                matrix = json.load(file)
                plt.plot(np.array(matrix).mean(dim), label=name)
        fig.patch.set_facecolor('white')
        plt.savefig(path+outfile, facecolor='white', edgecolor='none')
    
    def testLinearity(self):
        start = 50
        length = 400
        points = 256
        starts = np.linspace(start, start+length, num=points, endpoint=False)
        ends = starts+(float(length)/points)
        self.plotAverageMDS("chroma", "features/channels/", "plots/test/chroma_mds_"+str(points)+"_1", starts, ends)
