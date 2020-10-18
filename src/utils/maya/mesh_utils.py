import logging
logger = logging.getLogger(__name__)


def filter_mesh_components_in_selection():
    try:
        import pymel.core as pmc
    except ImportError:
        return []
    else:
        def is_mesh_component(node):
            return type(node) in (pmc.MeshVertex, pmc.MeshEdge, pmc.MeshFace)   
        return [i for i in pmc.selected(flatten=True) if is_mesh_component(i)]


def filter_mesh_components_of_type_in_selection(**kwargs):
    """
    component_enum: 1 for vertices, 2 for edges, 3 for faces
    :param callable get_component_enum_method:
    :rtype dict:
    :return: {"component_enum": 0, "children": []}
    """
    get_component_enum_method = kwargs.get("get_component_enum_method")
    ret = {"component_enum": 0, "children": []}
    
    if callable(get_component_enum_method):
        ret["component_enum"] = get_component_enum_method()

    logger.debug("Using component enum: {}".format(ret["component_enum"]))

    try:
        import pymel.core as pmc
    except ImportError:
        return ret
    else:
        if ret["component_enum"] == 1:  # vertices
            logger.info("Filtering components of polygonal mesh vertex type")
            ret["children"] = [node for node in pmc.selected() \
                if isinstance(node, pmc.MeshVertex)]
        elif ret["component_enum"] == 2:  # edges
            logger.info("Filtering components of polygonal mesh edge type")
            ret["children"] = [node for node in pmc.selected() \
                if isinstance(node, pmc.MeshEdge)]
        elif ret["component_enum"] == 3:  # faces
            logger.info("Filtering components of polygonal mesh face type")
            ret["children"] = [node for node in pmc.selected() \
                if isinstance(node, pmc.MeshFace)]
        
        return ret


def ls_ID_from_components(nodes):
    """
    Given a list of PyMEL mesh components, return a flattened list of IDs
    """
    try:
        import pymel.core as pmc
    except ImportError:
        return []
    else:
        # Flatten first
        nodes = pmc.ls(nodes, flatten=True)
        return [node.index() for node in nodes if hasattr(node, "index")]


def expand_mesh_with_component_IDs(mesh, component_IDs, component_enum=1):
    """
    :param pmc.nt.Mesh mesh:
    :param list component_IDs: expect a flattened list
    :param int component_enum: 1 for vertices, 2 for edges, 3 for faces
    """
    ret = []
    try:
        import pymel.core as pmc
    except ImportError:
        pass
    else:
        if isinstance(mesh, pmc.nt.Mesh):
            try:
                if component_enum == 1:  # vertices
                    ret = [mesh.vtx[i] for i in component_IDs]
                elif component_enum == 2:  # edges
                    ret = [mesh.e[i] for i in component_IDs]
                elif component_enum == 3:  # faces
                    ret = [mesh.f[i] for i in component_IDs]
            except Exception as e:
                logger.exception(e)
            
    return ret
