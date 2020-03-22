import maya.cmds as mc

def TransUV2MultipleObjects():
    #grab all the selected objects
    selectedObjects = mc.ls(sl=True)
    if not selectedObjects:
        mc.confirmDialog(m='Please select Source Mesh, and then list of destination Meshes', button='OK')
        return 0
    #save first one into variable
    #pop first one out of the selected objects list
    driver = selectedObjects.pop(0)
    #for each object in the selected objects list
    for object in selectedObjects:
        mc.select([driver,object])
        #transfer attributes
        try:
            mc.transferAttributes(sampleSpace=4,transferUVs=2, transferColors=2 )
        except:
            pass
    print "DONE: transfer UV"
        