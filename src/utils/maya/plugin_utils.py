import logging
logger = logging.getLogger(__name__)


# MODELING_UNRELATED_PLUGINS = ('hairPhysicalShader', 'lookdevKit', 'shaderFXPlugin', 'VectorRender',
#                               'ik2Bsolver', 'ikSpringSolver', 'matrixNodes', 'quatNodes',
#                               'invertShape', 'poseInterpolator',
#                               'mayaCharacterization', 'mayaHIK', 'MayaMuscle',
#                               'sceneAssembly', 'ATFPlugin',
#                               'BifrostMain', 'bifmeshio', 'bifrostshellnode', 'bifrostvisplugin', 'MASH',
#                               'CloudImportExport')


# def remove_plugin_autoload(plugins):
#     import maya.cmds as cmds
#     for plugin in plugins:
#         try:
#             cmds.pluginInfo(plugin, e=True, autoload=False)
#         except Exception as e:
#             logger.info('{}: Plugin {} is not registered.'.format(e, plugin))
#         else:
#             logger.info('Success. Plugin {} will not be automatically loaded next time.'.format(plugin))


def safe_load_plugin(plugin_name):
    """
    Check if the plugin is loaded, and load it if not
    """
    loaded = False
    try:
        import pymel.core as pmc
    except ImportError:
        pass
    else:
        if not pmc.pluginInfo(plugin_name, q=True, loaded=True):
            logger.info('Plugin "{}" is not loaded. Loading it...'.format(plugin_name))
            try:
                pmc.loadPlugin(plugin_name)
            except Exception as e:
                logger.exception('Unable to load plugin "{}" due to {}.'.format(plugin_name, e))
            else:
                logger.info('Plugin "{}" has been successfully loaded.'.format(plugin_name))
                loaded = True
        else:
            logger.info('Plugin "{}" is already loaded. Proceeding...'.format(plugin_name))
    
    return loaded
