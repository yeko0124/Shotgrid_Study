# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from tank.platform.qt import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(431, 392)
        self.horizontalLayout = QtGui.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.logo_example = QtGui.QLabel(Dialog)
        self.logo_example.setText("")
        self.logo_example.setPixmap(QtGui.QPixmap(":/res/sg_logo.png"))
        self.logo_example.setObjectName("logo_example")
        self.horizontalLayout.addWidget(self.logo_example)
        self.context = QtGui.QLabel(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.context.sizePolicy().hasHeightForWidth())
        self.context.setSizePolicy(sizePolicy)
        self.context.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.context.setObjectName("context")
        self.horizontalLayout.addWidget(self.context)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "The Current Sgtk Environment", None, QtGui.QApplication.UnicodeUTF8))
        self.context.setText(QtGui.QApplication.translate("Dialog", "Your Current Context: ", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc



class SearchWidgetDemo(QtGui.QWidget):
    """
    Demonstrates the use of the the SearchWidget class available in the
    tk-frameworks-qtwidgets framework.
    """

    def __init__(self, parent=None):
        """
        Initialize the demo widget.
        """

        # call the base class init
        super(SearchWidgetDemo, self).__init__(parent)

        # create the search widget instance
        search = search_widget.SearchWidget(self)
        search.setFixedWidth(300)

        search.set_placeholder_text("This is the placeholder text...")

        # info
        info_lbl = QtGui.QLabel(
            "Type in the search to see the <tt>search_edited</tt> signal "
            "firing. Then press <strong>Enter</strong> on the keyboard to see "
            "the <tt>search_changed</tt> signal fire."
        )
        info_lbl.setWordWrap(True)

        # signal lbl
        self._signal_lbl = QtGui.QLabel()

        # lay out the UI
        layout = QtGui.QVBoxLayout(self)
        layout.setSpacing(20)
        layout.addStretch()
        layout.addWidget(info_lbl)
        layout.addWidget(search)
        layout.addWidget(self._signal_lbl)
        layout.addStretch()

        # ---- connect the signals

        search.search_edited.connect(self._on_search_edited)
        search.search_changed.connect(self._on_search_changed)

    def _on_search_edited(self, text):
        """Update the signal label."""
        self._signal_lbl.setText(
            "<tt>search_edited</tt>: "
            "<font style='color:#18A7E3;'>%s</font>" % (text,)
        )

    def _on_search_changed(self, text):
        """Update the signal label."""
        self._signal_lbl.setText(
            "<tt>search_changed</tt>: "
            "<font style='color:#18A7E3;'>%s</font>" % (text,)
        )