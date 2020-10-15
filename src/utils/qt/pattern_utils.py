from functools import partial

try:
    from PySide2 import QtCore
    from PySide2.QtWidgets import *
except ImportError:
    from PySide import QtCore
    from PySide.QtGui import *  # equivalents of PySide2.QtWidgets child classes live here


class LoadAndDisplayToLineEdit(object):
    def __init__(self, label="", load_btn_label="Load", clear_btn_label=""):
        super(LoadAndDisplayToLineEdit, self).__init__()
        self.data = {"loaded": []}

        self.label = QLabel(label)
        self.label.setDisabled(True)
        self.label.setStyleSheet("font-size: 9px")

        self.line_edit = QLineEdit()
        self.line_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.line_edit.setReadOnly(True)
        self.print_line_edit_method = None

        self.load_btn = QPushButton(load_btn_label)

        if clear_btn_label is not None:
            self.clear_btn = QPushButton(clear_btn_label)
            self.clear_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
            self.clear_btn.setMaximumWidth(max(20 * len(clear_btn_label), 20))
        else:
            self.clear_btn = None

    def add_to_container(self, target=None, row=None):
        """
        Create a QHBoxLayout if no target is given, or populate to a 
        given QGridLayout as target, using provided row
        :param QGridLayout|None target:
        :param int|None row:
        """
        wdgs = (self.label, self.line_edit, self.load_btn, self.clear_btn)
        if not target:
            self.container = QHBoxLayout()
        else:
            self.container = target

        for i, wdg in enumerate(wdgs):
            if wdg is not None:
                if not isinstance(row, int):
                    self.container.addWidget(wdg)
                else:
                    self.container.addWidget(wdg, row, i)
        return self.container

    def update_app_model(self, app_model_data, data_key):
        """
        :param str data_key: support for keys of two-level nested dicts, e.g. "init.mesh_A"
        """
        if "." in data_key:
            key_1, key_2 = data_key.split(".")
            app_model_data[key_1][key_2] = self.data["loaded"]
        else:
            app_model_data[data_key] = self.data["loaded"]

    def load_btn_clicked(self, func, **kwargs):
        """
        :param callable func:
        """
        # Stash what returned
        if callable(func):
            self.data["loaded"] = func(**kwargs)
        self.update_line_edit("load")

    def loaded(self):
        self.load_btn.click()
    
    def clear_btn_clicked(self, func):
        """
        :param callable func:
        """
        if callable(func):
            self.data["loaded"] = func()
        self.update_line_edit()

    def cleared(self):
        if hasattr(self.clear_btn, "clicked"):
            self.clear_btn.click()

    def update_line_edit(self, method=""):
        """
        Display internal data to line edit
        :param str method: Providing hint if is "load"
        """
        data = self.data["loaded"]
        if callable(self.print_line_edit_method):
            data = self.print_line_edit_method(data)
        if not data:
            data = "{--Nothing loaded--}" if method == "load" else ""
        self.line_edit.setText(str(data))

    def create_simple_connections(self, load_func, clear_func, print_func=None):
        """
        :param callable print_func: return a list in place of loaded data
        that is processed for nice printing
        """
        self.load_btn.clicked.connect(partial(
            self.load_btn_clicked,
            func=load_func
        ))
        if self.clear_btn:
            self.clear_btn.clicked.connect(partial(
                self.clear_btn_clicked,
                func=clear_func
            ))
        self.print_line_edit_method = print_func

    def connect_app_model_update(self, app_model_data, data_key):
        # TODO: ensure these signals always emitted *after* the signals above
        self.load_btn.clicked.connect(partial(
            self.update_app_model,
            app_model_data=app_model_data,
            data_key=data_key
        ))
        if self.clear_btn:    
            self.clear_btn.clicked.connect(partial(
                self.update_app_model,
                app_model_data=app_model_data,
                data_key=data_key
            ))       


class LabeledSpinBox(object):
    def __init__(self, label="", data_key="", double=False, default_value=0):
        super(LabeledSpinBox, self).__init__()

        self.data = default_value  # store right away 
        # to avoid QSpinBox|QDoubleSpinBox auto truncation

        self.data_key = data_key
        self.is_double = double
        self.label = QLabel(label)
        self.label.setDisabled(True)

        self.spin_box = QSpinBox() if not self.is_double else QDoubleSpinBox()
        self.spin_box.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.spin_box.setValue(self.data)

    def set_step(self, step):
        self.spin_box.setSingleStep(step)

    def set_decimals(self, decimals):
        self.spin_box.setDecimals(decimals)
        self.spin_box.setValue(self.data)  # reapply value from stored data

    def value(self):
        # may want to update self.data as well
        return self.spin_box.value()

    def add_to_container(self, target=None, row=None, start_column=None):
        """
        Create a QHBoxLayout if no target is given, or populate to a 
        given QGridLayout as target, using provided row and column
        :param QGridLayout|None target:
        :param int|None row, column:
        """
        wdgs = (self.label, self.spin_box)
        if not target:
            self.container = QHBoxLayout()
        else:
            self.container = target

        for i, wdg in enumerate(wdgs):
            if not (isinstance(row, int) and isinstance(start_column, int)):
                self.container.addWidget(wdg)
            else:
                self.container.addWidget(wdg, row, start_column + i)
        return self.container


class CollapsibleGroupBox(object):
    """
    Encapsulate a QGroupBox and make it collapsible
    """
    def __init__(self, group_box, expanded_height=0, collapsed_height=20):
        """
        :param QGroupBox group_box:
        """
        super(CollapsibleGroupBox, self).__init__()

        self.group_box = group_box
        self.expanded_height = max(self.group_box.height(), expanded_height)
        self.collapsed_height = collapsed_height

        self.group_box.toggled.connect(self.toggle_height)

    def toggle_height(self, checked):
        height = self.collapsed_height if not checked else self.expanded_height
        self.group_box.setFixedHeight(height)

    def toggled(self):
        self.group_box.setChecked(not self.group_box.isChecked())
