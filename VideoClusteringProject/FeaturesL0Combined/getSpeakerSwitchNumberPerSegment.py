'''
Created on Jun 26, 2016

@author: root
'''

# in this module we compute for each segment how manuy times there is a switch from one speaker to another speaker during the segment. Even if the two speakers are separated by a long gap
# Whenever a speaker segment ends during the segmnet and another one starts in the segment and the two speakers are different we add to the counter 1
import xml.dom.minidom

def computeNumberSpeakerSwitchPerSegment(fileName, nbSegments):
    doc = xml.dom.minidom.parse(fileName)
    TableauDesParoles = []
    speaker = doc.getElementsByTagName("SpeechSegment")
    for s in speaker:
        idS = s.getAttribute('spkid')      
        # for tour in range(0,nbTour):
        debut = float(s.getAttribute('stime'))
        fin = float(s.getAttribute('etime'))
        loc = []
        loc.append(debut)
        loc.append(fin)
        loc.append(str(idS))
        TableauDesParoles.append(loc)
    TableauDesParoles.sort()
    # print(TableauDesParoles)
    if len(TableauDesParoles)==0:
        return [0]*nbSegments  
    duree= float(doc.getElementsByTagName("Duration")[0].childNodes[0].data)
    #print duree
    tailleDeCase = duree / nbSegments
    Resultat = []
    debutSeg = finSeg=0;
  
    for i in range(0, nbSegments):
        debutSeg=finSeg
        finSeg = finSeg + tailleDeCase
        cmpt = 0
        for j in range(len(TableauDesParoles)-1):
            if debut > finSeg:
                break
            if TableauDesParoles[j][1] > debutSeg and TableauDesParoles[j][1] < finSeg and TableauDesParoles[j+1][0] < finSeg and TableauDesParoles[j][2] != TableauDesParoles[j+1][2]:
                cmpt += 1
    
        Resultat.append(cmpt*100/tailleDeCase)
    return Resultat
'''
if __name__ == '__main__':
    print(computeNumberSpeakerSwitchPerSegment("/home/zein/Eclipse_Workspace/test_Dataset/DEV_DESCRIPTORS_L0/Culinarymedia-QuickBitesHawaiiDay1729.xml", 1))
pass
'''