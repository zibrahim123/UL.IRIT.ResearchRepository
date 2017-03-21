'''
Created on Jun 4, 2016

@author: zein
'''

from aubio import source, pvoc, mfcc
from numpy import vstack, zeros
from scipy.io.wavfile import read as waveread
import xml.dom.minidom
import io

def getMFCC(source_filename, win_s=512, n_coeffs=14, samplerate=0):
    #win_s = 512                 # fft size
    hop_s = win_s // 4          # hop size
    n_filters = 40              # must be 40 for mfcc
    #n_coeffs = 13
    #samplerate = 0


    s = source(source_filename, samplerate, hop_s)
    samplerate = s.samplerate
    p = pvoc(win_s, hop_s)
    m = mfcc(win_s, n_filters, n_coeffs, samplerate)
    
    mfccs = zeros([n_coeffs,])
    frames_read = 0
    while True:
        samples, read = s()
        spec = p(samples)
        mfcc_out = m(spec)
        mfccs = vstack((mfccs, mfcc_out))
        frames_read += read
        if read < hop_s: break
    return mfccs


def getZCR_BruteForce(source_filename):
    
    rate, wavedata = waveread(source_filename)
    zero_crossings = 0
    for i in range(1, len(wavedata)):
        
        if ( wavedata[i - 1] <  0 and wavedata[i] >  0 ) or \
           ( wavedata[i - 1] >  0 and wavedata[i] <  0 ) or \
           ( wavedata[i - 1] != 0 and wavedata[i] == 0):
                
                zero_crossings += 1
    zero_crossing_rate = zero_crossings / float(len(wavedata) - 1)
    return rate, zero_crossing_rate

def extractMFCC_ZCR(source_filename, outputXMLFile, win_s=512, n_coeffs=14, samplerate=0):
    
    try:
        DOMTreeOut = xml.dom.minidom.parse(outputXMLFile)
    except IOError:
        print ('Error while opening the xml file of the output results in order to write zcr and mfcc')
        return
    
    rootOut = DOMTreeOut.documentElement
    
    sr, zcrValue = getZCR_BruteForce(source_filename)  
      
    zcr = DOMTreeOut.createElement('ZCR')
    zcr.appendChild(DOMTreeOut.createTextNode(unicode(zcrValue)))
    rootOut.getElementsByTagName("Audio")[0].appendChild(zcr)

    mfccsValue = getMFCC(source_filename, win_s, n_coeffs, samplerate)
    
    mfccs = DOMTreeOut.createElement('MFCC')
    mfccs.setAttribute("win_size",str(win_s))
    mfccs.setAttribute("nbCoefficients",str(n_coeffs))
    mfccs.setAttribute("hop_size",str(win_s // 4))
    
    r,c = mfccsValue.shape
    #print type(mfccsValue)
    X = mfccsValue.astype(float) 
    #print type(X)
    for i in range(0,r):
        coeff = DOMTreeOut.createElement("Coefficients")
        #for j in range(0,c):
        #    cf = DOMTreeOut.createElement("Coefficient")
        #    v = X[i,j]
            #print v
            #cf.appendChild(DOMTreeOut.createTextNode(v))
        #    cf.setAttribute("Value", str(v))
        #coeff.appendChild(DOMTreeOut.createTextNode(str(X[i])))
        coeff.setAttribute("Value",str(X[i]))
        mfccs.appendChild(coeff)
    rootOut.getElementsByTagName("Audio")[0].appendChild(mfccs)
    
    #print rootOut.toprettyxml(indent="  ")
    
    file_handle = io.open(outputXMLFile, 'wb')
    rootOut.writexml(file_handle)
    file_handle.close()
    print "MFCC coefficients and zcr extracted successfully"