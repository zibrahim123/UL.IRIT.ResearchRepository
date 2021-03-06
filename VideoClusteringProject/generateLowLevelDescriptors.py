'''
Created on May 12, 2016

@author: zein
'''
#from FeaturesL0.extractAudioLowLevelFeatures import extractMFCC_ZCR
from FeaturesL0.extractMetaDataModule import extractMetaData
from FeaturesL0.extractVideoDataModule import extractVideoData
from FeaturesL0.PMBSegmentation_Julien.PMBFunction import PMBSegmentation
from FeaturesL0.FaceDetection.DetectNumberOfFaces import extractFaceFromKeyframes
from FeaturesL0.extractAudioDataModule import extractAudioData
import sys
from FeaturesL0Combined.combineLowLevelFeatures import generatePercentageDescriptors
import xml.dom.minidom
import io
#from FaceDetection import *
def loadPMBSegmentationFromOldFiles(oldPath, newPath, fileName):
    f = open("toDoCompletely.txt","a")
    try:
        DOMTreeIn = xml.dom.minidom.parse(oldPath)
        DOMTreeOut = xml.dom.minidom.parse(newPath)
        rootIn = DOMTreeIn.documentElement
        rootOut = DOMTreeOut.documentElement
    
        audio = DOMTreeOut.getElementsByTagName("Audio")[0]
        pseg = DOMTreeIn.getElementsByTagName("SpeechSegmentation")
        mseg = DOMTreeIn.getElementsByTagName("MusicSegmentation")
        if len(pseg)==0 or len(mseg)==0:
            f.write(fileName+"\n")
            f.close()
            return -1
        audio.appendChild(pseg[0])
        audio.appendChild(mseg[0])
    
        file_handle = io.open(newPath, 'wb')
        rootOut.writexml(file_handle)
        file_handle.close()
        f.close()
        return 0
        #print ('ASR file opened for processing: '+ asrFilePath)
    except IOError:
        f.write(fileName+"\n")
        print ('loading PMB segmentation from old file failed')
        print (oldPath)
        f.close()
        return -1
      
generalPath = '/media/zein/835C-4E2D/Research Datasets/test_Dataset/'
#lstVideos = 'listVideo.txt'
#script_dir = os.path.dirname(__file__)
part="DEV_"
#print script_dir
nameFileVideo =  sys.argv[1]
#print nameFileVideo
target = open("Output.txt", 'w')
try:
    #Creation of the name of the audio file
    #nameFileVideoPath = generalPath + part +"VIDEO/" + nameFileVideo

    nameFileVideoPath = '/media/zein/835C-4E2D/Research Datasets/DataSet - MediaEval/Dev/Video/MEDIAEVAL/DEV_VIDEO/' + nameFileVideo
    #print "nameFileVideo: "+nameFileVideo
    nameFileAudioPath = generalPath + part +"AUDIO/new/" + nameFileVideo[:len(nameFileVideo)-8] + ".wav"
    #print "nameFileAudioPath: "+nameFileAudioPath
    nameFileOutputXML = generalPath + part +"DESCRIPTORS_L0/new/" + nameFileVideo[:len(nameFileVideo)-8] + ".xml"
    #print "nameFileOutputXML: "+nameFileOutputXML
    #metadataFilePath = generalPath + part +"METADATA/" + nameFileVideo[:len(nameFileVideo)-8] + ".xml"
    metadataFilePath = generalPath + part +"METADATA/" + nameFileVideo[:len(nameFileVideo)-8] + ".xml"
    #print "metadataFilePath: "+metadataFilePath
    #asrFilePath = generalPath + part +"LIMSI_ASR/xml/" + nameFileVideo[:len(nameFileVideo)] + ".xml"
    asrFilePath = generalPath + part +"LIMSI_ASR/" + nameFileVideo[:len(nameFileVideo)] + ".xml"
    #print "asrFilePath: "+asrFilePath
    videoFilePath = generalPath + part +"SHOT/" + nameFileVideo[:len(nameFileVideo)-8] + ".xml"
    #print "videoFilePath: "+videoFilePath
    
    #outputXML=open(nameFileOutputXML,'w')
    vmeta = extractMetaData(metadataFilePath,nameFileOutputXML)
    vaudio = extractAudioData(asrFilePath,nameFileOutputXML)
    vvideo = extractVideoData(videoFilePath,nameFileOutputXML,nameFileVideoPath)
    
    if vmeta == -1 or vaudio == -1 or vvideo == -1:
        target. write(nameFileVideo + " failed:  vmeta = "+str(vmeta)+" , vaudio = "+ str(vaudio)+ " , vvideo = "+str(vvideo)+"\n")
    else:
        v = loadPMBSegmentationFromOldFiles(generalPath + part +"DESCRIPTORS_L0/old/"+nameFileVideo[:len(nameFileVideo)-8] + ".xml",generalPath + part +"DESCRIPTORS_L0/"+nameFileVideo[:len(nameFileVideo)-8] + ".xml", nameFileVideo)
        if v == -1:
            #print "loading from another location"
            v = loadPMBSegmentationFromOldFiles(generalPath + part +"DESCRIPTORS_L0/old+/"+nameFileVideo[:len(nameFileVideo)-8] + ".xml",generalPath + part +"DESCRIPTORS_L0/"+nameFileVideo[:len(nameFileVideo)-8] + ".xml", nameFileVideo)
            if v == -1:
                vseg = PMBSegmentation(['--4Hz','--NBS', '-i', generalPath + part+ "AUDIO/new/" + nameFileVideo + ".wav"],nameFileOutputXML)
                #print vseg
                if vseg == -1:
                    target.write(" Failed to extract audio segmentations " + nameFileVideo + "\n") 
                #else:
                    #extractMFCC_ZCR(generalPath + "Audio/" + nameFileVideo + ".wav", nameFileOutputXML, 512, 13, 0) # 0 for sampling rate means the original one
    
    vframes = extractFaceFromKeyframes(generalPath + part+"SHOT/",nameFileOutputXML,nameFileVideoPath)
    if vframes == -1:
        target. write(" Failed to extract faces " + nameFileVideo + " continue anyway\n") 
    
    for i in range(1,5):
        generatePercentageDescriptors(nameFileOutputXML, generalPath + part +"DESCRIPTORS_L1/new/" + nameFileVideo[:len(nameFileVideo)-8] + ".xml",i)
    
    target.write(nameFileVideo + " OK\n")
except:
    target.write(nameFileVideo + " failed: Error\n")
    target.write(str(sys.exc_info()[0]))
finally:
    target.close()
