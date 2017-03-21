'''
Created on Jun 11, 2016

@author: root
'''
import xml.dom.minidom
import io
def getSpeechSequence(fileName, seuil):
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
        return []  
    Resultat = []
    listLoc=[]
    i=1
    startI = TableauDesParoles[0][0]
    endI = TableauDesParoles[0][1]
    listLoc.append(TableauDesParoles[0][2])
    while(i<len(TableauDesParoles)):
        if TableauDesParoles[i][0] - endI <seuil:
            endI = TableauDesParoles[i][1]
            listLoc.append(TableauDesParoles[i][2])
        else:
            Resultat.append((startI, endI, listLoc))
            startI=TableauDesParoles[i][0]
            endI = TableauDesParoles[i][1]
            listLoc=[]
            listLoc.append(TableauDesParoles[i][2])
        i = i + 1
    Resultat.append((startI, endI, listLoc))
    return Resultat
def write_Interaction_Intervention_List(outputXMLFile, speechSequence, seuilInteraction, seuilIntervention):
    #speechSequence = getSpeechSequence(outputXMLFile, seuilInteraction)
    l = len(speechSequence)
    rootOut = xml.dom.minidom.parse(outputXMLFile)
    #descriptors = rootOut.createElement("Descriptors")
    #descriptors.setAttribute("level","1")
    #rootOut.appendChild(descriptors)
    audio = rootOut.documentElement.getElementsByTagName("Audio")[0]
    interac = audio.getElementsByTagName("Interactions")
    interv = audio.getElementsByTagName("Interventions")
    if len(interac) > 0:
        audio.removeChild(interac[0])
        audio.removeChild(interv[0])
    
    interactionList = rootOut.createElement("Interactions")
    interventionList = rootOut.createElement("Interventions")
    for i in range(0,l):
        start = speechSequence[i][0]
        end = speechSequence[i][1]
        listLoc = speechSequence[i][2]
        #print (str(start) +" , "+str(end)+" , "+ str(listLoc))
        if len(listLoc) > 1: # ici veut dire une interaction
            interaction = rootOut.createElement("Interaction")
            #interaction.setAttribute("locuteurs", listLoc)
            interaction.setAttribute("start", str(start))
            interaction.setAttribute("end", str(end))
            s = str(listLoc)[1:-1]
            s=s.replace("'", "")
            s=s.replace(",", " ")
            interaction.appendChild(rootOut.createTextNode(s))
            interactionList.appendChild(interaction)
        elif len(listLoc) == 1:
            intervention = rootOut.createElement("Intervention")
            if end - start > seuilIntervention:
                intervention.setAttribute("type", "long")
            else:
                intervention.setAttribute("type", "short")
            intervention.setAttribute("start", str(start))
            intervention.setAttribute("spkid", str(listLoc[0]))
            intervention.setAttribute("end", str(end))
            interventionList.appendChild(intervention)
    audio.appendChild(interactionList)
    audio.appendChild(interventionList)
    try:
        f = io.open(outputXMLFile, 'wb')
    except IOError:
        print "Unable to open file to write interactions and interventions"    
    
    rootOut.writexml(f)
    f.close()
    print "Interactions and interventions extracted successfully"
    '''
if __name__ == '__main__':
    spSegments = getSpeechSequence("/home/zein/Eclipse_Workspace/test_Dataset/DEV_DESCRIPTORS_L0/Culinarymedia-QuickBitesHawaiiDay1729.xml", 10)
    print spSegments
    pass
    '''