import logging
from src.utils.maya import maya_common


logger = logging.getLogger(__name__)


@maya_common.libs
def get_attrib(node, attrib, **kwargs):
    """
    :param str attrib:
    """
    pmc = kwargs[maya_common._PMC]
    try:
        return pmc.getAttr("{}.{}".format(node.nodeName(), attrib))
    except Exception as e:
        logger.exception('Unable to get "{}" attribute of {} due to {}'.format(attrib, node, e))
    

@maya_common.libs
def set_attrib(node, attrib, value, **kwargs):
    """
    :param str attrib:
    """
    pmc = kwargs[maya_common._PMC]
    try:
        pmc.setAttr("{}.{}".format(node.nodeName(), attrib), value)
    except Exception as e:
        logger.exception('Unable to set "{}" attribute of {} due to {}'.format(attrib, node, e))
    else:
        logger.info('Successfully set "{}" attribute of {} to {}'.format(attrib, node, value))
