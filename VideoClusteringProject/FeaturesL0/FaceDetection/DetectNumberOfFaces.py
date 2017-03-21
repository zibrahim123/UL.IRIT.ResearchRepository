'''
Created on Jun 1, 2016

@author: root
'''
import cv2
import xml.dom.minidom
import io

def extractFaceFromKeyframes(videoFilePath, outputXMLFile,videoPath):
    try:
        DOMTreeOut = xml.dom.minidom.parse(outputXMLFile)

        #print ('ASR file opened for processing: '+ asrFilePath)
    except IOError:
        print ('Error while opening the xml file of the video shots for face detection')
        #print (videoFilePath)
        return -1

    rootOut = DOMTreeOut.documentElement
    
    shtlist = DOMTreeOut.getElementsByTagName("Shot")
    #print videoFilePath + " : " + str(len(shtlist))
    for sht in shtlist:
        nameKeyframe = sht.getAttribute("keyframe")
        fullpath=videoFilePath+nameKeyframe
        #print "Process keyframe: "+ fullpath
        nb = numberOfFaces(fullpath)
        #print nb
        sht.setAttribute("nbFaces",str(nb))
        sht.setAttribute("Patches",str(getPatchesvalues(fullpath)))
        #print "Nb Faces : "+ str(nb)
        
    file_handle = io.open(outputXMLFile, 'wb')
    rootOut.writexml(file_handle)
    file_handle.close()
    #print "Keyframes' face detection processed successfully"    
    return 0
    
def numberOfFaces(keyframe):
    try:
        face_cascade = cv2.CascadeClassifier('/home/zein/Eclipse_Workspace/VideoClustering.v0/FeaturesL0/FaceDetection/haarcascade_frontalface_default.xml')
        #eye_cascade = cv2.CascadeClassifier('FaceDetection/haarcascade_eye.xml')
    except Exception:
        print "Unable to load haarcascade_frontal_face_default.xml or haarcascade_eye.xml"
        return -1

    try:
        img = cv2.imread(keyframe)
        #print img.shape
        #print "Loaded the image : "+ keyframe
        #print img.shape
    except Exception:
        print keyframe + " is not found"
        return -1
    #cv2.imshow('img',img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    #faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    faces = face_cascade.detectMultiScale(gray,scaleFactor=1.1, minNeighbors=5,minSize=(30, 30),
    flags = cv2.cv.CV_HAAR_SCALE_IMAGE )
    '''
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
     '''
    return len(faces)   
def getPatchesvalues(keyframe):
    
    try:
        #img = cv2.imread(keyframe, cv2.IMREAD_GRAYSCALE)
        gray = cv2.imread(keyframe, cv2.IMREAD_GRAYSCALE)
    except IOError:
        print keyframe + " is not found"
        return -1
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    height , width = gray.shape
    stepHeight = int(height/3)
    stepWidth = int(width/3)
    means=[]
    for i in range(0,3):
        for j in range(0,3):
            av = getAverage(gray[i*stepHeight:(i+1)*stepHeight-1,j*stepWidth:(j+1)*stepWidth-1])
            means.append(av)    
    return means
def getAverage(mat):
        s=0.0
        h,w=mat.shape
        for i in range(0,h):
            for j in range(0,w):
                s = s + mat[i,j]
        return int(s/(h*w))

#nb = numberOfFaces("/media/zein/835C-4E2D/Research Datasets/test_Dataset/DEV_SHOT/Aabbey1-HolyEnvyLecturesOnReligiousPluralismInHonorOfKristerSt239/27788.jpg")
#print nb