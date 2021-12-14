import unittest, pytest
from PySide6 import QtCore, QtGui
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QApplication, QWidget
from componente import componente

@pytest.fixture
def app(qtbot):
    test_componente = componente()
    qtbot.addWidget(test_componente)

    return test_componente


def test_color1(app):
    assert app.getColor1() == QtGui.QColor("#E9EBEF")
def test_color2(app):
    assert app.getColor2() == QtGui.QColor("#0000FF")
def test_color_after_click(app, qtbot):
    qtbot.mouseClick(app, QtCore.Qt.LeftButton)
    assert app.getBottom() == QtGui.QColor("#E9EBEF") or QtGui.QColor("#0000FF")
    