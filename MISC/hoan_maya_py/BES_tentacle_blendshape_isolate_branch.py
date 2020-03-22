import maya.cmds as cmds
import pymel.core as pm

current_branch = 20

for i in range(1,21):
    if i==current_branch:
        cmds.setAttr("curve_ref_original{}.v".format(i), 1)
        cmds.setAttr("ctrl_tentacle_{}.v".format(i), 1)
    else:
        cmds.setAttr("curve_ref_original{}.v".format(i), 0)
        cmds.setAttr("ctrl_tentacle_{}.v".format(i), 0)
        
