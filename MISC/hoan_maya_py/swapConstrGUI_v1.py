import maya.cmds as cmds

namespaceStr = "model:"

constraints = cmds.ls(sl=1)

for constr in constraints:
    constraintType = cmds.objectType(constr)
    if constraintType == "parentConstraint":
        parentObjs = cmds.parentConstraint(constr,q=1,tl=1)
        print ("Parent objs: ", parentObjs)
        childObj = cmds.listConnections(constr,s=0)[0]
        print ("Child obj: ", childObj)
        childObj_ref = namespaceStr + childObj
        print ("Ref child obj: ", childObj_ref)
        
        cmds.select(parentObjs,r=1)
        cmds.select(childObj_ref,add=1)
    
        cmds.parentConstraint(parentObjs,childObj_ref,sr="none",st="none",mo=1)
    elif constraintType == "scaleConstraint":
        parentObjs = cmds.scaleConstraint(constr,q=1,tl=1)
        print ("Parent objs: ", parentObjs)
        childObj = cmds.listConnections(constr,s=0)[0]
        print ("Child obj: ", childObj)
        childObj_ref = namespaceStr + childObj
        print ("Ref child obj: ", childObj_ref)
        
        cmds.select(parentObjs,r=1)
        cmds.select(childObj_ref,add=1)
    
        cmds.scaleConstraint(parentObjs,childObj_ref,mo=1)