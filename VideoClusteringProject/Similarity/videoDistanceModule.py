'''
Created on Jul 1, 2016

@author: malak
'''
import xml.dom.minidom
import numpy as np

def EuclidienneDistanceV1(v1,v2):
    sumV=0
    x=0
    if type(v1) is list and type(v2) is list:
        for i in range(len(v1)):
            if type(v1[i]) is list and type(v2[i]) is list:
                x=EuclidienneDistance(v1[i],v2[i])
                sumV=sumV+x
            else:
                a=float(v1[i])-float(v2[i])
                b=pow(a,2)
                sumV=sumV+b
        sumV=pow(sumV,0.5)
        return sumV
    else:
        return -1

def EuclidienneDistanceV2(v1,v2):
    sumV=0
    if type(v1) is list and type(v2) is list:
        for i in range(len(v1)):
            if type(v1[i]) is list and type(v2[i]) is list:
                a = float(Moyen(v1[i])) - float(Moyen(v2[i]))
            else:
                a=float(v1[i])-float(v2[i])
            b=pow(a,2)
            sumV=sumV+b
        sumV=pow(sumV,0.5)
        return sumV
    else:
        return -1
 
def EuclidienneDistance(v1,v2):
    sumV=0
    for i in range(0,len(v1)):
        a=float(v1[i])-float(v2[i])
        b=pow(a,2)
        sumV=sumV+b
    #sumV=pow(sumV,0.5)
    return sumV

def ManhatanDistanceV1(v1,v2):
    sumV=0
    x=0
    if type(v1) is list and type(v2) is list:
        for i in range(len(v1)):
            if type(v1[i]) is list and type(v2[i]) is list:
                x=ManhatanDistance(v1[i],v2[i])
                sumV=sumV+x
            else:
                a=abs(float(v1[i])-float(v2[i]))
                sumV=sumV+a
        return sumV
    else:
        return -1
def ManhatanDistanceV2(v1,v2):
    sumV=0
    if type(v1) is list and type(v2) is list:
        for i in range(len(v1)):
            if type(v1[i]) is list and type(v2[i]) is list:
                a = abs(float(Moyen(v1[i]))-float(Moyen(v2[i])))
            else:
                a=abs(float(v1[i])-float(v2[i]))
            sumV=sumV+a
        return sumV
    else:
        return -1
def ManhatanDistance(v1,v2):
    sumV=0
    for i in range(0,len(v1)):
        a=float(v1[i])-float(v2[i])
        a=abs(a)
        sumV=sumV+a
    return sumV

def ConvertAudioFeatureToVector(fileName,niveau,nbSeg):
    doc=xml.dom.minidom.parse(fileName)
    v=[] 
    desc=doc.getElementsByTagName("Descriptors")[niveau-1]
    interaction=float(desc.getElementsByTagName("Interaction")[nbSeg-1].childNodes[0].data)
    v.append(interaction)
    #interventions=desc.getElementsByTagName("Interventions")[niveau-1]
    interventionCourte=float(desc.getElementsByTagName("Intervention")[nbSeg-1].childNodes[0].data)
    v.append(interventionCourte)
    interventionLongue=float(desc.getElementsByTagName("Intervention")[nbSeg].childNodes[0].data)
    v.append(interventionLongue)
    PonctuelSpeaker=float(desc.getElementsByTagName("Ponctuel")[nbSeg-1].childNodes[0].data)
    v.append(PonctuelSpeaker)
    LocaliseSpeaker=float(desc.getElementsByTagName("Localise")[nbSeg-1].childNodes[0].data)
    v.append(LocaliseSpeaker)
    PresentSpeaker=float(desc.getElementsByTagName("Present")[nbSeg-1].childNodes[0].data)
    v.append(PresentSpeaker)
    RegulierSpeaker=float(desc.getElementsByTagName("Regulier")[nbSeg-1].childNodes[0].data)
    v.append(RegulierSpeaker)
    ImportantSpeaker=float(desc.getElementsByTagName("Important")[nbSeg-1].childNodes[0].data)
    v.append(ImportantSpeaker)
    SpeakerDistribution=float(desc.getElementsByTagName("SpeakerDistribution")[nbSeg-1].childNodes[0].data)
    v.append(SpeakerDistribution)
    NumberSpeakerTransition=float(desc.getElementsByTagName("NumberSpeakerTransition")[nbSeg-1].childNodes[0].data)
    v.append(NumberSpeakerTransition)
    Speech=float(desc.getElementsByTagName("Speech")[nbSeg-1].childNodes[0].data)
    v.append(Speech)
    Music=float(desc.getElementsByTagName("Music")[nbSeg-1].childNodes[0].data)
    v.append(Music)
    SpeechWithMusic=float(desc.getElementsByTagName("SpeechWithMusic")[nbSeg-1].childNodes[0].data)
    v.append(SpeechWithMusic)
    SpeechWithNonMusic=float(desc.getElementsByTagName("SpeechWithNonMusic")[nbSeg-1].childNodes[0].data)
    v.append(SpeechWithNonMusic)
    NonSpeechWithMusic=float(desc.getElementsByTagName("NonSpeechWithMusic")[nbSeg-1].childNodes[0].data)
    v.append(NonSpeechWithMusic)
    NonSpeechWithNonMusic=float(desc.getElementsByTagName("NonSpeechWithNonMusic")[nbSeg-1].childNodes[0].data)
    v.append(NonSpeechWithNonMusic)
    #print (v)
    return v
     
def ConvertVideoFeatureToVector(fileName,niveau,nbSeg):
    doc=xml.dom.minidom.parse(fileName)
    v=[] 
    desc=doc.getElementsByTagName("Descriptors")[niveau-1]
    MinValue=float(desc.getElementsByTagName("MinValue")[nbSeg-1].childNodes[0].data)
    v.append(MinValue)
    MaxValue=float(desc.getElementsByTagName("MaxValue")[nbSeg-1].childNodes[0].data)
    v.append(MaxValue)
    nbShotTransition=float(desc.getElementsByTagName("NumberShotTransition")[nbSeg-1].childNodes[0].data)
    v.append(nbShotTransition)
    if niveau!=1:
        InterIntensityVariation=desc.getElementsByTagName("InterIntensityVariation")[nbSeg-1].childNodes[0].data
        inter=splitString(InterIntensityVariation)
        v.append(inter)
    IntraIntensityVariation=desc.getElementsByTagName("IntraIntensityVariation")[nbSeg-1].childNodes[0].data
    intra=splitString(IntraIntensityVariation)
    v.append(intra)
    #print v
    return v
    
def Moyen(v):
    s=0
    for i in range(len(v)):
        j=float(v[i])
        s=s+j
    moyenV = s/len(v)
    return moyenV
             
def DistanceEntre2Descripteurs(modalite,f1,f2,niveau,nbSeg):
    if modalite=='Audio':
        v1=ConvertAudioFeatureToVector(f1,niveau,nbSeg)
        v2=ConvertAudioFeatureToVector(f2,niveau,nbSeg)
        value1 = ManhatanDistanceV2(v1,v2)
        value2 = EuclidienneDistanceV2(v1,v2)
    elif modalite=='Video':    
        v1=ConvertVideoFeatureToVector(f1,niveau,nbSeg)
        v2=ConvertVideoFeatureToVector(f2,niveau,nbSeg)
        value1 = ManhatanDistanceV2(v1,v2)
        value2 = EuclidienneDistanceV2(v1,v2)
    else:
        value1=-1
        value2=-1
    return value1,value2
 
def splitString(s):
    v=[]
    vecteur=s[1:-1].split(',')
    for i in range(len(vecteur)):
        v.append(float(vecteur[i]))
    return v          
     
if __name__ == '__main__':
    filename = "/media/zein/835C-4E2D/Research Datasets/test_Dataset/listReadyVideos.txt"
    
    videoList=[line.rstrip('\n') for line in open(filename)]
    
    #print videoList[0].childNodes[0].data
    cheminGenerale="/media/zein/835C-4E2D/Research Datasets/test_Dataset/DEV_DESCRIPTORS_L1/"
    
    l = len(videoList)
    DVideoE = np.zeros((l,l))
    DAudioE = np.zeros((l,l))
    DVideoM = np.zeros((l,l))
    DAudioM = np.zeros((l,l))
    for i in range(l-1):
        for j in range(i+1, l):
            distAM, distAE = DistanceEntre2Descripteurs('Audio',cheminGenerale+videoList[i],cheminGenerale+videoList[j],1,1)
            distVM, distVE = DistanceEntre2Descripteurs('Video',cheminGenerale+videoList[i],cheminGenerale+videoList[j],1,1)
            DAudioE[i][j] = distAE
            DAudioE[j][i] = distAE
            DVideoE[i][j] = distVE
            DVideoE[j][i] = distVE
            DAudioM[i][j] = distAM
            DAudioM[j][i] = distAM
            DVideoM[i][j] = distVM
            DVideoM[j][i] = distVM
    #print DAudio
    np.savetxt('DAudioM_V2.out', DAudioM, fmt='%.2f',delimiter='\t', newline='\n')
    np.savetxt('DVideoM_V2.out', DVideoM, fmt='%.2f',delimiter='\t', newline='\n')
    np.savetxt('DAudioE_V2.out', DAudioE, fmt='%.2f',delimiter='\t', newline='\n')
    np.savetxt('DVideoE_V2.out', DVideoE, fmt='%.2f',delimiter='\t', newline='\n')

    
pass