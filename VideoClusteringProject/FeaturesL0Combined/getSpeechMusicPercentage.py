'''
Created on Jun 13, 2016

@author: malak
'''
import xml.dom.minidom

def returnByTag(fileName, tagName):
    doc = xml.dom.minidom.parse(fileName)
    tab = doc.getElementsByTagName(tagName)
    Tab = []
    for s in tab:
        debut = float(s.getAttribute('start'))
        fin = float(s.getAttribute('end')) 
        loc = []
        loc.append(debut)
        loc.append(fin)
        Tab.append(loc)
    Tab.sort()
    return Tab

def intersection(startI, endI, startJ, endJ):
    i0 = max(startI, startJ)
    i1 = min(endI, endJ)
    return i0, i1 

def  IntersectionAvecUnSegment(dSeg, fSeg, Tab1, Tab2):
    Intersection = 0
    for j in range(len(Tab1)):
        for k in range(len(Tab2)):
            if Tab1[j][1] < Tab2[k][0]:
                break
            i0, i1 = intersection(Tab1[j][0], Tab1[j][1], Tab2[k][0], Tab2[k][1])
            if i0 < i1:
                dI, fI = intersection(dSeg, fSeg, i0, i1)
                if dI < fI:
                    Intersection = Intersection + (fI - dI)
                    #print(dI)
                    #print(fI)
                    #print('>')
                    #print(fI - dI)
                    #print('=========')            
    return Intersection
                       
                       
def  IntersectionSegmentSegment(dSeg, fSeg, Tab):
    Intersection = 0
    for k in range(len(Tab)):
        if fSeg < Tab[k][0]:
                break
        dI, fI = intersection(dSeg, fSeg, Tab[k][0], Tab[k][1])
        if dI < fI:
                    Intersection = Intersection + (fI - dI)
    return Intersection
                                              
def getSpeechMusicNonSpeechNonMusicPercentage(fileName, nbPartie):
    doc = xml.dom.minidom.parse(fileName)
    dureeString = doc.getElementsByTagName("Duration")[0].childNodes[0].data
    duree = float(dureeString)
    tailleDeCase = duree / nbPartie
    Video = {}
    for i in range(nbPartie):
        Video[i] = {}
        Video[i]['P'] = 0
        Video[i]['M'] = 0
        Video[i]['PM'] = 0
        Video[i]['NPM'] = 0
        Video[i]['PNM'] = 0
        Video[i]['NPNM'] = 0
          
    ParolTab = returnByTag(fileName, 'Speech')
    MusicTab = returnByTag(fileName, 'Music')
    NonParolTab = returnByTag(fileName, 'NonSpeech')
    NonMusicTab = returnByTag(fileName, 'NonMusic')
      
    dSeg = 0
    fSeg = tailleDeCase
   
    for i in range(nbPartie):
        
        Video[i]['P']= Video[i]['P']+IntersectionSegmentSegment(dSeg,fSeg,ParolTab)*100.0/(fSeg-dSeg)
        Video[i]['M']=Video[i]['M']+IntersectionSegmentSegment(dSeg,fSeg,MusicTab)*100.0/(fSeg-dSeg)
        Video[i]['PM'] = Video[i]['PM'] + IntersectionAvecUnSegment(dSeg, fSeg, ParolTab, MusicTab)*100.0/(fSeg-dSeg)
        Video[i]['NPM'] = Video[i]['NPM']+IntersectionAvecUnSegment(dSeg,fSeg,NonParolTab,MusicTab)*100.0/(fSeg-dSeg)
        Video[i]['PNM'] = Video[i]['PNM']+IntersectionAvecUnSegment(dSeg,fSeg,ParolTab,NonMusicTab)*100.0/(fSeg-dSeg)
        Video[i]['NPNM'] = Video[i]['NPNM']+IntersectionAvecUnSegment(dSeg,fSeg,NonParolTab,NonMusicTab)*100.0/(fSeg-dSeg)
        dSeg = fSeg
        fSeg = fSeg + tailleDeCase 
    return Video 
          
    '''
if __name__ == '__main__':
    V = getSpeechMusicNonSpeechNonMusicPercentage("/home/zein/Eclipse_Workspace/test_Dataset/DEV_DESCRIPTORS_L0/Culinarymedia-QuickBitesHawaiiDay1729.xml", 2)
    
    print(V)
                
    #speech = returnByTag("C:\Users\malak\Desktop\Culinarymedia-CMNVideoHiltlVegetarianRestaurantZurich590.xml", 'Speech')
    # print(speech)
    
    #music = returnByTag("C:\Users\malak\Desktop\Culinarymedia-CMNVideoHiltlVegetarianRestaurantZurich590.xml", 'Music')
    #print(music)                       
pass
'''
