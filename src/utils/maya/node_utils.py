import logging
logger = logging.getLogger(__name__)


def get_PyNode(a_str):
    try:
        import pymel.core as pmc
    except ImportError:
        return a_str
    else:
        try:
            if a_str is not None:
                return pmc.PyNode(a_str)
            else:
                return a_str
        except Exception as e:
            logger.exception('Unable to return PyNode for "{}" due to {}'.format(a_str, e))
            return a_str


def node_exists(a_str):
    try:
        import maya.cmds as cmds
    except ImportError:
        return False
    else:
        return cmds.objExists(a_str)
