'''
Created on May 29, 2016

@author: malak
'''

import xml.dom.minidom
def intersection(startI, endI, startJ,endJ):
    i0 = max(startI, startJ)
    i1 = min(endI, endJ)
    if i0 >= i1:
        return 0
    else:
        return i1-i0
    
def getSpeakerDistribution(fileName, NbDespartie):
    doc = xml.dom.minidom.parse(fileName)
    speaker = doc.getElementsByTagName("Speaker")
    nbSpeaker = len(speaker)
    speech = doc.getElementsByTagName("SpeechSegment")
    duree= float(doc.getElementsByTagName("Duration")[0].childNodes[0].data)
    tailleDeCase = duree / NbDespartie
    mySet = set()
    debutSeg = finSeg=0;
    pourcentage = []
    for i in range(0, NbDespartie):
        debutSeg=finSeg
        finSeg = finSeg + tailleDeCase
        for s in speech:
            debut = float(s.getAttribute('stime'))
            fin = float(s.getAttribute('etime'))
            idS = s.getAttribute('spkid')
            if debut > finSeg:
                break
            intersect = intersection(debutSeg,finSeg,debut,fin)
            #print str(i) + ": " + str(intersect)
            if intersect > 0:
                mySet.add(idS) 
        #print mySet
        pourcentage.append(round(float(len(mySet))*100.0/float(nbSpeaker),2))
        mySet.clear()    
    return pourcentage        
'''
if __name__ == '__main__':
    print(getSpeakerDistribution("/home/zein/Eclipse_Workspace/test_Dataset/DEV_DESCRIPTORS_L0/Culinarymedia-CMNVideoHiltlVegetarianRestaurantZurich590.xml", 3))   
    pass
'''
