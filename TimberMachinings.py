# coding:utf8

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

import FreeCAD,Part,Draft,ArchComponent,DraftVecUtils,DraftGeomUtils,ArchCommands,ArchStructure
import TimberComponent
from FreeCAD import Vector
from pivy import coin
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

__title__="FreeCAD Timber Machinings"
__author__ = "Jonathan Wiedemann"
__url__ = "http://www.freecadweb.org"


## Timber Machining Cut
## A simple cut along a plane

def makeTimberMachiningCut(beam=None, face=None, name="TimberMachiningCut"):
    '''makeTimberMachiningCut(): creates a machining cut on a timber beam'''
    #p = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Timber")
    #if beam and face:
    obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython",name)
    obj.Label = translate("TimberMachiningCut",name)
    TimberMachiningCut(obj)
    if FreeCAD.GuiUp:
        ViewProviderTimberMachining(obj.ViewObject)
    obj.Structure = beam.Base
    obj.Face = face
    return obj
    #else:
    #    print(translate("Timber","TimberMachiningcut need a reference plane and a beam to cut"))


class _CommandTimberMachiningCut:
    "the Timber Beam command definition"
    def GetResources(self):
        return {'Pixmap'  :  __dir__ + '/icons/Timber_MachiningCut.svg',
                'MenuText': QtCore.QT_TRANSLATE_NOOP("Timber_MachiningCut","MachiningCut"),
                'Accel': "T, C",
                'ToolTip': QtCore.QT_TRANSLATE_NOOP("Timber_MachiningCut","Creates a cut machining to a Timber Beam object, relative to a plane (face)")}

    def IsActive(self):
        return len(FreeCADGui.Selection.getSelectionEx()) > 1

    def Activated(self):
        sel = FreeCADGui.Selection.getSelectionEx()
        beam = sel[0].Object
        beam = 'FreeCAD.ActiveDocument.' + beam.Name
        structure = sel[0].Object.Base
        structure = 'FreeCAD.ActiveDocument.' + structure.Name
        face = sel[1].Object, sel[1].SubElementNames[0]
        face = '[FreeCAD.ActiveDocument.' + face[0].Name + ',"' + face[1] + '"]'
        if beam and face :
            FreeCAD.ActiveDocument.openTransaction(str(translate("Timber","Create Cut Machining")))
            FreeCADGui.addModule("Timber")
            FreeCADGui.addModule("ArchComponent")
            FreeCADGui.doCommand('m = Timber.makeTimberMachiningCut(' + structure + ' , ' + face + ')')
            FreeCADGui.doCommand('ArchComponent.addToComponent(' + beam + ' , ' + 'm, "Subtractions")')
            FreeCAD.ActiveDocument.commitTransaction()
            FreeCAD.ActiveDocument.recompute()
        else :
            ArchCommands.printMessage(translate("Timber","TimberMachiningcut need a reference plane and a beam to cut"))
            print(translate("Timber","TimberMachiningcut need a reference plane and a beam to cut"))


class TimberMachiningCut:
    "The Cut Timber Machning object"
    def __init__(self,obj):
        #print("TimberMachiningCut Start Init")
        obj.addProperty("App::PropertyLinkSub","Face","Timber","The face's plane to make the cut")
        obj.addProperty("App::PropertyLink","Structure","Timber","The Timber Structure to cut")
        obj.Proxy = self
        #print("TimberMachiningCut End Init")

    def execute(self, obj):
        #print("TimberMachiningCut Start Execute")
        face = obj.Face
        faceObject = face[0]
        faceNumber = int(face[1][0][4:]) - 1
        face = faceObject.Shape.Faces[faceNumber]
        structure = obj.Structure
        cutVolume = ArchCommands.getCutVolume(face, structure.Shape)
        machining = cutVolume[2].common(beam.Shape)
        obj.Shape = machining
        #print("TimberMachiningCut End Execute")

    #def onChanged(self,obj,prop):
        #print("TimberMachiningCut Start OnChanged")
        #FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")
        #print("TimberMachiningCut End OnChanged")


class ViewProviderTimberMachining:
    "A View Provider for the MyFeaturePython object"

    def __init__(self, vobj):
        vobj.Proxy = self

    def getIcon(self):
        #import Arch_rc
        #return ":/icons/Arch_Structure_Tree.svg"
        return __dir__ + '/icons/Timber_MachiningCut.svg'

    def getDefaultDisplayMode(self):
        "'''Return the name of the default display mode. It must be defined in getDisplayModes.'''"
        return "Flat Lines"


## Timber MAchining Tenon
## A Parametric Tenon do a mortaise with subshape.

## A simple tenon machining along a plane

def makeTimberMachiningTenon(beam=None, face=None, name="TimberMachiningTenon"):
    '''makeTimberMachiningCut(): creates a machining tenon on a timber beam'''
    #p = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Timber")
    #if beam and face:
    obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython",name)
    obj.Label = translate("TimberMachiningTenon",name)
    TimberMachiningTenon(obj)
    if FreeCAD.GuiUp:
        ViewProviderTimberMachining(obj.ViewObject)
    obj.Structure = beam.Base
    obj.Face = face
    obj.Orientation = True
    obj.Length = 20.0
    obj.Width = 30.0
    obj.Height = 40.0
    #obj.Placement = obj.
    return obj
    #else:
    #    print(translate("Timber","TimberMachiningcut need a reference plane and a beam to cut"))


class _CommandTimberMachiningTenon:
    "the Timber Beam command definition"
    def GetResources(self):
        return {'Pixmap'  :  __dir__ + '/icons/Timber_MachiningCut.svg',
                'MenuText': QtCore.QT_TRANSLATE_NOOP("Timber_MachiningTenon","MachiningTenon"),
                'Accel': "T, C",
                'ToolTip': QtCore.QT_TRANSLATE_NOOP("Timber_MachiningTenon","Creates a tenon machining to a Timber Beam object, relative to a plane (face)")}

    def IsActive(self):
        return len(FreeCADGui.Selection.getSelectionEx()) > 1

    def Activated(self):
        sel = FreeCADGui.Selection.getSelectionEx()
        beam = sel[0].Object
        beam = 'FreeCAD.ActiveDocument.' + beam.Name
        #structure = sel[0].Object.Base
        #structure = 'FreeCAD.ActiveDocument.' + structure.Name
        face = sel[1].Object, sel[1].SubElementNames[0]
        face = '[FreeCAD.ActiveDocument.' + face[0].Name + ',"' + face[1] + '"]'
        if beam and face :
            FreeCAD.ActiveDocument.openTransaction(str(translate("Timber","Create Tenon Machining")))
            FreeCADGui.addModule("Timber")
            FreeCADGui.addModule("ArchComponent")
            FreeCADGui.doCommand('m = Timber.makeTimberMachiningTenon(' + beam + ' , ' + face + ')')
            FreeCADGui.doCommand('ArchComponent.removeFromComponent(' + beam + ' , ' + 'm)')
            #FreeCADGui.doCommand('ArchComponent.addToComponent(' + beam + ' , ' + 'm, "Subtractions")')
            FreeCAD.ActiveDocument.commitTransaction()
            FreeCAD.ActiveDocument.recompute()
        else :
            ArchCommands.printMessage(translate("Timber","TimberMachiningcut need a reference plane and a beam to cut"))
            print(translate("Timber","TimberMachiningcut need a reference plane and a beam to cut"))



class TimberMachiningTenon:
    "The Cut Timber Machning object"
    def __init__(self,obj):
        #print("TimberMachiningCut Start Init")
        obj.addProperty("App::PropertyLinkSub","Face","Timber","The face of female timber beam.")
        obj.addProperty("App::PropertyLink","Structure","Timber","The Timber Structure to cut.")
        obj.addProperty("App::PropertyBool","Orientation","Timber","Orientation of the tenon.")
        obj.addProperty("App::PropertyLength","Width","Timber","Width of the tenon.")
        obj.addProperty("App::PropertyLength","Length","Timber","Length of the tenon.")
        obj.addProperty("App::PropertyLength","Height","Timber","Height of the tenon.")
        obj.Orientation = True
        obj.Proxy = self
        #print("TimberMachiningCut End Init")

    def execute(self, obj):
        #print("TimberMachiningCut Start Execute")
        if len(obj.Face) == 2 :
            obj.Shape = self.createMachining( obj )
            obj.Placement = self.createPlacement(obj)

    def getBeamNodes(self, obj):
        #print("nodes", obj.Structure.Nodes )
        nodes = obj.Nodes
        edg = DraftGeomUtils.edg(nodes[0],nodes[1])
        edg.Placement = obj.Placement
        return edg

    def getFace(self, obj):
        face = obj.Face
        faceObject = face[0]
        faceNumber = int(face[1][0][4:]) - 1
        face = faceObject.Shape.Faces[faceNumber]
        return face

    def getZAx(self, obj):
        face = self.getFace(obj)
        ZAx = face.normalAt(0,0).negative().normalize()
        return ZAx 

    def getXAx(self, obj):
        edg = self.getBeamNodes(obj)
        XAx = DraftGeomUtils.vec(edg).normalize()
        return XAx
        
    def getRotation(self, obj):
        ZAx = self.getZAx( obj )
        XAx = self.getXAx( obj.Face[0].Base )
        YAx = ZAx.cross(XAx)
        ParaConfusion = 1e-8
        if YAx.Length < ParaConfusion*10.0:
            #failed, try some other X axis direction hint
            XAx = FreeCAD.Vector(0,0,1)
            YAx = ZAx.cross(XAx)
            if YAx.Length < ParaConfusion*10.0:
                #failed again. Now, we can tell, that local Z axis is along global
                # Z axis
                XAx = FreeCAD.Vector(1,0,0)
                YAx = ZAx.cross(XAx)
        YAx = YAx.normalize()
        XAx = YAx.cross(ZAx)
        m = FreeCAD.Matrix()
        m.A = list(XAx)+[0.0]+list(YAx)+[0.0]+list(ZAx)+[0.0]+[0.0]*3+[1.0]
        m.transpose()
        tmpplm = FreeCAD.Placement(m)
        ori = tmpplm.Rotation
        return ori

    def getIntersectionPoint(self, obj):
        edg = self.getBeamNodes(obj.Structure)
        face = self.getFace(obj)
        pt = edg.Curve.intersect(face.Surface)
        print("getIntersectionPoint : ", pt)
        return pt[0][0]

    def createPlacement(self, obj):
        base = self.getIntersectionPoint(obj)
        base = FreeCAD.Vector(base.X,base.Y,base.Z)
        rot = self.getRotation(obj)
        pl = FreeCAD.Placement()
        pl.Base = base
        pl.Rotation = rot
        print pl
        return pl

    def createTenon(self, obj):
        v1 = FreeCAD.Vector( obj.Length * -1 / 2.0 , obj.Width * -1 / 2.0 , 0.0 )
        v2 = FreeCAD.Vector( obj.Length / 2.0 , obj.Width * -1 / 2.0 , 0.0 )
        v3 = FreeCAD.Vector( obj.Length / 2.0 , obj.Width / 2.0 , 0.0 )
        v4 = FreeCAD.Vector( obj.Length * -1 / 2.0 , obj.Width / 2.0 , 0.0 )
        wireV = [ v1 , v2 , v3 , v4 , v1 ]
        wire = Part.makePolygon( wireV )
        face = Part.Face( wire )
        shape = face.extrude( FreeCAD.Vector( 0.0 , 0.0 , obj.Height ) )
        return shape

    def createBloc(self, obj):
        v1 = FreeCAD.Vector( -1000.0 , -1000.0 , 0.0 )
        v2 = FreeCAD.Vector( 1000.0 , -1000.0 , 0.0 )
        v3 = FreeCAD.Vector( 1000.0 , 1000.0 , 0.0 )
        v4 = FreeCAD.Vector( -1000.0 , 1000.0 , 0.0 )
        wireV = [ v1 , v2 , v3 , v4 , v1 ]
        wire = Part.makePolygon( wireV )
        face = Part.Face( wire )
        shape = face.extrude( FreeCAD.Vector( 0.0 , 0.0 , 2000.0 ) )
        return shape
        
    def createMachining(self, obj ):
        shape = self.createBloc(obj).cut(self.createTenon(obj))
        shape.Placement = self.createPlacement(obj)
        return shape

    #def onChanged(self,obj,prop):
        #print("TimberMachiningCut Start OnChanged")
        #FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")
        #print("TimberMachiningCut End OnChanged")

if FreeCAD.GuiUp:
    FreeCADGui.addCommand('Timber_MachiningTenon',_CommandTimberMachiningTenon())
    FreeCADGui.addCommand('Timber_MachiningCut',_CommandTimberMachiningCut())
