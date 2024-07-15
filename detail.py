class Detail():
    """Класс для хранения информации о детали - ее ширине, длине, толщине, углах между сторонами и
     материале"""
    def __init__(self, width, length, thickness, angle1, angle2, material):
        self.width = width
        self.length = length
        self.thickness = thickness
        self.angle1 = angle1
        self.angle2 = angle2
        self.material = material

class Workpiece(Detail):
    """Класс для хранения информации о заготовке - ее ширине, длине, толщине,материале и координата
    X и Y правой верхней точки"""
    def __init__(self, width, length, thickness, angle1, angle2, material, x, y):
        super().__init__(width, length, thickness, angle1, angle2, material)
        self.x = x
        self.y = y

class Disk():
    """Класс для хранения информации о диске - его номере, диаметре, толщине суппорта,
    толщине резца и указание какой материал он режет"""
    def __init__(self, number, diameter, support_thickness, cutter_thickness, material):
        self.number = number
        self.diameter = diameter
        self.support_thickness = support_thickness
        self.cutter_thickness = cutter_thickness
        self.material = material
    #Метод, рассчитвающий на сколько продлевается пил в зависимости от диаметра диска
    def cutter_extension(self):
        return self.diameter / 2 + self.cutter_thickness
    def tickness_correction(self, size):
        return size + self.cutter_thickness/2
    
class Exercise():
    """Класс описывающий задание - объект деталь, объект заготовка, объект диск, количество 
    деталей"""
    def __init__(self, detail, workpiece, disk, count):
        self.detail = detail
        self.workpiece = workpiece
        self.disk = disk
        self.count = count
