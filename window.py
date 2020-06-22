# coding=utf-8

# import sys
import os
import maya.api.OpenMaya as OpenMaya
import maya.cmds as cmds

import Tcbn_AutoRig

from PySide2 import QtWidgets
from PySide2.QtUiTools import QUiLoader


def maya_useNewAPI():
    pass


def initializePlugin(mobject):
    mplugin = OpenMaya.MFnPlugin(mobject)
    mplugin.registerCommand(ShowTcbnAutoRigWindowCommand.kPluginCmdName,
                            ShowTcbnAutoRigWindowCommand.cmdCreateor)


def uninitializePlugin(mobject):
    mplugin = OpenMaya.MFnPlugin(mobject)
    mplugin.deregisterCommand(ShowTcbnAutoRigWindowCommand.kPluginCmdName)


class ShowTcbnAutoRigWindowCommand(OpenMaya.MPxCommand):
    kPluginCmdName = 'ShowTcbnAutoRigWindow'

    def __init__(self):
        OpenMaya.MPxCommand.__init__(self)

    @staticmethod
    def cmdCreateor():
        return ShowTcbnAutoRigWindowCommand()

    def doIt(self, args):
        app = QtWidgets.QApplication.instance()
        win = SampleWindow()
        win.show()
        app.exec_()


class SampleWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(SampleWindow, self).__init__(parent)

        print(cmds.workspace(q=True, rd=True))
        print(os.getcwd())
        self.ui = QUiLoader().load("./01.ui")
        self.setCentralWidget(self.ui)
        self.ui.pushButton.clicked.connect(self.click_btn)

        self.logic = Tcbn_AutoRig()

    def click_btn(self):
        root = self.ui.lineEdit_5.text()
        self.logic.SearchBody(root)
