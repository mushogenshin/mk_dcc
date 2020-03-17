import logging as logger


MODELING_UNRELATED_PLUGINS = ('hairPhysicalShader', 'lookdevKit', 'shaderFXPlugin', 'VectorRender',
                              'ik2Bsolver', 'ikSpringSolver', 'matrixNodes', 'quatNodes',
                              'invertShape', 'poseInterpolator',
                              'mayaCharacterization', 'mayaHIK', 'MayaMuscle',
                              'sceneAssembly', 'ATFPlugin',
                              'BifrostMain', 'bifmeshio', 'bifrostshellnode', 'bifrostvisplugin', 'MASH',
                              'CloudImportExport')


def remove_plugin_autoload(maya, plugins):
    '''
    :param module maya: Autodesk's maya scripting library
    '''
    for plugin in plugins:
        try:
            maya.cmds.pluginInfo(plugin, e=True, autoload=False)
        except Exception as e:
            logger.info('{}: Plugin {} is not registered.'.format(e, plugin))
        else:
            logger.info('Success. Plugin {} will not Auto Load next time.'.format(plugin))
