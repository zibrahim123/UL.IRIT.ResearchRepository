'''
Created on Jun 13, 2016

@author: root
'''

import xml.dom.minidom
def intersection(startI, endI, startJ,endJ):
    i0 = max(startI, startJ)
    i1 = min(endI, endJ)
    if i0 >= i1:
        return 0
    else:
        return i1-i0
def percentageInteraction(fileName, NbDespartie):
    doc = xml.dom.minidom.parse(fileName)
       
    interaction = doc.getElementsByTagName("Interaction")
      
    duree= float(doc.getElementsByTagName("Duration")[0].childNodes[0].data)

    #print duree
    tailleDeCase = duree / NbDespartie
    #print tailleDeCase
    pourcentage=[]
    for i in range(NbDespartie):
        pourcentage.append({'interaction2Speakers':0, 'interaction3Speakers':0, 'interaction4Speakers':0, 'interaction4+Speakers':0})

    debutSeg = finSeg=0;
    for i in range(0, NbDespartie):
        debutSeg=finSeg
        finSeg = finSeg + tailleDeCase
        for s in interaction:
            debut = float(s.getAttribute('start'))
            fin = float(s.getAttribute('end'))
            sequenceInteractions = str(s.childNodes[0].data).split()
            #print sequenceInteractions 
            #print str(len(sequenceInteractions))
            l = len(sequenceInteractions)
            if debut > finSeg:
                break
            intersect = intersection(debutSeg,finSeg,debut,fin)
            if l == 2:
                index = 'interaction2Speakers'
            elif l == 3:
                index = 'interaction3Speakers'
            elif l == 4:
                index = 'interaction4Speakers'
            else:
                index = 'interaction4+Speakers'
            #print str(i) + ": " + str(intersect)
            pourcentage[i][index] = pourcentage[i][index] + intersect
    #print pourcentage
    for i in range(0, NbDespartie):
        pourcentage[i]['interaction2Speakers'] = round(pourcentage[i]['interaction2Speakers'] *100 / tailleDeCase,2)
        pourcentage[i]['interaction3Speakers'] = round(pourcentage[i]['interaction3Speakers'] *100 / tailleDeCase,2)
        pourcentage[i]['interaction4Speakers'] = round(pourcentage[i]['interaction4Speakers'] *100 / tailleDeCase,2)
        pourcentage[i]['interaction4+Speakers'] = round(pourcentage[i]['interaction4+Speakers'] *100 / tailleDeCase,2)
    return pourcentage

if __name__ == '__main__':
    print(percentageInteraction("/home/zein/Eclipse_Workspace/test_Dataset/DEV_DESCRIPTORS_L0/Culinarymedia-BrunelloLuncheon617.xml", 3))
pass

