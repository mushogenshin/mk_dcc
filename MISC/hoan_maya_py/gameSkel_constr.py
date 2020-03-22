import pymel.core as pm

sceneNamespace = "rig"

for jnt in pm.ls(sl=1):
    pm.select(":".join([sceneNamespace, jnt.nodeName()]), r=1)
    pm.select(jnt, add=1)
    pm.parentConstraint(mo=1)