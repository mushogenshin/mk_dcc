import logging
logger = logging.getLogger(__name__)


def is_scene_modified():
    try:
        import maya.cmds as cmds
    except ImportError:
        return True
    else:
        return cmds.file(q=True, modified=True)


def get_scene_env():
    try:
        import pymel.core as pmc
    except ImportError:
        return None
    else:
        return pmc.language.Env()


def get_option_var_dict():
    try:
        from pymel.core.language import OptionVarDict
    except ImportError:
        return {}
    else:
        return OptionVarDict()


def get_scene_up_axis():
    return get_option_var_dict().get("upAxisDirection", "")


def get_current_frame(SCENE_ENV=None):
    SCENE_ENV = get_scene_env() if not SCENE_ENV else SCENE_ENV
    if hasattr(SCENE_ENV, "time"):
        return int(SCENE_ENV.time)
    else:
        return 0


def disable_cached_playback():
    try:
        import maya.cmds as cmds
    except ImportError:
        pass
    else:
        try:
            cmds.evaluator(name="cache", enable=0)
        except RuntimeError:
            pass


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


def toggle_interactive_playback(force_play=False, force_pause=False):
    logger.info("Toggling interactive playback")
    try:
        import pymel.core as pmc
    except ImportError:
        pass
    else:
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


def is_playback_running():
    try:
        import maya.cmds as cmds
    except ImportError:
        return
    else:
        return cmds.play(q=True, state=True)


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
