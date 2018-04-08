# FlowLayout

"""
This class implements a layout that flows with the container's size.

Based on this Qt documentation example:
https://doc.qt.io/qt-5/qtwidgets-layouts-flowlayout-example.html
"""

from PyQt5 import QtCore
from PyQt5.QtWidgets import *


class FlowLayout(QLayout):
    def __init__(self, parent=None, margin=0, spacing=-1):
        """
        Initializes the FlowLayout.

        :param parent: the parent widget
        :param margin: the size of margins
        :param spacing: the size of spacing
        """
        super(FlowLayout, self).__init__(parent)

        self.itemList = []

        if parent is not None:
            self.setContentsMargins(margin, margin, margin, margin)
        self.setSpacing(spacing)

    def __del__(self):
        """
        Deletes all items in the layout
        """
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item: QLayoutItem):
        """
        Adds an item to the layout.
        :param item: the QLayoutItem to be added.
        """
        self.itemList.append(item)

    def count(self):
        """
        :return: the number of items in the layout
        """
        return len(self.itemList)

    def itemAt(self, index: int):
        """
        Get the item at `index`
        :param index: the index of the desired item
        :return: if found, return the item at `index`, otherwise, return
        `None`.
        """
        if 0 <= index < len(self.itemList):
            return self.itemList[index]
        return None

    def takeAt(self, index: int):
        """
        Pop the item at `index`
        :param index: the index of the desired item
        :return: the item popped, if found, or `None`
        """
        if 0 <= index < len(self.itemList):
            return self.itemList.pop(index)
        return None

    def insertWidget(self, index: int, widget):
        """
        Insert a `widget` at `index`
        :param index: the desired index
        :param widget: the desired widget
        """
        self.itemList.insert(index, QWidgetItem(widget))

    def expandingDirections(self):
        """
        Override for `QLayout`
        :return: Horizontal Orientation
        """
        return QtCore.Qt.Orientations(QtCore.Qt.Horizontal)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width: int):
        """
        :param width: the width to get the height of
        :return: the height
        """
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
