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

import FreeCAD,Arch, Draft,ArchComponent,DraftVecUtils,ArchCommands,ArchStructure
import TimberComponent
from FreeCAD import Vector
if FreeCAD.GuiUp:
    import FreeCADGui
    from PySide import QtCore, QtGui
    from DraftTools import translate
else:
    def translate(ctxt,txt):
        return txt
# waiting for Timber_rc and eventual FreeCAD integration
import os
__dir__ = os.path.dirname(__file__)

__title__="FreeCAD Timber Beam"
__author__ = "Jonathan Wiedemann"
__url__ = "http://www.freecadweb.org"

# Make some strings picked by the translator
if FreeCAD.GuiUp:
    QtCore.QT_TRANSLATE_NOOP("Arch","Wood")
    QtCore.QT_TRANSLATE_NOOP("Arch","Steel")

# Possible roles for timber elements
Roles = ["Beam","Column","Slab","Wall","Curtain Wall","Roof","Foundation","Pile","Tendon"]

def makeTimberBeam(length=None, width=None, height=None, name="TimberBeam"):
    '''makeTimberBeam([length],[width],[heigth],[name]): creates a
    timber beam element based on the given profile object and the given
    extrusion height. If no base object is given, you can also specify
    length and width for a cubic object.'''
    p = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Timber")
    obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython",name)
    obj.Label = translate("TimberBeam",name)
    _TimberBeam(obj)
    if FreeCAD.GuiUp:
        _ViewProviderTimberBeam(obj.ViewObject)
    if width:
        obj.Width = width
    else:
        obj.Width = p.GetFloat("BeamWidth",100.)
        #obj.Width = 80.
    if height:
        obj.Height = height
    else:
        obj.Height = p.GetFloat("BeamHeight",200.)
        #obj.Height = 220.
    if length:
        obj.Length = length
    else:
        obj.Length = p.GetFloat("BeamLength",1000.)
        #obj.Length = 3500.
    if height > length:
        obj.Role = "Column"
    else:
        obj.Role = "Beam"
    return obj


class _CommandTimberBeam:
    "the Timber Beam command definition"
    def GetResources(self):
        return {'Pixmap'  :  __dir__ + '/icons/Timber_Beam.svg',
                'MenuText': QtCore.QT_TRANSLATE_NOOP("Timber_Beam","TimberBeam"),
                'Accel': "T, B",
                'ToolTip': QtCore.QT_TRANSLATE_NOOP("Timber_Beam","Creates a structure object from scratch or from a selected object (sketch, wire, face or solid)")}

    def IsActive(self):
        return not FreeCAD.ActiveDocument is None

    def Activated(self):
        p = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Timber")
        self.Length = p.GetFloat("BeamLength",1000)
        self.Width = p.GetFloat("BeamWidth",100)
        self.Height = p.GetFloat("BeamHeight",100)
        #self.Profile = 0
        self.continueCmd = False
        self.DECIMALS = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Units").GetInt("Decimals",2)
        import DraftGui
        self.FORMAT = DraftGui.makeFormatSpec(self.DECIMALS,'Length')
        """
        sel = FreeCADGui.Selection.getSelection()
        if sel:
            st = Draft.getObjectsOfType(sel,"Structure")
            ax = Draft.getObjectsOfType(sel,"Axis")
            if ax:
                FreeCAD.ActiveDocument.openTransaction(str(translate("Arch","Create Structural System")))
                FreeCADGui.addModule("Arch")
                if st:
                    FreeCADGui.doCommand("Arch.makeStructuralSystem(" + ArchCommands.getStringList(st) + "," + ArchCommands.getStringList(ax) + ")")
                else:
                    FreeCADGui.doCommand("Arch.makeStructuralSystem(axes=" + ArchCommands.getStringList(ax) + ")")
                FreeCAD.ActiveDocument.commitTransaction()
                FreeCAD.ActiveDocument.recompute()
                return
            elif not(ax) and not(st):
                FreeCAD.ActiveDocument.openTransaction(str(translate("Arch","Create Structure")))
                FreeCADGui.addModule("Arch")
                for obj in sel:
                    FreeCADGui.doCommand("Arch.makeStructure(FreeCAD.ActiveDocument." + obj.Name + ")")
                FreeCAD.ActiveDocument.commitTransaction()
                FreeCAD.ActiveDocument.recompute()
                return
        """

        # interactive mode
        if hasattr(FreeCAD,"DraftWorkingPlane"):
            FreeCAD.DraftWorkingPlane.setup()
        import DraftTrackers
        self.points = []
        self.tracker = DraftTrackers.boxTracker()
        self.tracker.width(self.Width)
        self.tracker.height(self.Height)
        self.tracker.length(self.Length)
        self.tracker.on()
        FreeCADGui.Snapper.getPoint(callback=self.getPoint,movecallback=self.update,extradlg=self.taskbox())

    def getPoint(self,point=None,obj=None):
        "this function is called by the snapper when it has a 3D point"
        self.tracker.finalize()
        if point == None:
            return
        FreeCAD.ActiveDocument.openTransaction(str(translate("Timber","Create Timber Beam")))
        FreeCADGui.addModule("Timber")
        #if self.Profile:
        #    pr = Presets[self.Profile]
        #    FreeCADGui.doCommand('p = Arch.makeProfile('+str(pr[2])+','+str(pr[3])+','+str(pr[4])+','+str(pr[5])+')')
        #    if self.Length == pr[2]:
                # vertical
        #        FreeCADGui.doCommand('s = Arch.makeStructure(p,height='+str(self.Height)+')')
        #    else:
                # horizontal
        #        FreeCADGui.doCommand('s = Arch.makeStructure(p,height='+str(self.Length)+')')
        #        FreeCADGui.doCommand('s.Placement.Rotation = FreeCAD.Rotation(-0.5,0.5,-0.5,0.5)')
        #    FreeCADGui.doCommand('s.Profile = "'+pr[1]+'"')
        #else:
        FreeCADGui.doCommand('s = Timber.makeTimberBeam(length='+str(self.Length)+',width='+str(self.Width)+',height='+str(self.Height)+')')
        FreeCADGui.doCommand('s.Placement.Base = '+DraftVecUtils.toString(point))
        FreeCADGui.doCommand('s.Placement.Rotation=FreeCAD.DraftWorkingPlane.getRotation().Rotation')
        FreeCAD.ActiveDocument.commitTransaction()
        FreeCAD.ActiveDocument.recompute()
        if self.continueCmd:
            self.Activated()

    def taskbox(self):
        "sets up a taskbox widget"
        w = QtGui.QWidget()
        ui = FreeCADGui.UiLoader()
        w.setWindowTitle(translate("Arch","Structure options").decode("utf8"))
        grid = QtGui.QGridLayout(w)

        # presets box
        labelp = QtGui.QLabel(translate("Timber","Preset").decode("utf8"))
        valuep = QtGui.QComboBox()
        presetslist = TimberComponent.getPresetsList()
        #fpresets = [" "]
        #for p in Presets[1:]:
        #    fpresets.append(str(translate("Arch",p[0]))+" "+p[1]+" ("+str(p[2])+"x"+str(p[3])+"mm)")
        valuep.addItems(presetslist)
        grid.addWidget(labelp,0,0,1,1)
        grid.addWidget(valuep,0,1,1,1)

        # length
        label1 = QtGui.QLabel(translate("Timber","Length").decode("utf8"))
        self.vLength = ui.createWidget("Gui::InputField")
        self.vLength.setText(self.FORMAT % self.Length)
        grid.addWidget(label1,1,0,1,1)
        grid.addWidget(self.vLength,1,1,1,1)

        # width
        label2 = QtGui.QLabel(translate("Timber","Width").decode("utf8"))
        self.vWidth = ui.createWidget("Gui::InputField")
        self.vWidth.setText(self.FORMAT % self.Width)
        grid.addWidget(label2,2,0,1,1)
        grid.addWidget(self.vWidth,2,1,1,1)

        # height
        label3 = QtGui.QLabel(translate("Timber","Height").decode("utf8"))
        self.vHeight = ui.createWidget("Gui::InputField")
        self.vHeight.setText(self.FORMAT % self.Height)
        grid.addWidget(label3,3,0,1,1)
        grid.addWidget(self.vHeight,3,1,1,1)

        # horizontal button
        value5 = QtGui.QPushButton(translate("Arch","Rotate").decode("utf8"))
        grid.addWidget(value5,4,0,1,2)

        # continue button
        label4 = QtGui.QLabel(translate("Arch","Con&tinue").decode("utf8"))
        value4 = QtGui.QCheckBox()
        value4.setObjectName("ContinueCmd")
        value4.setLayoutDirection(QtCore.Qt.RightToLeft)
        label4.setBuddy(value4)
        if hasattr(FreeCADGui,"draftToolBar"):
            value4.setChecked(FreeCADGui.draftToolBar.continueMode)
            self.continueCmd = FreeCADGui.draftToolBar.continueMode
        grid.addWidget(label4,5,0,1,1)
        grid.addWidget(value4,5,1,1,1)

        QtCore.QObject.connect(valuep,QtCore.SIGNAL("currentIndexChanged(QString)"),self.setPreset)
        QtCore.QObject.connect(self.vLength,QtCore.SIGNAL("valueChanged(double)"),self.setLength)
        QtCore.QObject.connect(self.vWidth,QtCore.SIGNAL("valueChanged(double)"),self.setWidth)
        QtCore.QObject.connect(self.vHeight,QtCore.SIGNAL("valueChanged(double)"),self.setHeight)
        QtCore.QObject.connect(value4,QtCore.SIGNAL("stateChanged(int)"),self.setContinue)
        QtCore.QObject.connect(value5,QtCore.SIGNAL("pressed()"),self.rotate)
        return w

    def update(self,point,info):
        "this function is called by the Snapper when the mouse is moved"
        if FreeCADGui.Control.activeDialog():
            if self.Height >= self.Length:
                delta = Vector(0,0,self.Height/2)
            else:
                delta = Vector(self.Length/2,0,0)
            self.tracker.pos(point.add(delta))

    def setWidth(self,d):
        self.Width = d
        self.tracker.width(d)

    def setHeight(self,d):
        self.Height = d
        self.tracker.height(d)

    def setLength(self,d):
        self.Length = d
        self.tracker.length(d)

    def setContinue(self,i):
        self.continueCmd = bool(i)
        if hasattr(FreeCADGui,"draftToolBar"):
            FreeCADGui.draftToolBar.continueMode = bool(i)

    def setPreset(self,preset):
        #preset =
        presetdata = TimberComponent.getPresetData(preset)
        if presetdata:
            self.vWidth.setText(presetdata[1])
            self.vHeight.setText(presetdata[0])

    def rotate(self):
        l = self.Length
        w = self.Width
        h = self.Height
        self.vLength.setText(self.FORMAT % h)
        self.vHeight.setText(self.FORMAT % w)
        self.vWidth.setText(self.FORMAT % l)

class _TimberBeam(ArchStructure._Structure):
    "The Structure object"
    def __init__(self,obj):
        #print("TimberBeam Start Init")
        ArchStructure._Structure.__init__(self,obj)
        obj.addProperty("App::PropertyEnumeration","Preset","Timber","Preset parameters for this beam")
        obj.addProperty("App::PropertyBool","Moise","Timber","Type of machining at beam start")
        obj.addProperty("App::PropertyLink","Start","Timber","Type of machining at beam start")
        obj.addProperty("App::PropertyLink","End","Timber","Type of machining at beam end")
        obj.addProperty("App::PropertyLinkList","Machinings","Timber","All machinings of this beam")
        self.Type = "TimberBeam"
        obj.Preset = TimberComponent.getPresetsList()
        base = Arch.makeStructure()
        #base.MoveWithHost = True
        base.setEditorMode("Width", 1)
        base.setEditorMode("Height", 1)
        base.setEditorMode("Length", 1)
        base.setEditorMode("Placement", 1)
        ArchComponent.addToComponent(obj,base,"Base")
        #print("TimberBeam End Init")

    def execute(self, obj):
        #print("TimberBeam Start Execute")
        currentpreset = obj.Preset
        if currentpreset in TimberComponent.getPresetsList() :
            obj.Preset = currentpreset
        else:
            obj.Preset = "None"
            print(translate("Timber","This preset is not either in the presets list"))
        pl = obj.Base.Placement
        base = obj.Base.Shape.copy()
        base = TimberComponent.processSubShapes(obj,base,pl)
        obj.Shape = base
        #print("TimberBeam End Execute")

    def onChanged(self,obj,prop):
        #print("TimberBeam OnChanged")
        #FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")
        if prop == "Height":
            obj.Base.Height = obj.Height
        if prop == "Width":
            obj.Base.Width = obj.Width
        if prop == "Length":
            obj.Base.Length = obj.Length
        if prop == "Preset":
            presetslist = TimberComponent.getPresetsList()
            if obj.Preset != "None":
                if obj.Preset in presetslist :
                    presetData = TimberComponent.getPresetData(obj.Preset)
                    obj.Width = presetData[0]
                    obj.Height = presetData[1]
        if prop == "Placement":
            obj.Base.Placement = obj.Placement
    """
    def getPresetData(self, preset):
        #print("TimberBeam getpresetData")
        #preset = obj.Preset
        if preset != "None":
            idx = self.presetslist.index(preset) - 1
            presetfolder = "User parameter:BaseApp/Preferences/Mod/Timber/TimberBeamPresets/TBPreset" + str(idx)
            width = FreeCAD.ParamGet(presetfolder).GetString("Width")
            height = FreeCAD.ParamGet(presetfolder).GetString("Height")
        return [width, height]
    """

class _ViewProviderTimberBeam(ArchStructure._ViewProviderStructure):
    "The Structure ViewProvider object"
    def __init__(self,vobj):
        ArchStructure._ViewProviderStructure.__init__(self,vobj)
        vobj.addProperty("App::PropertyBool","ShowChamfer","Timber","If the nodes are visible or not").ShowNodes = False

    def getIcon(self):
        #import Arch_rc
        #return ":/icons/Arch_Structure_Tree.svg"
        return __dir__ + '/icons/Timber_Beam_Tree.svg'


    def setEdit(self,vobj,mode):
        taskd = TimberComponent.TimberBeamTaskPanel()
        taskd.obj = self.Object
        taskd.update()
        FreeCADGui.Control.showDialog(taskd)
        FreeCADGui.Selection.addSelection(self.Object)
        FreeCADGui.SendMsgToActiveView("ViewSelection")
        self.Object.Base.ViewObject.ShowNodes = True
        if self.Object.Base.Nodes:
            self.annoA = FreeCAD.ActiveDocument.addObject("App::AnnotationLabel","Start")
            self.annoA.BasePosition = self.Object.Base.Placement.multVec(self.Object.Base.Nodes[0])
            self.annoA.LabelText = "Start"
            self.annoB = FreeCAD.ActiveDocument.addObject("App::AnnotationLabel","End")
            self.annoB.BasePosition = self.Object.Base.Placement.multVec(self.Object.Base.Nodes[1])
            self.annoB.LabelText = "End"
        return True

    def unsetEdit(self,vobj,mode):
        self.Object.Base.ViewObject.ShowNodes = False
        FreeCAD.ActiveDocument.removeObject("Start")
        FreeCAD.ActiveDocument.removeObject("End")
        FreeCADGui.Control.closeDialog()
        return False

if FreeCAD.GuiUp:
    FreeCADGui.addCommand('Timber_Beam',_CommandTimberBeam())
