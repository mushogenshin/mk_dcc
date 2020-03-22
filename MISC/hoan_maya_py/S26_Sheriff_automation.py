import maya.cmds as cmds

stuffs_to_replace = ["ReyeNUL", "LeyeNUL", "Ctooth1aOSDM", "Cradioa1aMSDM", "Cgeara1aMSDM", "Cpina1aMSDM",
"Cnametaga1aMSDM", "Cpensa1aMSDM", "Cstara1aMSDM", "Chata1aCSDM", "Cbelta1aCSDM"]

# eyes
cmds.parentConstraint("Eye_R", "ReyeNUL", mo=True)
cmds.scaleConstraint("Head_M", "ReyeNUL", mo=True)

cmds.parentConstraint("Eye_L", "LeyeNUL", mo=True)
cmds.scaleConstraint("Head_M", "LeyeNUL", mo=True)

# teeth
cmds.parentConstraint("Head_M", "Ctooth1aOSDM", mo=True)
cmds.scaleConstraint("Head_M", "Ctooth1aOSDM", mo=True)

# radio caller
cmds.parentConstraint("Root_M", "Cradioa1aMSDM", mo=True)
cmds.scaleConstraint("Root_M", "Cradioa1aMSDM", mo=True)

cmds.parentConstraint("Root_M", "Cgeara1aMSDM", mo=True)
cmds.scaleConstraint("Root_M", "Cgeara1aMSDM", mo=True)

# badge
cmds.parentConstraint("Chest_M", "Cpina1aMSDM", mo=True)
cmds.scaleConstraint("Chest_M", "Cpina1aMSDM", mo=True)

# name tag
cmds.parentConstraint("Chest_M", "Cnametaga1aMSDM", mo=True)
cmds.scaleConstraint("Chest_M", "Cnametaga1aMSDM", mo=True)

# pen
cmds.parentConstraint("Chest_M", "Cpensa1aMSDM", mo=True)
cmds.scaleConstraint("Chest_M", "Cpensa1aMSDM", mo=True)

# stars
cmds.parentConstraint("Chest_M", "Cstara1aMSDM", mo=True)
cmds.scaleConstraint("Chest_M", "Cstara1aMSDM", mo=True)

# hat
cmds.parentConstraint("Head_M", "Chata1aCSDM", mo=True)
cmds.scaleConstraint("Head_M", "Chata1aCSDM", mo=True)

# boots
cmds.parentConstraint("Root_M", "Cbelta1aCSDM", mo=True)
cmds.scaleConstraint("Root_M", "Cbelta1aCSDM", mo=True)


cmds.select(stuffs_to_replace, r=True)