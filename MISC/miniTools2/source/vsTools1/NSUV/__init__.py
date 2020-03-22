"""
    Package initiation for Nightshade UV editor (NSUV) v1.6.1
    
    NSUV offers extended utility to Maya's native UV Texture Editor
    Made by Martin (Nightshade) Dahlin - martin.dahlin@live.com - martin.dahlin.net
        
    Also included is this fantastic python script CalcUVStats by Guido Neumann.
    His site can be found here: http://blog.kernphase.com/
        
    Special thanks to:
    NaughtyNathan, Robert (rgkovach123) and David Johnson from CGTalk for all the coding help.
    And thanks to Anton Palmqvist, Malcolm Andrieshyn, and my former coworker Alexander Lilja 
    for all the feedback, bug reports and feature ideas.
        
    Script downloaded from Creative Crash
"""

## Import

import pymel.core as pm
 

## Version check

# Determine version, then import correct panel and toolbar replacements
version = pm.about(version=True)
if version.startswith("2015"):
    pm.mel.source("texturePanel_NSUV_2015.mel")
    pm.mel.source("textureWindowCreateToolBar_NSUV_2015.mel")

elif version.startswith("2014"):
    pm.mel.source("texturePanel_NSUV.mel")
    pm.mel.source("textureWindowCreateToolBar_NSUV_2014.mel")

elif version.startswith("2013"):
    pm.mel.source("texturePanel_NSUV.mel")
    pm.mel.source("textureWindowCreateToolBar_NSUV.mel")

elif version.startswith("2012"):
    pm.mel.source("texturePanel_NSUV.mel")
    pm.mel.source("textureWindowCreateToolBar_NSUV.mel")

else:
    print("Support for Maya 2011 and below has been discontinued!")

    
## Create optVars
   
if "textureWindowShaderFacesMode" not in pm.env.optionVars:
    pm.optionVar["textureWindowShaderFacesMode"] = 0

if "displayEditorImage" not in pm.env.optionVars:
    pm.optionVar["displayEditorImage"] = 0
    
    
# Frame optVars   
if "frameManipOptVar" not in pm.env.optionVars: 
    pm.optionVar["frameManipOptVar"] = False
    
if "frameAlignOptVar" not in pm.env.optionVars: 
    pm.optionVar["frameAlignOptVar"] = False
    
if "frameSetOptVar" not in pm.env.optionVars: 
    pm.optionVar["frameSetOptVar"] = False
    
if "frameMappingOptVar" not in pm.env.optionVars: 
    pm.optionVar["frameMappingOptVar"] = False
    
if "frameTDOptVar" not in pm.env.optionVars: 
    pm.optionVar["frameTDOptVar"] = False
    
if "btnGrpToolsOptVar" not in pm.env.optionVars: 
    pm.optionVar["btnGrpToolsOptVar"] = True
    
    


# Manipulator optVars

if "absToggleOptVar" not in pm.env.optionVars:
    pm.optionVar["absToggleOptVar"] = False

if "compSpaceOptVar" not in pm.env.optionVars:
    pm.optionVar["compSpaceOptVar"] = 0

if "manipAmtOptVar" not in pm.env.optionVars:
    pm.optionVar["manipAmtOptVar"] = 1.0

if "manipCoordsOptVar" not in pm.env.optionVars:
    pm.optionVar["manipCoordsOptVar"] = [0.0, 0.0]

if "manipVarAOptVar" not in pm.env.optionVars:
    pm.optionVar["manipVarAOptVar"] = 0.0

if "manipVarBOptVar" not in pm.env.optionVars:
    pm.optionVar["manipVarBOptVar"] = 0.0

# if "manipVarCOptVar" not in pm.env.optionVars:
#    pm.optionVar["manipVarCOptVar"] = 0.0


# Match UVs optVar

if "matchTolOptVar" not in pm.env.optionVars:
    pm.optionVar["matchTolOptVar"] = 0.005


# Orient Shells optVar

if "orientShellsOptVar" not in pm.env.optionVars:
    pm.optionVar["orientShellsOptVar"] = 2  

    
# Projection optVars

if "mapAutoMethodOptVar" not in pm.env.optionVars:
    pm.optionVar["mapAutoMethodOptVar"] = 1
    
if "mapAutoMSMenuOptVar" not in pm.env.optionVars:
    pm.optionVar["mapAutoMSMenuOptVar"] = 6
    
if "mapAutoMS1RadGrpOptVar" not in pm.env.optionVars:
    pm.optionVar["mapAutoMS1RadGrpOptVar"] = 1
    
if "mapAutoMS2RadGrpOptVar" not in pm.env.optionVars:
    pm.optionVar["mapAutoMS2RadGrpOptVar"] = 2
    
if "mapAutoMSBox1OptVar" not in pm.env.optionVars:
    pm.optionVar["mapAutoMSBox1OptVar"] = True
    
if "mapAutoMSBox2OptVar" not in pm.env.optionVars:
    pm.optionVar["mapAutoMSBox2OptVar"] = True    

if "mapAutoProjBox1OptVar" not in pm.env.optionVars:
    pm.optionVar["mapAutoProjBox1OptVar"] = False

if "mapAutoProjObjOptVar" not in pm.env.optionVars:
    pm.optionVar["mapAutoProjObjOptVar"] = ""

if "mapAutoProjBox2OptVar" not in pm.env.optionVars:
    pm.optionVar["mapAutoProjBox2OptVar"] = False
    
if "mapAutoLayoutMenuOptVar" not in pm.env.optionVars:
    pm.optionVar["mapAutoLayoutMenuOptVar"] = "Into Square"
    
if "mapAutoLayoutRadGrp1OptVar" not in pm.env.optionVars:
    pm.optionVar["mapAutoLayoutRadGrp1OptVar"] = 2

if "mapAutoLayoutRadGrp2OptVar" not in pm.env.optionVars:
    pm.optionVar["mapAutoLayoutRadGrp2OptVar"] = 1
    
if "mapAutoNormBoxOptVar" not in pm.env.optionVars:
    pm.optionVar["mapAutoNormBoxOptVar"] = False
    
if "mapAutoSpaceMenuOptVar" not in pm.env.optionVars:
    pm.optionVar["mapAutoSpaceMenuOptVar"] = "512 Map"
    
if "mapAutoSpaceValOptVar" not in pm.env.optionVars:
    pm.optionVar["mapAutoSpaceValOptVar"] = 0.2000
    
if "mapAutoSetBoxOptVar" not in pm.env.optionVars:
    pm.optionVar["mapAutoSetBoxOptVar"] = False
    
if "mapAutoSetOptVar" not in pm.env.optionVars:
    pm.optionVar["mapAutoSetOptVar"] = "uvSet1" 

    
if "mapCylindricalMS1BoxOptVar" not in pm.env.optionVars:
    pm.optionVar["mapCylindricalMS1BoxOptVar"] = True
    
if "mapCylindricalMS2BoxOptVar" not in pm.env.optionVars:
    pm.optionVar["mapCylindricalMS2BoxOptVar"] = True
    
if "mapCylindricalSetBoxOptVar" not in pm.env.optionVars:
    pm.optionVar["mapCylindricalSetBoxOptVar"] = False
    
if "mapCylindricalSetOptVar" not in pm.env.optionVars:
    pm.optionVar["mapCylindricalSetOptVar"] = "uvSet1"
    
if "mapCylindricalSweepOptVar" not in pm.env.optionVars:
    pm.optionVar["mapCylindricalSweepOptVar"] = 180
    
    
if "mapNormalMS1OptVar" not in pm.env.optionVars:
    pm.optionVar["mapNormalMS1OptVar"] = False
    
if "mapNormalMS2OptVar" not in pm.env.optionVars:
    pm.optionVar["mapNormalMS2OptVar"] = True
    
if "mapNormalMS3OptVar" not in pm.env.optionVars:
    pm.optionVar["mapNormalMS3OptVar"] = True
    
if "mapNormalSetBoxOptVar" not in pm.env.optionVars:
    pm.optionVar["mapNormalSetBoxOptVar"] = False
    
if "mapNormalSetOptVar" not in pm.env.optionVars:
    pm.optionVar["mapNormalSetOptVar"] = "uvSet1"
    
    
if "mapPlanarMethodOptVar" not in pm.env.optionVars:
    pm.optionVar["mapPlanarMethodOptVar"] = 1 
    
if "mapPlanarMS1RadGrpOptVar" not in pm.env.optionVars:
    pm.optionVar["mapPlanarMS1RadGrpOptVar"] = 2
    
if "mapPlanarMS2RadGrpOptVar" not in pm.env.optionVars:
    pm.optionVar["mapPlanarMS2RadGrpOptVar"] = 1
    
if "mapPlanarMS1BoxOptVar" not in pm.env.optionVars:
    pm.optionVar["mapPlanarMS1BoxOptVar"] = False 
    
if "mapPlanarMS2BoxOptVar" not in pm.env.optionVars:
    pm.optionVar["mapPlanarMS2BoxOptVar"] = True
    
if "mapPlanarMS3BoxOptVar" not in pm.env.optionVars:
    pm.optionVar["mapPlanarMS3BoxOptVar"] = True
    
if "mapPlanarSetBoxOptVar" not in pm.env.optionVars:
    pm.optionVar["mapPlanarSetBoxOptVar"] = False
    
if "mapPlanarSetOptVar" not in pm.env.optionVars:
    pm.optionVar["mapPlanarSetOptVar"] = "uvSet1"
    
    
if "mapSphericalMS1BoxOptVar" not in pm.env.optionVars:
    pm.optionVar["mapSphericalMS1BoxOptVar"] = True
    
if "mapSphericalSetBoxOptVar" not in pm.env.optionVars:
    pm.optionVar["mapSphericalSetBoxOptVar"] = False
    
if "mapSphericalMS2BoxOptVar" not in pm.env.optionVars:
    pm.optionVar["mapSphericalMS2BoxOptVar"] = True
    
if "mapSphericalSetOptVar" not in pm.env.optionVars:
    pm.optionVar["mapSphericalSetOptVar"] = "uvSet1"
    
if "mapSphericalSweep1OptVar" not in pm.env.optionVars:
    pm.optionVar["mapSphericalSweep1OptVar"] = 180
    
if "mapSphericalSweep2OptVar" not in pm.env.optionVars:
    pm.optionVar["mapSphericalSweep2OptVar"] = 90


# Shell randomize optVars

if "randTOptVar" not in pm.env.optionVars:
    pm.optionVar["randTOptVar"] = 0.1

if "randTBox1OptVar" not in pm.env.optionVars:
    pm.optionVar["randTBox1OptVar"] = False

if "randTBox2OptVar" not in pm.env.optionVars:
    pm.optionVar["randTBox2OptVar"] = False

if "randROptVar" not in pm.env.optionVars:
    pm.optionVar["randROptVar"] = 22.5

if "randRBox1OptVar" not in pm.env.optionVars:
    pm.optionVar["randRBox1OptVar"] = False

if "randRBox2OptVar" not in pm.env.optionVars:
    pm.optionVar["randRBox2OptVar"] = False

if "randSOptVar" not in pm.env.optionVars:
    pm.optionVar["randSOptVar"] = 10

if "randSBox1OptVar" not in pm.env.optionVars:
    pm.optionVar["randSBox1OptVar"] = False

if "randSBox2OptVar" not in pm.env.optionVars:
    pm.optionVar["randSBox2OptVar"] = False
    
    
# Relax optVars

if "relaxMethodOptVar" not in pm.env.optionVars:
    pm.optionVar["relaxMethodOptVar"] = 1

if "relaxItrOptVar" not in pm.env.optionVars:
    pm.optionVar["relaxItrOptVar"] = 1
    
if "relaxAngleOptVar" not in pm.env.optionVars:
    pm.optionVar["relaxAngleOptVar"] = 1.0
    
if "relaxPowerOptVar" not in pm.env.optionVars:
    pm.optionVar["relaxPowerOptVar"] = 100
    
if "relaxBorderOptVar" not in pm.env.optionVars:
    pm.optionVar["relaxBorderOptVar"] = True
    
if "relaxFlipsOptVar" not in pm.env.optionVars:
    pm.optionVar["relaxFlipsOptVar"] = True
    
if "relaxSizeOptVar" not in pm.env.optionVars:
    pm.optionVar["relaxSizeOptVar"] = 1028
    
if "relaxRoomOptVar" not in pm.env.optionVars:
    pm.optionVar["relaxRoomOptVar"] = 2
    
if "relaxPinBorderOptVar" not in pm.env.optionVars:
    pm.optionVar["relaxPinBorderOptVar"] = True
    
if "relaxPinOptVar" not in pm.env.optionVars:
    pm.optionVar["relaxPinOptVar"] = False
    
if "relaxPinTypeOptVar" not in pm.env.optionVars:
    pm.optionVar["relaxPinTypeOptVar"] = 1
    
if "relaxEdgeOptVar" not in pm.env.optionVars:
    pm.optionVar["relaxEdgeOptVar"] = 1
    
if "relaxMaxItrOptVar" not in pm.env.optionVars:
    pm.optionVar["relaxMaxItrOptVar"] = 5


# Snapshot optVars

if "shotUVpathOptVar" not in pm.env.optionVars:
    dir = pm.workspace(query=True, rootDirectory=True) + "images/outUV"
    pm.optionVar["shotUVpathOptVar"] = dir

if "shotUVxSizeOptVar" not in pm.env.optionVars:
    pm.optionVar["shotUVxSizeOptVar"] = 1024

if "shotUVySizeOptVar" not in pm.env.optionVars:
    pm.optionVar["shotUVySizeOptVar"] = 1024

if "shotUVaaOptVar" not in pm.env.optionVars:
    pm.optionVar["shotUVaaOptVar"] = 0

if "shotUVcolorOptVar" not in pm.env.optionVars:
    pm.optionVar["shotUVcolorOptVar"] = [ 1.0, 1.0, 1.0 ]

if "shotUVformatOptVar" not in pm.env.optionVars:
    pm.optionVar["shotUVformatOptVar"] = "Maya IFF"

if "shotUVrangeOptVar" not in pm.env.optionVars:
    pm.optionVar["shotUVrangeOptVar"] = 1

if "shotUVtypeOptVar" not in pm.env.optionVars:
    pm.optionVar["shotUVtypeOptVar"] = 1


# Straighten UVs optVar

if "strUVsAngleOptVar" not in pm.env.optionVars:
    pm.optionVar["strUVsAngleOptVar"] = 30

if "strUVsTypeOptVar" not in pm.env.optionVars:
    pm.optionVar["strUVsTypeOptVar"] = 0


# TD optVars

if "tdOptVar" not in pm.env.optionVars:
    pm.optionVar["tdOptVar"] = 32

if "tdSizeOptVar" not in pm.env.optionVars:
    pm.optionVar["tdSizeOptVar"] = 512

if "manipVarTDA1OptVar" not in pm.env.optionVars:
    pm.optionVar["manipVarTDA1OptVar"] = 32.0

if "manipVarTDA2OptVar" not in pm.env.optionVars:
    pm.optionVar["manipVarTDA2OptVar"] = 512

if "manipVarTDB1OptVar" not in pm.env.optionVars:
    pm.optionVar["manipVarTDB1OptVar"] = 32.0

if "manipVarTDB2OptVar" not in pm.env.optionVars:
    pm.optionVar["manipVarTDB2OptVar"] = 512


# Unfold optVars
    
if "unfoldMethodOptVar" not in pm.env.optionVars:
    pm.optionVar["unfoldMethodOptVar"] = 1  
    
if "unfoldItrOptVar" not in pm.env.optionVars:
    pm.optionVar["unfoldItrOptVar"] = 1 
    
if "unfoldPackOptVar" not in pm.env.optionVars:
    pm.optionVar["unfoldPackOptVar"] = True
   
if "unfoldBorderOptVar" not in pm.env.optionVars:
    pm.optionVar["unfoldBorderOptVar"] = True
   
if "unfoldFlipsOptVar" not in pm.env.optionVars:
    pm.optionVar["unfoldFlipsOptVar"] = True
    
if "unfoldSizeOptVar" not in pm.env.optionVars:
    pm.optionVar["unfoldSizeOptVar"] = 1024
    
if "unfoldRoomOptVar" not in pm.env.optionVars:
    pm.optionVar["unfoldRoomOptVar"] = 2
    
if "unfoldSolverOptVar" not in pm.env.optionVars:
    pm.optionVar["unfoldSolverOptVar"] = 0.0000
    
if "unfoldOtOOptVar" not in pm.env.optionVars:
    pm.optionVar["unfoldOtOOptVar"] = 0.5000

if "unfoldAreaOptVar" not in pm.env.optionVars:
    pm.optionVar["unfoldAreaOptVar"] = 0.0
    
if "unfoldPinBorderOptVar" not in pm.env.optionVars:
    pm.optionVar["unfoldPinBorderOptVar"] = False
    
if "unfoldPinOptVar" not in pm.env.optionVars:
    pm.optionVar["unfoldPinOptVar"] = True
    
if "unfoldPinTypeOptVar" not in pm.env.optionVars:
    pm.optionVar["unfoldPinTypeOptVar"] = 1
    
if "unfoldConstOptVar" not in pm.env.optionVars:
    pm.optionVar["unfoldConstOptVar"] = 0
    
if "unfoldMaxItrOptVar" not in pm.env.optionVars:
    pm.optionVar["unfoldMaxItrOptVar"] = 5000
    
if "unfoldStopOptVar" not in pm.env.optionVars:
    pm.optionVar["unfoldStopOptVar"] = 0.0010
    
if "unfoldRescaleOptVar" not in pm.env.optionVars:
    pm.optionVar["unfoldRescaleOptVar"] = False
    
if "unfoldSFactptVar" not in pm.env.optionVars:
    pm.optionVar["unfoldSFactOptVar"] = 0.0200
    
if "unfoldHistOptVar" not in pm.env.optionVars:
    pm.optionVar["unfoldHistOptVar"] = False

    
# UV Set optVars
if "copyNewUVSetOptVar" not in pm.env.optionVars:
    pm.optionVar["copyNewUVSetOptVar"] = "map2"

if "newUVSetOptVar" not in pm.env.optionVars:
    pm.optionVar["newUVSetOptVar"] = "map2"

if "newUVSetShareOptVar" not in pm.env.optionVars:
    pm.optionVar["newUVSetShareOptVar"] = 1  

    
## Create user-interface

#import NSUV.UI as UI
#UI.createUI()