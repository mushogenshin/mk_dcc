import logging
logger = logging.getLogger(__name__)


def ls_node_name(nodes):
    """
    :rtype list:
    """
    return [node.nodeName() for node in nodes if hasattr(node, "nodeName")]


def get_node_name(node):
    """
    :rtype str:
    """
    return node.nodeName() if hasattr(node, "nodeName") else str(node)


def ls_component_IDs(nodes):
    """
    :rtype list:
    """
    return [node.index() for node in nodes if hasattr(node, "index")]


def get_PyNode(a_str):
    logger.info('Getting PyNode of "{}"'.format(a_str))
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


def delete(node):
    logger.info('Deleting "{}"'.format(node))
    try:
        import pymel.core as pmc
    except ImportError:
        pass
    else:
        try:
            pmc.delete(node)
        except Exception as e:
            logger.exception("Unable to delete node {} due to {}".format(node, e))
        else:
            logger.info("Successfully deleted node {}".format(node))


def duplicate(node, name=""):
    logger.info('Duplicating "{}"'.format(node))
    try:
        import pymel.core as pmc
    except ImportError:
        return
    else:
        if name:
            return pmc.duplicate(node, n=name)
        else:
            return pmc.duplicate(node)  # auto naming


def parent_A_to_B(node_A, node_B):
    logger.info("Parenting {} to {}".format(node_A, node_B))
    try:
        import pymel.core as pmc
    except ImportError:
        pass
    else:
        pmc.parent(node_A, node_B)
