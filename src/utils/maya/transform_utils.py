import logging
from src.utils.maya import maya_common


logger = logging.getLogger(__name__)


WORLD_SPACE = "world"


@maya_common.libs
def get_center_position(objects, as_point=False, **kwargs):
    pmc = kwargs[maya_common._PMC]
    
    posX = posY = posZ = 0
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


@maya_common.libs
def create_center_thingy_from(objects=(), thingy="locator", name="", **kwargs):
    """
    :rtype PyNode:
    """
    pmc = kwargs[maya_common._PMC]

    centered_thingy = None
    objects = pmc.ls(sl=True, fl=True) if not objects else objects
    posX, posY, posZ = get_center_position(objects)

    pmc.select(cl=True)  # in case thingy is joint

    if thingy == "null":
        if not name:
            centered_thingy = pmc.group(em=True)
        else:
            centered_thingy = pmc.group(em=True, n=name)
        centered_thingy.translate.set(posX, posY, posZ)

    elif thingy == "locator":
        if not name:
            centered_thingy = pmc.spaceLocator()
        else:
            centered_thingy = pmc.spaceLocator(n=name)
        centered_thingy.translate.set(posX, posY, posZ)

    elif thingy == "joint":
        if not name:
            centered_thingy = pmc.joint(p=(posX, posY, posZ))
        else:
            centered_thingy = pmc.joint(p=(posX, posY, posZ), n=name)

    pmc.select(cl=True)

    return centered_thingy


@maya_common.libs
def orient_joint(joint, aim_axis, up_axis, **kwargs):
    """
    :param str aim_axis: e.g. "xyz"
    :param str up_axis: e.g. "yup"
    """
    pmc = kwargs[maya_common._PMC]
    logger.info('Orienting joint "{}" with aim axis "{}" and up axis "{}"'.format(
        joint, aim_axis, up_axis
    ))
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


@maya_common.libs
def aim_constrain_with_world_up_object(
    target, 
    obj, 
    aim_vector, 
    up_vector, 
    world_up_obj,
    **kwargs
):
    pmc = kwargs[maya_common._PMC]
    pmc.aimConstraint(
        target, 
        obj, 
        aimVector=aim_vector,
        upVector=up_vector,
        worldUpType="object", 
        worldUpObject=world_up_obj, 
        maintainOffset=False
    )


@maya_common.libs
def bake_aim_constraint_to_joint_orient(joint, **kwargs):
    pmc = kwargs[maya_common._PMC]
    # Remove Constraints
    constraints = set(pmc.listConnections(joint, source=True, destination=False, type="aimConstraint"))
    if constraints:
        try:
            pmc.delete(constraints)
        except:
            pass
    # Freeze Transforms
    pmc.makeIdentity(joint, apply=True, translate=False, scale=False, rotate=True)


@maya_common.libs
def match_transforms(obj, target, translation=True, rotation=True, **kwargs):
    """
    :param PyNode obj, target:
    """
    pmc = kwargs[maya_common._PMC]
    logger.info("Matching transforms of {} to those of {}".format(obj, target))
    # if translation and hasattr(obj, "setTranslation") and hasattr(target, "getTranslation"):
    #     obj.setTranslation(target.getTranslation(space=WORLD_SPACE), space=WORLD_SPACE)
    # if rotation and hasattr(obj, "setRotation") and hasattr(target, "getRotation"):
    #     obj.setRotation(target.getRotation(space=WORLD_SPACE), space=WORLD_SPACE)
    pmc.select(obj, target, replace=True)
    if translation:
        pmc.mel.eval("MatchTranslation")
    if rotation:
        pmc.mel.eval("MatchRotation")


def get_rotate_pivot(node, is_mesh=False):
    """
    :rtype pmc.dt.Point:
    """
    if is_mesh and hasattr(node, "getParent"):
        node = node.getParent()

    if hasattr(node, "getRotatePivot"):
        return node.getRotatePivot(space=WORLD_SPACE)


@maya_common.libs
def is_either_point_or_vector(node, **kwargs):
    pmc = kwargs[maya_common._PMC]
    return isinstance(node, pmc.dt.Point) or isinstance(node, pmc.dt.Vector)


def get_translation_between_two_points(src, dst, as_length=False):
    """
    :param pmc.dt.Point or pmc.dt.Vector src, dst:
    :rtype pmc.dt.Vector:
    """
    if is_either_point_or_vector(src) and is_either_point_or_vector(dst):
        if not as_length:
            return dst - src
        elif hasattr(dst - src, "length"):
            return (dst - src).length()
        else:
            return 0


@maya_common.libs
def make_space_locator(name="", **kwargs):
    pmc = kwargs[maya_common._PMC]
    if not name:
        return pmc.spaceLocator()
    else:
        return pmc.spaceLocator(n=name)


@maya_common.libs
def make_null(name="", children=None, **kwargs):
    pmc = kwargs[maya_common._PMC]
    if not name:
        grp = pmc.group(em=True)
    else:
        grp = pmc.group(em=True, n=name)

    if children is not None:
        pmc.parent(children, grp)

    return grp


def set_locator_local_scale(loc, dimensions):
    """
    :param pmc.nt.Locator loc:
    :param tuple dimensions: width, height, depth
    """
    if hasattr(loc, "getShape"):
        loc = loc.getShape()
    if hasattr(loc, "lsx"):
        loc.lsx.set(dimensions[0])
    if hasattr(loc, "lsy"):
        loc.lsy.set(dimensions[1])
    if hasattr(loc, "lsz"):
        loc.lsz.set(dimensions[2])


def set_translation(node, vector):
    if hasattr(node, "setTranslation"):
        node.setTranslation(vector)


def set_scale(node, scale):
    if hasattr(node, "setScale"):
        if type(scale) not in (list, tuple) and not is_either_point_or_vector(scale):
            scale = (scale, scale, scale)
        node.setScale(scale)


class zero_but_restore_transforms_afterwards(object):

    def __init__(self, node, is_mesh=False):
        super(zero_but_restore_transforms_afterwards, self).__init__()
        self.node = node
        self.xform_node = None
        self.parent = None
        self.rotation = None

        if not is_mesh:
            self.xform_node = self.node
        elif hasattr(node, "getParent"):
            self.xform_node = node.getParent()

        if hasattr(self.xform_node, "getParent"):
            self.parent = self.xform_node.getParent()

        logger.info("Storing transforms for {}".format(self.xform_node))
    
    @maya_common.libs
    def __enter__(self, **kwargs):
        pmc = kwargs[maya_common._PMC]

        self.is_rotation_zero = True

        if self.parent is not None:  # parent to world first
            pmc.parent(self.xform_node, world=True)

        if hasattr(self.xform_node, "getRotation"):
            self.rotation = self.xform_node.getRotation()
        
        if hasattr(self.rotation, "isZero"):
            self.is_rotation_zero = self.rotation.isZero()
            
        if not self.is_rotation_zero and hasattr(self.xform_node, "setRotation"):
            logger.info("Resetting transforms from rotation {}".format(self.rotation))
            self.xform_node.setRotation((0, 0, 0))
    
    @maya_common.libs
    def __exit__(self, *exec_info, **kwargs):
        pmc = kwargs[maya_common._PMC]
        
        if hasattr(self.xform_node, "getRotation"):
            logger.info("Transforms before exiting: rotation {}".format(self.xform_node.getRotation()))
        if not self.is_rotation_zero and hasattr(self.xform_node, "setRotation"):
            logger.info("Restoring transforms for {}".format(self.xform_node))
            self.xform_node.setRotation(self.rotation)
        if self.parent is not None:
            pmc.parent(self.xform_node, self.parent)
