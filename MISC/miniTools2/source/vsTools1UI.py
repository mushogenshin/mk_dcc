# MODIFIED ILMTOOLSUI FOR MINITOOLS2

import maya.mel as mel
import maya.cmds as cmds
import pymel.core as pm

import vsTools1.autoUdim as autoUdim
import vsTools1.uvSizeChecker as uvSizeChecker
import vsTools1.selectSimilar as selectSimilar
import vsTools1.restoreCrease as restoreCrease
import vsTools1.makeInstance as makeInstance
import vsTools1.ilmUDIMTool as ilmUDIMTool
import vsTools1.ilmUnpackUDIM as ilmUnpackUDIM
import vsTools1.TransUVBtw2Grp as tUVgrp
import vsTools1.TransUV2MultipleObjects as TransUV2MultipleObjects

import vsTools1.NSUV.core as NSUV
import vsTools1.txtTools.mesh as txtTools_mesh


# global settings
main_win = 'mnT2_vsTools1_window'
u_lim = 10
v_lim = 0
u_start = 0
v_start = 0
spacing = 0.2


# ----------------------------------------------------------------------------------------------------
# UI commands - AutoUV tab ---------------------------------------------------------------------------


def straigSh():
    NSUV.strShell()


def straigUV():
    NSUV.strUVs()


def aligUvMidU():
    NSUV.alignUVs("avgU")


def aligUvMidV():
    NSUV.alignUVs("avgV")


def unfoldUv():
    try:
        mel.eval('Unfold3D -u -ite 1 -p 0 -bi 1 -tf 1 -ms 1024 -rs 2;')
    except Exception as e:
        pm.confirmDialog(title='Hello', message='Please load Unfold3D plugin !', button=['OK'])
        print e


def centerUv():
    mel.eval('sdv_centerUvs')


def orientSh():
    mel.eval('sdv_orientUvShells')


def stackSh():
    mel.eval('sdv_alignUvShells(7)')


def aligShLeftU():
    mel.eval('sdv_alignUvShells(1)')


def aligShMidU():
    mel.eval('sdv_alignUvShells(5)')


def aligShRightU():
    mel.eval('sdv_alignUvShells(2)')


def aligShTopV():
    mel.eval('sdv_alignUvShells(4)')


def aligShMidV():
    mel.eval('sdv_alignUvShells(6)')


def aligShDownV():
    mel.eval('sdv_alignUvShells(3)')


def packUdim():
    autoUdim.autoUdim(1, 1, u_lim, v_lim, [u_start, v_start], spacing)

def unpackUdim():
    ilmUnpackUDIM.ilmUnpackUDIM()

def selectUvUdim():
    autoUdim.selectOnUdim(mode=1)


def uLimChange():
    global u_lim
    global v_lim

    if int(float(pm.textField('u_lim', q=1, text=1))) > 0:
        u_lim = int(float(pm.textField('u_lim', q=1, text=1)))
        pm.textField('u_lim', edit=1, text=u_lim)
        v_lim = 0
        pm.textField('v_lim', edit=1, text=0)
    else:
        pm.textField('u_lim', edit=1, text=u_lim)


def vLimChange():
    global u_lim
    global v_lim

    if int(float(pm.textField('v_lim', q=1, text=1))) > 0:
        v_lim = int(float(pm.textField('v_lim', q=1, text=1)))
        pm.textField('v_lim', edit=1, text=v_lim)
        u_lim = 0
        pm.textField('u_lim', edit=1, text=0)
    else:
        pm.textField('v_lim', edit=1, text=v_lim)


def uStartChange():
    global u_start
    u_start = int(float(pm.textField('u_start', q=1, text=1)))
    pm.textField('u_start', edit=1, text=u_start)


def vStartChange():
    global v_start
    v_start = int(float(pm.textField('v_start', q=1, text=1)))
    pm.textField('v_start', edit=1, text=v_start)


def spacingChange():
    global spacing
    spacing = float(pm.textField('spacing', q=1, text=1))


def pickSize():
    uvSizeChecker.get_sel_faces_UV_ratio_ilm(1)
    pm.text('picked_obj_label', edit=1, label=pm.selected()[0])


def setSize():
    uvSizeChecker.set_UV_ratio_ilm(1)


def transferMulti():
    TransUV2MultipleObjects.TransUV2MultipleObjects()


def transferBtwFlipped():
    sel = pm.selected()

    pm.polyNormal(sel[0], nm=0)

    pm.select(sel)

    transferMulti()

    pm.delete(sel[1:], ch=1)
    pm.polyNormal(sel[0], nm=0)


def transferGrp():
    tUVgrp.TransUVBtw2Grp()
# ----------------------------------------------------------------------------------------------------
# UI commands - Object tab ---------------------------------------------------------------------------


def creSelMinChange():
    try:
        print float(pm.textField('cre_sel_min', q=1, text=1))
    except Exception as e:
        pm.textField('cre_sel_min', edit=1, text=0)


def creSelMaxChange():
    try:
        print float(pm.textField('cre_sel_max', q=1, text=1))
    except Exception as e:
        pm.textField('cre_sel_max', edit=1, text=0)


def creSel():
    min_cre = pm.textField('cre_sel_min', q=1, text=1)
    max_cre = pm.textField('cre_sel_max', q=1, text=1)
    mode = '1' if pm.radioButton('vert_rb', q=1, select=1) else '2'
    mel.eval('tCreaseTool_select(%s,%s,%s)' % (min_cre, max_cre, mode))


def heCreValChange():
    try:
        print float(pm.textField('he_cre_val', q=1, text=1))
    except Exception as e:
        pm.textField('he_cre_val', edit=1, text=0)


def heConvert():
    he_cre_val = pm.textField('he_cre_val', q=1, text=1)
    hard_edges = mel.eval('tCreaseTool_selectHarEdge')
    pm.select(hard_edges)
    mel.eval('tCreaseTool_command_ilm %s' % he_cre_val)


def absCre(val):
    if type(pm.selected()[0]) == pm.nodetypes.Transform or type(pm.selected()[0]) == pm.nodetypes.Mesh:
        obj_sel = pm.selected()
        pm.select(cl=1)
        for sel in obj_sel:
            pm.select(sel.e, add=1)
    mel.eval('tCreaseTool_command_ilm %s' % str(val))


def transferCre():
    mel.eval('tCreaseToolCopy')


def selSimilar():
    selectSimilar.selectSimilar()


def lockCre():
    restoreCrease.lock()


def backCre():
    restoreCrease.restore()


def selHe():
    txtTools_mesh.selectHardBorderEdge('hardNoBorder')


def makeInst():
    makeInstance.makeInstance()


def autoFence():
    mel.eval('loadPlugin -qt ByronsPolyTools; eval(generateCmdString("-sc ",1));')


def selObjUdim():
    autoUdim.selectOnUdim(mode=0)


def resetXform():
    mel.eval('source mnT2_HKLocalTools')


def combByUdim():
    ilmUDIMTool.ilmCombineMeshByUDIMs()


def flipAllReversed():
    # added by Hoan
    # unused flags -ps 0.2 -l 0 -gu 1 -gv 1 -su 1 -sv 1 -ou 0 -ov 0
    cmds.polyMultiLayoutUV(prescale=0, flipReversed=1, layout=0, scale=0, layoutMethod=1, rotateForBestFit=0)

def UV_border_hard_edges():

    mel_cmd = '''
string $objList[] = `ls -sl -o`;
string $uvBorder[];
string $edgeUVs[];
string $finalBorder[];

for ($subObj in $objList) {
select -r $subObj;
polyNormalPerVertex -ufn true;
polySoftEdge -a 180 -ch 1 $subObj;
select -r $subObj.map["*"];

polySelectBorderShell 1;

$uvBorder = `polyListComponentConversion -te -in`;
$uvBorder = `ls -fl $uvBorder`;

clear( $finalBorder );

for( $curEdge in $uvBorder ) {
$edgeUVs = `polyListComponentConversion -tuv $curEdge`;
$edgeUVs = `ls -fl $edgeUVs`;

if( size( $edgeUVs ) > 2 ) {
$finalBorder[ size( $finalBorder ) ] = $curEdge;
}
}

polySoftEdge -a 0 -ch 1 $finalBorder;
}

select -r $objList;
    '''

    mel.eval(mel_cmd)


def createUI(ui_file_path):
    global main_win

    # print(__name__)

    try:
        if pm.window(main_win, q=True, exists=True):
            pm.deleteUI(main_win)
        main_win = pm.loadUI(f=ui_file_path)
        pm.showWindow(main_win)
        pm.window(main_win, edit=1, tlc=(400, 700))
    except Exception as e:
        pm.warning('There is something wrong : ' + str(e))
