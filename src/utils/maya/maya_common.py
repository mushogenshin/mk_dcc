import logging
from functools import wraps


_CMDS = "_cmds"
_MEL = "_mel"
_PMC = "_pmc"
_OMUI = "_omui"
logger = logging.getLogger(__name__)


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
        except ImportError:
            cmds = MayaCmds
            mel = MayaMel
            pmc = PymelCore

        kwargs.update(
            {
                "_cmds": cmds,
                "_mel": mel,
                "_pmc": pmc,
            }
        )

        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception(e)

    return wrapper


def libs_extended(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            import maya.OpenMayaUI as omui
        except ImportError:
            omui = OMUI

        kwargs.update(
            {
                "_omui": omui,
            }
        )

        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception(e)

    return wrapper
