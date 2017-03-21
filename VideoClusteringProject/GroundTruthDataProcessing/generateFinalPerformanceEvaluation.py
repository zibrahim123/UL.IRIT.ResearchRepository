'''
Created on Sep 21, 2016

@author: root
'''
def returnVideoTypeList(filename):
    videoTypeDict = {}
    infile = open(filename,"r")
    for line in infile:
        lineWords = line.split("\t")
        videoTypeDict[lineWords[0][:-8]] = lineWords[1]
    infile.close()
    return videoTypeDict
def attachGroundTructhtoClusters(clusterFileName, filename):
    videoTypeDict = returnVideoTypeList(filename)
    infile = open(clusterFileName,"r")
    outfile = open("myResults/Run4_75%Video_25%Audio/Run4_ResultatsSCwithTypes.txt","w")
    for line in infile:
        if line=="\n" or line.startswith("Classe"):
            outfile.write(line)
        else:
            type = videoTypeDict[line[:-9]]
            print line[:-9] + " , "+ type
            name = line[:-1]
            outfile.write(name)
            outfile.write("\t")
            outfile.write(type)
            outfile.write("\n")
    outfile.close()
    infile.close()
def computeDistributionPerClusters(clusterFileName, filename):
    videoTypeDict = returnVideoTypeList(filename)
    listvideos=[]
    totalPercentage = 0
    infile = open(clusterFileName,"r")
    outfile = open("myResults/Run4_75%Video_25%Audio/Run4_ResultatsSCwithTypesDistributionperClusters.txt","w")
    for line in infile:
        if line=="\n" or line.startswith("Classe"):
            outfile.write(line)
            dist = computeAndWriteDistribution(listvideos,outfile)
            totalPercentage = totalPercentage + dist
            listvideos=[]
        else:
            type = videoTypeDict[line[:-9]]
            listvideos.append(type)
    outfile.write(str(totalPercentage))
    outfile.close()
    infile.close()
def computeAndWriteDistribution(listvideos,outfile):
    if listvideos==[]:
        return 0
    listvideos.sort()
    dict = {}
    maxV=-1;
    sommeV=0.0;
    for v in listvideos:
        if dict.has_key(v):
            dict[v]=dict[v]+1
        else:
            dict[v]=1
    for key in dict:
        if maxV < dict[key]:
            maxV = dict[key]
        sommeV = sommeV + dict[key]
        outfile.write(key + "\t"+str(dict[key])+"\n")
    v = maxV*100/sommeV
    outfile.write(str(v))
    return v
        
attachGroundTructhtoClusters("myResults/Run4_75%Video_25%Audio/ResultatSC.txt", "IndexedVideoList.txt")
computeDistributionPerClusters("myResults/Run4_75%Video_25%Audio/ResultatSC.txt", "IndexedVideoList.txt")
