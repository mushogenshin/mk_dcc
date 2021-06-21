import logging
from src.utils.maya import maya_common


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


def create_center_thingy_from(objects=(), thingy="locator", name=""):
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
    logger.info("Matching transforms of {} to those of {}".format(obj, target))
    try:
        import pymel.core as pmc
    except ImportError:
        pass
    else:
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
    try:
        import pymel.core as pmc
    except ImportError:
        pass
    else:
        if is_mesh and hasattr(node, "getParent"):
            node = node.getParent()

        if hasattr(node, "getRotatePivot"):
            return node.getRotatePivot(space=WORLD_SPACE)


def is_either_point_or_vector(node):
    try:
        import pymel.core as pmc
    except ImportError:
        pass
    else:
        return isinstance(node, pmc.dt.Point) or isinstance(node, pmc.dt.Vector)


def get_translation_between_two_points(src, dst, as_length=False):
    """
    :param pmc.dt.Point or pmc.dt.Vector src, dst:
    :rtype pmc.dt.Vector:
    """
    try:
        import pymel.core as pmc
    except ImportError:
        pass
    else:
        if is_either_point_or_vector(src) and is_either_point_or_vector(dst):
            if not as_length:
                return dst - src
            elif hasattr(dst - src, "length"):
                return (dst - src).length()
            else:
                return 0


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


def make_null(name="", children=None):
    try:
        import pymel.core as pmc
    except ImportError:
        pass
    else:
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
    try:
        import pymel.core as pmc
    except ImportError:
        pass
    else:
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

        try:
            import pymel.core as pmc
        except ImportError:
            pass
        else:
            if not is_mesh:
                self.xform_node = self.node
            elif hasattr(node, "getParent"):
                self.xform_node = node.getParent()

            if hasattr(self.xform_node, "getParent"):
                self.parent = self.xform_node.getParent()

            logger.info("Storing transforms for {}".format(self.xform_node))
    
    def __enter__(self):
        self.is_rotation_zero = True
        try:
            import pymel.core as pmc
        except ImportError:
            pass
        else:
            if self.parent is not None:  # parent to world first
                pmc.parent(self.xform_node, world=True)

            if hasattr(self.xform_node, "getRotation"):
                self.rotation = self.xform_node.getRotation()
            
            if hasattr(self.rotation, "isZero"):
                self.is_rotation_zero = self.rotation.isZero()
                
            if not self.is_rotation_zero and hasattr(self.xform_node, "setRotation"):
                logger.info("Resetting transforms from rotation {}".format(self.rotation))
                self.xform_node.setRotation((0, 0, 0))
            
    def __exit__(self, *exec_info):
        try:
            import pymel.core as pmc
        except ImportError:
            pass
        else:
            if hasattr(self.xform_node, "getRotation"):
                logger.info("Transforms before exiting: rotation {}".format(self.xform_node.getRotation()))
            if not self.is_rotation_zero and hasattr(self.xform_node, "setRotation"):
                logger.info("Restoring transforms for {}".format(self.xform_node))
                self.xform_node.setRotation(self.rotation)
            if self.parent is not None:
                pmc.parent(self.xform_node, self.parent)
