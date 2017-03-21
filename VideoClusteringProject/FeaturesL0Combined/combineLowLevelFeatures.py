'''
Created on Jun 14, 2016

@author: root
'''
from getInteractionsInterventions import getSpeechSequence, write_Interaction_Intervention_List
from generateTypeSpeakers import classifiySpeakers
from getInteractionPercentage import percentageInteraction
from getInteventionPercentage import percentageIntervention
from getSpeakerTypePercentage import percentageLocuteur
from getSpeakerDistributionOverSegments import getSpeakerDistribution
from getImageDescriptors import getNbFacesVariation, getKeyframesInterIntraSegmentsIntensityVariation
from getSpeechMusicPercentage import getSpeechMusicNonSpeechNonMusicPercentage
from getSpeakerSwitchNumberPerSegment import computeNumberSpeakerSwitchPerSegment
import xml.dom.minidom
from xml.dom.minidom import Document
import os.path
import io

def generatePercentageDescriptors(inputXMLFile, outputXMLFile, nbSegments):
    
    #get the list of interaction and intervention
    speechSequence = getSpeechSequence(inputXMLFile, 2)
    write_Interaction_Intervention_List(inputXMLFile,speechSequence, 2, 10)
    
    
    #classify the type of speakers
    classifiySpeakers(inputXMLFile, 20, 20)
    if os.path.exists(outputXMLFile):
        DOMTreeOut = xml.dom.minidom.parse(outputXMLFile)
        root = DOMTreeOut.documentElement
        #remove the child for this number of segments if exists
        descList = root.getElementsByTagName("Descriptors")
        for d in descList:
            if int(d.getAttribute("nbSegments"))==nbSegments:
                root.removeChild(d)
                break
    else:
        DOMTreeOut = Document()
        root = DOMTreeOut.createElement("DescriptorsList")
        DOMTreeOut.appendChild(root)
        print "XML file for the descriptors does not exist yet. We will create it"
    
    descriptors = DOMTreeOut.createElement("Descriptors")
    descriptors.setAttribute("nbSegments", str(nbSegments))
    
    #get interaction percentage then add the values in the xml file
    pInteraction = percentageInteraction(inputXMLFile, nbSegments)
    #print pInteraction
    interactionList = DOMTreeOut.createElement("Interactions")
    for i in range(0,nbSegments):
        inter2sp = DOMTreeOut.createElement("Interaction")
        inter2sp.setAttribute("numSegment",str(i+1))
        inter2sp.setAttribute("numberSpeakers","2")
        inter2sp.appendChild(DOMTreeOut.createTextNode(str(pInteraction[i]["interaction2Speakers"])))
        interactionList.appendChild(inter2sp)
               
        inter3sp = DOMTreeOut.createElement("Interaction")
        inter3sp.setAttribute("numSegment",str(i+1))
        inter3sp.setAttribute("numberSpeakers","3")
        inter3sp.appendChild(DOMTreeOut.createTextNode(str(pInteraction[i]["interaction3Speakers"])))
        interactionList.appendChild(inter3sp)
        
        inter4sp = DOMTreeOut.createElement("Interaction")
        inter4sp.setAttribute("numSegment",str(i+1))
        inter4sp.setAttribute("numberSpeakers","4")
        inter4sp.appendChild(DOMTreeOut.createTextNode(str(pInteraction[i]["interaction4Speakers"])))
        interactionList.appendChild(inter4sp)
        
        inter5sp = DOMTreeOut.createElement("Interaction")
        inter5sp.setAttribute("numSegment",str(i+1))
        inter5sp.setAttribute("numberSpeakers","4+")
        inter5sp.appendChild(DOMTreeOut.createTextNode(str(pInteraction[i]["interaction4+Speakers"])))
        interactionList.appendChild(inter5sp)
        #print str(i)
    descriptors.appendChild(interactionList)
    
    #get intervention percentage and add them to the file
    pIntervention =  percentageIntervention(inputXMLFile, nbSegments)
    interventionList = DOMTreeOut.createElement("Interventions")
    for i in range(nbSegments):
        interCourte = DOMTreeOut.createElement("Intervention")
        interCourte.setAttribute("numSegment",str(i+1))
        interCourte.setAttribute("type","short")
        interCourte.appendChild(DOMTreeOut.createTextNode(str(pIntervention[i]["short"])))
        
        interLong = DOMTreeOut.createElement("Intervention")
        interLong.setAttribute("numSegment",str(i+1))
        interLong.setAttribute("type","long")
        interLong.appendChild(DOMTreeOut.createTextNode(str(pIntervention[i]["long"])))
        
        interventionList.appendChild(interCourte)
        interventionList.appendChild(interLong)
    descriptors.appendChild(interventionList)
    
    
    #get speaker distribution and add the values to the xml
    pSpeakers = percentageLocuteur(inputXMLFile, nbSegments)
    speakerTypeList = DOMTreeOut.createElement("SpeakersTypeList")
    for i in range(nbSegments):
        spType = DOMTreeOut.createElement("SpeakersType")
        spType.setAttribute("numSegment",str(i+1))
        
        ponctuel = DOMTreeOut.createElement("Ponctuel")
        ponctuel.appendChild(DOMTreeOut.createTextNode(str(pSpeakers[i]["ponctuel"])))
        spType.appendChild(ponctuel)
        
        localise = DOMTreeOut.createElement("Localise")
        localise.appendChild(DOMTreeOut.createTextNode(str(pSpeakers[i]["localise"])))
        spType.appendChild(localise)
        
        present = DOMTreeOut.createElement("Present")
        present.appendChild(DOMTreeOut.createTextNode(str(pSpeakers[i]["present"])))
        spType.appendChild(present)
        
        regulier = DOMTreeOut.createElement("Regulier")
        regulier.appendChild(DOMTreeOut.createTextNode(str(pSpeakers[i]["regulier"])))
        spType.appendChild(regulier)
        
        important = DOMTreeOut.createElement("Important")
        important.appendChild(DOMTreeOut.createTextNode(str(pSpeakers[i]["important"])))
        spType.appendChild(important)
        
        speakerTypeList.appendChild(spType)
    descriptors.appendChild(speakerTypeList)
    
    #get speaker distribution over segments (how many speakers from the total number is speaking during the segment)
    dSpeakers = getSpeakerDistribution(inputXMLFile, nbSegments)   
    dSpeakersList = DOMTreeOut.createElement("SpeakersDistribution")
    for i in range(nbSegments):
        dSpeaker = DOMTreeOut.createElement("SpeakerDistribution")
        dSpeaker.setAttribute("numSegment",str(i+1))
        dSpeaker.appendChild(DOMTreeOut.createTextNode(str(dSpeakers[i])))
        dSpeakersList.appendChild(dSpeaker)
    descriptors.appendChild(dSpeakersList)
    
    #get the list of nb of faces during segments
    listNbFaces = getNbFacesVariation(inputXMLFile, nbSegments)
    nbFacesList = DOMTreeOut.createElement("nbFacesList")
    for i in range(nbSegments):
        nbFaces = DOMTreeOut.createElement("nbFaces")
        nbFaces.setAttribute("numSegment",str(i+1))
        l = list(listNbFaces[i])
        mn = -1
        mx = -1
        if len(l) != 0:
            #print "len faces = 0"
            mn = min(l)
            mx = max(l)
        minNode = DOMTreeOut.createElement("MinValue")
        minNode.appendChild(DOMTreeOut.createTextNode(str(mn)))
        nbFaces.appendChild(minNode)
        maxNode = DOMTreeOut.createElement("MaxValue")
        maxNode.appendChild(DOMTreeOut.createTextNode(str(mx)))
        nbFaces.appendChild(maxNode)
        nbFacesList.appendChild(nbFaces)
    descriptors.appendChild(nbFacesList)
    
    #get the list of intensity variations
    listIntensityVariationsInter, listIntensityVariationsIntra, nbTransitions = getKeyframesInterIntraSegmentsIntensityVariation(inputXMLFile, nbSegments)
    intensityVar = DOMTreeOut.createElement("IntensityVariation")
    descriptors.appendChild(intensityVar)
    interIntensityVariation = DOMTreeOut.createElement("InterIntensityVariation")
    intensityVar.appendChild(interIntensityVariation)
    
    intraIntensityVariation = DOMTreeOut.createElement("IntraIntensityVariation")
    intensityVar.appendChild(interIntensityVariation)
    
    interIntensityVariationList = DOMTreeOut.createElement("InterIntensityVariationList")
    for i in range(nbSegments-1):
        iVariation = DOMTreeOut.createElement("InterIntensityVariation")
        iVariation.setAttribute("numSegment",str(i+1))
        txtNode = DOMTreeOut.createTextNode(str(listIntensityVariationsInter[i]))
        #print str(listIntensityVariations[i])
        iVariation.appendChild(txtNode)
        interIntensityVariationList.appendChild(iVariation)
    interIntensityVariation.appendChild(interIntensityVariationList)
    
    intraIntensityVariationList = DOMTreeOut.createElement("IntraIntensityVariationList")
    for i in range(nbSegments):
        iVariation = DOMTreeOut.createElement("IntraIntensityVariation")
        iVariation.setAttribute("numSegment",str(i+1))
        txtNode = DOMTreeOut.createTextNode(str(listIntensityVariationsIntra[i]))
        #print str(listIntensityVariations[i])
        iVariation.appendChild(txtNode)
        interIntensityVariationList.appendChild(iVariation)
    intraIntensityVariation.appendChild(intraIntensityVariationList)
    
    nbShotTransitionsList = DOMTreeOut.createElement("NumberShotTransitionList")
    for i in range(nbSegments):
        nbTrans = DOMTreeOut.createElement("NumberShotTransition")
        nbTrans.setAttribute("numSegment",str(i+1))
        txtNode = DOMTreeOut.createTextNode(str(nbTransitions[i]))
        #print str(listIntensityVariations[i])
        nbTrans.appendChild(txtNode)
        nbShotTransitionsList.appendChild(nbTrans)
    descriptors.appendChild(nbShotTransitionsList)
    
    nbSpeakerTransition = computeNumberSpeakerSwitchPerSegment(inputXMLFile, nbSegments)
    nbSpeakerTransitionList = DOMTreeOut.createElement("NumberSpeakerTransitionList")
    for i in range(nbSegments):
        nbTrans = DOMTreeOut.createElement("NumberSpeakerTransition")
        nbTrans.setAttribute("numSegment",str(i+1))
        txtNode = DOMTreeOut.createTextNode(str(nbSpeakerTransition[i]))
        #print str(listIntensityVariations[i])
        nbTrans.appendChild(txtNode)
        nbSpeakerTransitionList.appendChild(nbTrans)
    descriptors.appendChild(nbSpeakerTransitionList)
           
    listSpeechMusicCombinations = getSpeechMusicNonSpeechNonMusicPercentage(inputXMLFile,nbSegments)
    S_M_NS_NM_List = DOMTreeOut.createElement("SpeechMusicAlignmentList")   
    for i in range(nbSegments):
        alignment = DOMTreeOut.createElement("SpeechMusicAlignment")
        alignment.setAttribute("numSegment", str(i+1))
        
        S = DOMTreeOut.createElement("Speech")
        S.appendChild(DOMTreeOut.createTextNode(str(round(listSpeechMusicCombinations[i]["P"],2))))
        alignment.appendChild(S)
        #print type(round(listSpeechMusicCombinations[i]["P"],2))
        
        M = DOMTreeOut.createElement("Music")
        M.appendChild(DOMTreeOut.createTextNode(str(round(listSpeechMusicCombinations[i]["M"],2))))
        alignment.appendChild(M)
        #print round(listSpeechMusicCombinations[i]["M"],2)
        
        S_M = DOMTreeOut.createElement("SpeechWithMusic")
        S_M.appendChild(DOMTreeOut.createTextNode(str(round(listSpeechMusicCombinations[i]["PM"],2))))
        alignment.appendChild(S_M)
        #print round(listSpeechMusicCombinations[i]["PM"],2)
        
        S_NM = DOMTreeOut.createElement("SpeechWithNonMusic")
        S_NM.appendChild(DOMTreeOut.createTextNode(str(round(listSpeechMusicCombinations[i]["PNM"],2))))
        alignment.appendChild(S_NM)
        #print round(listSpeechMusicCombinations[i]["PNM"],2)
        
        NS_M = DOMTreeOut.createElement("NonSpeechWithMusic")
        NS_M.appendChild(DOMTreeOut.createTextNode(str(round(listSpeechMusicCombinations[i]["NPM"],2))))
        alignment.appendChild(NS_M)
        #print round(listSpeechMusicCombinations[i]["NPM"],2)
        
        NS_NM = DOMTreeOut.createElement("NonSpeechWithNonMusic")
        NS_NM.appendChild(DOMTreeOut.createTextNode(str(round(listSpeechMusicCombinations[i]["NPNM"],2))))
        alignment.appendChild(NS_NM)
        #print round(listSpeechMusicCombinations[i]["NPNM"],2)
        
        S_M_NS_NM_List.appendChild(alignment)
    descriptors.appendChild(S_M_NS_NM_List)
    
    root.appendChild(descriptors)
       
    file_handle = io.open(outputXMLFile, 'wb')
    DOMTreeOut.writexml(file_handle)
    file_handle.close()
    print "Combination of descriptors are generated successfully for "+ str(nbSegments) +" segments"
    
if __name__ == '__main__':
    inputXMLPath = "/home/zein/Eclipse_Workspace/test_Dataset/DEV_DESCRIPTORS_L0/"
    outputXMLPath = "/home/zein/Eclipse_Workspace/test_Dataset/DEV_DESCRIPTORS_L1/"
    
    f = open("listVideos.txt","r")
    for line in f:
        print line[:-1]
        generatePercentageDescriptors(inputXMLPath+line[:-1], outputXMLPath+line[:-1], 1)
        generatePercentageDescriptors(inputXMLPath+line[:-1], outputXMLPath+line[:-1], 2)
        generatePercentageDescriptors(inputXMLPath+line[:-1], outputXMLPath+line[:-1], 3)
        generatePercentageDescriptors(inputXMLPath+line[:-1], outputXMLPath+line[:-1], 4)
    f.close()
    
    pass