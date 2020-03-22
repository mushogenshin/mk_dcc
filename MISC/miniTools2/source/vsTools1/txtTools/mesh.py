'''
This module contains libraries for Maya meshes.

'''
import pymel.core as pmc
import maya.cmds as cmds

# ------------------------------------------------------------------------------
def offsetUv() :
    '''
    Quick small tool to offset UVs. 
    
    TODO : (one day) 
        - add extra support for subdiv nodes (subdEditUV)
        - symmetry UV ?
    '''
    
    wndName = 'wndVVOffsetUv'
    try : cmds.deleteUI(wndName)
    except : pass
    
    wnd = cmds.window(wndName, t='Offset UVs', tlb=1)

    layV = pmc.verticalLayout()
    up = cmds.button(l='Up', c='polyEditUV(u=0,v=1)')
    
    layH = pmc.horizontalLayout()
    lt = cmds.button(l='Left', c='polyEditUV(u=-1,v=0)')
    rt = cmds.button(l='Right', c='polyEditUV(u=1,v=0)')
    
    cmds.setParent('..')
    dw= cmds.button(l='Down', c='polyEditUV(u=0,v=-1)')
    
    layV.redistribute()
    layH.redistribute()
    
    cmds.showWindow(wnd)
    cmds.window(wnd, e=1, wh=(100,100))
    
    return wnd
# ------------------------------------------------------------------------------

def selectHardBorderEdge(mode):
    # select border edge or / and hard edge
    for i in cmds.ls(selection=True):
        if cmds.ls(selection=True):
            cmds.select(i)
            # hard edge
            cmds.selectType( pe=True )
            cmds.polySelectConstraint( m=3, t=0x8000, sm=1 ) # to get hard edges
            he=cmds.ls(selection=True,flatten=True)
            cmds.polySelectConstraint(sm=0,l=False) # turn off edge smoothness constraint
            # border edge
            cmds.selectType( pe=True )
            cmds.polySelectConstraint(w=1,m=3,bo=True,sh=False) # to get border edges
            be=cmds.ls(selection=True,flatten=True)
            cmds.polySelectConstraint(l=False,bo=False,w=0,sh=False) # turn off edge smoothness constraint
            if mode == "hard":
                cmds.select(he)
            elif mode == "border":
                cmds.select(be)
            elif mode == "hardNoBorder":
                for i in be:
                    if i in he:
                        he.remove(i) 
            if he:
                cmds.select(he)
            else :
                cmds.warning("No hard edges non border edges on selected objects !")
            
        else:
            cmds.warning("Nothing selected !!!")

