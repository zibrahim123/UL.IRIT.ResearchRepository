'''
Created on May 24, 2016

@author: root
'''
import cv2
import xml.dom.minidom
import io
#from scipy.stats.mstats_basic import moment

def extractVideoData(videoFilePath, outputXMLFile,videoPath):
    # Open XML document using minidom parser
    try:
        DOMTreeIn = xml.dom.minidom.parse(videoFilePath)
        DOMTreeOut = xml.dom.minidom.parse(outputXMLFile)

        #print ('ASR file opened for processing: '+ asrFilePath)
    except IOError:
        print ("Error while opening the xml file of the video shots: " + videoFilePath)
        return -1
    
    
    rootIn = DOMTreeIn.documentElement
    rootOut = DOMTreeOut.documentElement
    
    Image = DOMTreeOut.createElement('Image')
    rootOut.appendChild(Image)
    
    cap = cv2.VideoCapture(videoPath)
    #videoPath = "test_Dataset/Video/Avidcruiser-StockholmsVasaMuseum479.flv.ogv"
    #cap.open()
    #print str(cap.isOpened())
    if not cap.isOpened(): 
        print "could not open the video file to get fps & number of frames:",videoPath[:]
        #print ('Error while opening the video file')
        #fps = "nan"
        #nb = "nan"
        return -1
    else:
        #print "Video file opened : "+ videoPath[:]
        fps = str(cap.get(cv2.cv.CV_CAP_PROP_FPS))
        nb = cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
        #print "(nb,fps) = " + str(nb) + " , " + fps
        
        if fps=="nan":
            d = rootOut.getElementsByTagName("Duration")[0].firstChild.nodeValue
            #print d
            if int(d) == 0:
                fps = -1
            else:
                fps = nb/int(d) 
        
        #print "(nb,fps) = " + str(nb) + " , " + str(fps)
    cap.release()
    Node = DOMTreeOut.createElement("NbFrame")
    text=DOMTreeOut.createTextNode(str(nb))
    Node.appendChild(text)
    Image.appendChild(Node)
    
    Node = DOMTreeOut.createElement("FrameRate")
    text=DOMTreeOut.createTextNode(str(fps))
    Node.appendChild(text)
    Image.appendChild(Node)
    
    Node = DOMTreeOut.createElement("NbShots")
    lstsegments = rootIn.getElementsByTagName("Segment")
    text=DOMTreeOut.createTextNode(str(len(lstsegments)))
    Node.appendChild(text)
    Image.appendChild(Node)
    
    shotlist = DOMTreeOut.createElement("ShotList")
    Image.appendChild(shotlist)
    
    shtlist = DOMTreeIn.getElementsByTagName("Segment")
    #print videoFilePath + " : " + str(len(shtlist))
    for sht in shtlist:
        shot = DOMTreeOut.createElement("Shot")
        starttime = sht.getAttribute("start")
        s = int(starttime[1:3])*3600 + int(starttime[4:6])*60 + int(starttime[7:9]) + float("0."+starttime[10:13])
        endtime = sht.getAttribute("end")
        e = int(endtime[1:3])*3600 + int(endtime[4:6])*60 + int(endtime[7:9]) + float("0."+endtime[10:13])
        moment = sht.getElementsByTagName("KeyFrameID")[0].getAttribute("time")
        m = int(moment[1:3])*3600 + int(moment[4:6])*60 + int(moment[7:9]) + float("0."+moment[10:13])
        keyframepath =  sht.getElementsByTagName("KeyFrameID")[0].firstChild.nodeValue
        shot.setAttribute("stime", unicode(s))
        shot.setAttribute("etime", unicode(e))
        shot.setAttribute("moment", unicode(m))
        shot.setAttribute("keyframe",keyframepath)
        shotlist.appendChild(shot)
    Image.appendChild(shotlist)
    
    file_handle = io.open(outputXMLFile, 'wb')
    rootOut.writexml(file_handle)
    file_handle.close()
    #print "Video file processed successfully"
    return 0