import logging
logger = logging.getLogger(__name__)


def filter_meshes_in_selection():
    # Assume user already selected something
    try:
        import pymel.core as pmc
        pmc.select(hi=True)  # returns None
        return [node for node in pmc.selected() if isinstance(node, pmc.nt.Mesh)]
    except ImportError:
        return []

def ls_node_name(nodes):
    """
    :rtype list:
    """
    return [node.nodeName() for node in nodes if hasattr(node, "nodeName")]

def get_mesh_xforms_in_selection():
    return [node.getParent() for node in filter_meshes_in_selection()]