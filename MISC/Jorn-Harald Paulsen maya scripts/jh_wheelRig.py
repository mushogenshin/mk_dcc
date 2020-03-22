# ************************************************************************************************************
# Title:        jh_wheelRigger.py
# Author:       Jørn-Harald Paulsen
# Created:      February 06, 2013
# Last Update:  February 09, 2013
# Description:  Utility to rig wheels with the possibility to use blendShapes.
# ************************************************************************************************************


#Import everything in maya as the namespace "cmds"
import maya.cmds as cmds
#Import the math module
import math


# ************************************************************************************************************
# FUNCTION: MAIN WINDOW
# ************************************************************************************************************
def jh_wheelRiggerUI():
    #If the window already exists, delete it
    if cmds.windowPref("jh_wheelRigWindow", exists=True):
      cmds.windowPref("jh_wheelRigWindow", remove=True)
    if cmds.window("jh_wheelRigWindow", exists=True):
      cmds.deleteUI("jh_wheelRigWindow", wnd=True)
    #Create the window
    window = cmds.window("jh_wheelRigWindow", title="Wheel Rigger", width=370, height=296 )
    #Create a main layout
    mainLayout = cmds.columnLayout(adjustableColumn=True, width=370, height=296)
    #Create the content
    cmds.separator(style='single')
    cmds.text("\nMake sure your wheel is pointing in Z, so if it were to roll", font='boldLabelFont')
    cmds.text("it would roll forward towards positive Z. Also make sure that", font='boldLabelFont')
    cmds.text("your wheel-geo is grouped, and has it's pivot in the center.", font='boldLabelFont')
    cmds.separator(style='single', height=40)
    cmds.text("Enter the prefix for the wheel (example: car_l_front_):")
    cmds.textField("prefixField", enable=True)
    cmds.separator(style='single', height=40)
    cmds.button('Load the wheelGeo-group', command=jh_loadWheelGeo)
    cmds.textField("wheelGeoField", enable=False)
    cmds.separator(style='single', height=40)
    cmds.button("Rig The Wheel", command=jh_rigWheel)
    cmds.separator(style='single', height=20)
    #Open the window
    cmds.showWindow(window)
    


# ************************************************************************************************************
# FUNCTION: LOAD THE WHEEL
# ************************************************************************************************************
def jh_loadWheelGeo(*args):
    #Clear the textField
    cmds.textField("wheelGeoField", edit=True, text="")
    #Get the selected object
    selObj = cmds.ls(sl=True,type="transform")
    #If the selection isn't empty
    if(len(selObj) != 0):
      #Update the textField
      cmds.textField("wheelGeoField", edit=True, text=selObj[0])
      #Print information 
      print "Loaded %s." % (selObj[0]),



# ************************************************************************************************************
# FUNCTION: RIG THE WHEEL
# ************************************************************************************************************
def jh_rigWheel(*args):
# ************************************************************************************************************
# GATHER SOME DATA
# ************************************************************************************************************
  #Get the prefix
  prefix = cmds.textField("prefixField", query=True, text=True) + "wheel_"
  #Get the wheelGeo
  wheelGeo = cmds.textField("wheelGeoField", query=True, text=True)
  #Get the boundingBox of the wheel
  boundingBox = cmds.xform( wheelGeo, query=True, boundingBox=True )
  #Get the radius of the wheel
  wheelRadius = abs((boundingBox[2] - boundingBox[5]) / 2)
  #Get the height of the wheel
  wheelHeight = abs(boundingBox[2] - boundingBox[5])
  #Get the width of the wheel
  wheelWidth = abs(boundingBox[0] - boundingBox[3])


# ************************************************************************************************************
# CREATE THE GROUPS NEEDED
# ************************************************************************************************************
  geoGrp = cmds.group( empty=True, name=prefix + "geo_grp" )
  ctrlGrp = cmds.group( empty=True, name=prefix + "ctrl_grp" )
  ctrlDeformGrp = cmds.group( empty=True, name=prefix + "deform_ctrl_grp" )
  clusterGrp = cmds.group( empty=True, name=prefix + "cluster_grp" )
  latticeGrp = cmds.group( empty=True, name=prefix + "lattice_grp" )
  noTransformGrp = cmds.group( empty=True, name=prefix + "noTransform_grp" )
  latt1ClsTopGrp = cmds.group( empty=True, name=prefix + "top1_cluster_grp" )
  latt1ClsLowGrp = cmds.group( empty=True, name=prefix + "low1_cluster_grp" )
  latt2ClsTopGrp = cmds.group( empty=True, name=prefix + "top2_cluster_grp" )
  latt2ClsMidGrp = cmds.group( empty=True, name=prefix + "mid2_cluster_grp" )
  latt2ClsLowGrp = cmds.group( empty=True, name=prefix + "low2_cluster_grp" )
  topCtrlGrp = cmds.group( empty=True, name=prefix + "top_ctrl_grp" )
  midCtrlGrp = cmds.group( empty=True, name=prefix + "mid_ctrl_grp" )
  lowCtrlGrp = cmds.group( empty=True, name=prefix + "low_ctrl_grp" )
  posCtrlGrp = cmds.group( empty=True, name=prefix + "main_ctrl_grp" )
  rotCtrlGrp = cmds.group( empty=True, name=prefix + "rotate_ctrl_grp" )
  topExtraMicroGrp = cmds.group( empty=True, name=prefix + "top_extra_micro_ctrl_grp" )
  lowExtraMicroGrp = cmds.group( empty=True, name=prefix + "low_extra_micro_ctrl_grp" )


# ************************************************************************************************************
# CREATE AND POSITION THE PROXY-WHEEL AND THE DEFORMER-WHEELS
# ************************************************************************************************************
  #Create the proxy-wheel
  proxyWheel = cmds.polyCylinder(name=prefix + "proxy_geo", sx=32, sy=1, sz=4, ax=(1,0,0), ch=0)
  #Create a lattice for the proxy-wheel
  lattice1 = cmds.lattice( proxyWheel, divisions=(2, 2, 2), ldivisions=(2, 2, 2), objectCentered=True )
  #Position the proxy-wheel at the original wheel
  cmds.move( boundingBox[3], boundingBox[1], boundingBox[2], lattice1[1] + ".pt[1][0][0]" )
  cmds.move( boundingBox[0], boundingBox[1], boundingBox[2], lattice1[1] + ".pt[0][0][0]" )
  cmds.move( boundingBox[3], boundingBox[1], boundingBox[5], lattice1[1] + ".pt[1][0][1]" )
  cmds.move( boundingBox[0], boundingBox[1], boundingBox[5], lattice1[1] + ".pt[0][0][1]" )
  cmds.move( boundingBox[0], boundingBox[4], boundingBox[2], lattice1[1] + ".pt[0][1][0]" )
  cmds.move( boundingBox[3], boundingBox[4], boundingBox[2], lattice1[1] + ".pt[1][1][0]" )
  cmds.move( boundingBox[0], boundingBox[4], boundingBox[5], lattice1[1] + ".pt[0][1][1]" )
  cmds.move( boundingBox[3], boundingBox[4], boundingBox[5], lattice1[1] + ".pt[1][1][1]" )
  #Delete history and center pivot of the proxy-wheel
  cmds.delete( proxyWheel, constructionHistory=True )
  cmds.xform( proxyWheel, centerPivots=True )
  #Create the deformer-wheels
  deformWheel = cmds.duplicate( proxyWheel, returnRootsOnly=True, name=prefix + "deformInput_geo" )
  latt1Wheel = cmds.duplicate( proxyWheel, returnRootsOnly=True, name=prefix + "lattice_1_geo" )
  latt2Wheel = cmds.duplicate( proxyWheel, returnRootsOnly=True, name=prefix + "lattice_2_geo" )


# ************************************************************************************************************
# CREATE THE CONTROLLERS FOR THE WHEEL
# ************************************************************************************************************
  #Create the mid-controller for the wheel
  midCtrl = cmds.curve( p=[(-1,0,1),(1,0,1),(1,0,-1),(-1,0,-1),(-1,0,1)], degree=1 )
  #Create a the controller for the wheel rotation/position
  posCtrl = cmds.circle( radius=wheelRadius, nr=(1,0,0), center=(0,0,0), degree=3, sections=32, ch=0 )
  #Create a the controller for the wheel rotation
  rotCtrl = cmds.circle( radius=wheelRadius / 1.5, nr=(1,0,0), center=(0,0,0), degree=3, sections=32, ch=0 )
  #Create the deform-controller for the wheel
  wheelCtrl = cmds.curve( p=[(0,0,1),(0,0.4,0.9),(0,0.7,0.7),(0,0.9,0.4),(0,1,0),(-0.4,0.9,0),(-0.7,0.7,0),
              (-0.9,0.4,0),(-1,0,0),(-0.9,-0.4,0),(-0.7,-0.7,0),(-0.4,-0.9,0),(0,-1,0),(0,-0.9,0.4),
              (0,-0.7,0.7),(0,-0.4,0.9),(0,0,1),(-0.4,0,0.9),(-0.7,0,0.7),(-0.9,0,0.4),(-1,0,0),(-0.9,0,-0.4),
              (-0.7,0,-0.7),(-0.4,0,-0.9),(0,0,-1),(0,-0.4,-0.9),(0,-0.7,-0.7),(0,-0.9,-0.4),(0,-1,0),
              (0.4,-0.9,0),(0.7,-0.7,0),(0.9,-0.4,0),(1,0,0),(0.9,0,-0.4),(0.7,0,-0.7),(0.4,0,-0.9),
              (0,0,-1),(0,0.4,-0.9),(0,0.7,-0.7),(0,0.9,-0.4),(0,1,0),(0.4,0.9,0),(0.7,0.7,0),(0.9,0.4,0),
              (1,0,0),(0.9,0,0.4),(0.7,0,0.7),(0.4,0,0.9),(0,0,1)], degree=1 )

  #Rename the controllers
  midCtrl = cmds.rename( midCtrl, prefix + "mid_ctrl" )
  posCtrl[0] = cmds.rename( posCtrl[0], prefix + "main_ctrl" )
  rotCtrl[0] = cmds.rename( rotCtrl[0], prefix + "rotate_ctrl" )

  #Create the deform-controllers for the upper/lower part of the wheel
  cmds.scale( wheelHeight / 8, wheelHeight / 8, wheelHeight / 8, wheelCtrl, relative=True )
  topCtrl = cmds.duplicate( wheelCtrl, returnRootsOnly=True, name=prefix + "top_ctrl" )
  lowCtrl = cmds.duplicate( wheelCtrl, returnRootsOnly=True, name=prefix + "low_ctrl" )
  #Set the rotation orders for the deform-controllers
  cmds.setAttr( posCtrl[0] + ".rotateOrder", 3 )
  cmds.setAttr( posCtrlGrp + ".rotateOrder", 3 )
  cmds.setAttr( ctrlDeformGrp + ".rotateOrder", 3 )
  #Create the micro deform-controllers
  cmds.scale( 0.3, 0.3, 0.3, wheelCtrl, relative=True )
  topCtrl1 = cmds.duplicate( wheelCtrl, returnRootsOnly=True, name=prefix + "top_1_micro_ctrl" )
  topCtrl2 = cmds.duplicate( wheelCtrl, returnRootsOnly=True, name=prefix + "top_2_micro_ctrl" )
  topCtrl3 = cmds.duplicate( wheelCtrl, returnRootsOnly=True, name=prefix + "top_3_micro_ctrl" )
  topCtrl4 = cmds.duplicate( wheelCtrl, returnRootsOnly=True, name=prefix + "top_4_micro_ctrl" )
  topCtrl5 = cmds.duplicate( wheelCtrl, returnRootsOnly=True, name=prefix + "top_5_micro_ctrl" )
  topCtrl6 = cmds.duplicate( wheelCtrl, returnRootsOnly=True, name=prefix + "top_6_micro_ctrl" )
  midCtrl1 = cmds.duplicate( wheelCtrl, returnRootsOnly=True, name=prefix + "mid_1_micro_ctrl" )
  midCtrl2 = cmds.duplicate( wheelCtrl, returnRootsOnly=True, name=prefix + "mid_2_micro_ctrl" )
  midCtrl3 = cmds.duplicate( wheelCtrl, returnRootsOnly=True, name=prefix + "mid_3_micro_ctrl" )
  midCtrl4 = cmds.duplicate( wheelCtrl, returnRootsOnly=True, name=prefix + "mid_4_micro_ctrl" )
  midCtrl5 = cmds.duplicate( wheelCtrl, returnRootsOnly=True, name=prefix + "mid_5_micro_ctrl" )
  midCtrl6 = cmds.duplicate( wheelCtrl, returnRootsOnly=True, name=prefix + "mid_6_micro_ctrl" )
  lowCtrl1 = cmds.duplicate( wheelCtrl, returnRootsOnly=True, name=prefix + "low_1_micro_ctrl" )
  lowCtrl2 = cmds.duplicate( wheelCtrl, returnRootsOnly=True, name=prefix + "low_2_micro_ctrl" )
  lowCtrl3 = cmds.duplicate( wheelCtrl, returnRootsOnly=True, name=prefix + "low_3_micro_ctrl" )
  lowCtrl4 = cmds.duplicate( wheelCtrl, returnRootsOnly=True, name=prefix + "low_4_micro_ctrl" )
  lowCtrl5 = cmds.duplicate( wheelCtrl, returnRootsOnly=True, name=prefix + "low_5_micro_ctrl" )
  lowCtrl6 = cmds.duplicate( wheelCtrl, returnRootsOnly=True, name=prefix + "low_6_micro_ctrl" )

  #Shape the controller for the wheel rotation/position
  for i in range(0,32,2): cmds.scale(0.85,0.85,0.85, posCtrl[0] + ".cv[%d]"%i, r=True)
  #Shape the controller for the wheel rotation
  cmds.scale( 0.5,0.5,0.5,rotCtrl[0]+".cv[1]",rotCtrl[0]+".cv[9]",rotCtrl[0]+".cv[17]",rotCtrl[0]+".cv[25]" )
  #Scale the mid-controller to the correct size
  cmds.scale( wheelWidth / 1.5, wheelHeight / 1.5, wheelHeight / 1.5, midCtrl )
  

# ************************************************************************************************************
# POSITION THE CONTROLLERS
# ************************************************************************************************************
  #Position all of the controllers at the center of the wheel
  cmds.delete(cmds.pointConstraint( proxyWheel, midCtrl ) )
  cmds.delete(cmds.pointConstraint( proxyWheel, posCtrl[0] ) )
  cmds.delete(cmds.pointConstraint( proxyWheel, rotCtrl[0] ) )
  cmds.delete(cmds.pointConstraint( proxyWheel, topCtrl[0] ) )
  cmds.delete(cmds.pointConstraint( proxyWheel, lowCtrl[0] ) )
  #Position the upper/lower deform-controllers
  cmds.move( 0, (wheelHeight / 2), 0, topCtrl[0], r=True, os=True, wd=True )
  cmds.move( 0, ((wheelHeight / 2) * -1), 0, lowCtrl[0], r=True, os=True, wd=True )
  #Position the micro-controllers
  cmds.move( boundingBox[3], boundingBox[4], boundingBox[2], topCtrl1[0] )
  cmds.move( boundingBox[0], boundingBox[4], boundingBox[2], topCtrl2[0] )
  cmds.move( boundingBox[3], boundingBox[4], boundingBox[5], topCtrl3[0] )
  cmds.move( boundingBox[0], boundingBox[4], boundingBox[5], topCtrl4[0] )
  cmds.move( boundingBox[3], boundingBox[1], boundingBox[2], lowCtrl1[0] )
  cmds.move( boundingBox[0], boundingBox[1], boundingBox[2], lowCtrl2[0] )
  cmds.move( boundingBox[3], boundingBox[1], boundingBox[5], lowCtrl3[0] )
  cmds.move( boundingBox[0], boundingBox[1], boundingBox[5], lowCtrl4[0] )
  cmds.delete(cmds.pointConstraint( topCtrl1[0], topCtrl3[0], topCtrl5[0] ) )
  cmds.delete(cmds.pointConstraint( topCtrl2[0], topCtrl4[0], topCtrl6[0] ) )
  cmds.delete(cmds.pointConstraint( lowCtrl1[0], lowCtrl3[0], lowCtrl5[0] ) )
  cmds.delete(cmds.pointConstraint( lowCtrl2[0], lowCtrl4[0], lowCtrl6[0] ) )
  cmds.delete(cmds.pointConstraint( topCtrl1[0], lowCtrl1[0], midCtrl1[0] ) )
  cmds.delete(cmds.pointConstraint( topCtrl2[0], lowCtrl2[0], midCtrl2[0] ) )
  cmds.delete(cmds.pointConstraint( topCtrl3[0], lowCtrl3[0], midCtrl3[0] ) )
  cmds.delete(cmds.pointConstraint( topCtrl4[0], lowCtrl4[0], midCtrl4[0] ) )
  cmds.delete(cmds.pointConstraint( topCtrl5[0], lowCtrl5[0], midCtrl5[0] ) )
  cmds.delete(cmds.pointConstraint( topCtrl6[0], lowCtrl6[0], midCtrl6[0] ) )

  #If the wheel is in negative Z, place the controllers on negative Z
  if ( cmds.getAttr(midCtrl + ".tx") < 0 ) == True:
    cmds.move( ((wheelWidth / 1.5) * -1), 0, 0, posCtrl[0] + ".cv[*]", r=True, os=True, wd=True )
    cmds.move( ((wheelWidth / 1.5) * -1), 0, 0, rotCtrl[0], r=True, os=True, wd=True )
  #If the wheel is in positive Z, place the controllers on positive Z
  if ( cmds.getAttr(midCtrl + ".tx") > 0 ) == True:
    cmds.move( (wheelWidth / 1.5), 0, 0, posCtrl[0] + ".cv[*]", r=True, os=True, wd=True )
    cmds.move( (wheelWidth / 1.5), 0, 0, rotCtrl[0], r=True, os=True, wd=True )
  #If the wheel is in neither positive or negative Z, print error
  if ( cmds.getAttr(midCtrl + ".tx") == 0 ) == True:
    cmds.error( "You have to have the wheel pointing towards Z" ),


  #Position the groups for the deform-controllers
  cmds.delete(cmds.pointConstraint( topCtrl[0], topCtrlGrp ) )
  cmds.delete(cmds.pointConstraint( posCtrl[0], midCtrlGrp ) )
  cmds.delete(cmds.pointConstraint( lowCtrl[0], lowCtrlGrp ) )
  cmds.delete(cmds.pointConstraint( posCtrl[0], posCtrlGrp ) )
  cmds.delete(cmds.pointConstraint( posCtrl[0], rotCtrlGrp ) )
  cmds.delete(cmds.pointConstraint( posCtrl[0], ctrlDeformGrp ) )
  cmds.delete(cmds.pointConstraint( posCtrl[0], ctrlGrp ) )


# ************************************************************************************************************
# CLEANUP THE HIERARCHY
# ************************************************************************************************************
  #Delete the template-controller
  cmds.delete( wheelCtrl )
  #Parent the controllers in their groups
  cmds.parent( topCtrl[0], topCtrlGrp )
  cmds.parent( lowCtrl[0], lowCtrlGrp )
  cmds.parent( posCtrl[0], posCtrlGrp )
  cmds.parent( rotCtrl[0], rotCtrlGrp )
  cmds.parent( midCtrl, midCtrlGrp )
  cmds.parent( rotCtrlGrp, posCtrl[0] )
  cmds.parent( topCtrl5[0], topCtrl6[0], topExtraMicroGrp )
  cmds.parent( lowCtrl5[0], lowCtrl6[0], lowExtraMicroGrp )
  cmds.parent( topCtrlGrp, midCtrlGrp, lowCtrlGrp, ctrlDeformGrp )
  cmds.parent( ctrlDeformGrp, posCtrlGrp, ctrlGrp )
  #Parent the micro-controllers to the macro-controllers
  cmds.parent( topCtrl1[0], topCtrl2[0], topCtrl3[0], topCtrl4[0], topExtraMicroGrp, topCtrl[0] )
  cmds.parent( lowCtrl1[0], lowCtrl2[0], lowCtrl3[0], lowCtrl4[0], lowExtraMicroGrp, lowCtrl[0] )
  cmds.parent( midCtrl1[0], midCtrl2[0], midCtrl3[0], midCtrl4[0], midCtrl5[0], midCtrl6[0], midCtrl )
  #Center the controllers pivots
  cmds.xform( topExtraMicroGrp, lowExtraMicroGrp, centerPivots=True )
  #Freese the transforms of the controllers
  cmds.makeIdentity( ctrlGrp, apply=True, t=1, r=1, s=1, n=2 )


# ************************************************************************************************************
# CREATE THE ATTRIBUTES FOR THE CONTROLLERS
# ************************************************************************************************************
  cmds.addAttr( topCtrl[0], ln='extraAttr', nn="----------------", at="enum", en="Extra:", k=True )
  cmds.addAttr( topCtrl[0], ln='extraCtrl', at="enum", en="Hide:Show:", k=True )
  cmds.addAttr( topCtrl[0], ln='wheelSpin', at="double", k=True )
  cmds.addAttr( lowCtrl[0], ln='extraAttr', nn="----------------", at="enum", en="Extra:", k=True )
  cmds.addAttr( lowCtrl[0], ln='extraCtrl', at="enum", en="Hide:Show:", k=True )
  cmds.addAttr( lowCtrl[0], ln='wheelSpin', at="double", k=True )
  cmds.addAttr( posCtrl[0], ln='extraAttr', nn="----------------", at="enum", en="Extra:", k=True )
  cmds.addAttr( posCtrl[0], ln='wheelSpin', at="double", k=True )
  cmds.addAttr( posCtrl[0], ln='affectArea', at="double", min=0, max=1, k=True )
  cmds.addAttr( posCtrl[0], ln='showProxy', at="enum", en="No:Yes:", k=True )
  cmds.addAttr( rotCtrl[0], ln='extraAttr', nn="----------------", at="enum", en="Extra:", k=True )
  cmds.addAttr( rotCtrl[0], ln='wheelSpin', at="double", k=True )
  cmds.addAttr( midCtrl, ln='extraAttr', nn="----------------", at="enum", en="Extra:", k=True )
  cmds.addAttr( midCtrl, ln='extraCtrl', at="enum", en="Hide:Show:", k=True )
  cmds.addAttr( midCtrl, ln='wheelSpin', at="double", k=True )
  cmds.setAttr( topCtrl[0] + ".extraAttr", lock=True )
  cmds.setAttr( lowCtrl[0] + ".extraAttr", lock=True )
  cmds.setAttr( posCtrl[0] + ".extraAttr", lock=True )
  cmds.setAttr( rotCtrl[0] + ".extraAttr", lock=True )
  cmds.setAttr( midCtrl + ".extraAttr", lock=True )


# ************************************************************************************************************
# RIG THE WHEEL
# ************************************************************************************************************
  #Create a lattice for each of the lattice-wheels
  lattice1 = cmds.lattice( latt1Wheel, divisions=(2, 2, 2), ldivisions=(2, 2, 2), objectCentered=True )
  lattice2 = cmds.lattice( latt2Wheel, divisions=(2, 3, 3), ldivisions=(2, 3, 3), objectCentered=True )
  #Rename the lattices
  lattice1[0] = cmds.rename( lattice1[0], prefix + "lattice_1_latticeShape" )
  lattice1[1] = cmds.rename( lattice1[1], prefix + "lattice_1_lattice" )
  lattice1[2] = cmds.rename( lattice1[2], prefix + "lattice_1_lattice_base" )
  lattice2[0] = cmds.rename( lattice2[0], prefix + "lattice_2_latticeShape" )
  lattice2[1] = cmds.rename( lattice2[1], prefix + "lattice_2_lattice" )
  lattice2[2] = cmds.rename( lattice2[2], prefix + "lattice_2_lattice_base" )
  #Parent the lattices to the lattice-group
  cmds.parent( lattice1[1], lattice1[2], lattice2[1], lattice2[2], latticeGrp )
  #Parent the extra cluster-groups to the main cluster-group
  cmds.parent( latt1ClsTopGrp, latt1ClsLowGrp, latt2ClsTopGrp, latt2ClsMidGrp, latt2ClsLowGrp, clusterGrp )
  #Create the clusters for lattice1
  top1cls1 = cmds.cluster( (lattice1[1] + ".pt[1][1][0]"), name=(prefix + "top_1_1_cluster") )
  top1cls2 = cmds.cluster( (lattice1[1] + ".pt[0][1][0]"), name=(prefix + "top_1_2_cluster") )
  top1cls3 = cmds.cluster( (lattice1[1] + ".pt[1][1][1]"), name=(prefix + "top_1_3_cluster") )
  top1cls4 = cmds.cluster( (lattice1[1] + ".pt[0][1][1]"), name=(prefix + "top_1_4_cluster") )
  low1cls1 = cmds.cluster( (lattice1[1] + ".pt[1][0][0]"), name=(prefix + "low_1_1_cluster") )
  low1cls2 = cmds.cluster( (lattice1[1] + ".pt[0][0][0]"), name=(prefix + "low_1_2_cluster") )
  low1cls3 = cmds.cluster( (lattice1[1] + ".pt[1][0][1]"), name=(prefix + "low_1_3_cluster") )
  low1cls4 = cmds.cluster( (lattice1[1] + ".pt[0][0][1]"), name=(prefix + "low_1_4_cluster") )
  #Create the clusters for lattice2
  top2cls1 = cmds.cluster( (lattice2[1] + ".pt[1][2][0]"), name=(prefix + "top_2_1_cluster") )
  top2cls2 = cmds.cluster( (lattice2[1] + ".pt[0][2][0]"), name=(prefix + "top_2_2_cluster") )
  top2cls3 = cmds.cluster( (lattice2[1] + ".pt[1][2][2]"), name=(prefix + "top_2_3_cluster") )
  top2cls4 = cmds.cluster( (lattice2[1] + ".pt[0][2][2]"), name=(prefix + "top_2_4_cluster") )
  top2cls5 = cmds.cluster( (lattice2[1] + ".pt[1][2][1]"), name=(prefix + "top_2_5_cluster") )
  top2cls6 = cmds.cluster( (lattice2[1] + ".pt[0][2][1]"), name=(prefix + "top_2_6_cluster") )
  mid2cls1 = cmds.cluster( (lattice2[1] + ".pt[1][1][0]"), name=(prefix + "mid_2_1_cluster") )
  mid2cls2 = cmds.cluster( (lattice2[1] + ".pt[0][1][0]"), name=(prefix + "mid_2_2_cluster") )
  mid2cls3 = cmds.cluster( (lattice2[1] + ".pt[1][1][2]"), name=(prefix + "mid_2_3_cluster") )
  mid2cls4 = cmds.cluster( (lattice2[1] + ".pt[0][1][2]"), name=(prefix + "mid_2_4_cluster") )
  mid2cls5 = cmds.cluster( (lattice2[1] + ".pt[1][1][1]"), name=(prefix + "mid_2_5_cluster") )
  mid2cls6 = cmds.cluster( (lattice2[1] + ".pt[0][1][1]"), name=(prefix + "mid_2_6_cluster") )
  low2cls1 = cmds.cluster( (lattice2[1] + ".pt[1][0][0]"), name=(prefix + "low_2_1_cluster") )
  low2cls2 = cmds.cluster( (lattice2[1] + ".pt[0][0][0]"), name=(prefix + "low_2_2_cluster") )
  low2cls3 = cmds.cluster( (lattice2[1] + ".pt[1][0][2]"), name=(prefix + "low_2_3_cluster") )
  low2cls4 = cmds.cluster( (lattice2[1] + ".pt[0][0][2]"), name=(prefix + "low_2_4_cluster") )
  low2cls5 = cmds.cluster( (lattice2[1] + ".pt[1][0][1]"), name=(prefix + "low_2_5_cluster") )
  low2cls6 = cmds.cluster( (lattice2[1] + ".pt[0][0][1]"), name=(prefix + "low_2_6_cluster") )
  #Parent the clusters in the cluster-group
  cmds.parent( top1cls1[1], top1cls2[1], top1cls3[1], top1cls4[1], latt1ClsTopGrp )
  cmds.parent( low1cls1[1], low1cls2[1], low1cls3[1], low1cls4[1], latt1ClsLowGrp )
  cmds.parent( top2cls1[1], top2cls2[1], top2cls3[1], top2cls4[1], top2cls5[1], top2cls6[1], latt2ClsTopGrp )
  cmds.parent( mid2cls1[1], mid2cls2[1], mid2cls3[1], mid2cls4[1], mid2cls5[1], mid2cls6[1], latt2ClsMidGrp )
  cmds.parent( low2cls1[1], low2cls2[1], low2cls3[1], low2cls4[1], low2cls5[1], low2cls6[1], latt2ClsLowGrp )
  #Hide the clusterGrp, latticeGrp and the deformer-wheels
  cmds.hide( clusterGrp, latticeGrp, latt1Wheel, latt2Wheel, deformWheel )
  #ParentConstraint and ScaleConstraint the clusters to the main controllers
  cmds.parentConstraint( topCtrl[0], latt1ClsTopGrp, mo=True )
  cmds.parentConstraint( topCtrl[0], latt2ClsTopGrp, mo=True )
  cmds.parentConstraint( lowCtrl[0], latt1ClsLowGrp, mo=True )
  cmds.parentConstraint( lowCtrl[0], latt2ClsLowGrp, mo=True )
  cmds.parentConstraint( midCtrl, latt2ClsMidGrp, mo=True )
  cmds.scaleConstraint( topCtrl[0], latt1ClsTopGrp )
  cmds.scaleConstraint( topCtrl[0], latt2ClsTopGrp )
  cmds.scaleConstraint( lowCtrl[0], latt1ClsLowGrp )
  cmds.scaleConstraint( lowCtrl[0], latt2ClsLowGrp )
  cmds.scaleConstraint( midCtrl, latt2ClsMidGrp )
  #ParentConstraint the deformer-controls to the main controller
  cmds.parentConstraint( posCtrl[0], ctrlDeformGrp, mo=True )
  #Connect the lattice-rigged wheels into the deformedInput-mesh
  wheelBlnd = cmds.blendShape( latt1Wheel, latt2Wheel, deformWheel, name=(prefix + "blendShape") )


# ************************************************************************************************************
# SET UP THE CONNECTIONS FOR THE CONTROLLERS
# ************************************************************************************************************
  #Connect the micro controllers directly to the clusters
  cmds.connectAttr( (topCtrl1[0] + ".translate"), (top1cls1[1] + ".translate") )
  cmds.connectAttr( (topCtrl2[0] + ".translate"), (top1cls2[1] + ".translate") )
  cmds.connectAttr( (topCtrl3[0] + ".translate"), (top1cls3[1] + ".translate") )
  cmds.connectAttr( (topCtrl4[0] + ".translate"), (top1cls4[1] + ".translate") )
  cmds.connectAttr( (topCtrl1[0] + ".translate"), (top2cls1[1] + ".translate") )
  cmds.connectAttr( (topCtrl2[0] + ".translate"), (top2cls2[1] + ".translate") )
  cmds.connectAttr( (topCtrl3[0] + ".translate"), (top2cls3[1] + ".translate") )
  cmds.connectAttr( (topCtrl4[0] + ".translate"), (top2cls4[1] + ".translate") )
  cmds.connectAttr( (topCtrl5[0] + ".translate"), (top2cls5[1] + ".translate") )
  cmds.connectAttr( (topCtrl6[0] + ".translate"), (top2cls6[1] + ".translate") )
  cmds.connectAttr( (midCtrl1[0] + ".translate"), (mid2cls1[1] + ".translate") )
  cmds.connectAttr( (midCtrl2[0] + ".translate"), (mid2cls2[1] + ".translate") )
  cmds.connectAttr( (midCtrl3[0] + ".translate"), (mid2cls3[1] + ".translate") )
  cmds.connectAttr( (midCtrl4[0] + ".translate"), (mid2cls4[1] + ".translate") )
  cmds.connectAttr( (midCtrl5[0] + ".translate"), (mid2cls5[1] + ".translate") )
  cmds.connectAttr( (midCtrl6[0] + ".translate"), (mid2cls6[1] + ".translate") )
  cmds.connectAttr( (lowCtrl1[0] + ".translate"), (low1cls1[1] + ".translate") )
  cmds.connectAttr( (lowCtrl2[0] + ".translate"), (low1cls2[1] + ".translate") )
  cmds.connectAttr( (lowCtrl3[0] + ".translate"), (low1cls3[1] + ".translate") )
  cmds.connectAttr( (lowCtrl4[0] + ".translate"), (low1cls4[1] + ".translate") )
  cmds.connectAttr( (lowCtrl1[0] + ".translate"), (low2cls1[1] + ".translate") )
  cmds.connectAttr( (lowCtrl2[0] + ".translate"), (low2cls2[1] + ".translate") )
  cmds.connectAttr( (lowCtrl3[0] + ".translate"), (low2cls3[1] + ".translate") )
  cmds.connectAttr( (lowCtrl4[0] + ".translate"), (low2cls4[1] + ".translate") )
  cmds.connectAttr( (lowCtrl5[0] + ".translate"), (low2cls5[1] + ".translate") )
  cmds.connectAttr( (lowCtrl6[0] + ".translate"), (low2cls6[1] + ".translate") )
  #Connect the visibility of the controllers
  cmds.connectAttr( (topCtrl[0] + ".extraCtrl"), (topCtrl1[0] + ".visibility") )
  cmds.connectAttr( (topCtrl[0] + ".extraCtrl"), (topCtrl2[0] + ".visibility") )
  cmds.connectAttr( (topCtrl[0] + ".extraCtrl"), (topCtrl3[0] + ".visibility") )
  cmds.connectAttr( (topCtrl[0] + ".extraCtrl"), (topCtrl4[0] + ".visibility") )
  cmds.connectAttr( (topCtrl[0] + ".extraCtrl"), (topCtrl5[0] + ".visibility") )
  cmds.connectAttr( (topCtrl[0] + ".extraCtrl"), (topCtrl6[0] + ".visibility") )
  cmds.connectAttr( (midCtrl + ".extraCtrl"), (midCtrl1[0] + ".visibility") )
  cmds.connectAttr( (midCtrl + ".extraCtrl"), (midCtrl2[0] + ".visibility") )
  cmds.connectAttr( (midCtrl + ".extraCtrl"), (midCtrl3[0] + ".visibility") )
  cmds.connectAttr( (midCtrl + ".extraCtrl"), (midCtrl4[0] + ".visibility") )
  cmds.connectAttr( (midCtrl + ".extraCtrl"), (midCtrl5[0] + ".visibility") )
  cmds.connectAttr( (midCtrl + ".extraCtrl"), (midCtrl6[0] + ".visibility") )
  cmds.connectAttr( (lowCtrl[0] + ".extraCtrl"), (lowCtrl1[0] + ".visibility") )
  cmds.connectAttr( (lowCtrl[0] + ".extraCtrl"), (lowCtrl2[0] + ".visibility") )
  cmds.connectAttr( (lowCtrl[0] + ".extraCtrl"), (lowCtrl3[0] + ".visibility") )
  cmds.connectAttr( (lowCtrl[0] + ".extraCtrl"), (lowCtrl4[0] + ".visibility") )
  cmds.connectAttr( (lowCtrl[0] + ".extraCtrl"), (lowCtrl5[0] + ".visibility") )
  cmds.connectAttr( (lowCtrl[0] + ".extraCtrl"), (lowCtrl6[0] + ".visibility") )
  cmds.connectAttr( (posCtrl[0] + ".affectArea"), (topExtraMicroGrp + ".visibility") )
  cmds.connectAttr( (posCtrl[0] + ".affectArea"), (lowExtraMicroGrp + ".visibility") )
  cmds.connectAttr( (posCtrl[0] + ".affectArea"), (midCtrl + ".visibility") )
  #Set up the SDKs for the blending of the blendShapes
  cmds.setDrivenKeyframe( (wheelBlnd[0] + "." + latt1Wheel[0]), cd=(posCtrl[0] + ".affectArea"), dv=0, v=1 )
  cmds.setDrivenKeyframe( (wheelBlnd[0] + "." + latt1Wheel[0]), cd=(posCtrl[0] + ".affectArea"), dv=1, v=0 )
  cmds.setDrivenKeyframe( (wheelBlnd[0] + "." + latt2Wheel[0]), cd=(posCtrl[0] + ".affectArea"), dv=0, v=0 )
  cmds.setDrivenKeyframe( (wheelBlnd[0] + "." + latt2Wheel[0]), cd=(posCtrl[0] + ".affectArea"), dv=1, v=1 )
  cmds.setDrivenKeyframe( (proxyWheel[0] + ".visibility"), cd=(posCtrl[0] + ".showProxy"), dv=0, v=0 )
  cmds.setDrivenKeyframe( (proxyWheel[0] + ".visibility"), cd=(posCtrl[0] + ".showProxy"), dv=1, v=1 )
  cmds.setDrivenKeyframe( (wheelGeo + ".visibility"), cd=(posCtrl[0] + ".showProxy"), dv=0, v=1 )
  cmds.setDrivenKeyframe( (wheelGeo + ".visibility"), cd=(posCtrl[0] + ".showProxy"), dv=1, v=0 )
  #Set up the wheelSpin
  wheelSpinPma = cmds.shadingNode('plusMinusAverage', asUtility=True, name=(prefix + "spin_sum_pma") )
  cmds.connectAttr( (posCtrl[0] + ".wheelSpin"), (wheelSpinPma + ".input1D[0]") )
  cmds.connectAttr( (rotCtrl[0] + ".wheelSpin"), (wheelSpinPma + ".input1D[1]") )
  cmds.connectAttr( (topCtrl[0] + ".wheelSpin"), (wheelSpinPma + ".input1D[2]") )
  cmds.connectAttr( (lowCtrl[0] + ".wheelSpin"), (wheelSpinPma + ".input1D[3]") )
  cmds.connectAttr( (midCtrl + ".wheelSpin"), (wheelSpinPma + ".input1D[4]") )
  cmds.connectAttr( (rotCtrl[0] + ".rotateX"), (wheelSpinPma + ".input1D[5]") )
  cmds.connectAttr( (wheelSpinPma + ".output1D"), (proxyWheel[0] + ".rotateX") )


# ************************************************************************************************************
# WRAP-DEFORM THE WHEEL SO THAT THE WHEEL CAN SPIN RELATIVE TO IT'S SHAPE
# ************************************************************************************************************
  #Wrap the proxy-geo to the deformedInput-mesh
  cmds.select( proxyWheel )
  cmds.select( deformWheel[0], add=True )
  cmds.CreateWrap()
  #Get the name of the wrap, then rename it
  wrap = cmds.listConnections( deformWheel[0], type="wrap" )
  proxyWrap = cmds.rename( wrap[0], prefix + "deformInput_wrap")
  #Set the options for the wrap
  cmds.setAttr( proxyWrap + ".exclusiveBind", 0 )
  cmds.setAttr( proxyWrap + ".weightThreshold", 0 )
  cmds.setAttr( proxyWrap + ".maxDistance", 0 )
  cmds.setAttr( proxyWrap + ".autoWeightThreshold", 0 )
  #Wrap the original geo to the proxy-mesh
  cmds.select( wheelGeo )
  cmds.select( proxyWheel, add=True )
  cmds.CreateWrap()
  #Get the name of the wrap, then rename it
  wrap = cmds.listConnections( proxyWheel[0], type="wrap" )
  originalWrap = cmds.rename( wrap[0], prefix + "proxy_wrap")
  #Set the options for the wrap
  cmds.setAttr( originalWrap + ".exclusiveBind", 0 )
  cmds.setAttr( originalWrap + ".weightThreshold", 0 )
  cmds.setAttr( originalWrap + ".maxDistance", 0 )
  cmds.setAttr( originalWrap + ".autoWeightThreshold", 0 )


# ************************************************************************************************************
# CLEANUP
# ************************************************************************************************************
  #Clean the main hierarchy
  cmds.parent( wheelGeo, proxyWheel, deformWheel[0], latt1Wheel[0], latt2Wheel[0], geoGrp )
  cmds.parent( (proxyWheel[0] + "Base"), (deformWheel[0] + "Base"), geoGrp )
  cmds.parent( geoGrp, clusterGrp, latticeGrp, noTransformGrp)
  #Lock unused attributes
  cmds.setAttr( posCtrlGrp + ".scale", lock=True )
  cmds.setAttr( posCtrl[0] + ".scale", lock=True )
  cmds.setAttr( rotCtrlGrp + ".translate", lock=True )
  cmds.setAttr( rotCtrlGrp + ".rotate", lock=True )
  cmds.setAttr( rotCtrlGrp + ".scale", lock=True )
  cmds.setAttr( rotCtrl[0] + ".translate", lock=True )
  cmds.setAttr( rotCtrl[0] + ".scale", lock=True )
  cmds.setAttr( rotCtrl[0] + ".rotateY", lock=True )
  cmds.setAttr( rotCtrl[0] + ".rotateZ", lock=True )
  #Lock unused attributes on each micro-control
  microControllers = cmds.ls( prefix + "*_*_micro_ctrl")
  for micro in microControllers:
    cmds.setAttr( micro + ".rotate", lock=True) 
    cmds.setAttr( micro + ".scale", lock=True)
  #Rename all of the tweak-nodes
  tweakNodes = cmds.ls(type='tweak')
  for tweak in tweakNodes:
    tweakShape = cmds.listConnections( tweak, type="shape" )
    cmds.rename(tweak, (tweakShape[0] + "_tweak") )


# ************************************************************************************************************
# SET THE COLOR OF THE CONTROLLERS
# ************************************************************************************************************
  cmds.setAttr (posCtrl[0] + "Shape.overrideEnabled", 1)
  cmds.setAttr (rotCtrl[0] + "Shape.overrideEnabled", 1)
  cmds.setAttr (topCtrl[0] + "Shape.overrideEnabled", 1)
  cmds.setAttr (lowCtrl[0] + "Shape.overrideEnabled", 1)
  cmds.setAttr (midCtrl + "Shape.overrideEnabled", 1)
  cmds.setAttr (topCtrl1[0] + "Shape.overrideEnabled", 1)
  cmds.setAttr (topCtrl2[0] + "Shape.overrideEnabled", 1)
  cmds.setAttr (topCtrl3[0] + "Shape.overrideEnabled", 1)
  cmds.setAttr (topCtrl4[0] + "Shape.overrideEnabled", 1)
  cmds.setAttr (topCtrl5[0] + "Shape.overrideEnabled", 1)
  cmds.setAttr (topCtrl6[0] + "Shape.overrideEnabled", 1)
  cmds.setAttr (midCtrl1[0] + "Shape.overrideEnabled", 1)
  cmds.setAttr (midCtrl2[0] + "Shape.overrideEnabled", 1)
  cmds.setAttr (midCtrl3[0] + "Shape.overrideEnabled", 1)
  cmds.setAttr (midCtrl4[0] + "Shape.overrideEnabled", 1)
  cmds.setAttr (midCtrl5[0] + "Shape.overrideEnabled", 1)
  cmds.setAttr (midCtrl6[0] + "Shape.overrideEnabled", 1)
  cmds.setAttr (lowCtrl1[0] + "Shape.overrideEnabled", 1)
  cmds.setAttr (lowCtrl2[0] + "Shape.overrideEnabled", 1)
  cmds.setAttr (lowCtrl3[0] + "Shape.overrideEnabled", 1)
  cmds.setAttr (lowCtrl4[0] + "Shape.overrideEnabled", 1)
  cmds.setAttr (lowCtrl5[0] + "Shape.overrideEnabled", 1)
  cmds.setAttr (lowCtrl6[0] + "Shape.overrideEnabled", 1)
  cmds.setAttr (posCtrl[0] + "Shape.overrideColor", 19)
  cmds.setAttr (rotCtrl[0] + "Shape.overrideColor", 13)
  cmds.setAttr (topCtrl[0] + "Shape.overrideColor", 17)
  cmds.setAttr (midCtrl + "Shape.overrideColor", 17)
  cmds.setAttr (lowCtrl[0] + "Shape.overrideColor", 17)
  cmds.setAttr (topCtrl1[0] + "Shape.overrideColor", 9)
  cmds.setAttr (topCtrl2[0] + "Shape.overrideColor", 9)
  cmds.setAttr (topCtrl3[0] + "Shape.overrideColor", 9)
  cmds.setAttr (topCtrl4[0] + "Shape.overrideColor", 9)
  cmds.setAttr (topCtrl5[0] + "Shape.overrideColor", 9)
  cmds.setAttr (topCtrl6[0] + "Shape.overrideColor", 9)
  cmds.setAttr (midCtrl1[0] + "Shape.overrideColor", 9)
  cmds.setAttr (midCtrl2[0] + "Shape.overrideColor", 9)
  cmds.setAttr (midCtrl3[0] + "Shape.overrideColor", 9)
  cmds.setAttr (midCtrl4[0] + "Shape.overrideColor", 9)
  cmds.setAttr (midCtrl5[0] + "Shape.overrideColor", 9)
  cmds.setAttr (midCtrl6[0] + "Shape.overrideColor", 9)
  cmds.setAttr (lowCtrl1[0] + "Shape.overrideColor", 9)
  cmds.setAttr (lowCtrl2[0] + "Shape.overrideColor", 9)
  cmds.setAttr (lowCtrl3[0] + "Shape.overrideColor", 9)
  cmds.setAttr (lowCtrl4[0] + "Shape.overrideColor", 9)
  cmds.setAttr (lowCtrl5[0] + "Shape.overrideColor", 9)
  cmds.setAttr (lowCtrl6[0] + "Shape.overrideColor", 9)


# ************************************************************************************************************
# ************************************************************************************************************

#Run the script
jh_wheelRiggerUI()