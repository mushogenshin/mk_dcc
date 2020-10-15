import logging
logger = logging.getLogger(__name__)


def filter_meshes_in_selection():
    # Assume user already selected something
    try:
        import pymel.core as pmc
    except ImportError:
        return []
    else:
        pmc.select(hi=True)  # returns None
        return [node for node in pmc.selected() if isinstance(node, pmc.nt.Mesh)]


def get_mesh_xforms_in_selection():
    return [node.getParent() for node in filter_meshes_in_selection() if hasattr(node, "getParent")]


def replace_selection(nodes):
    logger.info("Replacing selection with specified nodes")
    try:
        import pymel.core as pmc
    except ImportError:
        return
    else:
        pmc.select(nodes, replace=True)


def clear_selection():
    try:
        import pymel.core as pmc
    except ImportError:
        pass
    else:
        pmc.select(cl=True)
