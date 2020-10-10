import logging
logger = logging.getLogger(__name__)


def get_scene_env():
    try:
        import pymel.core as pmc
    except ImportError:
        return None
    else:
        return pmc.language.Env()


def set_playback_range(start, end, SCENE_ENV=None):
    logger.info('Updating Playback range from {} to {}'.format(start, end))
    SCENE_ENV = get_scene_env() if not SCENE_ENV else SCENE_ENV
    if hasattr(SCENE_ENV, "setMinTime"):
        SCENE_ENV.setMinTime(start)
    if hasattr(SCENE_ENV, "setMaxTime"):
        SCENE_ENV.setMaxTime(end)


def reset_playback(SCENE_ENV=None):
    logger.info("Resetting playback")
    SCENE_ENV = get_scene_env() if not SCENE_ENV else SCENE_ENV

    try:
        import pymel.core as pmc
    except ImportError:
        pass
    else:
        if pmc.play(q=True, state=True):  # playing
            pmc.play(st=0)  # pause the playback

    if hasattr(SCENE_ENV, "setTime"):
        SCENE_ENV.setTime(0)


def toggle_interactive_playback():
    logger.info("Toggling interactive playback")
    try:
        import pymel.core as pmc
    except ImportError:
        pass
    else:
        if not pmc.play(q=True, state=True):  # not playing
            pmc.mel.InteractivePlayback()  # activate interactive playback
        else:
            pmc.play(state=0)  # pause the playback


def delete(obj):
    try:
        import maya.cmds as cmds
    except ImportError:
        pass
    else:
        try:
            cmds.delete(obj)
        except Exception as e:
            logger.exception('Unable to delete "{}" due to {}'.format(obj, e))
        else:
            logger.info('Successfully deleted "{}"'.format(obj))
