# coding=utf-8

# import sys
import os
import maya.api.OpenMaya as OpenMaya
import maya.cmds as cmds

from Tcbn_AutoRig import Tcbn_AutoRig

from PySide2 import QtWidgets
from PySide2.QtUiTools import QUiLoader
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin


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
        _app = QtWidgets.QApplication.instance()
        win = SampleWindow()
        win.show()


class SampleWindow(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(SampleWindow, self).__init__(parent)

        print(cmds.workspace(q=True, rd=True))
        print(os.getcwd())

        project_root = cmds.workspace(q=True, rd=True)
        relative_path = "scripts/Tcbn_AutoRig/01.ui"
        ui_filepath = os.path.join(project_root, relative_path)
        if not os.path.exists(ui_filepath):
            print ("FILE IS NOT EXISTS")
        print("LOAD:" + ui_filepath)
        self.ui = QUiLoader().load(ui_filepath)
        self.setCentralWidget(self.ui)
        self.ui.pushButton.clicked.connect(self.click_btn)

        self.logic = Tcbn_AutoRig()

    def click_btn(self):
        root = self.ui.lineEdit_5.text()
        self.logic.SearchBody(root)
