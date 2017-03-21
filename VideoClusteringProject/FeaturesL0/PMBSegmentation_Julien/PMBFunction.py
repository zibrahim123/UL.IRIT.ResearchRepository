'''
Created on May 29, 2016

@author: root
'''
#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from scipy.io.wavfile import read as wavread
from numpy import mean, diff, exp, arange, histogram, log, sqrt, zeros, var, iinfo, log10, ceil, linspace, hamming,\
    dot, array, logical_and, sum as npSum
from numpy.fft import rfft
from scipy.signal import firwin, lfilter
from diverg import segment
import xml.dom.minidom
import io


inputPath = None
outputPath = 'out.lab'
boundariesPath = None
verbose = False

# Communs
wLen = 0.016
wStep = 0.008
withEntropy = False
with4Hz = False
withNBS = False
withLS = False
moduLen = 1
speech_labels = {0: 'Non Speech', 1: 'Speech'}
music_labels = {0: 'Non Music', 1: 'Music'}

sort =False
# entropy
entropyTh = 0.4

# 4 Hz
fcenter = 4.0
fwidth = 0.5
normalized = True
N = 2048
ordre = 100
nbFilters = 30
energyTh = 1.5

# Music
musicLen = 1.0
musicStep = 0.1

maxSegForLength = 1000

thLen = 0.04
thNb = 20


def computeModulation(serie, wLen, withLog=True):
        """
        Compute the modulation of a parameter centered. Extremums are set to zero.
        
        Args :
            - serie       : list or numpy array containing the serie.
            - wLen        : Length of the analyzis window in samples.
            - withLog     : Whether compute the var() or log(var()) .    
        
        Returns :
            - modul       : Modulation of the serie.
        
        """
        
        modul = zeros((1, len(serie)))[0]
        w = int(wLen/2)
        
        for i in range(w, len(serie)-w):
            
            d = serie[i-w:i+w]
            if withLog:
                d = log(d)
            modul[i] = var(d)
        
        modul[:w] = modul[w]
        
        modul[-w:] = modul[-w-1]
    
        return modul
 

def melFilterBank(nbFilters, fftLen,sr):
    """
    Grenerate a Mel Filter-Bank
        
    Args :
        - nbFilters  : Number of filters.
        - fftLen     : Length of the frequency range.
        - sr         : Sampling rate of the signal to filter. 
    Returns :
        - filterbank : fftLen x nbFilters matrix containing one filter by column.
                        The filter bank can be applied by matrix multiplication 
                        (Use numpy *dot* function).      
    """
        
    fh = float(sr)/2.0    
    mh = 2595*log10(1+fh/700)
        
    step = mh/nbFilters
        
    mcenter = arange(step, mh, step)
        
    fcenter = 700*(10**(mcenter/2595)-1)
            
    filterbank = zeros((fftLen, nbFilters))
        
    for i, _ in enumerate(fcenter):
            
        if i == 0:
            fmin = 0.0
        else:
            fmin = fcenter[i-1]
                
        if i == len(fcenter)-1 :
            fmax = fh
        else:
            fmax = fcenter[i+1]    
            
        imin = ceil(fmin/fh*fftLen)
        imax = ceil(fmax/fh*fftLen)
            
        filterbank[imin:imax,i] = triangle(imax-imin)
    
    return filterbank


def triangle(length):
    '''
    Generate a triangle filter.
        
    Args :
         - length  : length of the filter.
    returns :
        - triangle : triangle filter.    
            
    '''
    triangle = zeros((1,length))[0]
    climax= ceil(length/2)
        
    triangle[0:climax] = linspace(0,1,climax)
    triangle[climax:length] = linspace(1,0,length-climax)
    return triangle
    
def entropy(serie,nbins=10,base=exp(1),approach='unbiased'):
        '''
        Compute entropy of a serie using the histogram method.

        Args :
            - serie     : Serie on witch compute the entropy
            - nbins     : Number of bins of the histogram
            - base      : Base used for normalisation
            - approach  : String in the following set : {unbiased,mmse}
                          for un-biasing value.

        Returns :
            - estimate  : Entropy value
            - nbias     : N-bias of the estimate
            - sigma     : Estimated standard error

        Raises :
            A warning in case of unknown 'approach' value.
            No un-biasing is then performed

        '''

        estimate = 0
        sigma = 0
        bins, edges = histogram(serie,nbins)
        ncell = len(bins)
        norm = (max(edges)-min(edges))/len(bins)


        for b in bins :
            if b == 0 :
                logf = 0
            else :
                logf = log(b)
            estimate = estimate - b*logf
            sigma = sigma + b * logf**2

        count = sum(bins)
        estimate=estimate/count
        sigma=sqrt( (sigma/count-estimate**2)/float(count-1) )
        estimate=estimate+log(count)+log(norm)
        nbias=-(ncell-1)/(2*count)

        if approach =='unbiased' :
            estimate=estimate-nbias
            nbias=0

        elif approach =='mmse' :
            estimate=estimate-nbias
            lambda_value=estimate^2/(estimate^2+sigma^2)
            nbias   =(1-lambda_value)*estimate
            estimate=lambda_value*estimate
            sigma   =lambda_value*sigma
        else :
            return 0

        estimate=estimate/log(base)
        nbias   =nbias   /log(base)
        sigma   =sigma   /log(base)
        return estimate


def readBoundaries(path) :
    boundaries = []
    weights    = []
    withWeight = True
    with open(path) as f :
        for l in f.readlines() :
            l = l.split('\t')
            if withWeight and len(l)< 3 :
                withWeight = False
            if withWeight :
                boundaries+=[(float(l[0]),float(l[1]),l[2].strip())]
            else :
                boundaries+=[(float(l[0]),l[1].strip())]
    return boundaries


def decoupe(values,th=0):
    values = [1 if v > th else 0 for v in values]
    frontieres = [t for t,v in enumerate(diff(values)) if abs(v) == 1]
    frontieres.append(len(values)-1)
    segments = [(frontieres[i-1],f,values[f]) if i> 0 else (0,f,values[f]) for i,f in enumerate(frontieres)]
    return segments



def printhelp():
    print 'Segmentation Parole/Musique'
    print 'Usage :'
    print '\tpmb.py -i <audiofile> [-b <fichier_frontieres>] [-v] [-h] [-w <longueur>] [-s <pas>]  [--4hz] [--Entropy] [--NBS] [--LS]'
    print '\t\t -i : Fichier audio a analyser'
    print '\t\t -o : Fichier de sortie. Par defaut :%s'%outputPath
    print '\t\t -h : Affiche ce message'
    print '\t\t -b : Fichier frontieres pour l\'analyse de la musique'
    print '\t\t --4Hz : Detection de parole par la methode de la modulation d\'energie a 4Hz.'
    print '\t\t --Entropy : Detection de parole par la methode de la modulation d\'entropie.'
    print '\t\t --NBS : Detection de musique par l\'analyse du nombre de segments.'
    print '\t\t --LS : Detection de musique par l\'analyse des longueurs de segments.'
    print '\t\t -w : Taille de la fenetre d\'analyse en secondes. Par defaut : %.3f'%wLen
    print '\t\t -s : Pas de la fenetre d\'analyse en secondes. Par defaut : %.3f'%wStep
    exit()

def PMBSegmentation(argv, nameFileOutputXML) :
    inputPath = None
    outputPath = 'out.lab'
    boundariesPath = None
    verbose = False

    # Communs
    wLen = 0.016
    wStep = 0.008
    withEntropy = False
    with4Hz = False
    withNBS = False
    withLS = False
    moduLen = 1
    speech_labels = {0: 'Non Speech', 1: 'Speech'}
    music_labels = {0: 'Non Music', 1: 'Music'}
    
    sort =False
    # entropy
    entropyTh = 0.4
    
    # 4 Hz
    fcenter = 4.0
    fwidth = 0.5
    normalized = True
    N = 2048
    ordre = 100
    nbFilters = 30
    energyTh = 1.5
    
    # Music
    musicLen = 1.0
    musicStep = 0.1
    
    maxSegForLength = 1000
    
    thLen = 0.04
    thNb = 20

    segments = []
    boundaries = None
    # Lecture des arguments
    opts = argv
    #print opts
    i=0
    while(i<len(argv)):
        #print str(i)
        if opts[i] == '-h' :
            printhelp()
        elif opts[i] =='-i' :
            i = i + 1
            inputPath = opts[i]
        elif opts[i] =='-o' :
            outputPath = opts[i]
        elif opts[i] =='-b' :
            i = i + 1
            boundariesPath = opts[i]
        elif opts[i] =='-v' :
            verbose = True

        elif opts[i] =='--sorted' :
            sort = True
        elif opts[i] =='--Entropy' :
            withEntropy = True
        elif opts[i] =='--4Hz' :
            with4Hz = True
        elif opts[i] =='--NBS' :
            withNBS = True
        elif opts[i] =='--LS' :
            withLS = True
        elif opts[i] =='-w' :
            i = i + 1
            wLen = float(opts[i])
        elif opts[i] =='-s' :
            i = i + 1
            wStep = float(opts[i])
        i = i + 1

    if inputPath == None  :
        printhelp()
        exit(1)
    else :
        #print "Audio file path : "+ inputPath
        fe, data = wavread(inputPath)
        print "Audio file opened : "+ inputPath
        fe= float(fe)
        m = iinfo(data[0]).max    
        data = [float(d)/m for d in data ]
        demi = int(wLen/2*fe)
        timeScale = range(demi,len(data)-demi,int(wStep*fe))
        frames = [data[t-demi:t+demi] for t in timeScale]

    if withEntropy :

        if verbose :
            print 'Analyse de la modulation d\'entropy'
        entropy_values = [entropy(f) for f in frames]
        entropy_modulation = computeModulation(entropy_values, moduLen/wStep,withLog=False)
        with open('entropy.lab','w') as f:
            for t,v in zip(timeScale,entropy_modulation) :
                f.write('%f\t%f\n'%(float(t)/fe,v))
        entropy_modulation = [(e/entropyTh)-1 if e< 2*entropyTh else 1 for e in entropy_modulation]

        segments_entropy = decoupe(entropy_modulation)
        segments_entropy=[(s[0]*wStep,s[1]*wStep,speech_labels[s[2]]+' (Entropy)') for s in segments_entropy]
        segments.extend(segments_entropy)

    if with4Hz :
        if verbose :
            print 'Analyse de la modulation d\'energie a 4Hz'
        Wo = fcenter/fe
        Wn = [ Wo-(fwidth/2)/fe , Wo+(fwidth/2)/fe]
        num = firwin(ordre, Wn,pass_zero=False)
        melFilter = melFilterBank(nbFilters,N,fe);
        hw = hamming(wLen*fe)
        energy = [dot(abs(rfft(hw*f,n=2*N)[0:N])**2,melFilter) for f in frames]
        #                      transposition de list of list
        energy = lfilter(num,1,map(list, zip(*energy)),0)
        energy = sum(energy)
        if normalized :
            energy =energy/mean(energy)

        energy_modulation = computeModulation(energy,moduLen/wStep,withLog=True)
        with open('energy.lab','w') as f :
            for t,v in zip(timeScale,energy_modulation) :
                f.write('%f\t%f\n'%(float(t)/fe,v))
        energy_modulation = [(e/energyTh)-1 if e< 2*energyTh else 1 for e in energy_modulation]
        segments_energy = decoupe(energy_modulation)
        segments_energy=[(s[0]*wStep,s[1]*wStep,speech_labels[s[2]]+' (4Hz)') for s in segments_energy]
        segments.extend(segments_energy)

    if withLS :

        if verbose :
            print 'Analyse de la longueur des segments'

        if boundariesPath == None:
            a,b = segment(data, fe)
            boundaries =[(float(st[0])/fe, ) for st in a]

        else :
            boundaries = readBoundaries(boundariesPath)

        times = array([ b[0] for b in boundaries ])
        demi = musicLen/2
        timeScale     = arange(demi,times[-1]-demi,musicStep)

        # On prend les plus petits !!
        segframes     = [sorted(diff(times[logical_and(times >= t-demi,times <= t+demi)]),reverse=True) for t in timeScale]
        lengths     = [mean(s[:min([maxSegForLength,len(s)])]) for s in segframes]

        with open('LS.lab','w') as f :
            for t,v in zip(timeScale,lengths) :
                f.write('%f\t%f\n'%(float(t)/fe,v))

        lengths     = [(l/thLen)-1 if l< 2*thLen else 1 for l in lengths]


        segments_length = decoupe(lengths)
        segments_length =[(s[0]*musicStep,s[1]*musicStep,music_labels[s[2]]+' (LS)') for s in segments_length]

        segments.extend(segments_length)

    if withNBS :
        if verbose :
            print 'Analyse du nombre de segments'

        if boundariesPath == None :

            if boundaries == None :
                a,b = segment(data, fe)
                boundaries =[(float(st[0])/fe, ) for st in a]

        else:

            if boundaries == None :
                boundaries = readBoundaries(boundariesPath)

        times = array([ b[0] for b in boundaries ])
        demi = musicLen/2
        timeScale = arange(demi,times[-1]-demi,musicStep)
        segnb = [float(npSum(logical_and(times >= t-demi,times <= t+demi))) for t in timeScale]
        with open('NBS.lab','w') as f :
            for t,v in zip(timeScale,segnb) :
                f.write('%f\t%f\n'%(float(t)/fe,v))

        segnb     = [-(l/thNb)+1 if l< 2*thNb else 1 for l in segnb]

        segments_nb = decoupe(segnb)
        segments_nb =[(s[0]*musicStep,s[1]*musicStep,music_labels[s[2]]+' (NBS)') for s in segments_nb]
        segments.extend(segments_nb)

    if sort:
        segments = sorted(segments, key=lambda x: x[0])
    v = writeToXML(segments, nameFileOutputXML, withNBS, with4Hz, withLS, withEntropy)
    return v
    #print "Audio file processed sucessfully"
    '''
    with open(outputPath, 'w') as f:
        for s in segments:
            print s
            f.write('%f\t%f\t%s\n' % s)
    '''
def writeToXML(seg, outputXMLFile,withNBS, with4Hz, withLS, withEntropy):
    try:
        DOMTreeOut = xml.dom.minidom.parse(outputXMLFile)
        rootOut = DOMTreeOut.documentElement
        #print ('ASR file opened for processing: '+ asrFilePath)
    except IOError:
        print ("Error while opening the xml file to write Speech and music segments: "+ outputXMLFile )
        return -1
        
    SpeechList = DOMTreeOut.createElement("SpeechSegmentation")
    MusicList = DOMTreeOut.createElement("MusicSegmentation")
    
    if(withNBS):
        MusicList.setAttribute("method","NBS")
    elif(withLS):
        MusicList.setAttribute("method","LS")
    else:
        MusicList.setAttribute("method","Not specified")
    
    if(with4Hz):
        SpeechList.setAttribute("method","4Hz")
    elif(withEntropy):
        SpeechList.setAttribute("method","Entropy")
    else:
        SpeechList.setAttribute("method","Not specified")
    
    for s in seg:
        if("Speech" in s[2]):
            if("Non Speech" in s[2]):
                NSpeech = DOMTreeOut.createElement("NonSpeech")
                NSpeech.setAttribute("start",str(s[0]))
                NSpeech.setAttribute("end",str(s[1]))
                SpeechList.appendChild(NSpeech)
            else:
                Speech = DOMTreeOut.createElement("Speech")
                Speech.setAttribute("start",str(s[0]))
                Speech.setAttribute("end",str(s[1]))
                SpeechList.appendChild(Speech)
        elif("Music" in s[2]):
            if("Non Music" in s[2]):
                NMusic = DOMTreeOut.createElement("NonMusic")
                NMusic.setAttribute("start",str(s[0]))
                NMusic.setAttribute("end",str(s[1]))
                MusicList.appendChild(NMusic)
            else:
                Music = DOMTreeOut.createElement("Music")
                Music.setAttribute("start",str(s[0]))
                Music.setAttribute("end",str(s[1]))
                MusicList.appendChild(Music)            
    rootOut.getElementsByTagName("Audio")[0].appendChild(SpeechList)
    rootOut.getElementsByTagName("Audio")[0].appendChild(MusicList)     
    
    file_handle = io.open(outputXMLFile, 'wb')
    rootOut.writexml(file_handle)
    file_handle.close()
    #print "Video file processed successfully" 
    return 0

#PMBSegmentation(['--4Hz','--NBS', '-i', "/home/zein/Desktop/test/Avidcruiser-StockholmsVasaMuseum479.flv.wav"],"/home/zein/Desktop/test/Avidcruiser-StockholmsVasaMuseum479.xml")    