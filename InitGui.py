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



class TimberWorkbench ( Workbench ):
    "Timber workbench object"
    Icon = """
/* XPM */
static char * infologo_xpm[] = {
"16 16 2 1",
" 	c None",
".	c #E55303",
"                ",
"       .        ",
"      ...       ",
"     . . .      ",
"    .  .  .     ",
"   . . . . .    ",
"  .   ...   .   ",
" .     .     .  ",
"............... ",
" .  .     .  .  ",
" . .       . .  ",
" ..         ..  ",
" .           .  ",
" .           .  ",
" .           .  ",
" .           .  "};
"""
    MenuText = "Timber"
    ToolTip = "Timber workbench"

    def Initialize(self) :
        import Timber
        #self.appendToolbar('TimberTools',['Timber_Tag','Timber_List'])
        #self.appendMenu('TimberTools',['Timber_Tag','Timber_List'])
        self.appendToolbar('TimberTools',['Timber_Repartition','Timber_Tag'])
        self.appendToolbar('TimberListing',['Timber_Listing'])
        self.appendToolbar('TimberBeam',['Timber_Beam'])
        self.appendToolbar('TimberMachinings',['Timber_MachiningCut'])
        self.appendMenu('TimberTools',['Timber_Repartition','Timber_Tag'])
        self.appendMenu('TimberListing',['Timber_Listing'])
        self.appendMenu('TimberBeam',['Timber_Beam'])
        self.appendMenu('TimberBeam',['Timber_MachiningCut'])
        FreeCADGui.addIconPath(":/icons")
        Log ('Loading Timber module... done\n')

    def GetClassName(self):
        #return "InfoGui::Workbench"
        return "Gui::PythonWorkbench"

Gui.addWorkbench(TimberWorkbench())

# add import/export types
#FreeCAD.addImportType("Wood Working Machine (*.btl)","importBTL")
#FreeCAD.addExportType("Wood Working Machine (*.btl)","exportBTL")
