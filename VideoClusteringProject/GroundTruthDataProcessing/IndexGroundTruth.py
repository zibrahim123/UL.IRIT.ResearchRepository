'''
Created on Jul 2, 2016

@author: root
'''
import xml.dom.minidom
from xml.dom.minidom import Document
import io

def getVideoDuration(videoName):
    try:
        DOMTreeOut = xml.dom.minidom.parse("../../test_Dataset/DEV_METADATA/" + str(videoName) + ".xml")
        root = DOMTreeOut.documentElement
        #remove the child for this number of segments if exists
        duration = root.getElementsByTagName("duration")
        return duration[0].firstChild.nodeValue
    except IOError:
        return "-1"
        
def indexGroundTruthByType(filename, filecode):
    
    fCodes = open(filecode,"r")
    fTypes = open(filename,"r")
    
    dictVideoName_CodeType = {}
    for line in fTypes:
        v = line.split(" ")
        #print v
        dictVideoName_CodeType[v[2]] = int(v[0])
    #print dictVideoName_CodeType
    
    
    dictCode_NameType = {}
    indexeVideoByType = {}
    for line in fCodes:
        v = line.split(" ")
        #print v[1][:-2]
        dictCode_NameType[int(v[0])] = v[1][:-2]
        indexeVideoByType[int(v[0])]=[]
    #print dictCode_NameType
    
    for key in dictVideoName_CodeType:
        codeType = dictVideoName_CodeType[key]
        l = indexeVideoByType[codeType]
        l.append(key)
        indexeVideoByType[codeType] = l
            
    DOMTreeOut1 = Document()
    root1 = DOMTreeOut1.createElement("VideoList")
    DOMTreeOut1.appendChild(root1)
    for key in dictVideoName_CodeType:
        code = dictVideoName_CodeType[key]
        typeV = dictCode_NameType[code]
        video = DOMTreeOut1.createElement("Video")
        video.setAttribute("type", typeV)
        video.setAttribute("codeType", str(code))
        #print key + " : " + getVideoDuration(key)
        video.setAttribute("duration",str(getVideoDuration(key)))
        video.appendChild(DOMTreeOut1.createTextNode(key))
        root1.appendChild(video)
    
    DOMTreeOut2 = Document()
    root2 = DOMTreeOut2.createElement("TypeList")
    root2.setAttribute("size", str(len(indexeVideoByType)))
    DOMTreeOut2.appendChild(root2)
    for key in indexeVideoByType:
        typeV = DOMTreeOut2.createElement("Type")
        typeV.setAttribute("typename", dictCode_NameType[key])
        nb = 0
        for v in indexeVideoByType[key]:
            video = DOMTreeOut2.createElement("Video")
            video.setAttribute("duration",str(getVideoDuration(v)))
            video.appendChild(DOMTreeOut2.createTextNode(v))
            typeV.appendChild(video)
            nb += 1
        typeV.setAttribute("size",str(nb))
        root2.appendChild(typeV)
    
    file_handle = io.open("videoList.xml", 'wb')
    DOMTreeOut1.writexml(file_handle)
    file_handle.close()
    
    file_handle = io.open("typeList.xml", 'wb')
    DOMTreeOut2.writexml(file_handle)
    file_handle.close()
    print "Indexed ground truth created successfully"   
    
indexGroundTruthByType("/media/zein/835C-4E2D/Research Datasets/DataSet - MediaEval/Dev/GroundTruth/me12_gt_devset_groundtruth.txt", "/media/zein/835C-4E2D/Research Datasets/DataSet - MediaEval/Dev/GroundTruth/me12_gt_genrecodes.txt")