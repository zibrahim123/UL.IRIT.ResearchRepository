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
def percentageIntervention(fileName, NbDespartie):
    doc = xml.dom.minidom.parse(fileName)
       
    intervention = doc.getElementsByTagName("Intervention")
      
    duree= float(doc.getElementsByTagName("Duration")[0].childNodes[0].data)
    tailleDeCase = duree / NbDespartie
    pourcentage=[]
    for i in range(NbDespartie):
        pourcentage.append({'long':0, 'short':0})

    debutSeg = finSeg=0;
    for i in range(0, NbDespartie):
        debutSeg=finSeg
        finSeg = finSeg + tailleDeCase
        for s in intervention:
            debut = float(s.getAttribute('start'))
            fin = float(s.getAttribute('end'))
            type = s.getAttribute('type')
            if debut > finSeg:
                break
            intersect = intersection(debutSeg,finSeg,debut,fin)
            #print str(i) + ": " + str(intersect)
            pourcentage[i][type] = pourcentage[i][type] + intersect
    #print pourcentage
    for i in range(0, NbDespartie):
        pourcentage[i]['long'] = round(pourcentage[i]['long'] *100 / tailleDeCase,2)
        pourcentage[i]['short'] = round(pourcentage[i]['short'] *100 / tailleDeCase,2)
    return  pourcentage
'''
if __name__ == '__main__':
    percentageIntervention("/home/zein/Eclipse_Workspace/test_Dataset/DEV_DESCRIPTORS_L0/Culinarymedia-QuickBitesHawaiiDay1729.xml", 3)
pass
'''