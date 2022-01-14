import PyQt5.Qt as Qt
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore

from src.polygon import Polygon


class ChooseField(QtWidgets.QLabel):
    def __init__(self, parent, num):
        super().__init__(parent)

        self.painter = Qt.QPainter()
        self.pen = Qt.QPen(Qt.QColor(255, 0, 0))
        self.pen.setWidth(1)
        self.brush = Qt.QBrush(Qt.QColor(255, 0, 0))
        self.num = num
        self.update()

    def paintEvent(self, e):
        self.painter.begin(self)
        self.painter.setPen(self.pen)
        self.painter.setBrush(self.brush)
        self.painter.drawPolygon(Polygon((self.width() // 2, self.height() // 2), self.num, 180))
        self.painter.end()

    def set_func(self, func):
        self.func = func

    def mousePressEvent(self, e):
        if e.type() == Qt.QEvent.MouseButtonPress and e.button() == QtCore.Qt.LeftButton:
            self.setStyleSheet('background: green;')
            self.func()


class MainField(QtWidgets.QLabel):
    def __init__(self, parent):
        super().__init__(parent)

        self.setStyleSheet('background: white;')

        self.painter = Qt.QPainter()
        self.pen = Qt.QPen(Qt.QColor(255, 0, 0))
        self.pen.setWidth(1)
        self.brush = Qt.QBrush(Qt.QColor(255, 0, 0))
        self.polygons = []
        self.pos = (0, 0)
        self.f = False
        self.num = 0

    def set_num(self, num):
        self.num = num

    def paintEvent(self, e):
        if self.f:
            self.f = False
            self.painter.begin(self)
            self.painter.setPen(self.pen)
            self.painter.setBrush(self.brush)
            for polygon in self.polygons:
                if polygon.active:
                    pen = Qt.QPen(Qt.QColor(0, 255, 0))
                    pen.setWidth(3)
                    self.painter.setPen(pen)
                    self.painter.drawPolygon(polygon)
                    self.painter.setPen(self.pen)
                    continue
                self.painter.drawPolygon(polygon)
            self.painter.end()

    def mousePressEvent(self, e):
        # Если нажата ПКМ, от забываем выбранный многоугольник
        if e.type() == Qt.QEvent.MouseButtonPress and e.button() == QtCore.Qt.RightButton:
            self.parent().btn6.setStyleSheet('background: white;')
            self.parent().btn7.setStyleSheet('background: white;')
            self.parent().btn3.setStyleSheet('background: white;')
            self.set_num(0)
        # Если ЛКМ, то делаем по логике
        if e.type() == Qt.QEvent.MouseButtonPress and e.button() == QtCore.Qt.LeftButton:
            pos = e.pos()

            self.pos = pos.x(), pos.y()
            in_polygon = None
            actived = False
            for polygon in self.polygons:
                if polygon.containsPoint(Qt.QPointF(self.pos[0], self.pos[1]), QtCore.Qt.OddEvenFill):
                    in_polygon = polygon
                if polygon.active:
                    actived = polygon
                polygon.active = False

            self.f = True
            if not in_polygon:
                if actived:
                    actived.active = False
                    self.update()
                    return
                self.parent().lbl_res.setText('')
                if self.num == 0 and len(self.polygons) == 0:
                    self.f = False
                    self.parent().lbl_res.setText('Выберите мн-ик!')
                    return
                elif len(self.polygons) == 5:
                    self.f = False
                    self.parent().lbl_res.setText('Слишком много!')
                    return
                elif self.num == 0:
                    self.num = self.get_num(self.pos)
                if self.num:
                    self.polygons.append(Polygon(self.pos, self.num, 50))
            else:
                in_polygon.active = True
            self.update()

    def get_active(self):  # Получаем активный
        for polygon in self.polygons:
            if polygon.active:
                return polygon
        return None

    def get_num(self, pos):  # Получаем кол-во углов ближайшего
        coords = [(polygon, (polygon.center[0] - pos[0], polygon.center[1] - pos[1])) for polygon in self.polygons]
        lengths = sorted(list(map(lambda x: (x[0], (x[1][0] ** 2 + x[1][1] ** 2) ** 0.5), coords)), key=lambda x: x[1])
        print(lengths)
        for polygon, length in lengths:
            if length <= 2 * polygon.r:
                return polygon.num
        return 0

    def wheelEvent(self, e):  # Когда колёсико вращается изменяем размер
        polygon = self.get_active()
        if not polygon:
            return
        self.f = True
        if e.angleDelta().y() > 0:
            poly = Polygon(polygon.center, polygon.num, polygon.r + 5)
            poly.active = True
            self.polygons[self.polygons.index(polygon)] = poly
        elif e.angleDelta().y() < 0:
            poly = Polygon(polygon.center, polygon.num, max(5, polygon.r - 5))
            poly.active = True
            self.polygons[self.polygons.index(polygon)] = poly
        self.update()
