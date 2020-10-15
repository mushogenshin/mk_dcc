import logging
logger = logging.getLogger(__name__)


def get_center_position(objects):
    posX = posY = posZ = 0
    try:
        import pymel.core as pmc
    except ImportError:
        pass
    else:
        pos = [pmc.xform(obj, q=True, ws=True, bb=True) for obj in objects]

        if pos:
            val = len(pos)
            pos = [sum(e) for e in zip(*pos)]
            pos = [e / val for e in pos]

            posX = (pos[0] + pos[3]) / 2
            posY = (pos[1] + pos[4]) / 2
            posZ = (pos[2] + pos[5]) / 2

    return posX, posY, posZ


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

        pmc.select(objects, r=True)

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
