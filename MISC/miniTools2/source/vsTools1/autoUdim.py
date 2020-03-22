# huuduy@virtuos-sparx.com - 4/15/2016 #

import pymel.core as pm
import maya.OpenMaya as om
import maya.mel as mel
import sys
import time
import math

'''
# parameters
u_dir = 1
v_dir = 1
u_bound = 10
v_bound = 0  # 0 used for unbound
udim_start = [0, 0]
space = 0.2  # percentage of 1
'''

#=======================================================================================================================
# Utilities


def fromUdim(udims, mode=0):
    """
    Return something based on UDIM coords.
    mode=0 : object
    mode=1 : uv
    """
    s = time.time()
    print 'Selecting from UDIM : ' + str(udims)
    result = []
    meshes = pm.ls(type='mesh')
    pm.select(meshes)
    obj_selection = om.MSelectionList()
    om.MGlobal.getActiveSelectionList(obj_selection)
    iterSel = om.MItSelectionList(obj_selection, om.MFn.kMesh)
    pm.select(cl=1)

    while not iterSel.isDone():
        dagPath = om.MDagPath()
        iterSel.getDagPath(dagPath)
        obj = pm.listRelatives(str(dagPath.fullPathName()), f=True, p=True)[0]
        if pm.polyEvaluate(obj, uv=1) > 0:
            for udim in udims:
                coord = pm.polyEditUV(obj.map[0], q=1)
                if coord[0] <= udim[0] + 1 and coord[0] >= udim[0] and coord[1] <= udim[1] + 1 and coord[1] >= udim[1]:
                    result.append(obj)
                    if mode == 1:
                        result.append(obj.map)
                    break
        iterSel.next()
    pm.select(result)
    print 'Select time : ' + str(round(time.time() - s, 2)) + ' seconds'


def selectOnUdim(mode=0):
    sel = pm.ls(sl=1, o=1)
    if len(sel) > 0 and isinstance(sel[0], pm.nodetypes.Transform):
        u, v = [], []
        udims = []
        for obj in sel:
            uv_coord = pm.polyEditUV(obj.map[0], q=1)
            u.append(int(uv_coord[0]))
            v.append(int(uv_coord[1]))
        raw_udims = zip(u, v)
        for udim in raw_udims:
            if not udim in udims:
                udims.append(udim)
        fromUdim(udims, mode)
    else:
        print 'Please select at least 1 object'


#=======================================================================================================================
# UV shell processing


def uvInner(obj_name):
    pm.select(obj_name)
    uv_full = range(0, len(pm.selected()[0].map))
    pm.select(obj_name + '.map[*]')
    mel.eval('polySelectBorderShell 1;')
    uv_border = []
    for m in pm.selected():
        for n in m:
            uv_border.append(n.index())
    return [i for i in uv_full if i not in uv_border]


def shellCount(dagPath):
    """Return number of UV shells in default uvset 'map1'."""

    meshNode = dagPath.fullPathName()
    uvSets = pm.polyUVSet(meshNode, query=True, allUVSets=True)
    allSets = {}
    for uvset in uvSets:
        shapeFn = om.MFnMesh(dagPath)
        shells = om.MScriptUtil()
        shells.createFromInt(0)
        nbUvShells = shells.asUintPtr()
        uvShellIds = om.MIntArray()  # The container for the uv shell Ids
        shapeFn.getUvShellsIds(uvShellIds, nbUvShells, uvset)
        shellCount = shells.getUint(nbUvShells)
        allSets[uvset] = shellCount
    return int(allSets['map1'])


def getUvShells(dagPath):
    """Return UV shells in default uvset 'map1'."""

    meshNode = dagPath.fullPathName()
    uvSets = pm.polyUVSet(meshNode, query=True, allUVSets=True)
    allSets = {}
    for uvset in uvSets:
        if uvset == 'map1':
            shapeFn = om.MFnMesh(dagPath)
            shells = om.MScriptUtil()
            shells.createFromInt(0)
            nbUvShells = shells.asUintPtr()

            uArray = om.MFloatArray()  # array for U coords
            vArray = om.MFloatArray()  # array for V coords
            uvShellIds = om.MIntArray()  # The container for the uv shell Ids

            shapeFn.getUVs(uArray, vArray)
            shapeFn.getUvShellsIds(uvShellIds, nbUvShells, uvset)

            # shellCount = shells.getUint(shellsPtr)
            shells = {}
            for i, n in enumerate(uvShellIds):
                if n in shells:
                    shells[n].append([i, uArray[i], vArray[i]])
                else:
                    shells[n] = [[i, uArray[i], vArray[i]]]
            allSets[uvset] = shells
        else:
            break
    return allSets['map1']


def fit(shell):
    """Shell is a list of [uv_index, u, v] list."""

    du = max([uv[1] for uv in shell]) - min([uv[1] for uv in shell])
    if du < 1:
        dv = max([uv[2] for uv in shell]) - min([uv[2] for uv in shell])
        if dv < 1:
            return True
        else:
            return False
    else:
        return False


def notFitShells(prog_bar, prog_start, prog_end):
    selList = om.MSelectionList()
    om.MGlobal.getActiveSelectionList(selList)
    not_fits = []

    if selList.length() > 0:
        iterSel = om.MItSelectionList(selList, om.MFn.kMesh)
        om.MGlobal.setActiveSelectionList(om.MSelectionList())
        total = selList.length()
        count = 1

        while not iterSel.isDone():
            ratio = float(count) / float(total)
            amount = prog_start + (prog_end - prog_start) * ratio
            updateProgress(prog_bar, amount, 'Step 1/4')
            dagPath = om.MDagPath()
            iterSel.getDagPath(dagPath)
            shells = getUvShells(dagPath)
            uv_inner = uvInner(str(dagPath.fullPathName()))

            # check if UV shell fit in an UV tile
            for s in shells:
                for uv in reversed(shells[s]):
                    if uv[0] in uv_inner:  # get UV shell border
                        shells[s].remove(uv)
                if fit(shells[s]) == False:
                    not_fits.append(pm.listRelatives(
                        str(dagPath.fullPathName()), f=True, p=True)[0])
                    break
            iterSel.next()
            count += 1

    return not_fits


def getArea(dagPath):
    """Return UV area."""

    areaParam = om.MScriptUtil()
    areaParam.createFromDouble(0.0)
    areaPtr = areaParam.asDoublePtr()
    area = 0
    iterPoly = om.MItMeshPolygon(dagPath)
    while not iterPoly.isDone():
        iterPoly.getUVArea(areaPtr)
        area += om.MScriptUtil(areaPtr).asDouble()
        iterPoly.next()
    return area


def layout(udim, space=0.2, force_move=False):
    temp = pm.selected()
    if len(pm.selected()) == 1:
        cur_sel = om.MSelectionList()
        om.MGlobal.getActiveSelectionList(cur_sel)
        iterSel = om.MItSelectionList(cur_sel, om.MFn.kMesh)
        dagPath = om.MDagPath()
        iterSel.getDagPath(dagPath)
        if shellCount(dagPath) == 1:
            pm.polyMultiLayoutUV(lm=0, sc=0, rbf=1, fr=1,
                                 ps=space, l=2, psc=0, su=1, sv=1, ou=0, ov=0)
        else:
            pm.polyMultiLayoutUV(lm=1, sc=0, rbf=1, fr=1,
                                 ps=space, l=2, psc=0, su=1, sv=1, ou=0, ov=0)
    else:
        pm.polyMultiLayoutUV(lm=1, sc=0, rbf=1, fr=1,
                             ps=space, l=2, psc=0, su=1, sv=1, ou=0, ov=0)

    uvb = pm.polyEvaluate(b2=True)
    if uvb[0][1] - uvb[0][0] >= 1 or uvb[1][1] - uvb[1][0] >= 1:
        if force_move:
            for i in temp:
                pm.polyMoveUV(i, tu=udim[0], tv=udim[1])
            pm.select(temp)
        return False
    else:
        for i in temp:
            pm.polyMoveUV(i, tu=udim[0], tv=udim[1])
        pm.select(temp)
        return True


def showList(skips):
    win = pm.window('Objects skipped')
    pm.paneLayout()
    sl = pm.textScrollList(numberOfRows=len(
        skips), allowMultiSelection=True, append=skips)

    def select_obj():
        selected = pm.textScrollList(sl, q=True, si=True)
        pm.select(selected)
    pm.textScrollList(sl, e=True, sc=select_obj)
    pm.showWindow()


def updateProgress(prog_bar, amount, status):
    if pm.progressWindow(prog_bar, query=True, isCancelled=True):
        pm.progressWindow(endProgress=1)
        sys.exit()
    pm.progressWindow(edit=True, progress=amount, status=status)


def pack(u_dir=1, v_dir=1, u_bound=10, v_bound=0, udim_start=[0, 0], space=0.2):
    # convert all selected object/group to a selection of transform nodes with
    # mesh inside
    s = pm.listRelatives(ad=1, s=1)
    t = pm.listRelatives(s, f=1, p=1)
    pm.select(t)

    # filter objects whose per UV shell don't fit in 1 UV tile
    amount = 0
    prog_bar = pm.progressWindow(
        title='Packing UDIM', progress=amount, status='Step 1/4', isInterruptable=True)
    print '1/4 - Filtering objects whose each UV shell don\'t fit in 1 UV tile...'
    raw_selection = pm.selected()
    skips = notFitShells(prog_bar, 0, 20)
    pm.select(raw_selection)
    pm.select(skips, d=True)

    # filter objects whose total UV area higher than 1 unit
    updateProgress(prog_bar, 20, 'Step 2/4')
    print '2/4 - Filtering objects whose total UV area higher than 1 unit...'
    obj_selection = om.MSelectionList()
    om.MGlobal.getActiveSelectionList(obj_selection)
    iterSel = om.MItSelectionList(obj_selection, om.MFn.kMesh)
    total = obj_selection.length()
    count = 1
    while not iterSel.isDone():
        ratio = float(count) / float(total)
        amount = 20 + 20 * ratio
        updateProgress(prog_bar, amount, 'Step 2/4')
        dagPath = om.MDagPath()
        iterSel.getDagPath(dagPath)
        area = getArea(dagPath)
        if area >= 0.95:
            skips.append(pm.listRelatives(
                str(dagPath.fullPathName()), f=True, p=True)[0])
        iterSel.next()
        count += 1
    pm.select(raw_selection)
    pm.select(skips, d=True)
    filtered_selection = pm.selected()  # backup selection for result select

    # filter smallest objects
    updateProgress(prog_bar, 40, 'Step 3/4')
    print '3/4 - Extract objects with smallest UV area...'
    smallests = []
    areas = []
    obj_selection = om.MSelectionList()
    om.MGlobal.getActiveSelectionList(obj_selection)
    iterSel = om.MItSelectionList(obj_selection, om.MFn.kMesh)
    total = obj_selection.length()
    count = 1
    while not iterSel.isDone():
        ratio = float(count) / float(total)
        amount = 40 + 20 * ratio
        updateProgress(prog_bar, amount, 'Step 3/4')
        dagPath = om.MDagPath()
        iterSel.getDagPath(dagPath)
        area = getArea(dagPath)
        if area < 0.2:
            areas.append(area)
            smallests.append(pm.listRelatives(
                str(dagPath.fullPathName()), f=True, p=True)[0])
        iterSel.next()
        count += 1
    pm.select(filtered_selection)
    pm.select(smallests, d=True)

    smallests = [b for (a, b) in sorted(
        zip(areas, smallests), key=lambda pair: pair[0])]
    print 'Number of smallests : ' + str(len(smallests))

    if len(pm.selected()) == 0:  # in case all we have are objects with small UV area
        pm.select(smallests)
        smallests = []

    # pack UDIM using filtered objects
    updateProgress(prog_bar, 60, 'Step 4/4')
    print '4/4 - Start packing...'
    obj_selection = om.MSelectionList()
    om.MGlobal.getActiveSelectionList(obj_selection)
    om.MGlobal.setActiveSelectionList(om.MSelectionList())
    udim_origin = [0, 0]
    # deep list clone, otherwise udim & udim_start ref to the same list object
    udim = udim_start[:]
    if u_bound > 0:
        if udim[0] > u_bound - 1:
            udim[0] = u_bound - 1
    elif v_bound > 0:
        if udim[1] > v_bound - 1:
            udim[1] = v_bound - 1

    num_total_obj = obj_selection.length() + len(smallests)
    u_dir = math.copysign(1, u_dir)
    v_dir = math.copysign(1, v_dir)

    while not obj_selection.isEmpty():
        num_packed_obj = num_total_obj - \
            (obj_selection.length() + len(smallests))
        ratio = float(num_packed_obj) / float(num_total_obj)
        amount = 60 + 40.0 * ratio
        updateProgress(prog_bar, amount, 'Step 4/4' +
                       ' - packed : %d / %d objects' % (num_packed_obj, num_total_obj))

        # prepare the ready-to-be-packed objects
        iterSel = om.MItSelectionList(obj_selection, om.MFn.kMesh)
        totalArea = 0
        while not iterSel.isDone():
            dagPath = om.MDagPath()
            iterSel.getDagPath(dagPath)
            totalArea += getArea(dagPath)

            # I use 0.95 because 1 is just applicable for a solid square, which
            # unlikely to happen in real life
            if totalArea <= 0.95:
                trans_node = pm.listRelatives(
                    str(dagPath.fullPathName()), f=True, p=True)[0]
                pm.select(trans_node, add=True)
                iterSel.next()
                # print iterSel.isDone()
            else:
                # print totalArea
                break

        # iteration for checking if packed UVs fit in 1 UV tile, and decrease
        # amount of objects until it fit
        cut = pm.selected()
        fitted = layout(udim, space)
        while not fitted:
            if len(cut) == 1:
                skips.append(pm.selected()[0])
                filtered_selection.remove(pm.selected()[0])
                break
            else:
                pm.select(pm.selected()[-1], d=True)
                del cut[-1]
                fitted = layout(udim, space)

        # optimize using smallest objects for un-used space in the new packed
        # UDIM tile
        if fitted:
            while len(smallests) > 0:
                pm.select(smallests[0], add=True)
                # print 'optimizing - num of selected : ' +
                # str(len(pm.selected())) + ' | smallests remain : ' +
                # str(len(smallests))
                if layout(udim, space):
                    del smallests[0]
                else:
                    pm.select(pm.selected()[-1], d=True)
                    attempt = 10
                    while attempt > 0:
                        if layout(udim, space, force_move=True):
                            break
                        else:
                            attempt -= 1
                    break

        while len(cut) > 0:
            obj_selection.remove(0)
            del cut[0]

        # if current objects were packed successful, move to the next UDIM tile
        if fitted:
            print 'Packed ' + str(udim)
            if u_bound > 0:
                temp = udim[0]
                rb = (u_bound - 1) * u_dir + udim_origin[0]
                udim[0] = udim[0] + \
                    u_dir if 0 < abs(rb - udim[0]) else udim_origin[0]
                udim[1] += v_dir if temp == rb else 0
            elif v_bound > 0:
                temp = udim[1]
                rb = (v_bound - 1) * v_dir + udim_origin[1]
                udim[1] = udim[1] + \
                    v_dir if 0 < abs(rb - udim[1]) else udim_origin[1]
                udim[0] += u_dir if temp == rb else 0

        # in the end of obj_selection, pack remaining item in smallests
        if obj_selection.isEmpty() and len(smallests) > 0:
            pm.select(smallests)
            om.MGlobal.getActiveSelectionList(obj_selection)
            smallests = []

        pm.select(cl=True)

    print 'Skipped objects : ' + str(skips)
    pm.select(filtered_selection)
    pm.delete(ch=True)

    if len(skips) > 0:
        showList([i.longName() for i in skips])

    pm.progressWindow(endProgress=1)


def autoUdim(u_dir=1, v_dir=1, u_bound=10, v_bound=0, udim_start=[0, 0], space=0.2):
    s = time.time()
    pm.undoInfo(state=False)
    pack(u_dir, v_dir, u_bound, v_bound, udim_start, space)
    pm.undoInfo(state=True, infinity=False, length=200)
    print 'Running time : ' + str(round(time.time() - s, 2)) + ' seconds'

# autoUdim(u_dir=1, v_dir=1, u_bound=10, v_bound=0, udim_start=[0, 0], space=0.2)
