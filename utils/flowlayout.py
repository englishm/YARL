# FlowLayout

"""
This class implements a layout that flows with the container's size.

Based on this Qt documentation example:
https://doc.qt.io/qt-5/qtwidgets-layouts-flowlayout-example.html
"""

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *


class FlowLayout(QLayout):
    def __init__(self, parent=None, margin=0, spacing=-1):
        super(FlowLayout, self).__init__(parent)

        self.itemList = []

        if parent is not None:
            self.setContentsMargins(margin, margin, margin, margin)
        self.setSpacing(spacing)

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item: QLayoutItem):
        self.itemList.append(item)

    def count(self):
        return len(self.itemList)

    def itemAt(self, index: int):
        if 0 <= index < len(self.itemList):
            return self.itemList[index]
        return None

    def takeAt(self, index: int):
        if 0 <= index < len(self.itemList):
            return self.itemList.pop(index)
        return None

    def insertWidget(self, index: int, widget):
        self.itemList.insert(index, QWidgetItem(widget))

    def expandingDirections(self):
        return QtCore.Qt.Orientations(QtCore.Qt.Horizontal)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width: int):
        return self.doLayout(QtCore.QRect(0, 0, width, 0), True)

    def setGeometry(self, rect: QtCore.QRect):
        super(FlowLayout, self).setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QtCore.QSize()

        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())

        margin, _, _, _ = self.getContentsMargins()

        size += QtCore.QSize(2 * margin, 2 * margin)
        return size

    def doLayout(self, rect: QtCore.QRect, testOnly: bool):
        x = rect.x()
        y = rect.y()
        lineHeight = 0

        for item in self.itemList:
            wid = item.widget()
            space = self.spacing()
            next_x = x + item.sizeHint().width() + space
            if next_x - space > rect.right() and lineHeight > 0:
                x = rect.x()
                y = y + lineHeight + space
                next_x = x + item.sizeHint().width() + space
                lineHeight = 0

            if not testOnly:
                item.setGeometry(QtCore.QRect(QtCore.QPoint(x, y),
                                              item.sizeHint()))

            x = next_x
            lineHeight = max(lineHeight, item.sizeHint().height())

        return y + lineHeight - rect.y()


if __name__ == '__main__':
    import sys

    class Window(QWidget):
        def __init__(self):
            super(Window, self).__init__()

            flowLayout = FlowLayout()
            flowLayout.addWidget(QPushButton("Short"))
            flowLayout.addWidget(QPushButton("Longer"))
            flowLayout.addWidget(QPushButton("Different text"))
            flowLayout.addWidget(QPushButton("More text"))
            flowLayout.addWidget(QPushButton("Even longer button text"))
            self.setLayout(flowLayout)

            self.setWindowTitle("Flow Layout")


    app = QApplication(sys.argv)
    m = Window()
    m.show()
    sys.exit(app.exec_())
