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
    
class Parameters():
    """Класс для хранения информации о параметрах резки:
    скорости прямого хода резки,
     скорость обратного хода резки,
      скорость заглубления инструмента, 
       шаг глубины работы инструмента,
        флаг режима зиг-заг"""
    def __init__(self, speed_forward, speed_backward, speed_depth, depth_step, zigzag):
        self.speed_forward = speed_forward
        self.speed_backward = speed_backward
        self.speed_depth = speed_depth
        self.depth_step = depth_step
        self.zigzag = zigzag
class Exercise():
    """Класс описывающий задание - объект деталь, объект заготовка, объект диск, количество 
    деталей"""
    def __init__(self, detail, workpiece, disk, count):
        self.detail = detail
        self.workpiece = workpiece
        self.disk = disk
        self.count = count
    def __str__(self):
        return f"Деталь: {self.detail.width}x{self.detail.length}x{self.detail.thickness}\n" \
               f"Заготовка: {self.workpiece.width}x{self.workpiece.length}x{self.workpiece.thickness}\n" \
               f"Диск: {self.disk.diameter}x{self.disk.support_thickness}x{self.disk.cutter_thickness}\n" \
               f"Количество: {self.count}"
    #Метод, рассчитывающий количество пилов по осям X и Y 
    def count_cutter(self):
        X_count = self.workpiece.length // self.detail.length
        Y_count = self.workpiece.width // self.detail.width
        return X_count, Y_count