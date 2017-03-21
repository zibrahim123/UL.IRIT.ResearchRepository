'''
Created on May 17, 2016

@author: root
'''
import xml.dom.minidom
from xml.dom.minidom import Document
import io
import sys

def extractAudioData(asrFilePath, outputXMLFile):
    # Open XML document using minidom parser
    try:
        DOMTreeIn = xml.dom.minidom.parse(asrFilePath)
        DOMTreeOut = xml.dom.minidom.parse(outputXMLFile)

        #print ('ASR file opened for processing: '+ asrFilePath)
    except IOError:
        print ('Error while opening the xml file of the ASR')
        print (asrFilePath)
        return -1
    
    
    rootIn = DOMTreeIn.documentElement
    rootOut = DOMTreeOut.documentElement
    #Speakers = root.getElementsByTagName("Speaker")
    #SpeechSegments = root.getElementsByTagName("SpeechSegment")

    Audio = DOMTreeOut.createElement('Audio')
    rootOut.appendChild(Audio)

   
    Node = DOMTreeOut.createElement("NameAudio")
    n = DOMTreeIn.getElementsByTagName('AudioDoc')[0].getAttribute('name')
    name = n[:len(n)-8]+".wav"

    text=DOMTreeOut.createTextNode(name)
    Node.appendChild(text)
    Audio.appendChild(Node)
    
    #for speakduration
    speakduration = DOMTreeOut.createElement("DurationSpeakTotal")
    chann = rootIn.getElementsByTagName('Channel')
    speakd = chann[0].getAttribute('spdur')
    text=DOMTreeOut.createTextNode(speakd)
    speakduration.appendChild(text)
    Audio.appendChild(speakduration)

    segDuration = chann[0].getAttribute('sigdur')

    #for channel
    channel = DOMTreeOut.createElement("Channel")
    ch = chann[0].getAttribute('num')
    text=DOMTreeOut.createTextNode(ch)
    channel.appendChild(text)
    Audio.appendChild(channel)
    
    #for sample rate
    sampleRate = DOMTreeOut.createElement("SampleRate")
    text=DOMTreeOut.createTextNode('16000')
    sampleRate.appendChild(text)
    Audio.appendChild(sampleRate)
    
    #for number of samples - set manually
    TotalSample = DOMTreeOut.createElement("TotalSample")
    nb = str(int((float(segDuration)*16000)))
    #print nb
    text=DOMTreeOut.createTextNode(unicode(nb))
    TotalSample.appendChild(text)
    Audio.appendChild(TotalSample)
    
    #for number of bits used - set manually
    Node = DOMTreeOut.createElement("NbBits")
    text=DOMTreeOut.createTextNode('16')
    Node.appendChild(text)
    Audio.appendChild(Node)
    
        
    #for number of speakers
    Node = DOMTreeOut.createElement("NbSpeaker")
    spklist = DOMTreeIn.getElementsByTagName('Speaker')
    text = DOMTreeOut.createTextNode(unicode(str(len(spklist))))
    Node.appendChild(text)
    Audio.appendChild(Node)
    
    Speak = DOMTreeOut.createElement("SpeakersList")
    lstSpeechsegments = DOMTreeIn.getElementsByTagName('SpeechSegment')
    for Sp in spklist:
        minstime = sys.float_info.max
        maxetime = sys.float_info.min
        for seg in lstSpeechsegments:
            if ((float(seg.getAttribute('stime')) < minstime) & (seg.getAttribute('spkid')==Sp.getAttribute('spkid'))):
                minstime = float(seg.getAttribute('stime')) 
            if ((float(seg.getAttribute('etime')) > maxetime) & (seg.getAttribute('spkid')==Sp.getAttribute('spkid'))):
                maxetime = float(seg.getAttribute('etime')) 
        Sp.setAttribute('extent',unicode(maxetime-minstime))
        Sp.setAttribute('Inactivity',unicode(float(speakd) - float(Sp.getAttribute('dur'))))
        Speak.appendChild(Sp)
    Audio.appendChild(Speak)
    
    speechseg=DOMTreeOut.createElement("SpeechSegments")
    shortBubbleSort(lstSpeechsegments)
    for sp in lstSpeechsegments:
        words = sp.getElementsByTagName('Word')
        for w in words:
            sp.removeChild(w)
        speechseg.appendChild(sp)
    Audio.appendChild(speechseg)

    interventionseq = DOMTreeOut.createElement("SuccessionIntervention")
    lst=""
    for seg in lstSpeechsegments:
        lst = lst + " " + seg.getAttribute("spkid")
    text = DOMTreeOut.createTextNode(unicode(lst))
    interventionseq.appendChild(text)
    Audio.appendChild(interventionseq)

    file_handle = io.open(outputXMLFile, 'wb')
    #file_handle.write(root)
    rootOut.writexml(file_handle)
    #print outputXMLFile+" processed successfully"
    file_handle.close()
    return 0
def shortBubbleSort(alist):
    exchanges = True
    passnum = len(alist)-1
    while passnum > 0 and exchanges:
        exchanges = False
        for i in range(passnum):
            if float(alist[i].getAttribute("stime")) > float(alist[i+1].getAttribute("stime")):
                exchanges = True
                temp = alist[i]
                alist[i] = alist[i+1]
                alist[i+1] = temp
        passnum = passnum-1