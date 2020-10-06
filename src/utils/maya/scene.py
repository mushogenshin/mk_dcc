def get_scene_env():
    try:
        import pymel.core as pmc
    except ImportError:
        return None
    else:
        return pmc.language.Env()
