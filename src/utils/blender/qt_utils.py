import sys
import os
import logging

import bpy

qt_binding = os.environ.get('QT_PREFERRED_BINDING', '') # correct qt bindings

if qt_binding:
    if qt_binding == 'PySide2':
        from PySide2 import QtWidgets, QtCore
    if qt_binding == 'PyQt5':
        from PyQt5 import QtWidgets, QtCore
else:
    from PySide2 import QtWidgets, QtCore

logger = logging.getLogger('qtutils')


class QtWindowEventLoop(bpy.types.Operator):
    """Allows PyQt or PySide to run inside Blender"""

    bl_idname = 'screen.qt_event_loop'
    bl_label = 'Qt Event Loop'

    def __init__(self, view, uic_main_window, control):
        self.view = view
        self.uic_main_window = uic_main_window
        self._control = control

    def modal(self, context, event):
        # bpy.context.window_manager
        window_manager = context.window_manager

        try:  # using try since we got error where the widget is already deleted
            if not self._view.isVisible():
                # if widget is closed
                logger.debug('Finishing modal operator')
                window_manager.event_timer_remove(self._timer)
                return {'FINISHED'}
            else:
                logger.debug('Processing the events for Qt window')
                self.event_loop.processEvents()
                self._app.sendPostedEvents(None, 0)
        except:
            pass

        return {'PASS_THROUGH'}
    
    def execute(self, context):
        logger.debug('Executing operator')

        self._app = QtWidgets.QApplication.instance()
        # instance() gives the possibility to have multiple windows
        # and close it one by one

        if not self._app:
            # create the first instance
            self._app = QtWidgets.QApplication(sys.argv)

        self.event_loop = QtCore.QEventLoop()
        self._view = self.view(self.uic_main_window, self._control)
        self._view.show()

        logger.debug(self._app)
        logger.debug(self._view)

        # run modal
        window_manager = context.window_manager
        self._timer = window_manager.event_timer_add(1 / 120, window=context.window)
        context.window_manager.modal_handler_add(self)

        return {'RUNNING_MODAL'}
