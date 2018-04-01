# -*- coding: utf-8 -*-
# FreeCAD init script of the Timber module
# (c) 2015 Jonathan Wiedemann

#***************************************************************************
#*   (c) Jonathan Wiedemann (jonatan@wiedemann.fr) 2015                    *
#*                                                                         *
#*   This file is part of the FreeCAD CAx development system.              *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   FreeCAD is distributed in the hope that it will be useful,            *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Lesser General Public License for more details.                   *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with FreeCAD; if not, write to the Free Software        *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#*   Jonathan Wiedemann 2015                                               *
#***************************************************************************/

import FreeCAD
import FreeCADGui
import Ui_EC5Dialog
from PyQt4 import QtCore, QtGui
#import oshE5data
import oshpoutre

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class EC5_Poutre():
    def IsActive(self):
      return bool(FreeCADGui.Selection.getSelectionEx())

    def Activated(self):
        app = QtGui.qApp
        FCmw = app.activeWindow() # the active qt window, = the freecad window since we are inside it
        self.myNewFreeCADWidget = QtGui.QDockWidget() # create a new dckwidget
        self.myNewFreeCADWidget.ui = Ui_EC5Dialog.Ui_Dialog() # load the Ui script
        self.myNewFreeCADWidget.ui.setupUi(self.myNewFreeCADWidget) # setup the ui
        FCmw.addDockWidget(QtCore.Qt.RightDockWidgetArea,self.myNewFreeCADWidget) # add the widget to the main window
        QtCore.QObject.connect(self.myNewFreeCADWidget.ui.pushButton,QtCore.SIGNAL("pressed()"),self.calculs_travail_flexion)
        QtCore.QObject.connect(self.myNewFreeCADWidget.ui.pushButton_2,QtCore.SIGNAL("pressed()"),self.calculs_travail_cisaillement)
        QtCore.QObject.connect(self.myNewFreeCADWidget.ui.pushButton_3,QtCore.SIGNAL("pressed()"),self.GetArchElementDatas)


        #panel = AddEC5Task()
        #FreeCADGui.Control.showDialog(panel)
        #AddEC5Task()

    def GetResources(self):
      return {'Pixmap': 'python', 'MenuText': 'EC5 Poutre', 'ToolTip': 'EC5 Poutre'}


    def GetArchElementDatas(self):
        self.GetHeight()
        self.GetWidth()
        self.GetLength()

    """Récupère la valeur de la hauteur de l'élément Arch Structure selectionné"""
    def GetHeight(self):
        selection = FreeCADGui.Selection.getSelection()
        if len(selection) == 1 :
            o = selection[0]
            if hasattr(o,"Proxy"):
                if hasattr(o.Proxy,"Type"):
                    if o.Proxy.Type == "Structure":
                        self.myNewFreeCADWidget.ui.doubleSpinBox_9.setValue(o.Height)
        elif len(selection) == 1 :
            print("Veuillez ne selectionner qu'un seul element")

    """Récupère la valeur de la base (largeur) de l'élément Arch Structure selectionné"""
    def GetWidth(self):
        selection = FreeCADGui.Selection.getSelection()
        if len(selection) == 1 :
            o = selection[0]
            if hasattr(o,"Proxy"):
                if hasattr(o.Proxy,"Type"):
                    if o.Proxy.Type == "Structure":
                        self.myNewFreeCADWidget.ui.doubleSpinBox_8.setValue(o.Width)
        elif len(selection) == 1 :
            print("Veuillez ne selectionner qu'un seul element")

    """Récupère la valeur de la longueur de l'élément Arch Structure selectionné"""
    def GetLength(self):
        selection = FreeCADGui.Selection.getSelection()
        if len(selection) == 1 :
            o = selection[0]
            if hasattr(o,"Proxy"):
                if hasattr(o.Proxy,"Type"):
                    if o.Proxy.Type == "Structure":
                        self.myNewFreeCADWidget.ui.doubleSpinBox_7.setValue(o.Length)
        elif len(selection) == 1 :
            print("Veuillez ne selectionner qu'un seul element")

    def calculs_travail_flexion(self):
        gui = self.myNewFreeCADWidget.ui
        p = oshpoutre.E5poutre()
        if gui.comboBox_2.currentText() == "Bois Massif" :
            p.setGammaM(1.3)
        else :
            p.setGammaM(1.25)
        classeBois = str(gui.comboBox.currentText())
        p.setClasseBois(classeBois.lower())
        longueur = gui.doubleSpinBox_7.value()
        p.setL(longueur)
        hauteur = gui.doubleSpinBox_9.value()
        p.setH(hauteur)
        hauteur_efficace = gui.doubleSpinBox_10.value()
        base = gui.doubleSpinBox_8.value()
        p.setB(base)
        moment_max = gui.doubleSpinBox.value()
        p.setMH(moment_max)
        kmod_associe = gui.doubleSpinBox_3.value()
        p.setKmod(kmod_associe)
        ksys_associe = gui.doubleSpinBox_5.value()
        p.setKsys(ksys_associe)
        kcrit_associe = gui.doubleSpinBox_4.value()
        p.setKcritH(kcrit_associe)
        sigmaMd = round(p.sigmaH(), 3)
        print(sigmaMd)
        fmd = round(p.fmd(), 3)
        print(fmd)
        tauxTravail = round(p.tauxTravailFlexionH()*100, 0)
        print(tauxTravail)
        results_flexion = ("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Cantarell\'; font-size:9pt; font-weight:400; font-style:normal;\">\n")
        string_aaa = "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Contrainte de flexion induite : {0} MPa</p>\n"
        results_flexion += string_aaa.format(sigmaMd)
        string_aaa = "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Resistance de calcul en flexion : {0} MPa</p>\n"
        results_flexion += string_aaa.format(fmd)
        string_aaa = "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Taux de travail : {0} %</p>\n"
        results_flexion += string_aaa.format(tauxTravail)
        if tauxTravail < 100 :
            results_flexion += "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#00ff00;\">Ok</span></p></body></html>"
        else :
            results_flexion += "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ff0000;\">NOK</span></p></body></html>"
#        results_flexion.format(sigmaMd, fmd, tauxTravail)

        gui.textBrowser_2.setHtml(QtGui.QApplication.translate("Dialog", results_flexion, None, QtGui.QApplication.UnicodeUTF8))
        """
        print ("Le DIC", p.dic())
        print("Contrainte de flexion calculee", p.sigmaH())
        print("Resisatnce de flexion calculee", p.fmd())
        print("Contrainte de cisaillement calculee", p.tauH())
        print("Resistance de cisaillement calculee", p.fvd())
        print("taux de travail", p.tauxTravail())
        print("taux de travail", p.tauxTravailFlexionH())
        print("taux de travail", p.tauxTravailCisaillement())
        print("taux de travail", p.tauxTravailCisaillementH())
        """

    def calculs_travail_cisaillement(self):
        gui = self.myNewFreeCADWidget.ui
        p = oshpoutre.E5poutre()
        if gui.comboBox_2.currentText() == "Bois Massif" :
            p.setGammaM(1.3)
        else :
            p.setGammaM(1.25)
        classeBois = str(gui.comboBox.currentText())
        p.setClasseBois(classeBois.lower())
        longueur = gui.doubleSpinBox_7.value()
        p.setL(longueur)
        hauteur = gui.doubleSpinBox_9.value()
        p.setH(hauteur)
        hauteur_efficace = gui.doubleSpinBox_10.value()
        p.setHef(hauteur_efficace)
        base = gui.doubleSpinBox_8.value()
        p.setB(base)
        tranchant_max = gui.doubleSpinBox_2.value()
        p.setCH(tranchant_max)
        kmod_associe = gui.doubleSpinBox_6.value()
        p.setKmod(kmod_associe)
        tauh = round(p.tauH(), 3)
        print(tauh)
        fvd = round(p.fvd(),3)
        print(fvd)
        tauxTravail = round(p.tauxTravailCisaillement()*100, 0)
        print(tauxTravail)
        results_flexion = ("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Cantarell\'; font-size:9pt; font-weight:400; font-style:normal;\">\n")
        string_aaa = "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Contrainte de cisaillement induite : {0} MPa</p>\n"
        results_flexion += string_aaa.format(tauh)
        string_aaa = "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Resistance de calcul au cisaillement : {0} MPa</p>\n"
        results_flexion += string_aaa.format(fvd)
        string_aaa = "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Taux de travail : {0} %</p>\n"
        results_flexion += string_aaa.format(tauxTravail)
        if tauxTravail < 100 :
            results_flexion += "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#00ff00;\">Ok</span></p></body></html>"
        else :
            results_flexion += "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ff0000;\">NOK</span></p></body></html>"
#        results_flexion.format(sigmaMd, fmd, tauxTravail)

        gui.textBrowser.setHtml(QtGui.QApplication.translate("Dialog", results_flexion, None, QtGui.QApplication.UnicodeUTF8))

FreeCADGui.addCommand('EC5_Poutre', EC5_Poutre())

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_EC5Dialog.Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
