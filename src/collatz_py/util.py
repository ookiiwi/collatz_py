from math import radians, sin, cos

class Point(tuple):
    def __new__(cls, x=0, y=0):
        return tuple.__new__(cls, (x, y))

    @property
    def x(self):
        return tuple.__getitem__(self, 0)
    
    @property
    def y(self):
        return tuple.__getitem__(self, 1)
    
    def __add__(self, p):
        return Point(self.x + p.x, self.y + p.y)
    
    def __sub__(self, p):
        return Point(self.x - p.x, self.y - p.y)
    
    def __rmul__(self, __value):
        return Point(__value * self.x, __value * self.y)

    def rotate(self, angle, center=None):
        _center = center or Point(0,0)
        angleToRad = radians(angle)
        s = sin(angleToRad)
        c = cos(angleToRad)

        # translate point back to origin
        p = Point(self.x - _center.x, self.y - _center.y)

        xnew = p.x * c - p.y * s
        ynew = p.x * s + p.y * c

        return Point(xnew + _center.x, ynew + _center.y)
