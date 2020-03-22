import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel
from maya.app.general import creaseSetEditor


def getSelectedMeshes():
    meshes = cmds.ls(sl=True, dag=True, noIntermediate=True, type='mesh')
    if len(meshes) > 0:
        return meshes


def restore():
    """Restore crease from existing crease sets."""

    try:
        mesh = pm.listRelatives(c=1)[0]
        if type(mesh) == pm.nodetypes.Mesh:
            mel.eval('DeleteHistory')   # if we don't delete history, crease set is likely messed up
            csl = pm.listConnections(mesh, t='creaseSet')
            csl = set(csl)
            print 'All crease sets : ' + str(csl)

            
            # set crease value directly, for debug only
            # it'll be much faster if we set crease value in batch
            for cs in csl:
                print cs
                cre_edges = []
                crlv = pm.getAttr(cs + '.' + 'creaseLevel')
                for i in cs:
                    cre_edges.extend(i)
                if len(cre_edges) > 0:
                    pm.polyCrease(cre_edges, v=crlv)
            

            meshes = getSelectedMeshes()
            creaseSetEditor.bakeOutCreaseSetValues(meshes)
        else:
            pm.warning('Please select combined object !')
    except Exception as e:
        pm.warning(str(e) + ' - Please select combined object !')


def lock():
    """Create crease sets."""

    meshes = getSelectedMeshes()
    creaseSetEditor.unbakeValuesIntoCreaseSets(meshes, name='creaseSet#')
    print 'Created crease set.'
