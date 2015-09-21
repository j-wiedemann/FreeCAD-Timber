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

import FreeCAD,Draft,ArchComponent,DraftVecUtils,ArchCommands,ArchStructure
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

def makeTimberMachiningCut(beam=None, face=None, name="TimberMachiningCut"):
    '''makeTimberMachiningCut(): creates a machining cut on a timber beam'''
    #p = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Timber")
    if beam and face:
        obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython",name)
        obj.Label = translate("TimberMachiningCut",name)
        TimberMachiningCut(obj)
        if FreeCAD.GuiUp:
            ViewProviderTimberMachiningCut(obj.ViewObject)
        obj.Beam = beam
        obj.CutPlane = face
        return obj
    else:
        print(translate("Timber","TimberMachiningcut need a reference plane and a beam to cut"))

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
        FreeCAD.ActiveDocument.openTransaction(str(translate("Timber","Create Cut Machining")))
        FreeCADGui.addModule("Timber")
        FreeCADGui.addModule("ArchComponent")
        FreeCADGui.doCommand('m = Timber.makeTimberMachiningCut(' + structure + ' , ' + face + ')')
        FreeCADGui.doCommand('ArchComponent.addToComponent(' + beam + ' , ' + 'm, "Subtractions")')
        FreeCAD.ActiveDocument.commitTransaction()
        FreeCAD.ActiveDocument.recompute()



class TimberMachiningCut:
    "The Cut Timber Machning object"
    def __init__(self,obj):
        #print("TimberMachiningCut Start Init")
        obj.addProperty("App::PropertyLinkSub","CutPlane","Timber","The face's plane to make the cut")
        obj.addProperty("App::PropertyLink","Beam","Timber","The Timber Beam to cut")
        obj.Proxy = self
        #print("TimberMachiningCut End Init")

    def execute(self, obj):
        #print("TimberMachiningCut Start Execute")
        cutplane = obj.CutPlane
        faceobject = cutplane[0]
        facenumber = int(cutplane[1][0][4:]) - 1
        face = faceobject.Shape.Faces[facenumber]
        beam = obj.Beam
        cutVolume = ArchCommands.getCutVolume(face, beam.Shape)
        machining = cutVolume[2].common(beam.Shape)
        obj.Shape = machining
        #print("TimberMachiningCut End Execute")

    #def onChanged(self,obj,prop):
        #print("TimberMachiningCut Start OnChanged")
        #FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")
        #print("TimberMachiningCut End OnChanged")

class ViewProviderTimberMachiningCut:
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


if FreeCAD.GuiUp:
    FreeCADGui.addCommand('Timber_MachiningCut',_CommandTimberMachiningCut())
