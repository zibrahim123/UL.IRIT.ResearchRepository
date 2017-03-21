

videoList = open("/media/zein/835C-4E2D/Research Datasets/DataSet - MediaEval/Dev/videoList.txt","r")
out = open("/media/zein/835C-4E2D/Research Datasets/DataSet - MediaEval/Dev/videoDevDownloadList.txt","w")

for v in videoList:
    out.write("http://skuld.cs.umass.edu/traces/mmsys/2013/blip/Dev/Video/"+v[:-2]+".flv.ogv\n")
videoList.close()
out.close()