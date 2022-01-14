import math
import PyQt5.Qt as Qt


class Polygon(Qt.QPolygonF):
    def __init__(self, center, num, r=20):
        self.center = center
        self.active = False
        self.r = r
        self.num = num
        centerx, centery = center
        points = []
        alpha = 2 * math.pi / num
        for i in range(num):
            x = r * math.cos(alpha * i) + centerx
            y = r * math.sin(alpha * i) + centery
            points.append(Qt.QPointF(x, y))
        super().__init__(points)

    def get_pos(self):
        return self.center
