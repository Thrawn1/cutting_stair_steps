class BaseShape():
    def __init__(self, width:float, length:float, thickness:float, material:str, area=None,
                  shape_type = None):
        self.width = width
        self.length = length
        self.thickness = thickness
        self.material = material
        self.area = self.calculate_area()
        self.type = shape_type

    def calculate_area(self)->float:
        self.area = (self.length * self.width) / 1000000
        return self.area
    
class Detail(BaseShape):
    def __init__(self, width:float, length:float, thickness:float, material:str, area:float, shape_type:str, rectangle:bool):
        super().__init__(width, length, thickness, material, area, shape_type)
        self.rectangle = rectangle

class Workpiece(BaseShape):
    def __init__(self, width:float, length:float, thickness:float, material:str, x:float, 
                 y:float, rectangle:bool, shape_type = 'Заготовка'):
        super().__init__(width, length, thickness, material, shape_type)
        self.x = x
        self.y = y
        self.rectangle = rectangle 

    def get_limits_workpiece(self) -> tuple:
        x_min = self.x
        y_max = self.y
        x_max = self.x + self.length
        y_min = self.y - self.width
        return x_max, y_max, x_min, y_min
