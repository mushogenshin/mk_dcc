try:
    # from PySide2 import QtCore
    from PySide2.QtWidgets import *
except ImportError:
    # from PySide import QtCore
    from PySide.QtGui import *


def show_warning_box(parent, message="Are you sure?", title="Warning"):
    reply = QMessageBox.warning(
        parent, 
        title, 
        message,
        QMessageBox.Yes | QMessageBox.No
    )
    return is_reply_yes_or_no(reply)


def is_reply_yes_or_no(reply):
    if reply in (QMessageBox.StandardButton.Yes, 1):
        return True
    elif reply in (QMessageBox.StandardButton.No, 0):
        return False
    else:
        return False


def show_info_box(parent, message="Notice", title="Info"):
    return QMessageBox.information(
        parent, 
        title, 
        message,
        QMessageBox.Ok
    )

# if __name__ == "__main__":
#     import sys
#     app = QApplication(sys.argv)
#     some_widget = QPushButton("Hello World!")

#     some_widget.show()
#     reply = show_warning_box(some_widget)
#     print(reply)
#     reply = show_info_box(some_widget)
#     print(reply)
#     sys.exit(app.exec_())
