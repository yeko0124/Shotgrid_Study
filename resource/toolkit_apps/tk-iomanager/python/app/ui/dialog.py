# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import resources_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1044, 685)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.lineEdit = QLineEdit(Dialog)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout_2.addWidget(self.lineEdit)

        self.select_dir = QPushButton(Dialog)
        self.select_dir.setObjectName(u"select_dir")

        self.horizontalLayout_2.addWidget(self.select_dir)

        self.create_excel = QPushButton(Dialog)
        self.create_excel.setObjectName(u"create_excel")

        self.horizontalLayout_2.addWidget(self.create_excel)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.check_all_btn = QPushButton(Dialog)
        self.check_all_btn.setObjectName(u"check_all_btn")

        self.horizontalLayout_3.addWidget(self.check_all_btn)

        self.uncheck_all_btn = QPushButton(Dialog)
        self.uncheck_all_btn.setObjectName(u"uncheck_all_btn")

        self.horizontalLayout_3.addWidget(self.uncheck_all_btn)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.seq_model_view = QTableView(Dialog)
        self.seq_model_view.setObjectName(u"seq_model_view")

        self.verticalLayout.addWidget(self.seq_model_view)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.save_excel = QPushButton(Dialog)
        self.save_excel.setObjectName(u"save_excel")

        self.horizontalLayout.addWidget(self.save_excel)

        self.publish = QPushButton(Dialog)
        self.publish.setObjectName(u"publish")

        self.horizontalLayout.addWidget(self.publish)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"The Current Sgtk Environment", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Path : ", None))
        self.select_dir.setText(QCoreApplication.translate("Dialog", u"Select", None))
        self.create_excel.setText(QCoreApplication.translate("Dialog", u"Load", None))
        self.check_all_btn.setText(QCoreApplication.translate("Dialog", u"Check All", None))
        self.uncheck_all_btn.setText(QCoreApplication.translate("Dialog", u"Uncheck All", None))
        self.save_excel.setText(QCoreApplication.translate("Dialog", u"Save", None))
        self.publish.setText(QCoreApplication.translate("Dialog", u"Publish", None))
    # retranslateUi

