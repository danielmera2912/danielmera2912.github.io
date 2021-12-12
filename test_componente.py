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
    assert app.getColor1() == "PySide6.QtGui.QColor.fromRgbF(0.913725, 0.921569, 0.937255, 1.000000)"
def test_color2(app):
    assert app.getColor2() == "PySide6.QtGui.QColor.fromRgbF(0.000000, 0.000000, 1.000000, 1.000000)"
def test_color_after_click(app, qtbot):
    qtbot.mouseClick(app, QtCore.Qt.LeftButton)
    assert app.getBottom() == "PySide6.QtGui.QColor.fromRgbF(0.913725, 0.921569, 0.937255, 1.000000)" or "PySide6.QtGui.QColor.fromRgbF(0.000000, 0.000000, 1.000000, 1.000000)"
    