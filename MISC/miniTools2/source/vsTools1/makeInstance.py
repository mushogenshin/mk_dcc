# huuduy@virtuos-sparx.com - 4/15/2016 #

import maya.mel as mel
import pymel.core as pm


def makeInstance():
    mel.eval('CenterPivot')
    mel.eval('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1;')

    result = []
    temp = pm.selected()
    temp_name = []
    inst = pm.instance(pm.selected()[-1])
    for i in temp:
        i_inst = pm.instance(inst)[0]
        if len(pm.listRelatives(i, f=True, p=True)) > 0:
            pm.parent(i_inst, pm.listRelatives(i, f=True, p=True)[0])
        else:
            pm.parent(i_inst, w=1)
        result.append(i_inst)
        temp_name.append(i.name())

        pm.select(cl=1)
        pm.select(i_inst.vtx[0], add=1)
        pm.select(i_inst.vtx[len(i_inst.vtx) / 2], add=1)
        pm.select(i_inst.vtx[-1], add=1)

        pm.select(i.vtx[0], add=1)
        pm.select(i.vtx[len(i.vtx) / 2], add=1)
        pm.select(i.vtx[-1], add=1)
        mel.eval('snap3PointsTo3Points(0)')

    pm.select(temp, inst)
    mel.eval('doDelete')

    for i in range(len(temp_name)):
        pm.rename(result[i], temp_name[i])

    pm.select(result)