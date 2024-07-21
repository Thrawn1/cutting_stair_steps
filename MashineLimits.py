class MachineLimits():
    """Класс описывающий ограничения станка"""
    def __init__(self,x_min,x_max,y_min,y_max,type_mashine):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.type_mashine = type_mashine

    def chek_coordinate(self,axis,value):
        if axis == 'X':
            if self.x_min<value<self.x_max:
                return value
            else:
                if value < self.x_min:
                    return self.x_min
                else:
                    return self.x_max
        elif axis == 'Y':
            if self.y_min<value<self.y_max:
                return value
            else:
                if value<self.y_min:
                    return self.y_min
                else:
                    return self.y_max