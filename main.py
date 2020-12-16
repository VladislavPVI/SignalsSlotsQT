import sys

from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class USD(QObject):

    def __init__(self, cost):
        super().__init__()
        self.cost = cost

    def getCost(self):
        return self.cost

    def setCost(self, cost):
        self.cost = cost

    def updateCost(self, cf):
        self.cost = self.cost * cf

    oil_update = pyqtSignal(float)


class RUB(QObject):
    def __init__(self, cost):
        super().__init__()
        self.cost = cost

    def getCost(self):
        return self.cost

    def setCost(self, cost):
        self.cost = cost

    def updateCost(self, cf):
        self.cost = self.cost * cf

    oil_update = pyqtSignal(float)


class OIL(QObject):
    def __init__(self, cost):
        super().__init__()
        self.cost = cost

    def getCost(self):
        return self.cost

    def setCost(self, cost):
        self.cost = cost


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.oil = OIL(50.89)
        self.rub = RUB(53.14)
        self.rub.oil_update.connect(self.rub.updateCost)
        self.usd = USD(73.5)
        self.usd.oil_update.connect(self.usd.updateCost)

        self.initUI()

    def initUI(self):
        label = QLabel('Генератор курсов валют', self)
        label.setFont(QtGui.QFont('Arial', 20, weight=QtGui.QFont.Bold))
        label.adjustSize()
        label.move(40, 20)

        label_oil = QLabel('Нефть, $/баррель', self)
        label_oil.setFont(QtGui.QFont('Arial', 15))
        label_oil.adjustSize()
        label_oil.move(50, 80)

        self.edit_oil = QDoubleSpinBox(self)
        self.edit_oil.setValue(self.oil.getCost())
        self.edit_oil.setMaximum(200)
        self.edit_oil.move(240, 80)

        label_usd = QLabel('Доллар, ₽', self)
        label_usd.setFont(QtGui.QFont('Arial', 15))
        label_usd.adjustSize()
        label_usd.move(50, 120)

        self.edit_usd = QDoubleSpinBox(self)
        self.edit_usd.setReadOnly(True)
        self.edit_usd.setMaximum(200)
        self.edit_usd.setValue(self.usd.getCost())
        self.edit_usd.move(240, 120)

        label_rub = QLabel('Рубль, ₽', self)
        label_rub.setFont(QtGui.QFont('Arial', 15))
        label_rub.adjustSize()
        label_rub.move(50, 160)

        self.edit_rub = QDoubleSpinBox(self)
        self.edit_rub.setReadOnly(True)
        self.edit_rub.setMaximum(200)
        self.edit_rub.setValue(self.rub.getCost())
        self.edit_rub.move(240, 160)

        btn1 = QPushButton("Обновить", self)
        btn1.move(150, 220)

        btn1.clicked.connect(self.buttonClicked)

        self.setFixedSize(400, 270)
        self.setWindowTitle('Генератор курсов валют на ТГ')
        self.show()

    def buttonClicked(self):
        cost_field = self.edit_oil.value()
        cost_old = self.oil.getCost()
        if cost_old != cost_field:
            cf = cost_field / cost_old
            self.oil.setCost(cost_field)
            self.rub.oil_update.emit(cf)
            self.usd.oil_update.emit(cf ** -1)
            self.edit_rub.setValue(self.rub.getCost())
            self.edit_usd.setValue(self.usd.getCost())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
