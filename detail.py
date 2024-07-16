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
    
class Parameters:
    """Класс для хранения информации о параметрах резки:
    скорости прямого хода резки,
    скорость обратного хода резки,
    скорость заглубления инструмента,
    шаг глубины работы инструмента по прямому ходу,
    шаг глубины работы инструмента по обратному ходу,
    флаг режима зиг-заг"""
    
    def __init__(self, speed_forward, speed_depth, depth_step_forward, 
                 speed_backward=None, depth_step_backward=None, zigzag=True):
        self.speed_forward = speed_forward
        self.speed_backward = speed_backward if speed_backward is not None else 0.7 * speed_forward
        self.speed_depth = speed_depth
        self.depth_step_forward = depth_step_forward
        self.depth_step_backward = depth_step_backward if depth_step_backward is not None else depth_step_forward
        self.zigzag = zigzag

    def __str__(self):
        return f"Скорость прямого хода: {self.speed_forward}\n" \
               f"Скорость обратного хода: {self.speed_backward}\n" \
               f"Скорость заглубления: {self.speed_depth}\n" \
               f"Шаг глубины по прямому ходу: {self.depth_step_forward}\n" \
               f"Шаг глубины по обратному ходу: {self.depth_step_backward}\n" \
               f"Режим зиг-заг: {self.zigzag}"
    def calculate_number_of_steps_to_cut(self, detail):
        if self.zigzag:
            return (detail.thickness - self.depth_step_forward) // (self.depth_step_forward + self.depth_step_backward) + 1
        else:
            #Переписать. Нужно учитывать остаток и рассчитывать последний пил отдельно
            return detail.thickness // self.depth_step_forward
class Exercise():
    """Класс описывающий задание - объект деталь, объект заготовка, объект диск, количество 
    деталей и отсуп от края заготовки"""
    def __init__(self, detail, workpiece, disk, count,offset=0):
        self.detail = detail
        self.workpiece = workpiece
        self.disk = disk
        self.count = count
        self.offset = offset
    def __str__(self):
        return f"Деталь: {self.detail.width}x{self.detail.length}x{self.detail.thickness}\n" \
               f"Заготовка: {self.workpiece.width}x{self.workpiece.length}x{self.workpiece.thickness}\n" \
               f"Диск: {self.disk.diameter}x{self.disk.support_thickness}x{self.disk.cutter_thickness}\n" \
               f"Количество: {self.count}"
    #Метод, рассчитывающий количество пилов по осям X и Y 
    def count_cutter(self):
        X_count = (self.workpiece.length-self.offset) // self.detail.length
        Y_count = (self.workpiece.width-self.offset) // self.detail.width
        return X_count, Y_count

class Worker():
    """Класс для рассчета работы станка. Принимает объект задания, заготовки , детали, 
    объект параметров резки"""
    def __init__(self, exercise:Exercise, parameters:Parameters,
                 detail:Detail,workpiece:Workpiece,disk:Disk,result=None):
        self.exercise = exercise
        self.parameters = parameters
        self.detail = detail
        self.workpiece = workpiece
        self.disk = disk
        self.result = result
    def __str__(self):
        return f"Задание: {self.exercise}\n" \
               f"Параметры резки: {self.parameters}\n" \
               f"Результат: {self.result}"
    def calculate_coordinates_X_Y_cuts(self):
        intermediate_result_xy = []
        X_START = self.workpiece.x
        Y_START = self.workpiece.y
        X_NOW = X_START
        Y_NOW = Y_START
        X_length = self.workpiece.length
        Y_length = self.workpiece.width
        X_count, Y_count = self.exercise.count_cutter()
        for i in range(Y_count):
            if i == 0:
                Y_NOW -= self.exercise.offset
            line = (X_NOW-self.disk.cutter_extension(), X_NOW +X_length + self.disk.cutter_extension(),Y_NOW)
            intermediate_result_xy.append(line)
            Y_NOW -= self.detail.width
        for i in range(X_count):
            if i == 0:
                X_NOW += self.exercise.offset
            line = (Y_NOW - self.disk.cutter_extension(), Y_NOW + Y_length + self.disk.cutter_extension(), X_NOW)
            intermediate_result_xy.append(line)
            X_NOW += self.detail.length
    def calculate_coordinates_Z_cuts(self):
        intermediate_result_z = []
        Z_START = 0
        Z_NOW = Z_START
        Z_count = self.parameters.calculate_number_of_steps_to_cut(self.detail)
        step = self.parameters.depth_step_forward



class Generator_gcode():
    """Класс для генерации g-code"""
    def __init__(self, worker):
        self.worker = worker
    def generate_gcode(self):
        pass
