'''
Created on Jun 13, 2016

@author: root
'''
import xml.dom.minidom
import math
'''
def Nearest(v, listV):
    minV = listV[len(listV)-1][1]
    value = minV
    for i in range(0,len(listV)):
        #if(abs(v-listV[i][0]) < minV):
        #    minV = abs(v-listV[i][0])
        #    value = listV[i][0]
        if(abs(v-listV[i][1]) < minV):
            minV = abs(v-listV[i][1])
            value = listV[i][1]
    return value    
def getBestSpliting(duree, NbDespartie, shotList):
    result=[]
    tailleDeCase = duree / NbDespartie
    debutSeg = finSeg=0;
    for i in range(0, NbDespartie):
        debutSeg = finSeg
        finSeg = Nearest(finSeg + tailleDeCase, shotList)
        result.append([debutSeg, finSeg])
    print result
'''
def intersection(startI, endI, startJ,endJ):
    i0 = max(startI, startJ)
    i1 = min(endI, endJ)
    if i0 >= i1:
        return 0
    else:
        return i1-i0
def getNbFacesVariation(fileName, NbDespartie):
    doc = xml.dom.minidom.parse(fileName)
    shotList = doc.getElementsByTagName("Shot")
    
    duree= float(doc.getElementsByTagName("Duration")[0].childNodes[0].data)
    tailleDeCase = duree / NbDespartie
    #print tailleDeCase
    pourcentage=[]
    listFaces=[]
    debutSeg = 0
    finSeg = 0
    for i in range(0, NbDespartie):
        debutSeg=finSeg
        finSeg = finSeg + tailleDeCase
        listFaces=set()
        for s in shotList:
            nbFaces = int(s.getAttribute('nbFaces'))      
            debut = float(s.getAttribute('stime'))
            fin = float(s.getAttribute('etime'))
            if debut > finSeg:
                break
            intersect = intersection(debutSeg,finSeg,debut,fin)
            if intersect > 0:
                listFaces.add(nbFaces)
        pourcentage.append(listFaces)
    return pourcentage
    #videoSegments = getBestSpliting(duree, NbDespartie, TableauDesPlans)
    #print videoSegments
def getMeanVariancePatches(allpatchesSegment):
    #print allpatchesSegment
    sumPatches=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    #sumPatchesSquare=[0,0,0,0,0,0,0,0,0]
    varianceP = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    for i in range(len(allpatchesSegment)):
        patch = allpatchesSegment[i]
        sumPatches = [sumPatches[j]+patch[j] for j in range(len(patch))]
        #sumPatchesSquare = [sumPatchesSquare[j]+(patch[j]*patch[j]) for j in range(len(patch))]
    meanP = [round(sumPatches[j]/len(allpatchesSegment)) for j in range(len(sumPatches))]
    
    for i in range(len(allpatchesSegment)):
        patch = allpatchesSegment[i]
        for j in range(len(patch)):
            varianceP[j] = varianceP[j]+((patch[j]-meanP[j])*(patch[j]-meanP[j]))
    #print varianceP    
    for i in range(len(patch)):
        varianceP[i] = round(math.sqrt(varianceP[i]/len(allpatchesSegment)))
    #varianceP = [sumPatchesSquare[j]/len(allpatchesSegment) for j in range(len(sumPatchesSquare))]
    #varianceP = [varianceP[j] - (meanP[j]*meanP[j]) for j in range(len(varianceP))]
    #print str(meanP) + " , " + str(varianceP)
    return meanP, varianceP

def getKeyframesInterIntraSegmentsIntensityVariation(fileName, NbDespartie):
    # in this method we calculate the inter and intra segment variation of the intensity colos over the patches
    #we compute also the number of transitions from one shot to another shot inside a segment
    doc = xml.dom.minidom.parse(fileName)
    shotList = doc.getElementsByTagName("Shot")
    
    duree= float(doc.getElementsByTagName("Duration")[0].childNodes[0].data)
    tailleDeCase = duree / NbDespartie
    #print tailleDeCase
    variationInter = []
    variationIntra = []
    debutSeg = 0
    finSeg = 0
    listpatches=[]
    allpatchesSegment = []
    nbTransitions =[]
    for i in range(0, NbDespartie):
        debutSeg=finSeg
        finSeg = finSeg + tailleDeCase
        averagePatches=[0,0,0,0,0,0,0,0,0]
        allpatchesSegment = []
        cmpt=0
        #print "########: " + str(debutSeg) + " : " + str(finSeg)
        for s in shotList:
            weight = 0
            patches = [int(v) for v in s.getAttribute('Patches')[1:-1].split(",")]      
            debut = float(s.getAttribute('stime'))
            fin = float(s.getAttribute('etime'))
            if debut > finSeg:
                break
            intersect = intersection(debutSeg,finSeg,debut,fin)
            if intersect > 0:
                #print str(i+1) + " : " + str(debut) + " , " + str(fin)
                weight = float(intersect)/ (finSeg-debutSeg)
                #print(weight)
                averagePatches = [averagePatches[j]+weight*patches[j] for j in range(len(patches))]
                allpatchesSegment.append(patches)
            if fin > debutSeg and fin < finSeg:
                cmpt = cmpt+1
        meanPatches, variancePatches = getMeanVariancePatches(allpatchesSegment)
        #print cmpt
        nbTransitions.append(cmpt*100/duree)
        #variationIntra.append(meanPatches)
        variationIntra.append(variancePatches)
        #averagePatches = [float(averagePatches[i])*weight for i in range(len(averagePatches))]
        listpatches.append(averagePatches)
        #pourcentage.append(listPatches)
    #print listpatches
    for i in range(0,len(listpatches)-1):
        l=[round(abs(listpatches[i][j]-listpatches[i+1][j]),2) for j in range(0,len(listpatches[i]))]
        variationInter.append(l)
    return variationInter, variationIntra, nbTransitions
    #videoSegments = getBestSpliting(duree, NbDespartie, TableauDesPlans)
    #print videoSegments    
'''    
if __name__ == '__main__':
    #getNbFacesVariation( "/home/zein/Eclipse_Workspace/test_Dataset/DEV_DESCRIPTORS_L0/Culinarymedia-QuickBitesHawaiiDay1729.xml", 4)
    inter, intra, nb = getKeyframesInterIntraSegmentsIntensityVariation( "/home/zein/Eclipse_Workspace/test_Dataset/DEV_DESCRIPTORS_L0/Culinarymedia-QuickBitesHawaiiDay1729.xml", 4)
    print nb
    i=0
    #while(i<len(intra)):
    #      print str(intra[i]) +" , "+str(intra[i+1])
    #      i=i+2
    pass
    
    '''