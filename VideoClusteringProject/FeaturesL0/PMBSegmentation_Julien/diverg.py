#!/usr/bin/env python
# -*- coding: utf-8 -*- 
'''

Created on 28 nov. 2013

@author: lecoz

Segmentation Forward/Backward

IRIT- 2013 - Maxime Le Coz <lecoz@irit.fr>

Temps de calcul indicatifs :

25 minutes  - Ordre 2 : 11759 Frontieres (2435.2275 sec)
12 secondes - Ordre 2 :   274 Frontieres   (19.0561 sec)
5  secondes - Ordre 2 :   141 Frontieres    (7.2487 sec)


'''

# Interrupteur pour l'affichage pas à pas et les message de temps de calcul
# Changer pour le développement uniquement
VERBOSE = False

# Interrupteur pour l'utilisation du critère voisé-non voisé pour 
# l'estimation des valeurs de lambda et de biais (experimental)
# Non correctement testé 
AUTOESTIM = False

from collections import deque
from scipy.io.wavfile import read as wavread
from sys import argv, exit
from numpy import spacing
from getopt import getopt, GetoptError

if AUTOESTIM : 
    from monopy import getCMNDF
    
if VERBOSE :
    import time
    from pylab import show, subplots
    from numpy.fft import fft
    from numpy import log, abs, zeros, NaN, array

order = 2
inputPath = None
outputPath = 'out.lab'

def printhelp():
    print 'Calcul de la segmentation en divergence F/B'
    print 'Usage :'
    print '\tdiverg.py -i <audiofile> -b <boundariesOutputFile> [ -o <ordre> ] [-v] [-h] '
    print '\t\t -i : Fichier audio à analyser'
    print '\t\t -o : Ordre de l\'analyse. Par défaut : %s' % order
    print '\t\t -b : Fichier de sortie. Par défaut : %s' % outputPath
    print '\t\t -h : Affiche ce message'
    exit(1)


class ModelLongTerm(object):
    '''
    Modelisation Long-Terme par la méthode d'autocorrelation.
    Initialisé sur les 'Lmin' premiers echantillons depuis la dernière
    rupture.
    
    Mis à jour echantillon après echantillon, le model grandit au fil
    des itérations.
    
    '''

    def __init__(self, ordre, echantillon):
        
        self.ordre = ordre
        self.ft = [0] * (ordre + 2)
        self.ftm1 = [0] * (ordre + 2)
        self.variance_f = [1] * (ordre + 2)
        self.variance_b = [1] * (ordre + 2)
        self.et = [0] * (ordre + 2)
        self.cor = [0] * (ordre + 2)
        self.length = 1
        self.erreur_residuelle = 0
        self.variance_erreur_residuelle = 0

        oubli = 1.0 / float(self.length) 

        self.variance_f[0] = self.variance_f[0] + oubli * (echantillon ** 2 - self.variance_f[0])
        self.variance_b[0] = self.variance_f[0]   
        self.et[0] = echantillon
        self.ft[0] = echantillon
        
        ik = min([ordre, self.length - 1])
        self.erreur_residuelle = self.et[ik]
        self.variance_erreur_residuelle = self.variance_f[ik]

    def miseAJour(self, echantillon):
        '''
        Mise a jour du model par ajout d'un echantillon.
        
        '''
                    
        self.length += 1
        self.ftm1 = self.ft[:]
        
        self.et[0] = echantillon      
         
        oubli = 1.0 / float(self.length) 
        self.variance_f[0] = self.variance_f[0] + oubli * (echantillon ** 2 - self.variance_f[0])
        self.variance_b[0] = self.variance_f[0]
        ik = min([self.ordre, self.length - 1])
        
        
        for n in xrange(ik + 1) :
            oubli = 1.0 / float(self.length - n) 
            
            self.cor[n] = self.cor[n] + oubli * (self.ftm1[n] * self.et[n] - self.cor[n]) 
            if (self.variance_f[n] + self.variance_b[n]) == 0 :
                knplus1 = 2 * self.cor[n] / spacing(self.variance_f[n])
            else :
                knplus1 = 2 * self.cor[n] / (self.variance_f[n] + self.variance_b[n])
            
            self.et[n + 1] = self.et[n] - knplus1 * self.ftm1[n] 
            self.ft[n + 1] = self.ftm1[n] - knplus1 * self.et[n]
            
            self.variance_f[n + 1] = self.variance_f[n + 1] + oubli * (self.et[n + 1] ** 2 - self.variance_f[n + 1])
            self.variance_b[n + 1] = self.variance_b[n + 1] + oubli * (self.ft[n + 1] ** 2 - self.variance_b[n + 1])
        
        self.ft[0] = echantillon
        self.erreur_residuelle = self.et[ik + 1]
        self.variance_erreur_residuelle = self.variance_f[ik + 1] 

    def __str__(self):
        '''
        Affichage console.
        '''
        
        s = 'Model Long Terme\n'
        s += '\tOrdre\t\t%d\n' % self.ordre
        s += '\tLongueur\t%d\n' % self.length
        s += '\tet\t\t['
        for e in self.et :
            s += '%f ' % e
        s += ']\n'
        s += '\tft\t\t['
        for e in self.ft :
            s += '%f ' % e
        s += ']\n'
        s += '\tft-1\t\t['
        for e in self.ftm1 :
            s += '%f ' % e
        s += ']\n'
        s += '\tVarb\t\t['
        for e in self.variance_b :
            s += '%f ' % e
        s += ']\n'
        s += '\tVarf\t\t['
        for e in self.variance_f :
            s += '%f ' % e
        s += ']\n'       
        s += '\tErreur\t\t%f\n' % self.erreur_residuelle
        s += '\tVar(err)\t%f\n' % self.variance_erreur_residuelle  
        return s


        
class ModelCourtTrerm(object):
    '''
    Model court terme, glissant de longueur fixe 'Lmin'. en utilisant la
    méthode des treillis.
    '''
    
    def __init__(self, ordre, buff):
        '''
        
        Constructor
        
        '''
        
        self.N = len(buff)
        self.ordre = ordre
        self.erreur_residuelle = 0
        self.variance_erreur_residuelle = 0
        self.coef_autocorr = [0] * (self.ordre + 2)
        self.AI = [0] * (self.ordre + 2)
        self.dernier_echantillon = 0
        self.buff = buff
        for tau in xrange(self.ordre + 1) :
            for i in xrange(self.N - tau):
                self.coef_autocorr[tau] = self.coef_autocorr[tau] + buff[i] * buff[i + tau - 1]
        self.estimModel()
        
    def estimModel(self):

        coef_reflexion = [0] * self.ordre
        
        if self.coef_autocorr[0] <= 0 :
            self.coef_autocorr[0] = 1.0
        
        coef_reflexion[0] = -self.coef_autocorr[1] / self.coef_autocorr[0]
        self.AI[0] = 1
        self.AI[1] = coef_reflexion[0]
        self.variance_erreur_residuelle = self.coef_autocorr[0] + self.coef_autocorr[1] * coef_reflexion[0] 
        
        if self.ordre > 1 :
            i_ordre = 1
            while i_ordre < self.ordre and self.variance_erreur_residuelle > 0  :

                if self.variance_erreur_residuelle > 0 :                    
                    S = 0
                    for i in xrange(i_ordre) :
                        S = S + self.AI[i] * self.coef_autocorr[i_ordre - i + 1]
                        
                    # coef reflexion
                    coef_reflexion[i_ordre] = -S / self.variance_erreur_residuelle
                    
                    MH = i_ordre / 2 + 1
                    for i in xrange(1, MH) :
                        
                        IB = i_ordre - i + 2
                        tmp = self.AI[i] + coef_reflexion[i_ordre] * self.AI[IB]
                        self.AI[IB] = self.AI[IB] + coef_reflexion[i_ordre] * self.AI[i]
                        self.AI[i] = tmp 
                    self.AI[i_ordre + 1] = coef_reflexion[i_ordre]
                    self.variance_erreur_residuelle = self.variance_erreur_residuelle + coef_reflexion[i_ordre] * S

                i_ordre += 1
                
        if self.variance_erreur_residuelle > 0 :
            self.variance_erreur_residuelle = self.variance_erreur_residuelle / float(self.N - 1)
            self.erreur_residuelle = 0 
            for i in range(self.ordre + 1) :
                self.erreur_residuelle = self.erreur_residuelle + self.AI[i] * self.buff[self.N - i - 1]        
                
    def miseAJour(self, echantillon):
        self.dernier_echantillon = self.buff.popleft()
        self.buff.append(echantillon)
        for tau in xrange(1, self.ordre + 1):
            self.coef_autocorr[tau] = self.coef_autocorr[tau] - self.dernier_echantillon * self.buff[tau - 1] + self.buff[self.N - tau - 1] * self.buff[self.N - 1]
        self.coef_autocorr[0] = self.coef_autocorr[0] - self.dernier_echantillon ** 2 + self.buff[self.N - 1] ** 2
        self.estimModel()
        
    def __str__(self):
        '''
        '''
        s = 'Model Court Terme\n'
        s += '\tOrdre\t%d\n' % self.ordre
        s += '\tAI\t['
        for e in self.AI :
            s += '%f ' % e
        s += ']\n' 
        s += '\tErreur\t%d\n' % self.erreur_residuelle
        s += '\tVar(err)\t%d\n' % self.variance_erreur_residuelle
        s += '\tAutocor\t ['
        for e in self.coef_autocorr :
            s += '%f ' % e
        s += ']\n'        
        return s     

def calculDistance(modeleLong, modeleCourt):
    '''
    Calcul de la distance entre les modèles longs et court terme
    
    args :
        - modeleLong (ModelLongTerme) : Modèle appris sur tous les echantillons depuis la dernière rupture
        - modeleCourt (ModelCourtTrerm): Modèle appris sur les Lmin derniers echantillons 
    '''
    
    if modeleCourt.variance_erreur_residuelle == 0 :
        # epsilon pour le type de donnés correspondant à modeleLong.variance_erreur_residuelle
        numerateur = spacing(modeleCourt.variance_erreur_residuelle)
    else :
        numerateur = modeleCourt.variance_erreur_residuelle
            
    QV = numerateur / modeleLong.variance_erreur_residuelle
    return (2 * modeleCourt.erreur_residuelle * modeleLong.erreur_residuelle / modeleLong.variance_erreur_residuelle - (1.0 + QV) * modeleLong.erreur_residuelle ** 2 / modeleLong.variance_erreur_residuelle + QV - 1.0) / (2.0 * QV)

def segment(data, fe, ordre=2, Lmin=0.02, lamb=40.0, biais=-0.2, with_backward=True, seuil_vois=None, withTrace=False):
    '''
    Fonction principale de segmentation.
    
    args : 
        - data (list of float): echantillons du signal
        - fe  (float) : fréquence d'échantillonage
        - ordre (int) : ordre des modèles. Par défaut = 2
        - Lmin (float) : longeur minimale d'un segment et taille du buffer pour l'apprentissage du model court terme. Par défaut = 0.02
        - lamb (float) : valeur de lambda pour la détection de chute de Wn. Par défaut = 40.0
        - biais (float) : valeur du bias à appliquer (en négatif). Par défaut = -0.2
        - with_backward (Bool) : Interrupteur du calcul ou non en backward. Par défaut = True
        - seuil_vois (float) : Si fixé, défini les valeurs de lambda et du biais en fonction du voisement ou non du buffer initial du model court terme.
                               (voisement_yin >  seuil_vois ==> Non voisé). Par défaut = None
        - withTrace (Bool) : Enregistre ou non la trace de tous les calculs pour un affichage à postériori. Par défaut = False 
    
    '''
    # Initialisation
    frontieres = []    
    t = 0 
    rupt_last = t 
    long_signal = len(data)
    # taille minimum en echantillons
    Lmin = int(Lmin * fe)
    # Trace de calcul
    trace = []
    while t < long_signal - 1 :
        # Nouvelle Rupture
        
        #    Critere d'arret : decouverte d'une rupture
        rupture = False
        
        # Cumulateur de vraissemblance
        Wn = 0.
        
        # Valeur et emplacement de la valeur max
        maxi = (0, -1)
        
        audio_buffer = deque([], Lmin)
            
        # Initialisation du modèle long terme
        echantillon = data[t]
        longTerme = ModelLongTerm(ordre, echantillon)
        

        if withTrace :
            dynaWn = []
            tWn = []
            
            
        while (not rupture) and t < long_signal - 1  : 
            
            t += 1
            
            # Mise à jour du long terme
            echantillon = data[t]
            longTerme.miseAJour(echantillon)

            # Si l'ecart avec la dernière rupture est suffisant
            # pour utiliser le modèle court terme 
            if t - rupt_last >= Lmin :
                
                # Initialisation du modèle court terme
                if t - rupt_last == Lmin :
                    courtTerme = ModelCourtTrerm(ordre, audio_buffer)
                    
                    # Estimation automatique du biais et de lambda 
                    # par detection de voisement
                    if not seuil_vois == None:                                
                            if min(getCMNDF(list(audio_buffer), 270)) > seuil_vois : 
                                # Non voisé
                                biais = -0.2
                                lamb = 40
                            else :
                                # Voisé
                                biais = -0.8 
                                lamb = 80
                # Mise à jour du modèle court terme                               
                if t - rupt_last > Lmin :
                    courtTerme.miseAJour(echantillon)
                
                # mise à jour du critère
                Wn = Wn + calculDistance(longTerme, courtTerme) - biais
                
                # Recherche de nouveau maximum
                if Wn > maxi[0] :
                    maxi = (Wn, t)
                
                if withTrace :
                    dynaWn += [Wn]
                    tWn += [t]
                    
                # Recherche de rupture par chute superieure à lambda
                if (maxi[0] - Wn) > lamb :
                    rupture = True
            else :
                # Sinon, on prepare l'initialisation
                audio_buffer.append(echantillon)
        
        # Positionnement de la rupture au dernier point maximum        
        t_rupt = maxi[1]
        
        if withTrace :
            evnt = {'Wn':dynaWn, 'timeLine':tWn, 't_rupt':t_rupt, 'Wn_max':maxi[0]}
        
        # Si une rupture à été detecté avec un modèle stable (Wn à croit)   
        if t_rupt > -1 :
            
            m = 'forward'                
            if with_backward :
                
                bdata = data[t_rupt:rupt_last:-1]
                
                if len(bdata) > 0 :
                
                    front, btrace = segment(bdata, fe, ordre, float(Lmin) / fe, lamb, biais, with_backward=False, seuil_vois=seuil_vois, withTrace=withTrace)
                    t_bs = [ t_rupt - tr for tr, _ in front]
                    
                    if len(t_bs) > 0 :
                        t_rupt = t_bs[-1]
                        m = 'backward'
                    
                    if withTrace :
                        evnt['back_rupt'] = t_bs
                        for b in btrace:
                            b['timeLine'] = [t_rupt - t for t in b['timeLine']]
                        evnt['back_Wn'] = btrace     
        
        # Sinon on crée un segment de longueur minimale
        else :
            t_rupt = rupt_last + Lmin
            m = 'instable'
            
        if withTrace :
            evnt['selected'] = t_rupt
            evnt['comment'] = m
            trace += [evnt]

        # Mise à jour des frontières
        t = t_rupt 
        rupt_last = t_rupt
        
        if rupture :
            frontieres.append((t_rupt, m))
            
    return frontieres, trace

class LineBuilder:
    '''
    Classe d'affichage de la trace
    '''
    def __init__(self, trace, signal, Wlen=256, pas=25, Nfft=1024):
        
        self.idx = 0
        self.mod = True
        self.trace = trace        
        spectro, timeLine = self.getSpectro(signal, Wlen, pas, Nfft)
        self.f, self.axarr = subplots(2, sharex=True)
        self.axarr[0].imshow(spectro, origin='lower', extent=[timeLine[0], timeLine[-1], 0, fe / 2], aspect='auto')
        self.axarr[1].plot(array(signal) / max(abs(signal)))
        self.fplot = self.axarr[0].plot(0, 0, 'b')[0]
        self.bplot = self.axarr[0].plot(0, 0, 'r')[0]
        self.cid = self.f.canvas.mpl_connect('key_press_event', self)    
        show()
        
    def getSpectro(self, signal, Wlen, pas, Nfft):
        '''
        Calcule le spectro d'un signal
        '''
        
        w = Wlen / 2
        timeLine = range(w, len(signal) - w, pas) 
        spectro = zeros((Nfft, len(timeLine)))
        for i, t in enumerate(timeLine):
            spectro[:, i] = log(abs(fft(signal[t - w:t + w], 2 * Nfft)))[:Nfft]
        return spectro, timeLine
    def __call__(self, event):
        '''
        Fonction d'affichage progressif
        '''
        if  event.key == 'n':
            if self.mod :
                self.mod = False
                self.bplot.set_data(0, 0)
                x = self.trace[self.idx]['timeLine']
                y = self.trace[self.idx]['Wn']
                y = array(y)
                y = 8000.0 * y / max(y)
                
                self.fplot.set_data(x, y)
                x = []
                y = []
                if self.trace[self.idx].has_key('back_Wn'):
                    for b in self.trace[self.idx]['back_Wn'] : 
                        x.extend(b['timeLine'])
                        y.extend(b['Wn'])
                        x.append(NaN)
                        y.append(NaN)
                    y = array(y)
                    y = 8000.0 * y / max(y)
                self.bplot.set_data(x, y)
            else :
                self.mod = True    
                sx = self.trace[self.idx]['selected']       
                self.axarr[0].plot([sx, sx], [0, 8000], 'k')
                self.axarr[1].plot([sx, sx], [-1, 1], 'k')
                self.idx += 1
                print self.trace[self.idx]['comment'] 
    
            self.f.canvas.draw()
        elif event.key == 'b' :
            self.idx = self.idx - 1
    

if __name__ == '__main__':
    #  Lecture du fichier son et passage en float
    try :	
        opts, args = getopt(argv[1:], 'hi:o:vb:')
    except GetoptError:
        printhelp()	
    for opt, arg in opts:	
        if opt == '-h' :
            printhelp()	
        elif opt == '-i' :
            inputPath = arg
        elif opt == '-o' :
            order = int(arg)
        elif opt == '-b' :
            outputPath = arg
        elif opt == '-v' :
            VERBOSE = True

    if not inputPath == None :
        fe, data = wavread(inputPath) 
    else : 
        printhelp()

    data = [float(i) for i in data]
   
    if AUTOESTIM :
        seuil_vois = 0.5 
    else :
        seuil_vois = None 
    
    if VERBOSE :
            st = time.time()
            
    frontieres, trace = segment(data, fe, ordre=order, with_backward=True, withTrace=VERBOSE, seuil_vois=seuil_vois)
    
    if VERBOSE :
        print 'Ordre %d : %d Frontieres (%.4f sec)' % (ordre, len(frontieres), time.time() - st)          
        LineBuilder(trace, data)
     
    # Sortie texte
    with open(outputPath, 'w') as f :
        for t, m in frontieres :
            f.write('%f\t%s\n' % (float(t) / fe, m));
                
