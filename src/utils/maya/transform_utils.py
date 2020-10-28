import logging
logger = logging.getLogger(__name__)


WORLD_SPACE = "world"


def get_center_position(objects, as_point=False):
    posX = posY = posZ = 0
    try:
        import pymel.core as pmc
    except ImportError:
        return posX, posY, posZ
    else:
        pos = [pmc.xform(obj, q=True, ws=True, bb=True) for obj in objects]

        if pos:
            val = len(pos)
            pos = [sum(e) for e in zip(*pos)]
            pos = [e / val for e in pos]

            posX = (pos[0] + pos[3]) / 2
            posY = (pos[1] + pos[4]) / 2
            posZ = (pos[2] + pos[5]) / 2

        if not as_point:
            return posX, posY, posZ
        else:
            return pmc.dt.Point(posX, posY, posZ)


def create_center_thingy_from(objects=(), thingy="locator"):
    """
    :rtype PyNode:
    """
    centered_thingy = None
    try:
        import pymel.core as pmc
    except ImportError:
        pass
    else:
        objects = pmc.ls(sl=True, fl=True) if not objects else objects
        posX, posY, posZ = get_center_position(objects)

        pmc.select(cl=True)  # in case thingy is joint

        if thingy == "null":
            centered_thingy = pmc.group(em=True)
            centered_thingy.translate.set(posX, posY, posZ)

        elif thingy == "locator":
            centered_thingy = pmc.spaceLocator()
            centered_thingy.translate.set(posX, posY, posZ)

        elif thingy == "joint":
            centered_thingy = pmc.joint(p=(posX, posY, posZ))

        pmc.select(cl=True)

    return centered_thingy


def orient_joint(joint, aim_axis, up_axis):
    """
    :param str aim_axis: e.g. "xyz"
    :param str up_axis: e.g. "yup"
    """
    logger.info('Orienting joint "{}" with aim axis "{}" and up axis "{}"'.format(
        joint, aim_axis, up_axis
    ))
    try:
        import pymel.core as pmc
    except ImportError:
        pass
    else:
        pmc.joint(
            joint,
            edit=True,
            orientJoint=aim_axis,
            secondaryAxisOrient=up_axis,
        )


def set_rotation_from_joint_orient(obj, joint):
    """
    :param PyNode obj, joint:
    """
    logger.info('Setting rotation of "{}" with orientation of "{}"'.format(obj, joint))
    if hasattr(obj, "setRotation") and hasattr(joint, "getOrientation"):
        obj.setRotation(joint.getOrientation())


def aim_constrain_with_world_up_object(
    target, 
    obj, 
    aim_vector, 
    up_vector, 
    world_up_obj
):
    try:
        import pymel.core as pmc
    except ImportError:
        pass
    else:
        pmc.aimConstraint(
            target, 
            obj, 
            aimVector=aim_vector,
            upVector=up_vector,
            worldUpType="object", 
            worldUpObject=world_up_obj, 
            maintainOffset=False
        )


def bake_aim_constraint_to_joint_orient(joint):
    try:
        import pymel.core as pmc
    except ImportError:
        pass
    else:
        # Remove Constraints
        constraints = set(pmc.listConnections(joint, source=True, destination=False, type="aimConstraint"))
        if constraints:
            try:
                pmc.delete(constraints)
            except:
                pass
        # Freeze Transforms
        pmc.makeIdentity(joint, apply=True, translate=False, scale=False, rotate=True)


def match_transforms(obj, target, translation=True, rotation=True):
    """
    :param PyNode obj, target:
    """
    try:
        import pymel.core as pmc
    except ImportError:
        pass
    else:
        if translation and hasattr(obj, "setTranslation") and hasattr(target, "getTranslation"):
            obj.setTranslation(target.getTranslation(space=WORLD_SPACE), space=WORLD_SPACE)
        if rotation and hasattr(obj, "setRotation") and hasattr(target, "getRotation"):
            obj.setRotation(target.getRotation(space=WORLD_SPACE), space=WORLD_SPACE)


def get_rotate_pivot(node, is_mesh=False):
    try:
        import pymel.core as pmc
    except ImportError:
        pass
    else:
        if is_mesh and hasattr(node, "getParent"):
            node = node.getParent()

        if hasattr(node, "getRotatePivot"):
            return node.getRotatePivot(space=WORLD_SPACE)


def get_translation_between_two_points(src, dst):
    """
    :param pmc.dt.Point src, dst:
    """
    try:
        import pymel.core as pmc
    except ImportError:
        pass
    else:
        if isinstance(src, pmc.dt.Point) and isinstance(dst, pmc.dt.Point):
            return dst - src


def make_space_locator(name=""):
    try:
        import pymel.core as pmc
    except ImportError:
        pass
    else:
        if not name:
            return pmc.spaceLocator()
        else:
            return pmc.spaceLocator(n=name)


def set_translation(node, vector):
    if hasattr(node, "setTranslation"):
        node.setTranslation(vector)
