import logging
from src.utils.maya import maya_common


logger = logging.getLogger(__name__)


@maya_common.libs
def filter_meshes_in_selection(*args, **kwargs):
    pmc = kwargs[maya_common._PMC]
    # Assume user already selected something
    pmc.select(hi=True)  # returns None
    return [node for node in pmc.selected() if isinstance(node, pmc.nt.Mesh)]


def get_mesh_xforms_in_selection():
    return [node.getParent() for node in filter_meshes_in_selection() if hasattr(node, "getParent")]


@maya_common.libs
def get_first_xform_in_selection(*args, **kwargs):
    pmc = kwargs[maya_common._PMC]
    xforms = pmc.ls(sl=True, type="transform")
    return xforms[0] if xforms else None


def replace_selection(nodes, **kwargs):
    pmc = kwargs[maya_common._PMC]
    logger.info("Replacing selection with specified nodes")
    pmc.select(nodes, replace=True)


def clear_selection(*args, **kwargs):
    pmc = kwargs[maya_common._PMC]
    pmc.select(cl=True)
