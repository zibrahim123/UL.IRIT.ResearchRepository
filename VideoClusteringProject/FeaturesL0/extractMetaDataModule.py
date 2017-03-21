'''
Created on May 17, 2016

@author: root
'''
import xml.dom.minidom
from xml.dom.minidom import Document
import io

def extractMetaData(metadataFilePath, outputXMLFile):
    # Open XML document using minidom parser
    doc = Document()
    try:
        DOMTreeIn = xml.dom.minidom.parse(metadataFilePath)
        #print ('Metadata file opened for processing: '+ metadataFilePath)
    except IOError:
        print ('Error while opening the xml file of the metadata')
        print (metadataFilePath)
        return -1
    #DOMTreeOut = xml.dom.minidom.parse(outputXMLFile) 
    root = doc.createElement('Descriptors')
    doc.appendChild(root)
    metadata = doc.createElement("Metadata")
    root.appendChild(metadata)
    
    #here we are creating and appending the filename of a video
    NameFile = doc.createElement("NameFile")
    #print DOMTreeIn.documentElement.getElementsByTagName('filename')[0].firstChild.nodeValue
    text = doc.createTextNode(str(DOMTreeIn.documentElement.getElementsByTagName('filename')[0].firstChild.nodeValue+'.ogv'))
    NameFile.appendChild(text)
    metadata.appendChild(NameFile)
    
    title = doc.createElement('Title')
    titleVideo = unicode(DOMTreeIn.documentElement.getElementsByTagName('title')[0].firstChild.nodeValue)
    #print titleVideo
    text = doc.createTextNode(titleVideo)
    title.appendChild(text)
    metadata.appendChild(title)
    
    duration = doc.createElement('Duration')
    text = doc.createTextNode(str(DOMTreeIn.documentElement.getElementsByTagName('duration')[0].firstChild.nodeValue))
    duration.appendChild(text)
    metadata.appendChild(duration)
    
    tags = doc.createElement('Tags')
    for t in DOMTreeIn.documentElement.getElementsByTagName('string'):
        #print t.firstChild.nodeValue
        tag = doc.createElement('Tag')
        tag.appendChild(doc.createTextNode(str(t.firstChild.nodeValue)))
        tags.appendChild(tag)
    metadata.appendChild(tags)
    
    sz = doc.createElement('Size')
    text = doc.createTextNode(str(DOMTreeIn.documentElement.getElementsByTagName('size')[0].firstChild.nodeValue))
    sz.appendChild(text)
    metadata.appendChild(sz)


    uid = doc.createElement('IdUploader')
    text = doc.createTextNode(DOMTreeIn.documentElement.getElementsByTagName('uid')[0].firstChild.nodeValue)
    uid.appendChild(text)
    metadata.appendChild(uid) 
    file_handle = io.open(outputXMLFile, 'wb')
    #file_handle.write(root)
    doc.writexml(file_handle)
    file_handle.close()
    return 0