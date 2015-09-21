#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2015                                                    *
#*   Jonathan Wiedemann <contact@freecad-france.com                        *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************

import FreeCAD,Draft,ArchComponent,DraftVecUtils,ArchCommands
from FreeCAD import Vector
if FreeCAD.GuiUp:
    import FreeCADGui
    import DraftGui
    from PySide import QtCore, QtGui
    from DraftTools import translate
else:
    def translate(ctxt,txt):
        return txt

__title__="FreeCAD Timber Component"
__author__ = "Jonathan Wiedemann"
__url__ = "http://www.freecadweb.org"

# Make some strings picked by the translator
if FreeCAD.GuiUp:
    QtCore.QT_TRANSLATE_NOOP("Arch","Wood")
    QtCore.QT_TRANSLATE_NOOP("Arch","Steel")

def getExtremityTypesList():
    return ExtremityTypes

def getPresetsList():
    presets = ["None"]
    n=0
    paramfolder = "User parameter:BaseApp/Preferences/Mod/Timber/TimberBeamPresets/TBPreset"
    presetname = FreeCAD.ParamGet(paramfolder+str(n)).GetString("Name")
    if presetname :
        while presetname :
            presetfolder = paramfolder+str(n)
            presetname = FreeCAD.ParamGet(presetfolder).GetString("Name")
            if presetname :
                presets.append(presetname)
                n += 1
            else:
                FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Timber/TimberBeamPresets").RemGroup("TBPreset"+str(n))
    else:
        FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Timber/TimberBeamPresets").RemGroup("TBPreset"+str(n))
    return presets

def getPresetData(preset):
    #print("TimberBeam getpresetData")
    #preset = obj.Preset
    if preset != "None":
        presetslist = getPresetsList()
        idx = presetslist.index(preset) - 1
        presetfolder = "User parameter:BaseApp/Preferences/Mod/Timber/TimberBeamPresets/TBPreset" + str(idx)
        width = FreeCAD.ParamGet(presetfolder).GetString("Width")
        height = FreeCAD.ParamGet(presetfolder).GetString("Height")
    return [width, height]

class TimberBeamTaskPanel:
    '''The Timber Beam TaskPanel'''
    def __init__(self):
        # the panel has a tree widget that contains categories
        # for the subcomponents, such as additions, subtractions.
        # the categories are shown only if they are not empty.
        #print("TimberBeamTaskPanel Start init")

        self.obj = None
        self.attribs = ["Base","Additions","Subtractions","Objects","Components","Axes","Fixtures","Machinings"]
        self.form = QtGui.QWidget()
        self.form.setObjectName("TaskPanel")

        # tab1 : Components
        self.tab1 = QtGui.QWidget()

        self.grid = QtGui.QGridLayout(self.tab1)
        self.grid.setObjectName("grid")
        self.title = QtGui.QLabel(self.tab1)
        self.grid.addWidget(self.title, 0, 0, 1, 2)

        # tree
        self.tree = QtGui.QTreeWidget(self.tab1)
        self.grid.addWidget(self.tree, 1, 0, 1, 2)
        self.tree.setColumnCount(1)
        self.tree.header().hide()

        # buttons
        self.addButton = QtGui.QPushButton(self.tab1)
        self.addButton.setObjectName("addButton")
        self.addButton.setIcon(QtGui.QIcon(":/icons/Arch_Add.svg"))
        self.grid.addWidget(self.addButton, 3, 0, 1, 1)
        self.addButton.setEnabled(False)

        self.delButton = QtGui.QPushButton(self.tab1)
        self.delButton.setObjectName("delButton")
        self.delButton.setIcon(QtGui.QIcon(":/icons/Arch_Remove.svg"))
        self.grid.addWidget(self.delButton, 3, 1, 1, 1)
        self.delButton.setEnabled(False)

        QtCore.QObject.connect(self.addButton, QtCore.SIGNAL("clicked()"), self.addElement)
        QtCore.QObject.connect(self.delButton, QtCore.SIGNAL("clicked()"), self.removeElement)
        QtCore.QObject.connect(self.tree, QtCore.SIGNAL("itemClicked(QTreeWidgetItem*,int)"), self.check)
        QtCore.QObject.connect(self.tree, QtCore.SIGNAL("itemDoubleClicked(QTreeWidgetItem *,int)"), self.editObject)

        # tab2 : Timber
        #wood quality, section, preset, list machining
        self.tab2 = QtGui.QWidget()

        self.gridTimber = QtGui.QGridLayout(self.tab2)

        self.presetsL = QtGui.QLabel(self.tab2)
        self.gridTimber.addWidget(self.presetsL, 0, 0, 1, 1)

        self.presetsCBB = QtGui.QComboBox(self.tab2)
        self.gridTimber.addWidget(self.presetsCBB, 0, 1, 1, 3)

        self.presetRenameBT = QtGui.QPushButton(self.tab2)
        self.presetRenameBT.setToolTip(translate("Timber", "Renamme the current preset"))
        self.gridTimber.addWidget(self.presetRenameBT, 1, 1, 1, 1)

        self.presetNewBT = QtGui.QPushButton(self.tab2)
        self.presetNewBT.setToolTip(translate("Timber", "Create a new preset based on the current parameters"))
        self.gridTimber.addWidget(self.presetNewBT, 1, 2, 1, 1)

        self.presetSaveBT = QtGui.QPushButton(self.tab2)
        self.presetSaveBT.setToolTip(translate("Timber", "Save change on the current preset"))
        self.gridTimber.addWidget(self.presetSaveBT, 1, 3, 1, 1)

        ui = FreeCADGui.UiLoader()
        self.widthL = QtGui.QLabel(self.tab2)
        self.gridTimber.addWidget(self.widthL, 3, 0, 1, 1)
        self.vWidth = ui.createWidget("Gui::InputField")
        self.gridTimber.addWidget(self.vWidth, 3, 1, 1, 3)
        self.heightL = QtGui.QLabel(self.tab2)
        self.gridTimber.addWidget(self.heightL, 4, 0, 1, 1)
        self.vHeight = ui.createWidget("Gui::InputField")
        self.gridTimber.addWidget(self.vHeight, 4, 1, 1, 3)

        QtCore.QObject.connect(self.presetRenameBT, QtCore.SIGNAL("clicked()"), self.renamePreset)
        QtCore.QObject.connect(self.presetNewBT, QtCore.SIGNAL("clicked()"), self.newPreset)
        QtCore.QObject.connect(self.presetSaveBT, QtCore.SIGNAL("clicked()"), self.savePreset)
        QtCore.QObject.connect(self.vHeight,QtCore.SIGNAL("valueChanged(double)"),self.setHeight)
        QtCore.QObject.connect(self.vWidth,QtCore.SIGNAL("valueChanged(double)"),self.setWidth)
        QtCore.QObject.connect(self.presetsCBB,QtCore.SIGNAL("activated(int)"),self.setPreset)
        QtCore.QObject.connect(self.presetsCBB,QtCore.SIGNAL("editTextChanged(QString)"),self.getCBBText)

        # tab3 : Beam Start
        # Machining at beam start
        # Type of machining and parameters, preset, store presets
        self.tab3 = QtGui.QWidget()

        # tab4 : Beam End
        # Machining at beam end
        # Type of machining and parameters, preset, store presets
        self.tab4 = QtGui.QWidget()

        self.gridtabs = QtGui.QGridLayout(self.form)
        self.tabwidget = QtGui.QTabWidget(self.form)
        self.gridtabs.addWidget(self.tabwidget,0,0)
        self.tabwidget.addTab(self.tab1, "Component")
        self.tabwidget.addTab(self.tab2, "Timber")
        self.tabwidget.addTab(self.tab3, "Start")
        self.tabwidget.addTab(self.tab4, "End")
        #self.tabwidget.addTab(1, "IFC")
        self.applyrename = False
        self.applynew = False
        self.update()
        #print("TimberBeamTaskPanel End Init")

    def isAllowedAlterSelection(self):
        return True

    def isAllowedAlterView(self):
        return True

    def getStandardButtons(self):
        return int(QtGui.QDialogButtonBox.Ok)

    def check(self,wid,col):
        if not wid.parent():
            self.delButton.setEnabled(False)
            if self.obj:
                sel = FreeCADGui.Selection.getSelection()
                if sel:
                    if not(self.obj in sel):
                        self.addButton.setEnabled(True)
        else:
            self.delButton.setEnabled(True)
            self.addButton.setEnabled(False)

    def getIcon(self,obj):
        if hasattr(obj.ViewObject,"Proxy"):
            return QtGui.QIcon(obj.ViewObject.Proxy.getIcon())
        elif obj.isDerivedFrom("Sketcher::SketchObject"):
            return QtGui.QIcon(":/icons/Sketcher_Sketch.svg")
        else:
            return QtGui.QIcon(":/icons/Tree_Part.svg")

    def update(self):
        #print("TimberTaskPanel update")
        'fills the treewidget'
        self.tree.clear()
        dirIcon = QtGui.QApplication.style().standardIcon(QtGui.QStyle.SP_DirIcon)
        for a in self.attribs:
            setattr(self,"tree"+a,QtGui.QTreeWidgetItem(self.tree))
            c = getattr(self,"tree"+a)
            c.setIcon(0,dirIcon)
            c.ChildIndicatorPolicy = 2
            if self.obj:
                if not hasattr(self.obj,a):
                           c.setHidden(True)
            else:
                c.setHidden(True)
        if self.obj:
            for attrib in self.attribs:
                if hasattr(self.obj,attrib):
                    Oattrib = getattr(self.obj,attrib)
                    Tattrib = getattr(self,"tree"+attrib)
                    if Oattrib:
                        if attrib == "Base":
                            Oattrib = [Oattrib]
                        for o in Oattrib:
                            item = QtGui.QTreeWidgetItem()
                            item.setText(0,o.Name)
                            item.setIcon(0,self.getIcon(o))
                            Tattrib.addChild(item)
                        self.tree.expandItem(Tattrib)
            self.DECIMALS = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Units").GetInt("Decimals",2)
            self.FORMAT = DraftGui.makeFormatSpec(self.DECIMALS,'Length')
            self.vWidth.setText(self.FORMAT % self.obj.Width)
            self.vHeight.setText(self.FORMAT % self.obj.Height)

            "fill the presets combobox"
            presetslist = getPresetsList()
            presetname = self.obj.Preset
            idx = presetslist.index(presetname)
            self.presetsCBB.clear()
            self.presetsCBB.addItems(presetslist)
            self.presetsCBB.setCurrentIndex(idx)
            if idx < 1:
                self.presetRenameBT.setEnabled(False)
                self.presetSaveBT.setEnabled(False)
            else:
                self.presetRenameBT.setEnabled(True)
                self.presetSaveBT.setEnabled(True)

        self.retranslateUi(self.form)

    def addElement(self):
        it = self.tree.currentItem()
        if it:
            mod = None
            for a in self.attribs:
                if it.text(0) == getattr(self,"tree"+a).text(0):
                    mod = a
            if mod == "Machinings":
                print "TODO : Add Machinings"
            else :
                for o in FreeCADGui.Selection.getSelection():
                    ArchComponent.addToComponent(self.obj,o,mod)
        self.update()

    def removeElement(self):
        it = self.tree.currentItem()
        if it:
            comp = FreeCAD.ActiveDocument.getObject(str(it.text(0)))
            ArchComponent.removeFromComponent(self.obj,comp)
        self.update()

    def accept(self):
        FreeCAD.ActiveDocument.recompute()
        FreeCADGui.ActiveDocument.resetEdit()
        return True

    def editObject(self,wid,col):
        if wid.parent():
            obj = FreeCAD.ActiveDocument.getObject(str(wid.text(0)))
            if obj:
                self.obj.ViewObject.Transparency = 80
                self.obj.ViewObject.Selectable = False
                obj.ViewObject.show()
                self.accept()
                if obj.isDerivedFrom("Sketcher::SketchObject"):
                    FreeCADGui.activateWorkbench("SketcherWorkbench")
                FreeCAD.ArchObserver = ArchSelectionObserver(self.obj,obj)
                FreeCADGui.Selection.addObserver(FreeCAD.ArchObserver)
                FreeCADGui.ActiveDocument.setEdit(obj.Name,0)

    def setHeight(self, d):
        self.obj.Height = d

    def setWidth(self, d):
        self.obj.Width = d

    def getCBBText(self, arg):
        self.newpresetname = arg

    def setPreset(self, idx):
        self.newpresetname = self.presetsCBB.currentText()
        if idx > 0 :
            presetfolder = "User parameter:BaseApp/Preferences/Mod/Timber/TimberBeamPresets/TBPreset" + str(idx - 1)
            newpreset = FreeCAD.ParamGet(presetfolder).GetString('Name')
        else:
            newpreset = "None"
        self.obj.Preset = newpreset
        FreeCAD.ActiveDocument.recompute()
        self.update()

    def renamePreset(self):
        if self.applyrename :
            self.presetsCBB.setEditable(False)
            self.presetNewBT.setEnabled(True)
            self.presetSaveBT.setEnabled(True)
            newname = self.newpresetname
            idx = self.presetsCBB.currentIndex() - 1
            presetfolder = "User parameter:BaseApp/Preferences/Mod/Timber/TimberBeamPresets/TBPreset" + str(idx)
            FreeCAD.ParamGet(presetfolder).SetString('Name', newname)
            FreeCAD.ActiveDocument.recompute()
            self.obj.Preset = str(newname)
            self.applyrename = False
            self.update()
        else:
            self.presetsCBB.setEditable(True)
            self.presetNewBT.setEnabled(False)
            self.presetSaveBT.setEnabled(False)
            self.applyrename = True
            self.retranslateUi(self.form)

    def newPreset(self):
        if self.applynew:
            self.presetsCBB.setEditable(False)
            self.presetRenameBT.setEnabled(True)
            self.presetSaveBT.setEnabled(True)
            idx = len(getPresetsList()) - 1
            self.savePreset(True,idx)
            self.applynew = False
        else:
            self.presetsCBB.setEditable(True)
            idx = len(getPresetsList())
            self.presetsCBB.addItem(translate("Timber","New Preset"))
            self.presetsCBB.setCurrentIndex(idx)
            self.presetRenameBT.setEnabled(False)
            self.presetSaveBT.setEnabled(False)
            self.applynew = True
            self.retranslateUi(self.form)

    def savePreset(self, new=False, newidx=0):
        height = self.obj.Height.UserString
        width = self.obj.Width.UserString
        newname = self.newpresetname
        if new :
            idx = newidx
        else :
            idx = self.presetsCBB.currentIndex() - 1
        presetfolder = "User parameter:BaseApp/Preferences/Mod/Timber/TimberBeamPresets/TBPreset" + str(idx)
        FreeCAD.ParamGet(presetfolder).SetString('Name', newname)
        FreeCAD.ParamGet(presetfolder).SetString('Width', width)
        FreeCAD.ParamGet(presetfolder).SetString('Height', height)
        FreeCAD.ActiveDocument.recompute()
        self.obj.Preset = str(newname)
        self.update()

    def retranslateUi(self, TaskPanel):
        TaskPanel.setWindowTitle(QtGui.QApplication.translate("Timber", "Timber", None, QtGui.QApplication.UnicodeUTF8))
        self.delButton.setText(QtGui.QApplication.translate("Arch", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.addButton.setText(QtGui.QApplication.translate("Arch", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.title.setText(QtGui.QApplication.translate("Arch", "Components of this object", None, QtGui.QApplication.UnicodeUTF8))
        self.treeBase.setText(0,QtGui.QApplication.translate("Arch", "Base component", None, QtGui.QApplication.UnicodeUTF8))
        self.treeAdditions.setText(0,QtGui.QApplication.translate("Arch", "Additions", None, QtGui.QApplication.UnicodeUTF8))
        self.treeSubtractions.setText(0,QtGui.QApplication.translate("Arch", "Subtractions", None, QtGui.QApplication.UnicodeUTF8))
        self.treeObjects.setText(0,QtGui.QApplication.translate("Arch", "Objects", None, QtGui.QApplication.UnicodeUTF8))
        self.treeAxes.setText(0,QtGui.QApplication.translate("Arch", "Axes", None, QtGui.QApplication.UnicodeUTF8))
        self.treeComponents.setText(0,QtGui.QApplication.translate("Arch", "Components", None, QtGui.QApplication.UnicodeUTF8))
        self.treeFixtures.setText(0,QtGui.QApplication.translate("Arch", "Fixtures", None, QtGui.QApplication.UnicodeUTF8))
        self.treeMachinings.setText(0,QtGui.QApplication.translate("Timber", "Machinings", None, QtGui.QApplication.UnicodeUTF8))

        applybutton = QtGui.QApplication.translate("Timber", "Apply", None, QtGui.QApplication.UnicodeUTF8)
        self.widthL.setText(QtGui.QApplication.translate("Timber", "Width", None, QtGui.QApplication.UnicodeUTF8))
        self.heightL.setText(QtGui.QApplication.translate("Timber", "Height", None, QtGui.QApplication.UnicodeUTF8))
        self.presetsL.setText(QtGui.QApplication.translate("Timber", "Presets", None, QtGui.QApplication.UnicodeUTF8))
        if self.applyrename :
            self.presetRenameBT.setText(applybutton)
        else:
            self.presetRenameBT.setText(QtGui.QApplication.translate("Timber", "Rename", None, QtGui.QApplication.UnicodeUTF8))
        if self.applynew :
            self.presetNewBT.setText(applybutton)
        else:
            self.presetNewBT.setText(QtGui.QApplication.translate("Timber", "New", None, QtGui.QApplication.UnicodeUTF8))
        self.presetSaveBT.setText(QtGui.QApplication.translate("Timber", "Save", None, QtGui.QApplication.UnicodeUTF8))

def processSubShapes(obj,base,placement=None):
    "Adds additions and subtractions to a base shape"
    #print("processSubShapes Start")
    import Draft,Part

    if placement:
        if placement.isNull():
            placement = None
        else:
            placement = FreeCAD.Placement(placement)
            placement = placement.inverse()

    # treat additions
    for o in obj.Additions:

        if not base:
            if o.isDerivedFrom("Part::Feature"):
                base = o.Shape
        else:
            if base.isNull():
                if o.isDerivedFrom("Part::Feature"):
                    base = o.Shape
            else:
                # special case, both walls with coinciding endpoints
                import ArchWall
                js = ArchWall.mergeShapes(o,obj)
                if js:
                    add = js.cut(base)
                    if placement:
                        add.Placement = add.Placement.multiply(placement)
                    base = base.fuse(add)

                elif (Draft.getType(o) == "Window") or (Draft.isClone(o,"Window",True)):
                    f = o.Proxy.getSubVolume(o)
                    if f:
                        if base.Solids and f.Solids:
                            if placement:
                                f.Placement = f.Placement.multiply(placement)
                            base = base.cut(f)

                elif o.isDerivedFrom("Part::Feature"):
                    if o.Shape:
                        if not o.Shape.isNull():
                            if o.Shape.Solids:
                                s = o.Shape.copy()
                                if placement:
                                    s.Placement = s.Placement.multiply(placement)
                                if base:
                                    if base.Solids:
                                        try:
                                            base.Placement = FreeCAD.Placement()
                                            base = base.fuse(s)
                                        except Part.OCCError:
                                            print "Arch: unable to fuse object ",obj.Name, " with ", o.Name
                                else:
                                    base = s

    # treat subtractions
    for o in obj.Subtractions:

        if base:
            if base.isNull():
                base = None

        if base:
            if (Draft.getType(o) == "Window") or (Draft.isClone(o,"Window",True)):
                    # windows can be additions or subtractions, treated the same way
                    f = o.Proxy.getSubVolume(o)
                    if f:
                        if base.Solids and f.Solids:
                            if placement:
                                f.Placement = f.Placement.multiply(placement)
                            base = base.cut(f)

            elif (Draft.getType(o) == "Roof") or (Draft.isClone(o,"Roof")):
                # roofs define their own special subtraction volume
                f = o.Proxy.getSubVolume(o)
                if f:
                    if base.Solids and f.Solids:
                        base = base.cut(f)

            elif o.isDerivedFrom("Part::Feature"):
                if o.Shape:
                    if not o.Shape.isNull():
                        if o.Shape.Solids and base.Solids:
                                s = o.Shape.copy()
                                if placement:
                                    s.Placement = s.Placement.multiply(placement)
                                try:
                                    base.Placement = FreeCAD.Placement()
                                    base = base.cut(s)
                                except Part.OCCError:
                                    print "Arch: unable to cut object ",o.Name, " from ", obj.Name

    #print("processSubShapes End")
    return base

class TimberBeamComponent:
    "The default Timber Component object"
    def __init__(self, obj):
        pass
