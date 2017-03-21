'''
Created on Jul 23, 2016
this script aims to write the list of descriptors for a set of videos into a text file instead of xml file.
@author: root
'''
import xml.dom.minidom
import math
import numpy as np

def toText(videoListPath,xmlVideoPathL1,xmlVideoPathL0,nbsegment):
    videoList=[line.rstrip('\n') for line in open(videoListPath)]
    l = len(videoList)
    f=open("/home/zein/Desktop/Final Descriptors/DescriptorsList.txt","w")
    Headers =   "NomVideo\tDuree\tInteraction2Locuteurs\tInteraction3Locuteurs\tInteraction4Locuteurs\tInteraction4+Locuteurs\tInterventionCourte\tInterventionLongue\tSPonctuel\tSLocalise\tSPresent\tSRegulier\tSImportant\t"  
    Headers += "DistributionLocuteur\tTransitionLocuteur\tParole\tMusique\tParole+Musique\tParole+NonMusique\tNonParole+Musique\tNonParole+NonMusique\t"
    Headers += "VisageNombreMin\tVisageNombreMax\tNombreTransitionPlan\tIntraVariationMoyen\n"
    f.write(Headers)  
    for i in range(l):
        filename = videoList[i]
        print filename
        writeDescriptorsForAVideo(xmlVideoPathL1, xmlVideoPathL0, filename,f,nbsegment)

    f.close()    
        
def writeDescriptorsForAVideo(xmlVideoPath,xmlVideoPath2, fileName,outFile,niveau):        
    doc=xml.dom.minidom.parse(xmlVideoPath+fileName)
    doc2 = xml.dom.minidom.parse(xmlVideoPath2+fileName)
    duree = doc2.getElementsByTagName("Duration")[0].childNodes[0].data
    outFile.write(fileName + "\t")
    outFile.write(duree + "\t")
    desc=doc.getElementsByTagName("Descriptors")[niveau-1]
    interaction=desc.getElementsByTagName("Interaction")
    locs_2 = interaction[1].childNodes[0].data
    outFile.write(locs_2+"\t")
    locs_3 = interaction[2].childNodes[0].data
    outFile.write(locs_3+"\t")
    locs_4 = interaction[3].childNodes[0].data
    outFile.write(locs_4+"\t")
    locs_4 = interaction[3].childNodes[0].data
    outFile.write(locs_4+"\t")
    
    interventionCourte=desc.getElementsByTagName("Intervention")[0].childNodes[0].data
    outFile.write(interventionCourte+"\t")
    interventionLongue=desc.getElementsByTagName("Intervention")[1].childNodes[0].data
    outFile.write(interventionLongue+"\t")
    PonctuelSpeaker=desc.getElementsByTagName("Ponctuel")[0].childNodes[0].data
    outFile.write(PonctuelSpeaker+"\t")
    LocaliseSpeaker=desc.getElementsByTagName("Localise")[0].childNodes[0].data
    outFile.write(LocaliseSpeaker+"\t")
    PresentSpeaker=desc.getElementsByTagName("Present")[0].childNodes[0].data
    outFile.write(PresentSpeaker+"\t")
    RegulierSpeaker=desc.getElementsByTagName("Regulier")[0].childNodes[0].data
    outFile.write(RegulierSpeaker+"\t")
    ImportantSpeaker=desc.getElementsByTagName("Important")[0].childNodes[0].data
    outFile.write(ImportantSpeaker+"\t")
    SpeakerDistribution=desc.getElementsByTagName("SpeakerDistribution")[0].childNodes[0].data
    outFile.write(SpeakerDistribution+"\t")
    NumberSpeakerTransition=desc.getElementsByTagName("NumberSpeakerTransition")[0].childNodes[0].data
    v = (float(NumberSpeakerTransition)/int(duree))*100
    outFile.write(str(v)+"\t")
    Speech=desc.getElementsByTagName("Speech")[0].childNodes[0].data
    outFile.write(Speech+"\t")
    Music=desc.getElementsByTagName("Music")[0].childNodes[0].data
    outFile.write(Music+"\t")
    SpeechWithMusic=desc.getElementsByTagName("SpeechWithMusic")[0].childNodes[0].data
    outFile.write(SpeechWithMusic+"\t")
    SpeechWithNonMusic=desc.getElementsByTagName("SpeechWithNonMusic")[0].childNodes[0].data
    outFile.write(SpeechWithNonMusic+"\t")
    NonSpeechWithMusic=desc.getElementsByTagName("NonSpeechWithMusic")[0].childNodes[0].data
    outFile.write(NonSpeechWithMusic+"\t")
    NonSpeechWithNonMusic=desc.getElementsByTagName("NonSpeechWithNonMusic")[0].childNodes[0].data
    outFile.write(NonSpeechWithNonMusic+"\t")
    
    MinValue=desc.getElementsByTagName("MinValue")[0].childNodes[0].data
    outFile.write(MinValue+"\t")
    MaxValue=desc.getElementsByTagName("MaxValue")[0].childNodes[0].data
    outFile.write(MaxValue+"\t")
    nbShotTransition=desc.getElementsByTagName("NumberShotTransition")[0].childNodes[0].data
    v = (float(nbShotTransition)/int(duree))*100
    outFile.write(str(v) +"\t")

    IntraIntensityVariation=desc.getElementsByTagName("IntraIntensityVariation")[0].childNodes[0].data
    intra=splitString(IntraIntensityVariation)
    v = Moyen(intra)
    outFile.write(str(v)+"\n")    
        
        
def Moyen(v):
    s=0
    for i in range(len(v)):
        s = s + v[i]
    moyenV = s/len(v)
    return moyenV

def splitString(s):
    v=[]
    vecteur=s[1:-1].split(',')
    for i in range(len(vecteur)):
        v.append(math.sqrt(float(vecteur[i])))
    return v   

def generateMatrixDistances(listVideoDescriptors):
    f = open(listVideoDescriptors,"r")
    M=[]
    j=0
    for line in f:
        if j!=0:
            v = line[:-1].split("\t")
            l=[]
            for i in range(2,len(v)):
                l.append(float(v[i]))
            M.append(l)
            #print l
        else:
            j=1
    f.close()
    l=len(M)
    #print l
    Mat = np.zeros((l,l))

    for i in range(len(M[0])):
        #print "Processing feature "+str(i+1)
        for j in range(l-1):
            for k in range(j+1,l):
                Mat[j][k] = math.fabs(M[j][i]-M[k][i])
                Mat[k][j] = Mat[j][k]
        np.savetxt("/home/zein/Desktop/Final Descriptors/Features/Feature_"+str(i+1)+'.out', Mat, fmt='%.4f',delimiter='\t', newline='\n')
        print "Feature"+str(i+1) + " / "+ str(len(M[0]))

def generateAudioVideoMatrixDistances(listVideoDescriptors):
    f = open(listVideoDescriptors,"r")
    M=[]
    j=0
    for line in f:
        if j!=0:
            v = line[:-1].split("\t")
            l=[]
            for i in range(2,len(v)):
                l.append(float(v[i]))
            M.append(l)
            #print l
        else:
            j=1
    f.close()
    l=len(M)
    #print l
    MatAudio = np.zeros((l,l))
    MatVideo = np.zeros((l,l))
    for i in range(l-1):
        for j in range(i+1,l):
            s=0
            for k in range(0,16): 
                s = s + math.pow(M[i][k]-M[j][k],2)
            MatAudio[i][j]=math.sqrt(s)
            MatAudio[j][i]=MatAudio[i][j]     
            s=0
            for k in range(16,20): 
                s = s + math.pow(M[i][k]-M[j][k],2)
            MatVideo[i][j]=math.sqrt(s)
            MatVideo[j][i]=MatVideo[i][j] 
          
    np.savetxt("/home/zein/Desktop/Final Descriptors/Features/Feature_Audio.out", MatAudio, fmt='%.4f',delimiter='\t', newline='\n')
    np.savetxt("/home/zein/Desktop/Final Descriptors/Features/Feature_Video.out", MatVideo, fmt='%.4f',delimiter='\t', newline='\n')       
filename = "/home/zein/Desktop/Final Descriptors/finalDescriptorsList.txt"
cheminGeneraleL1="/home/zein/Desktop/Final Descriptors/DEV_DESCRIPTORS_L1/"
cheminGeneraleL0="/home/zein/Desktop/Final Descriptors/DEV_DESCRIPTORS_L0/"
toText(filename,cheminGeneraleL1,cheminGeneraleL0,1)
generateMatrixDistances("/home/zein/Desktop/Final Descriptors/DescriptorsList.txt")
generateAudioVideoMatrixDistances("/home/zein/Desktop/Final Descriptors/DescriptorsList.txt")