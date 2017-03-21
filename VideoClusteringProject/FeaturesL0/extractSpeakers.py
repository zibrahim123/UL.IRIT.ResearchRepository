'''
Created on May 17, 2016

@author: zein
'''
import xml.dom.minidom

# Open XML document using minidom parser
DOMTree = xml.dom.minidom.parse("ASR/AliaK-NaVloPoMo26Day26SultanAhmetHagiaSofia834.flv.ogv.xml")
collection = DOMTree.documentElement

Speakers = collection.getElementsByTagName("Speaker")
SpeechSegments = collection.getElementsByTagName("SpeechSegment")


root = DOMTree.createElement("Audio")
Speak = DOMTree.createElement("SpeakersList")
for Sp in Speakers:
    Speak.appendChild(Sp)
root.appendChild(Speak)
speech=DOMTree.createElement("SpeechSegments")
for sp in SpeechSegments:
    words = sp.getElementsByTagName('Word')
    for w in words:
        sp.removeChild(w)
    speech.appendChild(sp)
root.appendChild(speech)
file_handle = open("out.xml","w")
root.writexml(file_handle)
file_handle.close()



# Print segment lists attributes of each movie.
for SpeechSegment in SpeechSegments:
    print "*****SpeechSegment*****"
    spkid = SpeechSegment.getAttribute('spkid')
    print "spkid: %s" % spkid
    
    stime = SpeechSegment.getAttribute('stime')
    print "stime: %s" % stime
    
    etime = SpeechSegment.getAttribute('etime')
    print "etime: %s" % etime
    
    ch = SpeechSegment.getAttribute('ch')
    print "ch: %s" % ch
    
    lang = SpeechSegment.getAttribute('lang')
    print "lang: %s" % lang