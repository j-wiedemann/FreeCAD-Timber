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

c14=[14.,  8., 0.4, 16., 2.0, 1.7, 7., 4.7, 0.23, 0.44, 290., 350.]
c16=[16., 10., 0.5, 17., 2.2, 1.8, 8., 5.4, 0.27, 0.5, 310., 370.]
c18=[18., 11., 0.5, 18., 2.2, 2.0, 9., 6.0, 0.3, 0.56, 320., 380.]
c22=[22., 13., 0.5, 20., 2.4, 2.4, 10., 6.7, 0.33, 0.63, 340., 410.]
c24=[24., 14., 0.5, 21., 2.5, 2.5, 11., 7.4, 0.37, 0.69, 350., 420.]
c27=[27., 16., 0.6, 22., 2.6, 2.8, 11.5, 7.7, 0.38, 0.72, 370., 450.]
c30=[30., 18., 0.6, 23., 2.7, 3.0, 12., 8.0, 0.40, 0.75, 380., 460.]
c35=[35., 21., 0.6, 25., 2.8, 3.4, 13., 8.7, 0.43, 0.81, 400., 480.]
c40=[40., 24., 0.6, 26., 2.9, 3.8, 14., 9.4, 0.47, 0.88, 420., 500.]


d30=[30., 18., 0.6, 23., 8.0, 3.0, 10., 8.0, 0.64, 0.60, 530., 640.]
d35=[35., 21., 0.6, 25., 8.4, 3.4, 10., 8.7, 0.69, 0.65, 560., 670.]
d40=[40., 24., 0.6, 26., 8.8, 3.8, 11., 9.4, 0.75, 0.70, 590., 700.]
d50=[50., 30., 0.6, 29., 9.7, 4.6, 14., 11.8, 0.93, 0.88, 650., 780.]
d60=[60., 36., 0.6, 32., 10.5, 5.3, 17., 14.3, 1.13, 1.06, 700., 840.]
d70=[70., 42., 0.6, 34., 13.5, 6.0, 20., 16.8, 1.33, 1.25, 900., 1080.]

caraBois={
                    "c14": c14, 
                    "c16":c16, 
                    "c18":c18,
                   "c22":c22, 
                  "c24":c24,  
                  "c27":c27, 
                  "c30":c30, 
                  "c35":c35, 
                  "c40":c40, 
                  "d30":d30, 
                  "d40":d40, 
                  "d50":d50, 
                  "d60":d60, 
                  "d70":d70
                    
                    }



# boulons
ABOULONS={
         10:79., 
         12:113., 
         14:154., 
         16:201., 
         18: 254., 
         20: 314., 
         22: 380.,
         24:452., 
         27:573., 
         30:707., 
         33:855.
         }

ASBOULONS={
         10:58., 
         12:84., 
         14:115., 
         16:156., 
         18:192., 
         20:245., 
         22:303.,
         24:352., 
         27:459., 
         30:560., 
         33:693.
         }

ALPHAVBOULONS={
        "4,6":0.5, 
        "4,8":0.6, 
        "5,6":0.5, 
        "5,8":0.6, 
        "6,8":0.6, 
        "8,8":0.5, 
        "10,8":0.6
               }
FUBOULONS={
        "4,6":400., 
        "4,8":400., 
        "5,6":500., 
        "5,8":500., 
        "6,8":600., 
        "8,8":800., 
        "10,8":1000.
               }


FUACIER={
         "S235":360., 
         "S275":430., 
         "S355":510., 
         "S450":550.
         }
         
DMTETEHEXA={
            10:17.2, 
            12:19.3, 
            14:22.5, 
            16:25.8, 
            18:28, 
            20:32.2, 
            22:35.4, 
            24:38.7, 
            27:44,
           30:49.4 
            }

class E5cara():
    
    def __init__(self, classe="C14"):
        
        self.classe=classe
        
        
    def dicMat(self):
        """
                return {
        "E":self.E0mean()*1000.,   E en MPa
        "NU":0.3, 
        "RHO":self.rho()/1000  rho en tonnes/m*  --> forces en kN
        }
        
        """
        
        return {
        "E":self.E0mean()*1000., 
        "NU":0.3, 
        "RHO":self.rho()/1000
        }
    def dicMatL(self):
        """
                return {
        "E":self.E0mean()*1000.,   E en MPa
        "NU":0.3, 
        "RHO":self.rho()/1000  rho en tonnes/m*  --> forces en kN
        }
        
        """
        
        return {
        "E":self.E0mean()*1000., 
        "NU":0.3, 
        "RHO":0.
        }
    def rho(self):
        """
        Masse volumique caracteristique (kg/m3)
        """
        return caraBois[self.classe][10]
    def str_rho(self, style="full", format="%.0f"):
        title="Masse volumique caracteristique"
        simple= "rho="
        value=self.rho()
        unit=self.rhoU()
        return self.str_(style, format, title, simple, value, unit) 
    def rhoU(self):
        return "kg/m3"
    def rhom(self):
        """
        Masse volumique moyenne (kg/m3)
        """
        return caraBois[self.classe][11]
    
    def str_rhom(self, style="full", format="%.0f"):
        title="Masse volumique moyenne"
        simple= "rhom="
        value=self.rhom()
        unit=self.rhomU()
        return self.str_(style, format, title, simple, value, unit) 
    
    
    def rhomU(self):
        return "kg/m3"
        

        
    def fmk(self):
        """
        contrainte de flexion MPa
        """
        return caraBois[self.classe][0]
    def str_fmk(self, style="full", format="%.0f"):
        title="Contrainte caracteristique de flexion"
        simple= "fmk="
        value=self.fmk()
        unit="MPa"
        return self.str_(style, format, title, simple, value, unit) 
        
    def ft0k(self):
        """
        contrainte de traction axiale MPa
        """
        return caraBois[self.classe][1]
    def str_ft0k(self, style="full", format="%.0f"):
        title="Contrainte caracteristique de traction axiale"
        simple= "ft0k="
        value=self.ft0k()
        unit="MPa"
        return self.str_(style, format, title, simple, value, unit) 
        
    def ft90k(self):
        """
        contrainte de traction perpendiculaire MPa
        """
        return caraBois[self.classe][2]
    def str_ft90k(self, style="full", format="%.0f"):
        title="Contrainte caracteristique de traction perpendiculaire"
        simple= "ft90k="
        value=self.ft90k()
        unit="MPa"
        return self.str_(style, format, title, simple, value, unit) 
        
    def fc0k(self):
        """
        contrainte de compression axiale
        """
        return caraBois[self.classe][3]     
    def str_fc0k(self, style="full", format="%.0f"):
        title="Contrainte caracteristique de compression axiale"
        simple= "fc0k="
        value=self.fc0k()
        unit="MPa"
        return self.str_(style, format, title, simple, value, unit) 
     
    def fc90k(self):
        """
        contrainte de compression perpendiculaire
        """
        return caraBois[self.classe][4]     
    def str_fc90k(self, style="full", format="%.0f"):
        title="Contrainte caracteristique de compression perpendiculaire"
        simple= "fc90k="
        value=self.fc90k()
        unit="MPa"
        return self.str_(style, format, title, simple, value, unit) 
    def fvk(self):
        """
        contrainte de cisaillement
        """
        return caraBois[self.classe][5]   
    def str_fvk(self, style="full", format="%.0f"):
        title="Contrainte caracteristique de cisaillement"
        simple= "fvk="
        value=self.fvk()
        unit="MPa"
        return self.str_(style, format, title, simple, value, unit) 
  
    def E0mean(self):
        """
        module moyen axial 
        """
        return caraBois[self.classe][6]
    def str_E0mean(self, style="full", format="%.0f"):
        title="Module moyen axial"
        simple= "E0mean="
        value=self.E0mean()
        unit="1000MPa"
        return self.str_(style, format, title, simple, value, unit) 
    def E0meanMPa(self):
        """
        module moyen axial 
        """
        return caraBois[self.classe][6]*1000.
    def str_E0meanMPa(self, style="full", format="%.0f"):
        title="Module moyen axial"
        simple= "E0mean="
        value=self.E0meanMPa()
        unit="MPa"
        return self.str_(style, format, title, simple, value, unit) 
        
    def E05(self):
        """
        module axial au 5ieme pourcentile
        """
        return caraBois[self.classe][7]
    def str_E05(self, style="full", format="%.0f"):
        title="Module moyen au 5ième pourcentile"
        simple= "E05="
        value=self.E05()
        unit="1000MPa"
        return self.str_(style, format, title, simple, value, unit) 
        
    def E05MPa(self):
        """
        module axial au 5ieme pourcentile
        """
        return caraBois[self.classe][7]*1000.
    def str_E05MPa(self, style="full", format="%.0f"):
        title="Module moyen au 5ième pourcentile"
        simple= "E05="
        value=self.E05MPa()
        unit="MPa"
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
        
PSI={}
# facteur d'accompagnement Benoit p14
PSI["TITRE"]=["action variable d'accompagnement", 
                        "combinaison accidentelle (incendie)", 
                        "fluage et combinaison accidentelle", 
                        "action variable"]
PSI["A"]=[0.7, 0.5, 0.3, "habitations residentielles"]
PSI["B"]=[0.7, 0.5, 0.3, "bureaux"]
PSI["C"]=[0.7, 0.7, 0.6, "lieux de reunion"]
PSI["D"]=[0.7, 0.7, 0.6, "commerces"]
PSI["E"]=[1., 0.9,  0.8, "stockages"]
PSI["H"]=[0., 0., 0., "toits"]
PSI["S1"]=[0.7,0.5, 0.2, "neige altitude>1000m" ]
PSI["S0"]=[0.5,0.3, 0., "neige altitude<=1000m" ]
PSI["W"]=[0.6,0.2, 0., "vent" ]

GAMMA={}
GAMMA["Gsup"]=1.35
GAMMA["Ginf"]=1.
GAMMA["GinfEQU"]=0.9
GAMMA["Q"]=1.5




