try:
    from PySide2 import QtCore, QtWidgets
except ImportError:
    from PySide import QtCore, QtWidgets


class LoadAndDisplayToLineEdit(object):
    def __init__(self, label="", button_label="Load", clear_label="", add_to_container=True):
        super(LoadAndDisplayToLineEdit, self).__init__()

        self.data = {}

        self.label = QtWidgets.QLabel(label)

        self.line_edit = QtWidgets.QLineEdit()
        self.line_edit.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.line_edit.setReadOnly(True)

        self.load_btn = QtWidgets.QPushButton(button_label)

        if clear_label:
            self.clear_btn = QtWidgets.QPushButton(clear_label)
            self.clear_btn.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        else:
            self.clear_btn = None

        if add_to_container:
            self.container = QtWidgets.QHBoxLayout()
            for wdg in (self.label, self.line_edit, self.load_btn, self.clear_btn):
                if wdg is not None:
                    self.container.addWidget(wdg)
        else:
            self.container = None
