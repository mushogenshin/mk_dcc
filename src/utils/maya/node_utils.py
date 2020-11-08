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
    if node is not None:
        return node.nodeName() if hasattr(node, "nodeName") else str(node)
    else:
        return ""


def ls_component_IDs(nodes):
    """
    :rtype str: e.g. '[3:9], [13:15], 39, 41, [53:54], [78:79], 84'
    """
    from re import findall
    def get_nice_unflattened_bracket(node):
        """
        :rtype str:
        :return: "[{int}:{int}]" from a PyMEL mesh component, e.g. MeshVertex(u'pSphereShape1.vtx[82:83]')
        """
        ret = findall("\[\d+:\d+\]", repr(node))
        return ret[0] if ret else ""
        
    ret = []
    for node in nodes:
        if hasattr(node, "index") and hasattr(node, "count"):
            if node.count() < 2:
                ret.append(node.index())
            else:
                ret.append(get_nice_unflattened_bracket(node))
                
    ret_str = ""
    for i in ret:
        ret_str += ", {}".format(i)

    return ret_str[2:]


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


def node_exists(node, as_string=False):
    try:
        import maya.cmds as cmds
    except ImportError:
        return False
    else:
        if not node:
            return False
        if as_string:
            return cmds.objExists(node)
        else:
            import pymel.core as pmc
            return pmc.objExists(node)


def delete_one(node, is_mesh=False, delete_construction_history_only=False):
    log_item = "node" if not delete_construction_history_only else "construction history of node"
    logger.info('Deleting {} "{}"'.format(log_item, node))
    try:
        import pymel.core as pmc
    except ImportError:
        pass
    else:
        if is_mesh and hasattr(node, "getParent"):
            node = node.getParent()
        if node_exists(node):
            node_name = get_node_name(node)
            try:
                if not delete_construction_history_only:
                    pmc.delete(node)
                else:
                    pmc.delete(node, constructionHistory=True)
            except Exception as e:
                logger.exception("Unable to delete {} {} due to {}".format(log_item, node, e))
            else:
                logger.info("Successfully deleted {} {}".format(log_item, node_name))
        else:
            logger.warning("{} doesn't exist in scene. Skipped deleting.".format(node))


def delete_many(nodes):
    for node in nodes:
        delete_one(node)


def duplicate(node, as_instance=False, name=""):
    """
    :rtype list:
    :return: list of pmc.nt.Transform even if node is of pmc.nt.Mesh type
    """
    logger.info('Duplicating "{}"'.format(node))
    try:
        import pymel.core as pmc
    except ImportError:
        return []
    else:
        if not node:
            return []
        cmd = getattr(pmc, "duplicate") if not as_instance else getattr(pmc, "instance")
        if name:
            return cmd(node, n=name)
        else:
            return cmd(node)  # auto naming


def parent_A_to_B(node_A, node_B, zero_child_transforms=False):
    logger.info("Parenting {} to {}".format(node_A, node_B))
    try:
        import pymel.core as pmc
    except ImportError:
        pass
    else:
        pmc.parent(node_A, node_B)
        if zero_child_transforms:
            node_A.setTranslation((0, 0, 0))


def parent_to_world(node, former_parent_to_delete=None):
    try:
        import pymel.core as pmc
    except ImportError:
        pass
    else:
        pmc.parent(node, world=True)
        if former_parent_to_delete is not None:
            pmc.delete(former_parent_to_delete)


def set_visibility(nodes, on=True):
    for node in nodes:
        if hasattr(node, "visibility"):
            node.visibility.set(True if on else False)
