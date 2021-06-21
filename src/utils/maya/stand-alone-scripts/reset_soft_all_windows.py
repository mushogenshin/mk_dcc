"""
__author__ = "Truong CG Artist"
__email__ = "truongcgartist@gmail.com"
"""

def onMayaDroppedPythonFile(*args, **kwargs):
    print("Python file dropped into Maya")
    reset_all_windows()


def reset_all_windows():
    import maya.cmds as cmds
    ret = False
    open_windows = cmds.lsUI(windows=True)

    for win in open_windows:
        if win != "MayaWindow":
            cmds.deleteUI(win)
            cmds.windowPref(win, remove=True)
            print('Window "{}" deleted and reset.'.format(win))
    else:
        ret = True

    return ret        


if __name__ == "__main__":
    reset_all_windows()
