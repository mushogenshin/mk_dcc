import logging as logger


def remove_plugin_autoload(func, plugins):
    '''
    :param function object func: should be Maya cmds.pluginInfo
    '''
    for plugin in plugins:
        try:
            func(plugin, e=True, autoload=False)
        except Exception as e:
            logger.info('{}: Plugin {} is not registered.'.format(e, plugin))
        else:
            logger.info('Success. Plugin {} will not Auto Load next time.'.format(plugin))
