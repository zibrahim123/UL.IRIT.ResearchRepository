'''
Created on Jul 3, 2016

@author: root
'''
import urllib
import urllib2
from urllib2 import URLError

def downloadFile(url):
    file_name = url.split('/')[-1]
    u = urllib2.urlopen(url)
    f = open("/media/zein/835C-4E2D/Research Datasets/DataSet - MediaEval/Dev/"+file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 1048576
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        #status = r"%10d  [%3.2f],  " % (file_size_dl, file_size_dl * 100. / file_size)
        #status = status + chr(8)*(len(status)+1)
        status = "%3.2f%% ...  " % (file_size_dl * 100. / file_size)
        print status,

    f.close()
    print "\n"
    return 0

def runDownload():
    videoDownloadList = open("/media/zein/835C-4E2D/Research Datasets/DataSet - MediaEval/Dev/videoDevDownloadList.txt","r")
    videoDownloadedList = open("/media/zein/835C-4E2D/Research Datasets/DataSet - MediaEval/Dev/videoDevDownloadedList.txt","a+")

    numberOfVideoToDownload = 10
    count = 0
    downloadedSet = set()
    for v in videoDownloadedList:
        downloadedSet.add(v[:-1])
        #print v[:-1]
        
    for v in videoDownloadList:
        value = v.split("/")
        videoName = value[len(value)-1][:-1]
        print "Downloading ... " + videoName
        if not (videoName in downloadedSet):
            '''
            try: 
                v = urllib2.urlopen(v)
                video = open("/media/zein/835C-4E2D/Research Datasets/DataSet - MediaEval/Dev/"+videoName,"w")
                video.write(v.read())
            except URLError as e:
                print e.reason   
            video.close()
            '''
            x = downloadFile(v[:-1])
            if x==0:
                videoDownloadedList.write(videoName+"\n")
                count += 1
                print str(count) +" /" + str(numberOfVideoToDownload) + " downloaded successfully"
                if count == numberOfVideoToDownload:
                    videoDownloadList.close()
                    videoDownloadedList.close() 
                    return
        else:
            print videoName + " is already downloaded"
    videoDownloadList.close()
    videoDownloadedList.close()   

runDownload()    