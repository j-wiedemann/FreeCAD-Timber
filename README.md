# FreeCAD Timber Workbench
A Timber module for FreeCAD

## Important Note
This workbench is no longer being maintained. Here's why:  
I started the development of the Timber workbench when I was working in the wood-frame and house construction industry.  
The idea was to address the following:

* generating wood assembly machining operations (tenon/mortar pair for example)
* make the BTL format compatible with FreeCAD `design2machine` a standard that some frame size centers can use.
* facilitate the design and modeling of wood-frame and structural walls
* use the model to extract cut lists and drawings or send them to the center of the framework pruning

I no longer work in this field.  
I've never been able to make sure that I can make parametric assembly torques without breaking the DAG.  
I didn't dig any deeper to read the BTL format especially for the placement of objects: 
https://forum.freecadweb.org/viewtopic.php?f=22&t=6766=22&t=6766

IMO, the only interesting feature is the Timber listing tool which generates a cut list of rectangular 
and arranged parts by section, length, and quantity.

If someone is interested in continuing this work, by all means, feel free. Open an issue or mention something
in the feeback forum thread below. The idea for keeping this workbench in the Addon Manager is to serve as an
example project whose code can be referenced or used for other tools.

## Usage

I started the development of the Timber workbench when I was working in the wood frame and house construction industry.
The idea was in bulk from:

* generate wood assembly machining operations (tenon/mortar pair for example)
* Make the BTL format compatible with FreeCAD design2machine a standard that some frame size centers can use.
* facilitate the design and modeling of wood-frame and structural walls
* use the model to extract cut lists and drawings or send them to the center of the framework pruning

I no longer work in this field.
I've never been able to make sure that I can make parametric assembly torques without breaking the DAG.
I didn't dig any deeper to read the BTL format especially for the placement of objects: https://forum.freecadweb.org/viewtopic.php?f=22&t=6766=22&t=6766

The only interesting feature in my opinion is the Timber listing tool which generates a cut list of rectangular and arranged parts by section, length and quantity.

What do you think of that? Are there any users of this workbench ? Geek: 

You can install this workbennch via https://github.com/FreeCAD/FreeCAD-addons#installing


## Screenshots 
![image](https://user-images.githubusercontent.com/4140247/59509848-3228bf00-8e80-11e9-8be9-aa457fde7e63.png)


## Installation
You can install this workbench via the FreeCAD built-in [Addon Manager](https://github.com/FreeCAD/FreeCAD-addons#1-builtin-addon-manager)


## Feedback
Give feedback to the author via the dedicated FreeCAD [thread discussing Timber workbench](https://forum.freecadweb.org/viewtopic.php?t=12559)  


## Known Limitations
* Not Python3 compatible yet  
* Not actively in development or maintained.  


## Author
[@wood-galaxy](https://github.com/wood-galaxy)


## License
GNU General Public License v2.0