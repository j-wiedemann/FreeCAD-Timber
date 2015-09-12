# -*- coding: utf-8 -*-
##    This file is part of pyOpenShelter
##    see: www.pyopenshelter.com
##    pyOpenShelter is written by Gerard Nespoulous
##     contact: jonathan@wiedemann.fr
##    
##    pyOpenShelter is a python implementation of mechanical computation
##
##    pyOpenShelter is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    pyOpenShelter is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with pyOpenShelter.  If not, see <http://www.gnu.org/licenses/>.

from math import *
from oshE5data import E5cara

class E5poutre():
    """
    VERIF POTEAU

    """
    def __init__(self, dic={}):
        self._dic=dic
        return 

    def dic(self):
        return self._dic

    def setM(self, value):
        """
        coef de flambement pour calculer la longueur lf!
        """
        self.dic()["m"]=value
        return self

    def m(self):
        """
        coef de flambement pour calculer la longueur lf!
        2 encastre en pied
        1 articule - articule (defaut)
        """
        try:
            return self.dic()["m"]
        except:
            return 1.

    def setLfH(self, value):
        """
        longueur en m
        """
        self.dic()["lfH"]=value
        return self
    def setLfB(self, value):
        """
        longueur en m
        """
        self.dic()["lfB"]=value
        return self

    def setLefB(self, value):
        """
        longueur efficace (pour deversement) en m
        voir tableau 6.1 eurocode5
        valeur par defaut : L
        """
        self.dic()["lefb"]=value
        return self

    def setLefH(self, value):
        """
        longueur efficace (pour deversement) en m
        voir tableau 6.1 eurocode5
        valeur par defaut : L
        """
        self.dic()["lefh"]=value
        return self

    def LefH(self):
        """
        longueur efficace en m
        par defaut: L
        """
        try:
            return self.dic()["lefh"]
        except:
            return self.L()

    def LefB(self):
        """
        longueur efficace en m
        par defaut: L
        """
        try:
            return self.dic()["lefb"]
        except:
            return self.L()


    def setL(self, value):
        """
        longueur en m
        """
        self.dic()["l"]=value
        return self

    def L(self):
        """
        longueur en m
        par defaut: 5m !!!
        """
        try:
            return self.dic()["l"]
        except:
            return 5.

    def LfH(self):
        try:
            return self.dic()["lfH"]*1000.
        except:
            return self.Lf()
    def LfB(self):
        try:
            return self.dic()["lfB"]*1000.
        except:
            return self.Lf()

    def Lf(self):
        """
        longueur de flambement en mm

        """
        return self.L()*self.m()*1000.

    def setSection(self, value):
        self._section=value

    def setH(self, value):
        """
        epaisseur de la poutre en mm!
       dans la direction de flambement 
        pour poutre rectangulaire
        """
        self.dic()["h"]=value
        return self

    def str_h(self, style="full", format="%.0f"):
        title="hauteur de la poutre"
        simple= "H="
        value=self.h()
        unit="mm"
        return self.str_(style, format, title, simple, value, unit)

    def str_b(self, style="full", format="%.0f"):
        title="largeur de la poutre"
        simple= "B="
        value=self.b()
        unit="mm"
        return self.str_(style, format, title, simple, value, unit)

    def str_Hef(self, style="full", format="%.0f"):
        title="hauteur efficace de la poutre"
        simple= "Hef="
        value=self.Hef()
        unit="mm"
        return self.str_(style, format, title, simple, value, unit)

    def str_Bef(self, style="full", format="%.0f"):
        title="largeur efficace de la poutre"
        simple= "Bef="
        value=self.Bef()
        unit="mm"
        return self.str_(style, format, title, simple, value, unit)



    def h(self):
        """
        epaisseur de la poutre en mm
       dans la direction de flambement 
        pour poutre rectangulaire
        valeur par defaut: 200
        """
        try:
            return self.dic()["h"]
        except:
            return 200.

    def setL1(self, value):
        """
        longueur des membrures pour
        un poteau reconstitué en m
        """
        self.dic()["l1"]=value
        return self

    def l1(self):
        """
        longueur des membrures pour
        un poteau reconstitué en mm
        valeur par defaut=L/2
        """
        try:
            return self.dic()["l1"]*1000.
        except:
            return self.L()/2.

    def setB(self, value):
        """
        epaisseur de la poutre en mm!
       dans la direction de non-flambement 
        pour poutre rectangulaire
        """
        self.dic()["b"]=value
        return self


    def b(self):
        """
        epaisseur de la poutre en mm
       dans la direction de non-flambement 
        pour poutre rectangulaire
        valeur par defaut: 100
        """
        try:
            return self.dic()["b"]
        except:
            return 100.


    def setAmembrures(self, value):
        """
        espacement membrures en mm
        dans le cas de poteaux reconstitues
        (annexe C eurocode5)
        1 pour un poteau monolythique
        """
        self.dic()["amembrures"]=value
        return self


    def aMembrures(self):
        """
        espacement membrures en mm
        dans le cas de poteaux reconstitues
        (annexe C eurocode5)
        valeur par defaut: b
        """
        try:
            return self.dic()["amembrures"]
        except:
            return self.b()


    def setNmembrures(self, value):
        """
        nombre de membrures
        dans le cas de poteaux reconstitues
        (annexe C eurocode5)
        1 pour un poteau monolythique
        """
        self.dic()["nmembrures"]=value
        return self


    def nMembrures(self):
        """
        nombre de membrures
        dans le cas de poteaux reconstitues
        (annexe C eurocode5)
        1 pour un poteau monolythique
        """
        try:
            return self.dic()["nmembrures"]
        except:
            return 1


    def setFacteurN(self, value):
        """
        facteur n 
        (annexe C eurocode5)
        6 par defaut
        """
        self.dic()["facteurN"]=value
        return self


    def facteurN(self):
        """
        facteur n
        dans le cas de poteaux reconstitues
        (annexe C eurocode5)
       6 par defaut
        """
        try:
            return self.dic()["facteurN"]
        except:
            return 6.

    def setFc0k(self, value):
        """
        contrainte caracteristique de resistance
        en compression axiale en MPa
        defaut=16
        """
        self.dic()["fcok"]=value
        return self

    def ft0k(self):
        """
        contrainte caracteristique de resistance
        en compression axiale en MPa
        defaut=16
        """
        try:
            return self.dic()["ftok"]
        except:
            return self.cara().ft0k()

    def fc0k(self):
        """
        contrainte caracteristique de resistance
        en compression axiale en MPa
        defaut=16
        """
        try:
            return self.dic()["fcok"]
        except:
            return self.cara().fc0k()

    def setFmk(self, value):
        """
        contrainte caracteristique de resistance
        en flexion en MPa
        defaut=
        """
        self.dic()["fmk"]=value
        return self

    def fmk(self):
        """
        contrainte caracteristique de resistance
        en flexion en MPa
        defaut
        """
        try:
            return self.dic()["fmk"]
        except:
            return self.cara().fmk()            

    def str_fmk(self, style="full", format="%.2f"):
        title="Contrainte caractéristique de résistance en flexion:"
        simple= "fmk="
        value=self.fmk()
        unit=self.uContraintes()
        return self.str_(style, format, title, simple, value, unit)        
        return 



    def setFvk(self, value):
        """
        contrainte caracteristique de resistance
        en cisaillement en MPa
        defaut=
        """
        self.dic()["fvk"]=value
        return self

    def fvk(self):
        """
        contrainte caracteristique de resistance
        en cisaillement en MPa
        defaut
        """
        try:
            return self.dic()["fvk"]
        except:
            return self.cara().fvk()            

    def str_fvk(self, style="full", format="%.2f"):
        title="Contrainte caractéristique de résistance en cisaillement:"
        simple= "fvk="
        value=self.fvk()
        unit=self.uContraintes()
        return self.str_(style, format, title, simple, value, unit)        
        return 




    def setE05(self, value):
        """
        module axial au 5ieme pourcentile
        defaut 4700 MPa
        """
        self.dic()["e05"]=value
        return self

    def E05(self):
        """
        module axial au 5ieme pourcentile
        defaut 4700 MPa
        """
        try:
            return self.dic()["e05"]
        except:
            return self.cara().E05()*1000.


    def momentInertieH(self, section="RECTANGLE"):
        """
        moment d'inertie en mm4
        bh3/12 pour un rectangle
        """
        return self.b()*pow(self.h(), 3)/12.

    def momentInertieB(self, section="RECTANGLE"):
        """
        moment d'inertie en mm4
        hb3/12 pour un rectangle

        """
        return self.h()*pow(self.b(), 3)/12.


    def momentInertieTot(self):
        """
        moment d'inertie en mm4
        hb3/12 pour un rectangle
        annexe C eurocode5
        """
        if self.nMembrures()==1:
            return self.h()*pow(self.b(), 3)/12.
        elif self.nMembrures()==2:
            return self.h()*( pow(2*self.b()+self.aMembrures(), 3)-pow(self.aMembrures(), 3))/12.

    def lambdaEf(self):
        """
        elancement pour un poteau reconstitue
        """
#        print "lambdaef oshpoteau"
#        print "lambda1 ", self.l1()/self.b()*sqrt(12.)
        lambda1=max(self.l1()/self.b()*sqrt(12.), 30)
        lambdA=self.LfB()*sqrt(self.Atot()/self.momentInertieTot())
        return sqrt(pow(lambdA, 2)+self.facteurN()*self.nMembrures()/2.*pow(lambda1, 2))


    def aire(self, section="RECTANGLE"):
        """
        aire de la section en mm²
        """
        return float(self.b()*self.h())



    def rayonGirationH(self):
        """
        racine(I/A)
        """
        return sqrt(self.momentInertieH()/self.aire())   

    def rayonGirationB(self):
        """
        racine(I/A)
        """
        return sqrt(self.momentInertieB()/self.aire())   

    def Atot(self):
        """
        2 fois l'aire, pour un poteau à 2 pieds
        self.nMembrures()*self.aire()
        """
        return self.nMembrures()*self.aire()



    def lambdaZH(self):
        """
        elancement mecanique:
        longueur flambement  / rayon giration
        """

        return self.LfH()/self.rayonGirationH()


    def lambdaZB(self):
        """
        elancement mecanique:
        longueur flambement  / rayon giration
        """
        return self.LfB()/self.rayonGirationB()


    def lambdaRtot(self):
        """
        elancement relatif
        """
        return self.lambdaEf()/pi*sqrt(self.fc0k()/self.E05())

    def lambdaRmH(self):
        """
        elancement relatif de flexion
        """
        return sqrt(self.fmk()/self.sigmaCritH())

    def lambdaRmB(self):
        """
        elancement relatif de flexion
        """
        return sqrt(self.fmk()/self.sigmaCritB())

    def str_kcrit(self, style="full", format="%.2f"):
        title="Elancement relatif de flexion:"
        simple= "lambda r,m="
        value=self.lambdaRm()
        unit=""
        return self.str_(style, format, title, simple, value, unit)        
        return 


    def str_kczH(self, style="full", format="%.2f"):
        title="Coefficicent reducteur compression (H):"
        simple= "kc,z,H="
        value=self.kczH()
        unit=""
        return self.str_(style, format, title, simple, value, unit)        
        return 

    def str_kczB(self, style="full", format="%.2f"):
        title="Coefficicent reducteur compression (B):"
        simple= "kc,z,B="
        value=self.kczB()
        unit=""
        return self.str_(style, format, title, simple, value, unit)        
        return 

    def str_kczTot(self, style="full", format="%.2f"):
        title="Coefficicent reducteur compression (T):"
        simple= "kc,z,Tot="
        value=self.kczTot()
        unit=""
        return self.str_(style, format, title, simple, value, unit)        
        return 

    def lambdaRH(self):
        """
        elancement relatif
        """
        return self.lambdaZH()/pi*sqrt(self.fc0k()/self.E05())

    def lambdaRB(self):
        """
        elancement relatif
        """
        return self.lambdaZB()/pi*sqrt(self.fc0k()/self.E05())



    def setClasseBois(self, value):
        """
        ex "c18"
        """
        self.dic()["classebois"]=value
        return self
    def classeBois(self):
        """
        classe de bois
        defaut c14
        """
        try:
            return self.dic()["classebois"]
        except:
            return "c14"

    def str_classeBois(self, style="title", format="%.0f"):
        style="title"
        title="Bois de classe %s" %self.classeBois()
        simple= ""
        value=0
        unit=""
        return self.str_(style, format, title, simple, value, unit)


    def cara(self):
        return E5cara(self.classeBois())

    def setBetac(self, value):
        """
        0.2 pour bois massif
        """
        self.dic()["betac"]=value
        return self
    def betac(self):
        """
        defaut 0.2
        """
        try:
            return self.dic()["betac"]
        except:
            return 0.2



    def kzH(self):
        """
        """
        return 0.5*(1+self.betac()*(self.lambdaRH()-0.3)+pow(self.lambdaRH(), 2.))
    def kzB(self):
        """
        """
        return 0.5*(1+self.betac()*(self.lambdaRB()-0.3)+pow(self.lambdaRB(), 2.))

    def kzTot(self):
        """
        """
        return 0.5*(1+self.betac()*(self.lambdaRtot()-0.3)+pow(self.lambdaRtot(), 2.))



    def kczH(self):
        """
        coefficient reducteur de la resistance du bois
        """
        return 1./(self.kzH()+sqrt(pow(self.kzH(), 2)-pow(self.lambdaRH(), 2)))

    def kczB(self):
        """
        coefficient reducteur de la resistance du bois
        """
        return 1./(self.kzB()+sqrt(pow(self.kzB(), 2)-pow(self.lambdaRB(), 2)))

    def kczTot(self):
        """
        coefficient reducteur de la resistance du bois
        """
        return 1./(self.kzTot()+sqrt(pow(self.kzTot(), 2)-pow(self.lambdaRtot(), 2)))


    ######################CHARGES
    def setN(self, value):
        """
        charge de compression axiale
        en kN
        """
        self.dic()["n"]=value

    def setTraction(self, value):
        """
        charge de traction axiale
        en kN
        """
        self.dic()["traction"]=value
    def Traction(self):
        """
        charge de traction axiale
        en kN
        """
        try:
            return self.dic()["traction"]
        except:
            return 0.
    def N(self):
        """
        charge de compression axiale
        en kN
        """
        try:
            return self.dic()["n"]
        except:
            return 0.
    def setMB(self, value):
        """
        charge de flexion selon B
        en kNm
        """
        self.dic()["mb"]=value

    def str_MH(self, style="full", format="%.2f"):
        title="Moment de flexion selon H"
        simple= "Mh="
        value=self.MH()
        unit="kNm"
        return self.str_(style, format, title, simple, value, unit)

    def str_N(self, style="full", format="%.2f"):
        title="Effort normal de compression:"
        simple= "N="
        value=self.N()
        unit="kN"
        return self.str_(style, format, title, simple, value, unit)


    def str_MB(self, style="full", format="%.2f"):
        title="Moment de flexion selon B"
        simple= "Mb="
        value=self.MB()
        unit="kNm"
        return self.str_(style, format, title, simple, value, unit)

    def str_CB(self, style="full", format="%.2f"):
        title="Effort de cisaillement selon B"
        simple= "Cb="
        value=self.CB()
        unit="kN"
        return self.str_(style, format, title, simple, value, unit)
    def str_CH(self, style="full", format="%.2f"):
        title="Effort de cisaillement selon H"
        simple= "Ch="
        value=self.CH()
        unit="kN"
        return self.str_(style, format, title, simple, value, unit)

    def MB(self):
        """
        charge de  flexion selon B
        en kNm
        """
        try:
            return self.dic()["mb"]
        except:
            return 0.

    def MH(self):
        """
        charge de flexion selon H
        en kNm
        """
        try:
            return self.dic()["mh"]
        except:
            return 0.



    def setMH(self, value):
        """
        charge de  flexion selon H
        en kNm
        """
        self.dic()["mh"]=value
        return self

    def CH(self):
        """
        charge de cisaillement selon H
        en kNm
        """
        try:
            return self.dic()["ch"]
        except:
            return 0.

    def setCH(self, value):
        """
        charge de  cisaillement selon H
        en kNm
        """
        self.dic()["ch"]=value
        return self

    def CB(self):
        """
        charge de cisaillement selon B
        en kNm
        """
        try:
            return self.dic()["cb"]
        except:
            return 0.

    def setCB(self, value):
        """
        charge de  cisaillement selon B
        en kNm
        """
        self.dic()["cb"]=value
        return self


    def Hef(self):
        """
        Hauteur efficace pour vérification des appuis
        defaut: h()
        """
        try:
            return self.dic()["hef"]
        except:
            return self.h()

    def setHef(self, value):
        """
        Hauteur efficace pour vérification des appuis
        defaut: h()
        """
        self.dic()["hef"]=value
        return self

    def Bef(self):
        """
        largeur efficace pour vérification des appuis
        defaut: b()
        """
        try:
            return self.dic()["bef"]
        except:
            return self.b()

    def setBef(self, value):
        """
        Largeur efficace pour vérification des appuis
        defaut: b()
        """
        self.dic()["bef"]=value
        return self

    def kf(self):
        """
        coefficient de forme pour le cisaillement
        defaut 3/2
        """
        try:
            return self.dic()["kf"]
        except:
            return 3./2.

    def setKf(self, value):
        """
        coefficient de forme pour le cisaillement
        defaut 3/2
        """
        self.dic()["kf"]=value
        return self


    ######### CONTRAINTES

    def tauB(self):
        """
        contrainte de cisaillement induite
        par le cisaillement selon B
        """
        return self.kf()*self.CB()/self.Bef()/self.h()*1000.

    def tauH(self):
        """
        contrainte de cisaillement induite
        par le cisaillement selon H
        """
        return self.kf()*self.CH()/self.b()/self.Hef()*1000.




    def sigmaC0d(self):
        """
        contrainte de compression
       axiale en MPA 
        """
        return 1000.*self.N()/self.Atot()

    def str_sigmaN(self, style="full", format="%.2f"):
        title="Contrainte de compression axiale"
        simple= "sigmaN (C0,d)="
        value=self.sigmaC0d()
        unit=self.uContraintes()
        return self.str_(style, format, title, simple, value, unit)        
        return 

    def VB(self):
        """
        distance a la fibre neutre en mm
        """
        return self.b()/2.
    def VH(self):
        """
        distance a la fibre neutre en mm
        """
        return self.h()/2.

    def moduleInertieB(self):
        """
        module d'inertie selon B en mm3
        """
        return self.momentInertieB()/self.VB()

    def moduleInertieH(self):
        """
        module d'inertie selon H e mm3
        """
        return self.momentInertieH()/self.VH()

    def sigmaCritH(self):
        """
        contrainte critique de flexion
        pour moment selon h
        (deversement)
        """
        return 0.78*self.E05()*self.b()*self.b()/self.h()/(self.LefH()*1000.+2*self.h())

    def sigmaCritB(self):
        """
        contrainte critique de flexion
        pour moment selon b
        (deversement)
        """
        return 0.78*self.E05()*self.h()*self.h()/self.b()/(self.LefB()*1000.+2*self.b())







    def sigmaB(self):
        """
        contrainte de flexion selon B en MPA
        """
        return self.MB()/self.moduleInertieB()*10.e5

    def setUcontraintes(self, value):
        self.dic()["ucontraintes"]=value
        return self
    def uContraintes(self):
        try:
            return self.dic()["ucontraintes"]
        except:
            return "MPa"


    def str_tauB(self, style="full", format="%.2f"):
        title="Contrainte de cisaillement selon B:"
        simple= "tauB="
        value=self.tauB()
        unit=self.uContraintes()
        return self.str_(style, format, title, simple, value, unit)        
    def str_tauH(self, style="full", format="%.2f"):
        title="Contrainte de cisaillement selon H:"
        simple= "tauH="
        value=self.tauH()
        unit=self.uContraintes()
        return self.str_(style, format, title, simple, value, unit)      


    def str_sigmaB(self, style="full", format="%.2f"):
        title="Contrainte de flexion selon B:"
        simple= "sigmaB="
        value=self.sigmaB()
        unit=self.uContraintes()
        return self.str_(style, format, title, simple, value, unit)        


    def str_sigmaH(self, style="full", format="%.2f"):
        title="Contrainte de flexion selon H"
        simple= "sigmaH="
        value=self.sigmaH()
        unit=self.uContraintes()
        return self.str_(style, format, title, simple, value, unit)        
        return 

    def sigmaH(self):
        """
        contrainte de flexion selon H en MPA
        """
        return self.MH()/self.moduleInertieH()*10.e5

    def setKcritB(self, value):
        """
        coefficient deversement
        """
        self.dic()["kcritb"]=value
        return self
    def kcritB(self):
        """
        defaut 1.
        """
        try:
            return self.dic()["kcritb"]
        except:
            l=self.lambdaRmB()
            if l<=0.75:
                k=1
            elif l<=1.4:
                k=1.56-0.75*l
            else:
                k=1/(l*l)
            return k

    def setKcritH(self, value):
        """
        coefficient deversement
        """
        self.dic()["kcrith"]=value
        return self
    def kcritH(self):
        """
        defaut 1.
        """
        try:
            return self.dic()["kcrith"]
        except:
            l=self.lambdaRmH()
            if l<=0.75:
                k=1
            elif l<=1.4:
                k=1.56-0.75*l
            else:
                k=1/(l*l)
            return k

    def str_kcritH(self, style="full", format="%.2f"):
        title="Coefficient d'instabilité provenant du déversement moment selon H:"
        simple= "kcrit="
        value=self.kcritH()
        unit=""
        return self.str_(style, format, title, simple, value, unit)        
        return 
    def str_kcritB(self, style="full", format="%.2f"):
        title="Coefficient d'instabilité provenant du déversement moment selon H:"
        simple= "kcrit="
        value=self.kcritH()
        unit=""
        return self.str_(style, format, title, simple, value, unit)        
        return 

    def setKsys(self, value):
        """
        coefficient systeme
        """
        self.dic()["ksys"]=value
        return self
    def ksys(self):
        """
        defaut 1.
        """
        try:
            return self.dic()["ksys"]
        except:
            return 1.

    def str_ksys(self, style="full", format="%.2f"):
        title="Coefficient d'effet système:"
        simple= "ksys="
        value=self.ksys()
        unit=""
        return self.str_(style, format, title, simple, value, unit)        
        return 

    def kh(self):
        """
        coefficient de hauteur
        """
        return 1.

    def kv(self):
        """
        coefficient d'aentaillage
        """
        try:
            return self.dic()["kv"]
        except:
            return 1.
    def setKv(self, value):
        """
        coefficient d'aentaillage
        """
        self.dic()["kv"]=value
        return self


    def str_kh(self, style="full", format="%.2f"):
        title="Coefficient de hauteur:"
        simple= "kh="
        value=self.kh()
        unit=""
        return self.str_(style, format, title, simple, value, unit)        


    def str_kf(self, style="full", format="%.2f"):
        title="Coefficient d'entaille pour le cisaillement:"
        simple= "kv="
        value=self.kv()
        unit=""
        return self.str_(style, format, title, simple, value, unit)        

    def str_kv(self, style="full", format="%.2f"):
        title="Coefficient de forme pour le cisaillement:"
        simple= "kf="
        value=self.kf()
        unit=""
        return self.str_(style, format, title, simple, value, unit)    



    def fmd(self):
        """
        resistance de flexion calculee
        """
#        print self.fmk()
#        print self.kmod()
#        print self.gammaM()
#        print self.ksys()
#        print self.kh() 

        return self.fmk()*self.kmod()/self.gammaM()*self.ksys()*self.kh()


    def fvd(self):
        """
        resistance de cisaillement calculée
        """
        return self.fvk()*self.kmod()/self.gammaM()

    def str_fmd(self, style="full", format="%.2f"):
        title="Contrainte caractéristique de résistance en flexion calculée:"
        simple= "fm,d="
        value=self.fmd()
        unit=self.uContraintes()
        return self.str_(style, format, title, simple, value, unit)        
    def str_fvd(self, style="full", format="%.2f"):
        title="Contrainte caractéristique de résistance en cisaillement calculée:"
        simple= "fv,d="
        value=self.fvd()
        unit=self.uContraintes()
        return self.str_(style, format, title, simple, value, unit)   


    def setKmod(self, value):
        """
        coefficient modificatif
        """
        self.dic()["kmod"]=value
        return self
    def kmod(self):
        """
        defaut 0.7
        """
        try:
            return self.dic()["kmod"]
        except:
            return 0.7
    def str_kmod(self, style="full", format="%.2f"):
        title="Coefficient modificatif"
        simple= "kmod="
        value=self.kmod()
        unit=""
        return self.str_(style, format, title, simple, value, unit)

    def setGammaM(self, value):
        """
        coefficient partiel dispersion materiau
        """
        self.dic()["gammaM"]=value
        return self
    def gammaM(self):
        """
        defaut 1.3
        """
        try:
            return self.dic()["gammaM"]
        except:
            return 1.3

    def str_gammaM(self, style="full", format="%.2f"):
        title="Coefficient partiel matériau"
        simple= "gammaM="
        value=self.gammaM()
        unit=""
        return self.str_(style, format, title, simple, value, unit)


    def ft0d(self):
        """
        contrainte de resistance en compression axiale
        """
        return self.ft0k()*self.kmod()/self.gammaM()
    def fc0d(self):
        """
        contrainte de resistance en compression axiale
        """
        return self.fc0k()*self.kmod()/self.gammaM()

    def tauxTravail(self):
        return max(self.tauxTravailH(), self.tauxTravailB(), self.tauxTravailCombine())
#        return self.sigmaC0d()/self.kcz()/self.fc0d()

    def tauxTravailCompression(self):
        return max(self.tauxTravailH(), self.tauxTravailB())
    def str_tauxTravail(self, style="full", format="%.2f"):
        title="Taux de travail :"
        simple= "tx="
        value=self.tauxTravail()
        unit=""
        return self.str_(style, format, title, simple, value, unit)        
        return 

    def str_tauxTravailCompression(self, style="full", format="%.2f"):
        title="Taux de travail compression seule selon H:"
        simple= "tx="
        value=self.tauxTravailCompression()
        unit=""
        return self.str_(style, format, title, simple, value, unit)        
        return 
    def str_tauxTravailCompressionH(self, style="full", format="%.2f"):
        title="Taux de travail compression seule flambement selon H:"
        simple= "tx="
        value=self.tauxTravailH()
        unit=""
        return self.str_(style, format, title, simple, value, unit)        
        return 
    def str_tauxTravailCompressionB(self, style="full", format="%.2f"):
        title="Taux de travail compression seule flambement selon B:"
        simple= "tx="
        value=self.tauxTravailB()
        unit=""
        return self.str_(style, format, title, simple, value, unit)        
        return 
    def tauxTravailFlexionH(self):
        return  self.sigmaH()/self.kcritH()/self.fmd()
    def str_tauxTravailFlexionH(self, style="full", format="%.2f"):
        title="Taux de travail flexion seule selon H:"
        simple= "tx="
        value=self.tauxTravailFlexionH()
        unit=""
        return self.str_(style, format, title, simple, value, unit)        
        return 
    def str_tauxTravailFlexionB(self, style="full", format="%.2f"):
        title="Taux de travail flexion seule selon B:"
        simple= "tx="
        value=self.tauxTravailFlexionB()
        unit=""
        return self.str_(style, format, title, simple, value, unit)        
        return 

    def tauxTravailFlexionB(self):
        return  self.sigmaB()/self.kcritB()/self.fmd()


    def tauxTravailCisaillementB(self):
        return  self.tauB()/self.kv()/self.fvd()
    def tauxTravailCisaillementH(self):
        return  self.tauH()/self.kv()/self.fvd()
    def tauxTravailCisaillement(self):
        return  self.tauxTravailCisaillementB()+self.tauxTravailCisaillementH()

    def km(self):
        return 0.7

    def tauxTravailCombine(self, N="compression"):
        """
        moment + compression
        """
        if N=="compression":
            return max(
                       pow(self.sigmaC0d()/self.fc0d(), 2) +self.tauxTravailFlexionH()+self.km()*self.tauxTravailFlexionB(), 
                            pow(self.sigmaC0d()/self.fc0d(), 2) +self.tauxTravailFlexionB()+self.km()*self.tauxTravailFlexionH()
                            )
        if N=="traction":
            return 



    def str_tauxTravailCisaillement(self, style="full", format="%.2f"):
        title="Taux de travail cisaillement:"
        simple= "tx="
        value=self.tauxTravailCisaillement()
        unit=""
        return self.str_(style, format, title, simple, value, unit)        
        return 

    def str_tauxTravailCombine(self, style="full", format="%.2f"):
        title="Taux de travail combiné:"
        simple= "tx="
        value=self.tauxTravailCombine()
        unit=""
        return self.str_(style, format, title, simple, value, unit)        
        return 
    def str_tauxTravailTraction(self, style="full", format="%.2f"):
        title="Taux de travail traction:"
        simple= "tx="
        value=self.tauxTravailTraction()
        unit=""
        return self.str_(style, format, title, simple, value, unit)        
        return 
    def tauxTravailTraction(self):
        return self.sigmaC0d()/self.ft0d()

    def tauxTravailH(self):
        return self.sigmaC0d()/self.kczH()/self.fc0d()
    def tauxTravailB(self):
        return self.sigmaC0d()/self.kczB()/self.fc0d()

    def tauxTravailTot(self):
        return self.sigmaC0d()/self.kczTot()/self.fc0d()

    def NmaxH(self):
        """
        effort normal maxi admissible en kN
        """
        return self.kczH()*self.fc0d()*self.Atot()/1000.

    def NmaxB(self):
        """
        effort normal maxi admissible en kN
        """
        return self.kczB()*self.fc0d()*self.Atot()/1000.
    def NmaxTot(self):
        """
        effort normal maxi admissible en kN
        """
        return self.kczTot()*self.fc0d()*self.Atot()/1000.        

    def Nmax(self):
        """
        effort normal maxi admissible en kN
        """
        if self.nMembrures()==1:
            return min(self.NmaxH(), self.NmaxB())
        else:
            return min(self.NmaxH(), self.NmaxTot())


    def str_LfH(self, style="full", format="%.2f"):
        title="Longueur de flambement selon H"
        simple= "LfH="
        value=self.LfH()
        unit="mm"
        return self.str_(style, format, title, simple, value, unit)
    def str_LfB(self, style="full", format="%.2f"):
        title="Longueur de flambement selon B"
        simple= "LfB="
        value=self.LfB()
        unit="mm"
        return self.str_(style, format, title, simple, value, unit)

    def str_lambdaRB(self, style="full", format="%.2f"):
        title="elancement selon B"
        simple= "LfB="
        value=self.lambdaRB()
        unit=""
        return self.str_(style, format, title, simple, value, unit)
    def str_lambdaRH(self, style="full", format="%.2f"):
        title="elancement selon H"
        simple= "LfH="
        value=self.lambdaRH()
        unit=""
        return self.str_(style, format, title, simple, value, unit)

    def str_lambdaRtot(self, style="full", format="%.2f"):
        title="elancement selon B (reconstitue)"
        simple= "LfTot="
        value=self.lambdaRtot()
        unit=""
        return self.str_(style, format, title, simple, value, unit)



    def str_(self, style, format, title, simple, value, unit):
        if style=="full":
            return title+"  "+simple+format %value+ " %s" %( unit)
        if style=="simple":
            return simple +format %value+ " %s" %( unit)
        if style=="title":
            return title
        if style=="value":
            return format %value
        return style


def test():
    """
    d'apres yves benoit p113
    """
    p=E5poutre()

    p.setH(200)
    p.setB(45)
    p.setClasseBois("c24")
    p.setKmod(0.9)
    p.setGammaM(1.3)
    p.setKsys(1.1)

#    M=13
    p.setMH(5)
    p.setN(11)
    p.setLfB(0)
    p.setLfH(3.)
    #p.setKcrit(1.)
    print("sigm,d  %0.2f MPa" %p.sigmaH())  
    print(" resistance calculee %0.1f MPa"  %p.fmd())

#    p.setLef(0.)
#    print p.Lef()
#    print(" sigma critique %0.1f MPa"  %p.sigmaCrit())
    print("elancement relatif de flexion %0.3f " %p.lambdaRm())
    print("kcrit", p.kcrit())
    print(" taux de travail %0.2f "  %p.tauxTravailCombine())    

def verifYB113():
    """
    d'apres yves benoit p113
    """
    p=E5poutre()

    p.setH(200)
    p.setB(50)
    p.setClasseBois("c24")
    p.setKmod(0.9)
    p.setGammaM(1.3)
    p.setKsys(1.1)

    q=0.887#kN/m!
    L=5 #m
    M=q*L*L/8.    # kNm
    print("moment",  M)
    p.setMH(M)
    p.setN(2.19)
    p.setLfB(1.667)
    p.setLfH(5.)
#    p.setKcrit(0.938)
    print("sigm,d  %0.2f MPa" %p.sigmaH())  
    print(" resistance calculee %0.1f MPa"  %p.fmd())

    p.setLef(5/3.)
    print(p.Lef())
    print(" sigma critique %0.1f MPa"  %p.sigmaCrit())
    print("elancement relatif de flexion %0.3f " %p.lambdaRm())
    print("kcrit", p.kcrit())
    print(" taux de travail %0.2f "  %p.tauxTravailCombine())    


def verifYB76():
    """
    d'apres yves benoit p76
    """
    p=E5poteau()

    p.setH(200)
    p.setB(75)
    p.setClasseBois("c24")
    p.setKmod(0.8)
    p.setGammaM(1.3)
    p.setKsys(1.1)

    q=1.463  #kN/m!
    L=4.5 #m
    M=q*L*L/8.    # kNm
    print("moment",  M)
    p.setMH(M)
    print("sigm,d  %0.1f MPa" %p.sigmaH())  
    print(" resistance calculee %0.1f MPa"  %p.fmd())

def verifYB42():
    """
    d'apres yves benoit p42
    """
    p=E5poteau()
    p.setLfB(3.2)
    p.setLfH(4.5)
    p.setM(1.)
    p.setH(150)
    p.setB(100)
    classe="c18"
    p.setClasseBois("c18")

    p.setN(20.)  # kN  /10 --> tonnes

    print(p.lambdaRB())
    print(p.kzB())
    print(p.kczB())
    print(p.sigmaC0d())
    print(p.fc0d())
    print("taux de travail", p.tauxTravail())

    print("Nmax", p.Nmax())

    print("taux de travail H", p.tauxTravailH())
    print("taux de travail B", p.tauxTravailB())
    print("Nmax H", p.NmaxH())
    print("Nmax B", p.NmaxB())

    return

def essai_old():
    """
    d'apres yves benoit p42
    """
    p=E5poutre()
    p.setL(3.2)
    p.setFacteurN(6)
    p.setM(1.)
    p.setH(150)
    p.setB(100)
    p.setAmembrures(1)
    p.setNmembrures(1.)
#    p.setL1(0.5)

    classe="c18"
    p.setClasseBois("c18")

    p.setN(40.)  # kN  /10 --> tonnes
    print("aire tot",  p.Atot())

    print(p.sigmaC0d())
    print(p.fc0d())
    print("taux de travail", p.tauxTravail())

    print("NmaxB", p.NmaxB())
    print("NmaxH", p.NmaxH())
    print("Nmax tot", p.NmaxTot())    
    print("------------------------")
    print("Nmax", p.Nmax())
    print(p.str_tauxTravailCompression())
    print(p.str_kczH())
    print(p.str_kczB())
    print(p.str_kczTot())
    print(p.str_lambdaRB())
    print(p.str_lambdaRH())
    print(p.str_lambdaRtot())
    return
    
def essai():
    """On va tester"""
    p=E5poutre()
    p.setL(4.5)
    p.setClasseBois("c24")
    p.setH(225)
    p.setHef(150)
    p.setB(75)
    p.setMH(3.7)
    p.setCH(3.656)
    p.setKmod(0.8)
    p.setGammaM(1.3)
    p.setKsys(1.1)
    p.setKcritH(1.)
    print ("Le DIC", p.dic())
    print("Contrainte de flexion calculee", p.sigmaH())
    print("Resisatnce de flexion calculee", p.fmd())
    print("Contrainte de cisaillement calculee", p.tauH())
    print("Resistance de cisaillement calculee", p.fvd())
    print("taux de travail", p.tauxTravail())
    print("taux de travail", p.tauxTravailFlexionH())
    print("taux de travail", p.tauxTravailCisaillement())
    print("taux de travail", p.tauxTravailCisaillementH())
    
if __name__=="__main__":

##    verifYB42()
##    verifYB76()
#    print "-----YB113------"
#    verifYB113()
   essai()
#    test()


