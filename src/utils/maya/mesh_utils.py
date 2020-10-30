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
    :return: {"component_enum": 0, "children": [], "mesh": None}
    """
    component_enum_dict = {1: "Vertex", 2: "Edge", 3: "Face"}

    get_component_enum_method = kwargs.get("get_component_enum_method")
    ret = {"component_enum": 0, "children": [], "mesh": None}
    
    if callable(get_component_enum_method):
        ret["component_enum"] = get_component_enum_method()

    logger.debug("Using component enum: {} ({})".format(
        ret["component_enum"],
        component_enum_dict.get(ret["component_enum"], "")
    ))

    def get_mesh_node_from_first_component(components):
        component = components[0] if components else None
        if component and hasattr(component, "node"):
            return component.node()

    try:
        import pymel.core as pmc
    except ImportError:
        return ret
    else:
        if ret["component_enum"] == 1:  # vertices
            ret["children"] = [node for node in pmc.selected() \
                if isinstance(node, pmc.MeshVertex)]
        elif ret["component_enum"] == 2:  # edges
            ret["children"] = [node for node in pmc.selected() \
                if isinstance(node, pmc.MeshEdge)]
        elif ret["component_enum"] == 3:  # faces
            ret["children"] = [node for node in pmc.selected() \
                if isinstance(node, pmc.MeshFace)]
        
        ret["mesh"] = get_mesh_node_from_first_component(ret["children"])
        return ret


def filter_mesh_components_of_type_in_selection_as_IDs(**kwargs):
    ret = filter_mesh_components_of_type_in_selection(**kwargs)
    ret["children"] = ls_ID_from_components(ret["children"])
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


def get_bounding_box_center(mesh):
    if hasattr(mesh, "boundingBox"):
        return mesh.boundingBox().center()  # returned in object-space


def get_bounding_box_dimensions(mesh):
    if hasattr(mesh, "boundingBox"):
        bbox = mesh.boundingBox()
        return bbox.width(), bbox.height(), bbox.depth()
    else:
        return 1, 1, 1


def explode_and_group_by_poly_count(meshes=None, make_groups=True, grp_prefix="grouped_by_polyCount"):
    """
    Do explode (polySeparate) only if meshes is given, otherwise running through the whole scene as-is
    """
    num_grouped = {}
    try:
        import pymel.core as pmc
    except ImportError:
        return num_grouped
    else:
        if meshes is not None:
            # Run on polySeparated meshes
            all_separated = []
            for mesh in meshes:
                try:
                    exploded = pmc.polySeparate(mesh, constructionHistory=False)
                    # return list of pmc.nt.Transform
                except:
                    all_separated.append(exploded)
                else:
                    all_separated.extend(exploded)
        else:
            # Run through scene as-is
            all_separated = [mesh.getParent() for mesh in pmc.ls(type="mesh")]
                    
        for xform in all_separated:
            polycount = xform.numFaces()
            if polycount not in num_grouped:
                num_grouped[polycount] = [xform]
            else:
                num_grouped[polycount].append(xform)
                
        pmc.select(cl=True)
        
        if not make_groups:
            return num_grouped
        else:
            null_grouped = {}
            for k, v in num_grouped.items():
                empty_grp = pmc.group(em=True, n="_".join([grp_prefix, str(k)]))
                pmc.parent(v, empty_grp)
                null_grouped[empty_grp] = v
            pmc.select(cl=True)
            return null_grouped
