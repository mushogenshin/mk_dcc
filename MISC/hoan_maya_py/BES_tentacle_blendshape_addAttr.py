import maya.cmds as cmds

ctrl = cmds.ls(sl=1)[0]

cmds.addAttr(ctrl, k=1, at="enum", ln="tentacle_shapes", nn="*** TENTACLE", enumName="SHAPES")

cmds.addAttr(ctrl, k=1, at="float", ln="arc_1", nn="Arc 1", min=-1.1, max=1.1, dv=0.0)
cmds.addAttr(ctrl, k=1, at="float", ln="arc_2", nn="Arc 2", min=-1.1, max=1.1, dv=0.0)
cmds.addAttr(ctrl, k=1, at="float", ln="arc_3", nn="Arc 3", min=-1.1, max=1.1, dv=0.0)
cmds.addAttr(ctrl, k=1, at="float", ln="arc_4", nn="Arc 4", min=-1.1, max=1.1, dv=0.0)

cmds.addAttr(ctrl, k=1, at="float", ln="wiggle_A", nn="Wiggle A", min=-1.1, max=1.1, dv=0.0)
cmds.addAttr(ctrl, k=1, at="float", ln="wiggle_B", nn="Wiggle B", min=-1.1, max=1.1, dv=0.0)
