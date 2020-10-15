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
    Component Enum: 1 for vertices, 2 for edges, 3 for faces
    :param callable get_component_enum_method:
    """
    get_component_enum_method = kwargs.get("get_component_enum_method")
    component_enum = 0
    
    if callable(get_component_enum_method):
        component_enum = get_component_enum_method()

    logger.info("Using component enum: {}".format(component_enum))

    try:
        import pymel.core as pmc
    except ImportError:
        return []
    else:

        if component_enum == 1:  # vertices
            logger.info("Filtering components of polygonal mesh vertex type")
            return [node for node in pmc.selected(flatten=True) \
                if isinstance(node, pmc.MeshVertex)]
        elif component_enum == 2:  # edges
            logger.info("Filtering components of polygonal mesh edge type")
            return [node for node in pmc.selected(flatten=True) \
                if isinstance(node, pmc.MeshEdge)]
        elif component_enum == 3:  # faces
            logger.info("Filtering components of polygonal mesh face type")
            return [node for node in pmc.selected(flatten=True) \
                if isinstance(node, pmc.MeshFace)]
        else:
            return []
