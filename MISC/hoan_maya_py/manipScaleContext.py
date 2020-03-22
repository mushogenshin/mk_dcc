import pymel.core as pm

verts_selection = pm.selected()

persp_cam = pm.PyNode("persp")
persp_cam_pos_vec = persp_cam.translate.get()

if pm.mel.manipScaleContext("Scale", q=True, vis=True):
    selection_pivot_pos_vec = pm.dt.Vector(pm.mel.manipScaleContext("Scale", q=True, p=True))
    temp_loc = pm.spaceLocator()
    temp_loc.translate.set(selection_pivot_pos_vec)
    pm.aimConstraint(persp_cam, temp_loc, mo=False)
    aim_angle = list(temp_loc.rotate.get())
    pm.select(verts_selection, r=1)
    pm.mel.manipPivot(o=aim_angle)



pm.mel.manipPivot(resetOri=True)
pm.mel.manipPivot(resetPos=True)
pm.mel.manipPivot(p=[1,0,0])
pm.mel.manipPivot(o=[3,6,9])
pm.mel.ctxEditMode()
# pm.mel.manipPivot(ori=[3, 6, 9]) 1

pm.mel.manipScaleContext("Scale", e=True, currentActiveHandle=2)  # Z axis
# pm.mel.manipScaleContext("Scale", e=True, orientTowards=[1.2, 2.4, 4.7])
pm.mel.manipScaleContext("Scale", e=True, spp=True, oa=[1, 1, 1])
pm.mel.manipScaleContext("Scale", e=True, spo=True, oo="persp")

pm.mel.manipScaleContext("Scale", e=True, )