import sys
import PyQt5.Qt as Qt
import PyQt5.QtWidgets as QtWidgets

from src.widgets import ChooseField, MainField


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.size = self.width, self.height = 1400, 1300
        self.setGeometry(0, 0, self.width, self.height)
        self.setFont(Qt.QFont(None, 18))

        # Кнопка выхода
        self.btnExit = Qt.QPushButton(self)
        self.btnExit.setText('Exit')
        self.btnExit.setGeometry(self.width - 250 - 5, self.height - 100 - 5, 250, 100)
        self.btnExit.setStyleSheet('background: orange;')
        self.btnExit.clicked.connect(sys.exit)

        # Кнопка удаления
        self.btnDelete = QtWidgets.QPushButton(self)
        self.btnDelete.setText('Delete')
        self.btnDelete.setGeometry(self.width - 500 - 10, self.height - 100 - 5, 250, 100)
        self.btnDelete.setStyleSheet('background: white;')
        self.btnDelete.clicked.connect(self.delete)

        self.lbl_res = QtWidgets.QLabel(self)
        self.lbl_res.setGeometry(self.width - 850 - 15, self.height - 100 - 5, 400, 100)

        # Главное поле
        self.drawing_field = MainField(self)
        self.drawing_field.setGeometry(self.width // 3 - 5, 5, 2 * self.width // 3, self.height - 120)

        # Поля для выбора
        self.btn3 = ChooseField(self, 3)
        self.btn3.setStyleSheet('background: white;')
        self.btn3.setGeometry(25, 25, 400, 400)
        self.btn3.set_func(self.switch_3)
        self.btn6 = ChooseField(self, 6)
        self.btn6.setStyleSheet('background: white;')
        self.btn6.setGeometry(25, 450, 400, 400)
        self.btn6.set_func(self.switch_6)
        self.btn7 = ChooseField(self, 7)
        self.btn7.setStyleSheet('background: white;')
        self.btn7.setGeometry(25, 875, 400, 400)
        self.btn7.set_func(self.switch_7)

    def delete(self):  # Удаление
        active = self.drawing_field.get_active()
        if active:
            self.drawing_field.polygons.remove(active)
            self.drawing_field.f = True
            self.drawing_field.update()

    def keyPressEvent(self, e):
        if e.type() == Qt.QEvent.KeyPress:
            if e.key() == 16777223:
                self.delete()

    def switch_3(self):
        self.btn6.setStyleSheet('background: white;')
        self.btn7.setStyleSheet('background: white;')
        self.drawing_field.set_num(3)

    def switch_6(self):
        self.btn3.setStyleSheet('background: white;')
        self.btn7.setStyleSheet('background: white;')
        self.drawing_field.set_num(6)

    def switch_7(self):
        self.btn6.setStyleSheet('background: white;')
        self.btn3.setStyleSheet('background: white;')
        self.drawing_field.set_num(7)


if __name__ == '__main__':
    app = Qt.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
