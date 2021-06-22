import logging
from src.utils.maya import maya_common


logger = logging.getLogger(__name__)


@maya_common.libs
def is_scene_modified(*args, **kwargs):
    cmds = kwargs[maya_common._CMDS]
    return cmds.file(q=True, modified=True)


@maya_common.libs
def get_scene_env(*args, **kwargs):
    pmc = kwargs[maya_common._PMC]
    return pmc.language.Env()


@maya_common.libs
def get_option_var_dict(*args, **kwargs):
    pmc = kwargs[maya_common._PMC]
    return pmc.language.OptionVarDict()


def get_scene_up_axis():
    return get_option_var_dict().get("upAxisDirection", "")


def get_current_frame(SCENE_ENV=None):
    SCENE_ENV = get_scene_env() if not SCENE_ENV else SCENE_ENV
    if hasattr(SCENE_ENV, "time"):
        return int(SCENE_ENV.time)
    else:
        return 0


@maya_common.libs
def disable_cached_playback(*args, **kwargs):
    cmds = kwargs[maya_common._CMDS]
    cmds.evaluator(name="cache", enable=0)


def set_playback_range(start, end, SCENE_ENV=None):
    logger.info('Updating Playback range from {} to {}'.format(start, end))
    SCENE_ENV = get_scene_env() if not SCENE_ENV else SCENE_ENV
    if hasattr(SCENE_ENV, "setMinTime"):
        SCENE_ENV.setMinTime(start)
    if hasattr(SCENE_ENV, "setMaxTime"):
        SCENE_ENV.setMaxTime(end)


@maya_common.libs
def reset_playback(SCENE_ENV=None, **kwargs):
    pmc = kwargs[maya_common._PMC]
    logger.info("Resetting playback")
    SCENE_ENV = get_scene_env() if not SCENE_ENV else SCENE_ENV

    if pmc.play(q=True, state=True):  # playing
        pmc.play(st=0)  # pause the playback

    if hasattr(SCENE_ENV, "setTime"):
        SCENE_ENV.setTime(0)


@maya_common.libs
def toggle_interactive_playback(force_play=False, force_pause=False, **kwargs):
    pmc = kwargs[maya_common._PMC]
    logger.info("Toggling interactive playback")
    was_playing = pmc.play(q=True, state=True)
    
    # Start forcing
    if force_play:
        pmc.mel.InteractivePlayback()  # activate interactive playback
        return
    if force_pause:
        pmc.play(state=0)
        return
    # End forcing

    if was_playing:
        pmc.play(state=0)  # pause the playback
    else:
        pmc.mel.InteractivePlayback()  # activate interactive playback


@maya_common.libs
def is_playback_running(*args, **kwargs):
    cmds = kwargs[maya_common._CMDS]
    return cmds.play(q=True, state=True)


@maya_common.libs
def delete(obj, **kwargs):
    cmds = kwargs[maya_common._CMDS]
    try:
        cmds.delete(obj)
    except Exception as e:
        logger.exception('Unable to delete "{}" due to {}'.format(obj, e))
    else:
        logger.info('Successfully deleted "{}"'.format(obj))
