'''
Created on Jun 11, 2016

@author: root
'''
import xml.dom.minidom
import io
def classifiySpeakers(outputXMLFile, seuilactivite, seuiletendue):
    doc=xml.dom.minidom.parse(outputXMLFile)
    #chercher la duree du video
    dureeString=doc.getElementsByTagName("Duration")[0].childNodes[0].data
    duree=float(dureeString)
    durationSpeakTotal=float(doc.getElementsByTagName("DurationSpeakTotal")[0].childNodes[0].data)
    speaker=doc.getElementsByTagName("Speaker")
    for s in speaker:
        etendu=float(s.getAttribute('extent'))
        activite=duree-float(s.getAttribute('Inactivity'))
        pourcentageActivity=(activite*100)/durationSpeakTotal
        pourcentageEtendu=(etendu*100)/duree
        t1=0
        t2=0
        if pourcentageActivity<seuilactivite:
            t1=0
        else :t1=1
        
        if pourcentageEtendu<seuiletendue:
            t2=0
        else :t2=1
        
        if etendu==activite:
            s.setAttribute("type","ponctuel")
        elif t1==1 and t2==0:
            s.setAttribute("type","localise")
        elif t1==0 and t2==0:
            s.setAttribute("type","present")
        elif t1==0 and t2==1:
            s.setAttribute("type","regulier")
        elif t1==1 and t2==1:
            s.setAttribute("type","important")
            
    file_handle = io.open(outputXMLFile, 'wb')
    doc.writexml(file_handle)
    file_handle.close()
    #print(TableDesLocuteurs) 
    #return  TableDesLocuteurs 
    print "type of speakers appended to the file successfully"
    '''
if __name__ == '__main__':
    classifiySpeakers( "/home/zein/Eclipse_Workspace/test_Dataset/DEV_DESCRIPTORS_L0/Culinarymedia-QuickBitesHawaiiDay1729.xml", 20, 20)

    pass
    '''