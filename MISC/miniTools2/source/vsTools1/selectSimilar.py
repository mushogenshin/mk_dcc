# huuduy@virtuos-sparx.com - 4/15/2016 #

import pymel.core as pm


def isFlipped(obj_a, obj_b):  # assume that 2 objects are the same
    pm.select(obj_a.f[0])
    raw_verts_a = pm.polyListComponentConversion(tv=1)
    verts_a = []
    for i in raw_verts_a:
        pm.select(i)
        for v in pm.selected():
            verts_a.extend(v)

    pm.select(obj_b.f[0])
    raw_verts_b = pm.polyListComponentConversion(tv=1)
    verts_b = []
    for i in raw_verts_b:
        pm.select(i)
        for v in pm.selected():
            verts_b.extend(v)

    va_1 = verts_a[1].getPosition(
        space='world') - verts_a[0].getPosition(space='world')
    va_2 = verts_a[2].getPosition(
        space='world') - verts_a[0].getPosition(space='world')
    cross_a = va_1.cross(va_2)
    n_a = obj_a.f[0].getNormal(space='world')
    dot_a = cross_a.dot(n_a)

    vb_1 = verts_b[1].getPosition(
        space='world') - verts_b[0].getPosition(space='world')
    vb_2 = verts_b[2].getPosition(
        space='world') - verts_b[0].getPosition(space='world')
    cross_b = vb_1.cross(vb_2)
    n_b = obj_b.f[0].getNormal(space='world')
    dot_b = cross_b.dot(n_b)

    if dot_a * dot_b < 0:
        return True
    else:
        return False


def selectSimilar():
    if len(pm.selected()) > 0:
        sel = pm.selected()[0]
        num_sel_vtx = pm.polyEvaluate(sel, vertex=1)
        area_sel = pm.polyEvaluate(sel, worldArea=1)
        area_sel_sub = sel.f[-1].getArea(space='world')

        all_poly_objects = pm.ls(exactType='mesh')
        result = []

        for o in all_poly_objects:
            o_num_sel_vtx = pm.polyEvaluate(o, vertex=1)
            o_area_sel = pm.polyEvaluate(o, worldArea=1)

            if num_sel_vtx == o_num_sel_vtx and abs(area_sel - o_area_sel) < 0.01:
                if not isFlipped(sel, o):
                    result.append(pm.listRelatives(o, f=True, p=True)[0])

        pm.select(result)
    else:
        print 'Please select some mesh object !'
