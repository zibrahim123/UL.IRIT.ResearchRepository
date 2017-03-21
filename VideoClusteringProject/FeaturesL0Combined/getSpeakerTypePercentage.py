'''
Created on Jun 10, 2016

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
def percentageLocuteur(fileName, NbDespartie):
    doc = xml.dom.minidom.parse(fileName)
    speakerDict=dict()
    speaker = doc.getElementsByTagName("Speaker")
    for s in speaker:
        speakerDict[s.getAttribute("spkid")]=s.getAttribute("type")
        
    speech = doc.getElementsByTagName("SpeechSegment")
      
    duree= float(doc.getElementsByTagName("Duration")[0].childNodes[0].data)
    tailleDeCase = duree / NbDespartie
    pourcentage=[]
    for i in range(NbDespartie):
        pourcentage.append({'ponctuel':0, 'localise':0,'present':0,'regulier':0,'important':0})

    debutSeg = finSeg=0;
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
            typeLoc = speakerDict[idS] 
            pourcentage[i][typeLoc] = pourcentage[i][typeLoc] + intersect
    #print pourcentage
    for i in range(0, NbDespartie):
        pourcentage[i]['ponctuel'] = round(pourcentage[i]['ponctuel'] *100 / tailleDeCase,2)
        pourcentage[i]['localise'] = round(pourcentage[i]['localise'] *100 / tailleDeCase,2)
        pourcentage[i]['present'] = round(pourcentage[i]['present'] *100 / tailleDeCase,2)
        pourcentage[i]['regulier'] = round(pourcentage[i]['regulier'] *100 / tailleDeCase,2)
        pourcentage[i]['important'] = round(pourcentage[i]['important'] *100 / tailleDeCase,2)
    return pourcentage
'''
if __name__ == '__main__':
    percentageLocuteur("/home/zein/Eclipse_Workspace/test_Dataset/DEV_DESCRIPTORS_L0/Culinarymedia-QuickBitesHawaiiDay1729.xml", 3)
pass
'''
          
