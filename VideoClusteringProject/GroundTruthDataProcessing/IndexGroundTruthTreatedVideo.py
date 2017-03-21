'''
Created on Sep 19, 2016

@author: root
'''
'''
Created on Jul 2, 2016

@author: root
'''
import xml.dom.minidom
from xml.dom.minidom import Document


def getVideoDuration(videoName):
    try:
        DOMTreeOut = xml.dom.minidom.parse("../../test_Dataset/DEV_METADATA/" + str(videoName) + ".xml")
        root = DOMTreeOut.documentElement
        #remove the child for this number of segments if exists
        duration = root.getElementsByTagName("duration")
        return duration[0].firstChild.nodeValue
    except IOError:
        return "-1"
        
def indexGroundTruthByType(filename, filecode, videoTreatedListTxT):
    try:
        fCodes = open(filecode,"r")
        fTypes = open(filename,"r")
        fVideoList = open(videoTreatedListTxT,"r")
    except:
        print "No opened files"
        return
    dictVideoName_CodeType = {}
    for line in fTypes:
        v = line.split(" ")
        #print v
        dictVideoName_CodeType[v[2]] = int(v[0])
    #print dictVideoName_CodeType
    TreatedVideos =set()
    types = []
    durations =[]
    
    for line in fVideoList:
        v = line[:-9]
        #print v
        TreatedVideos.add(v)
    #print dictTreatedVideos
    #print len(dictTreatedVideos)
    videoTreatedList = {}

    dictCode_NameType = {}
    indexeVideoByType = {}
    Type_Video_dict={}
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
    
    fCodes.close()
    fTypes.close() 
    fVideoList.close()      
    lst=[]
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
        d = str(getVideoDuration(key))
        video.setAttribute("duration",d)
        video.appendChild(DOMTreeOut1.createTextNode(key))
        root1.appendChild(video)
        if key in TreatedVideos:
            videoTreatedList[key]=[typeV,d]
            types.append(typeV)
            durations.append(int(d))
            
            if Type_Video_dict.has_key(typeV):
                l = Type_Video_dict[typeV]
                l.append(key)
                Type_Video_dict[typeV]=l
            else:
                lst=[]
                lst.append(key)
                Type_Video_dict[typeV]=lst
               
    types.sort()
    durations.sort()
    #print videoTreatedList
    fVideoList = open(videoTreatedListTxT,"r")
    file_handle = open("IndexedVideoList.txt", 'w')
    #for key in videoTreatedList:
    for line in fVideoList:
        v = line[:-9]
        print v
        file_handle.write(v + ".flv.ogv\t" + videoTreatedList[v][0] + "\t"+ videoTreatedList[v][1] + "\n")
        #print key + "\t" + videoTreatedList[key][0] + "\t"+ videoTreatedList[key][1] + "\n"
    fVideoList.close()
    file_handle.close()
    
    file_handle = open("IndexedVideoList_Types.txt", 'w')
    for v in types:
        file_handle.write(v + "\n")
        #print key + "\t" + videoTreatedList[key][0] + "\t"+ videoTreatedList[key][1] + "\n"
    file_handle.close()
    
    file_handle = open("IndexedVideoList_Durations.txt", 'w')
    for v in durations:
        file_handle.write(str(v) + "\n")
        #print key + "\t" + videoTreatedList[key][0] + "\t"+ videoTreatedList[key][1] + "\n"
    file_handle.close()
    '''
    file_handle = open("IndexedVideoList_OrginizedByType.txt", 'w')
    for key in Type_Video_dict:
        videos = Type_Video_dict[key]
        for v in videos:
            file_handle.write(v + ".flv.ogv\n")
        #print key + "\t" + videoTreatedList[key][0] + "\t"+ videoTreatedList[key][1] + "\n"
    file_handle.close()
    '''
    print "Indexed ground truth created successfully"   
    
indexGroundTruthByType("/media/zein/835C-4E2D/Research Datasets/DataSet - MediaEval/Dev/GroundTruth/me12_gt_devset_groundtruth.txt", "/media/zein/835C-4E2D/Research Datasets/DataSet - MediaEval/Dev/GroundTruth/me12_gt_genrecodes.txt","/home/zein/Desktop/Final Descriptors/finalVideoList.txt")