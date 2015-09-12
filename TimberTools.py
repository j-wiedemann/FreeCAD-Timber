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

__title__="FreeCAD Timber API"
__author__ = "Jonathan Wiedemann"
__url__ = "http://www.freecadweb.org"

import FreeCAD, FreeCADGui
import Arch, Draft, Part
import math, DraftGeomUtils, DraftVecUtils
from FreeCAD import Vector, Rotation, Placement, Console
from PySide import QtCore, QtGui

import os
__dir__ = os.path.dirname(__file__)

def makeTimberListing(display=True):
    tb = Listing()
    tb.makeTimberList()
    if display:
        tb.printTimberList()
    #return tb.getTimberList()

def getTagList():
    taglist = []
    for obj in FreeCAD.ActiveDocument.Objects :
        try :
            if obj.Tag:
                if taglist.count(str(obj.Tag)) == 0:
                    taglist.append(str(obj.Tag))
        except AttributeError:
            pass
    return taglist

def addTag(objects,tag):
    for obj in objects:
        try:
            obj.Tag = tag
        except AttributeError:
            print "Cet objet n'est pas tagable"

class _CommandListing:
        "the Timber Listing command definition"
        def GetResources(self):
           return {'Pixmap'  : __dir__ + '/icons/Timber_Listing.svg',
                    'MenuText': QtCore.QT_TRANSLATE_NOOP("Timber_Listing","Make listing"),
                    'ToolTip': QtCore.QT_TRANSLATE_NOOP("Timber_Listing","List objects")}

        def IsActive(self):
            return True

        def Activated(self):
            panel = _ListingTaskPanel()
            FreeCADGui.Control.showDialog(panel)

class _ListingTaskPanel:
    def __init__(self):
        self.form = QtGui.QWidget()
        self.form.setObjectName("TaskPanel")
        self.grid = QtGui.QGridLayout(self.form)
        self.grid.setObjectName("grid")
        self.title = QtGui.QLabel(self.form)
        self.grid.addWidget(self.title, 1, 0)
        self.taglistwidget = QtGui.QListWidget(self.form)
        self.grid.addWidget(self.taglistwidget, 2, 0)
        for tag in getTagList():
            self.taglistwidget.addItem(tag)
        self.infoText =  QtGui.QLabel(self.form)
        self.grid.addWidget(self.infoText, 3, 0)
        self.combobox = QtGui.QComboBox()
        self.combobox.setCurrentIndex(0)
        self.grid.addWidget(self.combobox, 3, 1)
        #self.linedit = QtGui.QLineEdit()
        #self.combobox.setCurrentIndex(0)
        #self.grid.addWidget(self.linedit, 3, 1)
        #self.taglistwidget.itemClicked.connect(self.setTag)
        #QtCore.QObject.connect(self.taglistwidget,QtCore.SIGNAL("itemClicked(item)"),self.setTag)
        #self.previewObj = FreeCAD.ActiveDocument.addObject("Part::Feature", str(translate("Arch", "PreviewCutVolume")))
        self.retranslateUi(self.form)
        #self.previewCutVolume(self.combobox.currentIndex())

    def setTag(self,item):
        #print "setText"
        self.linedit.setText(str(item.text()))

    def printTimberList(self):
        pass

    def accept(self):
        #FreeCAD.ActiveDocument.removeObject(self.previewObj.Name)
        #destination = str(self.combobox.currentItem.text())
        #tag = self.linedit.text()
        #print makeTimberListing(tag,destination)
        makeTimberListing()
        #FreeCAD.ActiveDocument.recompute()
        return True

    def reject(self):
        FreeCAD.Console.PrintMessage("Cancel Listing\n")
        return True

    def getStandardButtons(self):
        return int(QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Cancel)

    def retranslateUi(self, TaskPanel):
        TaskPanel.setWindowTitle(QtGui.QApplication.translate("Timber", "Listing", None, QtGui.QApplication.UnicodeUTF8))
        self.title.setText(QtGui.QApplication.translate("Arch", "Choose tag to list", None, QtGui.QApplication.UnicodeUTF8))
        self.infoText.setText(QtGui.QApplication.translate("Arch", "Destination", None, QtGui.QApplication.UnicodeUTF8))
        self.combobox.addItems([QtGui.QApplication.translate("Arch", "Window", None, QtGui.QApplication.UnicodeUTF8),
                                    QtGui.QApplication.translate("Arch", "Report View", None, QtGui.QApplication.UnicodeUTF8),
                                    QtGui.QApplication.translate("Arch", "Spreadsheet", None, QtGui.QApplication.UnicodeUTF8),
                                    QtGui.QApplication.translate("Arch", "CuttingStock .dat", None, QtGui.QApplication.UnicodeUTF8)])

class Listing:
    def __init__(self):
        doc = FreeCAD.ActiveDocument
        objs = FreeCAD.ActiveDocument.Objects
        self.objlist=[]
        #print("Il y a "+str(len(objs))+" objets dans le document.")
        for obj in objs:
            #a = obj.Name
            #print("Objet : " + str(a))
            #b = obj.Label
            if hasattr(obj,"Proxy"):
                #print(" - hasattr Proxy : ok")
                if hasattr(obj.Proxy,"Type"):
                    #print(" - hasattr Type : ok")
                    if FreeCADGui.ActiveDocument.getObject(obj.Name).Visibility :
                        #print(" - Visibility : True")
                        try:
                            if obj.Tag:
                                self.objlist.append(obj)
                        except AttributeError:
                            pass
                        #Listing()
                        #objectAnalyse(obj)
                    else:
                        #print(" - Visibility : False")
                        pass
                else:
                    #print(" - hasattr Type : no")
                    pass
            else:
                #print(" - hasattr Proxy : no")
                pass

        parms = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Units")
        self.timberlist=[]

    def makeTimberList(self):
        for tag in getTagList():
            timberlistbytag = []
            for obj in self.objlist:
                if obj.Tag == tag:
                    if obj.Proxy.Type in ["Structure", "Panel", "StructuralSystem", "Frame"]:
                        for solid in obj.Shape.Solids:
                            name = str("Aligned_"+str(obj.Name))
                            timber_part = self.shapeAnalyse(name,solid,)
                            timberlistbytag = self.addListe(timberlistbytag, timber_part[0], timber_part[1], timber_part[2])
                    else :
                        print("Type structurel non pris en charge")
            self.timberlist.append([tag,timberlistbytag])
        return self.timberlist

    def getTimberList():
        makeTimberList()
        return self.timberlist

    def printTimberList(self):
        for listbytag in self.timberlist:
            print("Tag : " + str(listbytag[0]))
            for section in listbytag[1]:
                print("Section : " + str(section[0])+"x"+str(section[1]))
                print("Qte    Longueur")
                for debit in section[2]:
                    print(str(debit[1])+"      "+str(debit[0]))
            print("")
        mySheet = FreeCAD.ActiveDocument.addObject('Spreadsheet::Sheet','Spreadsheet')
        mySheet.set('A1', 'Liste')
        n=1
        for listbytag in self.timberlist:
            n += 1
            mySheet.set('A'+str(n), str(listbytag[0]))
            #print("Tag : " + str(listbytag[0]))
            n += 1
            mySheet.set('A'+str(n), "Base : ")
            #mySheet.set('B'+str(n), str(section[0])+"x"+str(section[1]))
            mySheet.set('B'+str(n), "Hauteur : ")
            mySheet.set('C'+str(n), "Longueur : ")
            mySheet.set('D'+str(n), "Quantite : ")
            for section in listbytag[1]:
                partBase = str(section[0])
                partHeight = str(section[1])
                #print("Section : " + str(section[0])+"x"+str(section[1]))
                #print("Qte    Longueur")
                #n += 1
                #mySheet.set('A'+str(n), "Quantite")
                #mySheet.set('B'+str(n), "Longueur")
                for debit in section[2]:
                    n += 1
                    mySheet.set('A'+str(n), partBase)
                    mySheet.set('B'+str(n), partHeight)
                    mySheet.set('C'+str(n), str(debit[0]))
                    mySheet.set('D'+str(n), str(debit[1]))
                    #print(str(debit[1])+"      "+str(debit[0]))
            #print("")

    def addListe(self, listbytag, base, hauteur, longueur):
        #precision = parms.GetInt('Decimals')
        precision = 0
        base = round(base,precision)
        hauteur = round(hauteur,precision)
        longueur = round(longueur,precision)
        base = int(base)
        hauteur = int(hauteur)
        longueur = int(longueur)
        liste =  sorted([base, hauteur, longueur])
        base = liste[0]
        hauteur = liste[1]
        longueur = liste[2]
        #print "self.timberlist : ,",self.timberlist
        added = False
        if len(listbytag) > 0 :
            #print "self.timberlist est > 0"
            for x in listbytag :
                if x[0]==base and x[1]==hauteur :
                    #print "la section existe"
                    for qte in x[2]:
                        if qte[0] == longueur :
                            #print "la longueur existe"
                            #print "ajout une unite a longueur"
                            qte[1] += 1
                            added = True
                    if not added:
                        #print "ajout une longueur et une unite"
                        x[2].append([longueur,1])
                        added = True
            if not added:    #else:
                #print "la section existe pas"
                #print "ajout section , longueur, qte"
                listbytag.append([base, hauteur,[[longueur,1],],])
        else:
            #print "la liste est vide"
            #print "ajout section , longueur, qte"
            listbytag.append([base, hauteur,[[longueur,1],],])
        return listbytag
        #print "self.timberlist : ,",self.timberlist

    def getArea(self, face):
        return face.Area

    def getFacesMax(self, faces):
        faces = sorted(faces,key=self.getArea, reverse = True)
        facesMax = faces[0:4]
        return facesMax

    def getCoupleFacesEquerre(self, faces):
        listeCouple = []
        lenfaces = len(faces)
        faces.append(faces[0])
        for n in range(lenfaces):
            norm2 = faces[n+1].normalAt(0,0)
            norm1 = faces[n].normalAt(0,0)
            norm0 = faces[n-1].normalAt(0,0)
            if abs(round(math.degrees(DraftVecUtils.angle(norm1,norm0)))) == 90.:
                listeCouple.append([faces[n],faces[n-1]])
            if abs(round(math.degrees(DraftVecUtils.angle(norm1,norm2)))) == 90.:
                listeCouple.append([faces[n],faces[n+1]])
        return listeCouple

    def shapeAnalyse(self, name, shape):
        ## Create a new object with the shape of the current arch object
        ## His placment is set to 0,0,0
        obj = FreeCAD.ActiveDocument.addObject('Part::Feature',name)
        obj.Shape=shape
        obj.Placement.Base = FreeCAD.Vector(0.0,0.0,0.0)
        obj.Placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector(0.0,0.0,1.0),0.0)
        FreeCAD.ActiveDocument.recompute()
        ## Get the face to align with XY plane
        faces = obj.Shape.Faces
        facesMax = self.getFacesMax(faces)
        coupleEquerre = self.getCoupleFacesEquerre(facesMax)
        ## Get the normal of this face
        nv1 = coupleEquerre[0][0].normalAt(0,0)
        ## Get the goal normal vector
        zv = Vector(0,0,1)
        ## Find and apply a rotation to the object to align face
        pla = obj.Placement
        rot = pla.Rotation
        rot1 = Rotation(nv1, zv)
        newrot = rot.multiply(rot1)
        pla.Rotation = newrot
        ## Get the face to align with XY plane
        faces = obj.Shape.Faces
        facesMax = self.getFacesMax(faces)
        coupleEquerre = self.getCoupleFacesEquerre(facesMax)
        ## Get the longest edge from aligned face
        maxLength = 0.
        for e in coupleEquerre[0][0].Edges:
            if e.Length > maxLength:
                maxLength = e.Length
                edgeMax = e
        ## Get the angle between edge and X axis and rotate object
        vec = DraftGeomUtils.vec(edgeMax)
        vecZ = FreeCAD.Vector(vec[0],vec[1],0.0)
        pos2 = obj.Placement.Base
        rotZ = math.degrees(DraftVecUtils.angle(vecZ,FreeCAD.Vector(1.0,0.0,0.0),zv))
        Draft.rotate([obj],rotZ,pos2,axis=zv,copy=False)
        FreeCAD.ActiveDocument.recompute()
        ## Get the boundbox
        return [obj.Shape.BoundBox.YLength, obj.Shape.BoundBox.ZLength, obj.Shape.BoundBox.XLength]

class _CommandAddTag:
    "the Timber Repartition command definition"
    def GetResources(self):
       return {'Pixmap'  : __dir__ + '/icons/Timber_Tag.svg',
                'MenuText': QtCore.QT_TRANSLATE_NOOP("Timber_Tag","Add tag"),
                'ToolTip': QtCore.QT_TRANSLATE_NOOP("Timber_Tag","Add a tag to selected object(s)")}

    def IsActive(self):
        return True

    def Activated(self):
        panel = _AddTagTaskPanel()
        FreeCADGui.Control.showDialog(panel)

class _AddTagTaskPanel:
    def __init__(self):
        self.form = QtGui.QWidget()
        self.form.setObjectName("TaskPanel")
        self.grid = QtGui.QGridLayout(self.form)
        self.grid.setObjectName("grid")
        self.title = QtGui.QLabel(self.form)
        self.grid.addWidget(self.title, 1, 0)
        self.taglistwidget = QtGui.QListWidget(self.form)
        self.grid.addWidget(self.taglistwidget, 2, 0)
        for tag in getTagList():
            self.taglistwidget.addItem(tag)
        self.infoText =  QtGui.QLabel(self.form)
        self.grid.addWidget(self.infoText, 3, 0)
        self.linedit = QtGui.QLineEdit()
        #self.combobox.setCurrentIndex(0)
        self.grid.addWidget(self.linedit, 3, 1)
        self.taglistwidget.itemClicked.connect(self.setTag)
        #QtCore.QObject.connect(self.taglistwidget,QtCore.SIGNAL("itemClicked(item)"),self.setTag)
        #self.previewObj = FreeCAD.ActiveDocument.addObject("Part::Feature", str(translate("Arch", "PreviewCutVolume")))
        self.retranslateUi(self.form)
        #self.previewCutVolume(self.combobox.currentIndex())

    def setTag(self,item):
        print "setText"
        self.linedit.setText(str(item.text()))

    def accept(self):
        #FreeCAD.ActiveDocument.removeObject(self.previewObj.Name)
        tag = self.linedit.text()
        addTag(FreeCADGui.Selection.getSelection(),tag)
        FreeCAD.ActiveDocument.recompute()
        return True

    def reject(self):
        FreeCAD.Console.PrintMessage("Cancel Add Tag\n")
        return True

    def getStandardButtons(self):
        return int(QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Cancel)

    def retranslateUi(self, TaskPanel):
        TaskPanel.setWindowTitle(QtGui.QApplication.translate("Arch", "Add Tag", None, QtGui.QApplication.UnicodeUTF8))
        self.title.setText(QtGui.QApplication.translate("Arch", "Existing Tag", None, QtGui.QApplication.UnicodeUTF8))
        self.infoText.setText(QtGui.QApplication.translate("Arch", "Tag", None, QtGui.QApplication.UnicodeUTF8))

class _CommandRepartition:
    "the Timber Repartition command definition"
    def GetResources(self):
       return {'Pixmap'  : __dir__ + '/icons/Timber_Repartition.svg',
                'MenuText': QtCore.QT_TRANSLATE_NOOP("Timber_Repartition","Repartition"),
                'ToolTip': QtCore.QT_TRANSLATE_NOOP("Timber_Repartition","Make axis or Strucural system along a line")}

    def IsActive(self):
        return True

    def Activated(self):
        panel = _RepartitionTaskPanel()
        FreeCADGui.Control.showDialog(panel)

class _RepartitionTaskPanel:
    def __init__(self):
        self.title = QtGui.QLabel('Repartition')
        self.grid = QtGui.QGridLayout()
        self.grid.addWidget(self.title, 1, 0)

        self.longueurLabel = QtGui.QLabel('Longueur')

        self.dSBLongueur = QtGui.QDoubleSpinBox()
        self.dSBLongueur.setRange(0., 9999999.)
        self.sel = FreeCADGui.Selection.getSelection()
        if self.sel:
            self.longueur = self.sel[0].Shape.Length
            self.dSBLongueur.setValue(self.longueur)
        else:
            self.dSBLongueur.setValue(5000.)

        self.grid.addWidget(self.longueurLabel, 2, 0)
        self.grid.addWidget(self.dSBLongueur, 2, 1)

        self.ecartementLabel = QtGui.QLabel('Ecartement')
        self.ecartementDSB = QtGui.QDoubleSpinBox()
        self.ecartementDSB.setRange(0., 9999999.)
        self.ecartementDSB.setValue(500.)
        self.grid.addWidget(self.ecartementLabel, 3, 0)
        self.grid.addWidget(self.ecartementDSB, 3, 1)

        self.qteLabel = QtGui.QLabel('Quantite')
        self.qteSB = QtGui.QSpinBox()
        self.qteSB.setRange(0,99999)
        self.grid.addWidget(self.qteLabel, 4, 0)
        self.grid.addWidget(self.qteSB, 4, 1)

        self.infoText = QtGui.QLabel('Espace restant = ')
        self.grid.addWidget(self.infoText, 5, 0)
        self.combobox = QtGui.QComboBox()
        items = ["Debut","Fin","Divise"]
        self.combobox.addItems(items)
        self.combobox.setCurrentIndex(items.index("Fin"))
        self.grid.addWidget(self.combobox, 5, 1)

        self.debutLabel = QtGui.QLabel('Debut')
        self.grid.addWidget(self.debutLabel, 6, 0)

        self.debutRepartitionCB = QtGui.QCheckBox()
        self.debutRepartitionCB.setCheckState(QtCore.Qt.CheckState.Checked)
        self.grid.addWidget(self.debutRepartitionCB, 6, 1)

        self.decalageDebutLabel = QtGui.QLabel('Decalage')
        self.grid.addWidget(self.decalageDebutLabel, 7, 0)

        self.decalageDebutDSB = QtGui.QDoubleSpinBox()
        self.decalageDebutDSB.setRange(0., 9999999.)
        self.grid.addWidget(self.decalageDebutDSB, 7, 1)

        self.finLabel = QtGui.QLabel('Fin')
        self.grid.addWidget(self.finLabel, 8, 0)

        self.finRepartitionCB = QtGui.QCheckBox()
        self.finRepartitionCB.setCheckState(QtCore.Qt.CheckState.Checked)
        self.grid.addWidget(self.finRepartitionCB, 8, 1)

        self.decalageFinLabel = QtGui.QLabel('Decalage')
        self.grid.addWidget(self.decalageFinLabel, 9, 0)

        self.decalageFinDSB = QtGui.QDoubleSpinBox()
        self.decalageFinDSB.setRange(0., 9999999.)
        self.grid.addWidget(self.decalageFinDSB, 9, 1)

        groupBox = QtGui.QGroupBox()
        groupBox.setLayout(self.grid)
        self.form = groupBox

        QtCore.QObject.connect(self.dSBLongueur,QtCore.SIGNAL("valueChanged(double)"),self.changerLongueur)
        QtCore.QObject.connect(self.ecartementDSB,QtCore.SIGNAL("valueChanged(double)"),self.changerEcartement)
        QtCore.QObject.connect(self.qteSB,QtCore.SIGNAL("valueChanged(int)"),self.changerQte)
        QtCore.QObject.connect(self.combobox,QtCore.SIGNAL("currentIndexChanged(int)"),self.afficherResultats)
        self.changerLongueur()

    def recupererDonnees(self):
        self.sel = FreeCADGui.Selection.getSelection()
        if self.sel:
            self.longueur = self.sel[0].Shape.Length
        else:
            self.longueur = self.dSBLongueur.value()
        self.ecartementRegulier = self.ecartementDSB.value()
        self.qteEcartement = self.qteSB.value()

        self.objetDebut =  self.debutRepartitionCB.isChecked()
        self.decalageDebut = self.decalageDebutDSB.value()
        self.plEspaceRestant = self.combobox.currentIndex()
        self.objetFin = self.finRepartitionCB.isChecked()
        self.decalageFin = self.decalageFinDSB.value()

    def changerLongueur(self):
        self.recupererDonnees()
        self.qteEcartement = int(math.ceil(self.longueur/self.ecartementRegulier))
        self.afficherResultats()

    def changerEcartement(self):
        self.recupererDonnees()
        self.qteEcartement = int(math.ceil(self.longueur/self.ecartementRegulier))
        self.afficherResultats()

    def changerQte(self):
        self.recupererDonnees()
        self.ecartementRegulier = self.longueur/self.qteEcartement
        self.afficherResultats()

    def afficherResultats(self):
        self.dSBLongueur.blockSignals(True)
        self.dSBLongueur.setValue(self.longueur)
        self.dSBLongueur.blockSignals(False)

        self.ecartementDSB.blockSignals(True)
        self.ecartementDSB.setValue(self.ecartementRegulier)
        self.ecartementDSB.blockSignals(False)


        self.qteSB.blockSignals(True)
        self.qteSB.setValue(self.qteEcartement)
        self.qteSB.blockSignals(False)

        self.espaceRestant = self.longueur - (self.qteEcartement-1) * self.ecartementRegulier
        if round(self.espaceRestant,2) == round(self.ecartementRegulier,2):
            self.espaceRestant = 0.
        if self.combobox.currentIndex() == 2:
            self.infoText.setText( str('Espace restant = 2 x ') + str(round(self.espaceRestant/2,2)) + str(' mm') )
        else:
            self.infoText.setText( str('Espace restant = ') + str(round(self.espaceRestant,2)) + str(' mm') )

    def accept(self):
        self.recupererDonnees()
        distancesListe = []
        if self.objetDebut:
            distancesListe.append(self.decalageDebut)
        if self.plEspaceRestant == 0:
            distancesListe.append(self.espaceRestant)
        if self.plEspaceRestant == 1:
            distancesListe.append(self.ecartementRegulier-self.decalageDebut)
        if self.plEspaceRestant == 2:
            distancesListe.append(self.espaceRestant/2-self.decalageDebut)
        for i in range(self.qteEcartement-2):
            distancesListe.append(self.ecartementRegulier)
        if self.objetFin:
            if self.plEspaceRestant == 0:
                distancesListe.append(self.ecartementRegulier-self.decalageFin-self.decalageDebut)
            if self.plEspaceRestant == 1:
                distancesListe.append(self.espaceRestant-self.decalageFin)
            if self.plEspaceRestant == 2:
                distancesListe.append(self.ecartementRegulier)
                distancesListe.append((self.espaceRestant/2)-self.decalageFin)
        repartition = Arch.makeAxis(num=len(distancesListe), name="Repartition")
        repartition.Length = 1000.00
        repartition.Distances= distancesListe

        self.sel = FreeCADGui.Selection.getSelection()
        if self.sel:
            edges = DraftGeomUtils.sortEdges(self.sel[0].Shape.Wires[0].Edges)
            vec1 = edges[0].Vertexes[-1].Point.sub(edges[0].Vertexes[0].Point)
            point1 = edges[0].Vertexes[0].Point
            rot = math.degrees(DraftVecUtils.angle(vec1))*-1
            repartition.Placement = FreeCAD.Placement(FreeCAD.Vector(point1),FreeCAD.Rotation(FreeCAD.Vector(0.0,0.0,1.0),rot))
            FreeCAD.ActiveDocument.recompute()
        else:
            repartition.Placement = FreeCAD.Placement(FreeCAD.Vector(0.0,0.0,0.0),FreeCAD.Rotation(FreeCAD.Vector(0.0,0.0,1.0),0))

        m = FreeCADGui.getMainWindow()
        w = m.findChild(QtGui.QDockWidget,"PartsLibrary")
        if w:
            if w.isVisible():
                index = w.folder_view.selectedIndexes()[0]
                path = w.dirmodel.filePath(index)
                if path.lower().endswith(".stp") or path.lower().endswith(".step") or path.lower().endswith(".brep"):
                    objetRepartit = Part.show(Part.read(path))
                else:
                    objetRepartit = FreeCADGui.ActiveDocument.mergeProject(path)
                repartitionStructurel = Arch.makeStructuralSystem([FreeCAD.ActiveDocument.Objects[-1],],[repartition,], name="RepartitionStructurelle")
        return True

    def reject(self):
        return True

    def getStandardButtons(self):
        return int(QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Cancel)

if FreeCAD.GuiUp:
    FreeCADGui.addCommand('Timber_Repartition',_CommandRepartition())
    FreeCADGui.addCommand('Timber_Tag',_CommandAddTag())
    FreeCADGui.addCommand('Timber_Listing',_CommandListing())
