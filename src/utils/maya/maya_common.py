from functools import wraps


_CMDS = "_cmds"
_MEL = "_mel"
_PMC = "_pmc"
_OMUI = "_omui"


class MayaCmds(object):
    pass


class MayaMel(object):
    pass


class PymelCore(object):
    pass


class OMUI(object):
    pass


def libs(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            import maya.cmds as cmds
            import maya.mel as mel
            import pymel.core as pmc
            import maya.OpenMayaUI as omui
        except ImportError:
            cmds = MayaCmds
            mel = MayaMel
            pmc = PymelCore
            omui = OMUI

        kwargs.update(
            {
                "_cmds": cmds,
                "_mel": mel,
                "_pmc": pmc,
                "_omui": omui,
            }
        )

        return func(*args, **kwargs)

    return wrapper
