import logging
logger = logging.getLogger(__name__)


def get_attrib(node, attrib):
    """
    :param str attrib:
    """
    try:
        import pymel.core as pmc
    except ImportError:
        pass
    else:
        try:
            return pmc.getAttr("{}.{}".format(node.nodeName(), attrib))
        except Exception as e:
            logger.exception('Unable to get "{}" attribute of {} due to {}'.format(attrib, node, e))
    

def set_attrib(node, attrib, value):
    """
    :param str attrib:
    """
    try:
        import pymel.core as pmc
    except ImportError:
        pass
    else:
        try:
            pmc.setAttr("{}.{}".format(node.nodeName(), attrib), value)
        except Exception as e:
            logger.exception('Unable to set "{}" attribute of {} due to {}'.format(attrib, node, e))
        else:
            logger.info('Successfully set "{}" attribute of {} to {}'.format(attrib, node, value))
