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
    def __init__(self, number, diameter, support_thickness, cutter_thickness, material,name,Z_sec=50,Z_approach=5):
        self.number = number
        self.diameter = diameter
        self.support_thickness = support_thickness
        self.cutter_thickness = cutter_thickness
        self.material = material
        self.name = name
        self.Z_sec = Z_sec
        self.Z_approach = Z_approach
    #Метод, рассчитвающий на сколько продлевается пил в зависимости от диаметра диска
    def cutter_extension(self):
        return self.diameter / 2 + self.cutter_thickness
    def tickness_correction(self, size):
        return size + self.cutter_thickness
    
class Parameters:
    """Класс для хранения информации о параметрах резки:
    скорости прямого хода резки,
    скорость обратного хода резки,
    скорость заглубления инструмента,
    шаг глубины работы инструмента по прямому ходу,
    шаг глубины работы инструмента по обратному ходу,
    флаг режима зиг-заг"""
    
    def __init__(self, speed_forward, speed_depth, depth_step_forward, 
                 speed_backward=None, depth_step_backward=None, zigzag=True,extra_depth=0):
        self.speed_forward = speed_forward
        self.speed_backward = speed_backward if speed_backward is not None else 0.7 * speed_forward
        self.speed_depth = speed_depth
        self.depth_step_forward = depth_step_forward
        self.depth_step_backward = depth_step_backward if depth_step_backward is not None else depth_step_forward
        self.zigzag = zigzag
        self.extra_depth = extra_depth

    def __str__(self):
        return f"Скорость прямого хода: {self.speed_forward}\n" \
               f"Скорость обратного хода: {self.speed_backward}\n" \
               f"Скорость заглубления: {self.speed_depth}\n" \
               f"Шаг глубины по прямому ходу: {self.depth_step_forward}\n" \
               f"Шаг глубины по обратному ходу: {self.depth_step_backward}\n" \
               f"Режим зиг-заг: {self.zigzag}"
    def calculate_number_of_steps_to_cut(self, detail):
        if self.zigzag:
            count = 1
            tickness = detail.thickness
            depth_forward = self.depth_step_forward
            depth_backward = self.depth_step_backward
            while tickness > 0:
                if count % 2 == 0:
                    tickness -= depth_backward
                else:
                    tickness -= depth_forward
                count += 1
            return count
            
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
    def round_coordinates(self, value):
        return round(value, 3)
    def calculate_coordinates_X_Y_cuts(self):
        intermediate_result_xy = []
        X_START = self.workpiece.x
        Y_START = self.workpiece.y
        X_NOW = X_START
        Y_NOW = Y_START
        X_length = self.workpiece.length
        Y_length = self.workpiece.width
        X_count, Y_count = self.exercise.count_cutter()
        if self.exercise.offset > 0:
            X_count += 1
            Y_count += 1
        for i in range(Y_count):
            if i == 0:
                Y_NOW -= self.exercise.offset
            line = (self.round_coordinates(X_NOW-self.disk.cutter_extension()), self.round_coordinates(X_NOW + X_length + self.disk.cutter_extension()),self.round_coordinates(Y_NOW))
            intermediate_result_xy.append(line)
            Y_NOW -= self.disk.tickness_correction(self.detail.width)
        for i in range(X_count):
            if i == 0:
                X_NOW += self.exercise.offset
            line = (self.round_coordinates(Y_NOW - self.disk.cutter_extension()), self.round_coordinates(Y_NOW + Y_length + self.disk.cutter_extension()),self.round_coordinates(X_NOW))
            intermediate_result_xy.append(line)
            X_NOW += self.disk.tickness_correction(self.detail.length)
        return intermediate_result_xy
    def calculate_coordinates_Z_cuts(self):
        intermediate_result_z = []
        Z_START = 0
        Z_END = -1 * self.detail.thickness
        Z_NOW = Z_START
        Z_count = self.parameters.calculate_number_of_steps_to_cut(self.detail)
        flag_not_full_step_cut = False
        for _ in range(Z_count):
            Z_NOW -= self.parameters.depth_step_forward
            if -1*Z_END+(-1*Z_NOW) < self.parameters.depth_step_forward:
                if (Z_END+(-1*Z_NOW)) < self.parameters.depth_step_forward/2:
                    Z_NOW = Z_END
                else:
                    flag_not_full_step_cut = True
            intermediate_result_z.append(Z_NOW)
            if flag_not_full_step_cut:
                intermediate_result_z.append(Z_END)
        return intermediate_result_z

    def calculate_coordinates(self):
        intermediate_result_xy = self.calculate_coordinates_X_Y_cuts()
        intermediate_result_z = self.calculate_coordinates_Z_cuts()
        return intermediate_result_xy, intermediate_result_z


class Block_4axis_Denver():
    """Класс для генерации блоков кода для станка Denver с 4-мя осями"""
    def __init__(self,name_programm,disk:Disk,worker:Worker,parametrs:Parameters,count_line=1):
        self.count_line = count_line
        self.name_programm = name_programm
        self.disk = disk 
        self.worker = worker
        self.parametrs = parametrs

    def start_block(self):
        start_blok = []
        line = f";({self.name_programm})"
        start_blok.append(line)
        line = f"N{self.count_line} (UAO,1)"
        self.count_line += 1
        start_blok.append(line)
        line = f"N{self.count_line} G331 S60"
        self.count_line += 1
        start_blok.append(line)
        line = f"N{self.count_line} (UIO,Z(E31))"
        self.count_line += 1
        start_blok.append(line)
        line = f";{self.disk.name} [D. {self.disk.diameter} ] D. {self.disk.diameter}"
        start_blok.append(line)
        line = f"N{self.count_line} G398"
        self.count_line += 1
        start_blok.append(line)
        line = f"N{self.count_line} #G0 C0"
        self.count_line += 1
        start_blok.append(line)
        line = f"N{self.count_line} T{self.disk.number}"
        self.count_line += 1
        start_blok.append(line)
        line = f"N{self.count_line} M52"
        self.count_line += 1
        start_blok.append(line)
        line = f"N{self.count_line} G376"
        self.count_line += 1
        start_blok.append(line)
        line = f"N{self.count_line} G17"
        self.count_line += 1
        start_blok.append(line)
        line = f"N{self.count_line} G317 P12"
        self.count_line += 1
        start_blok.append(line)
        line = f"N{self.count_line} L365=3"
        self.count_line += 1
        start_blok.append(line)
        line = f"N{self.count_line} M41"
        self.count_line += 1
        start_blok.append(line)
        line = ";(MMSystem)"
        start_blok.append(line)
        line = f"N{self.count_line} M44"
        self.count_line += 1
        start_blok.append(line)
        line = f"N{self.count_line} G397 A0"
        self.count_line += 1
        start_blok.append(line)
        line = f"N{self.count_line} M41"
        self.count_line += 1
        start_blok.append(line)
        self.start_block = start_blok
    def end_block(self):
        end_blok = []
        line = f"N{self.count_line} G00 Z{self.disk.Z_sec}"
        self.count_line += 1
        end_blok.append(line)
        line = f"N{self.count_line} M44"
        self.count_line += 1
        end_blok.append(line)
        line = f"N{self.count_line} M05"
        self.count_line += 1
        end_blok.append(line)
        line = f"N{self.count_line} M09 M10"
        self.count_line += 1
        end_blok.append(line)
        line = f"N{self.count_line} G398"
        self.count_line += 1
        end_blok.append(line)
        line = f"N{self.count_line} #G0 G79 X0 Y0 C0"
        self.count_line += 1
        end_blok.append(line)
        line = f"N{self.count_line} M30"
        self.count_line += 1
        end_blok.append(line)
        line = '\n'
        end_blok.append(line)
        self.end_block = end_blok

    def work_blok(self):
        work_blok = []
        line_start = f'N{self.count_line} M140[1]'
        work_blok.append(line_start)
        self.count_line += 1
        line_end = f'N{self.count_line} M140[0]'
        f_speed = self.parametrs.speed_forward
        b_speed = self.parametrs.speed_backward
        zf_speed = self.parametrs.speed_depth
        all_coordinate_xy = self.worker.calculate_coordinates()[0]
        all_coordinate_z = self.worker.calculate_coordinates()[1]
        for coordinate in all_coordinate_xy:
            count = 1
            for z in all_coordinate_z:
                if count % 2 != 0:
                    line = f'N{self.count_line} X{coordinate[0]} F{f_speed}'
                    self.count_line += 1
                    work_blok.append(line)
                    line = f'N{self.count_line} X{coordinate[0]} Z{z} F{zf_speed}'
                    self.count_line += 1
                    work_blok.append(line)
                else:
                    line = f'N{self.count_line} X{coordinate[1]} F{b_speed}'
                    self.count_line += 1
                    work_blok.append(line)
                    line = f'N{self.count_line} X{coordinate[1]} Z{z} F{zf_speed}'
                    self.count_line += 1
                    work_blok.append(line)
        work_blok.append(line_end)
        return work_blok

    def moving_between_work_blok(self):
        moving_between_work_blok = []
        line = f'N{self.count_line} Z{self.disk.Z_sec}'
        moving_between_work_blok.append(line)
        self.count_line += 1
        line = f'N{self.count_line} G00 X0 Y0 C0'



"""
N47 #G00 Z50
N48 G00 X708.31298 Y-1341.1325
N49 G00 Z5
N50 G1 Y-1341.1325 Z-5.08333 F300"""
"""
N16 #G00 X708.31298 Y-1545.3325 C0
N17 G00 Z50
N18 M07 M08
N19 S1750 M04
N20 G00 Z5
"""

class Generator_gcode():
    """Класс для генерации g-code"""
    def __init__(self, worker,parameters):
        self.worker = worker
        self.parameters = parameters
    def generate_gcode(self):
        pass


detali = Detail(length=1100, width=420, thickness=120, angle1=90, angle2=90, material="granite")
zagotovka = Workpiece(length=3000, width=1500, thickness=20, angle1=90, angle2=90, material="granite", x=500, y=-500)
disk = Disk(number=20, diameter=510, support_thickness=3, cutter_thickness=3.8, material="granite",name="Granit Marimal D510")
zadanie = Exercise(detali, zagotovka, disk, 2, offset=10)
parametry = Parameters(speed_forward=1000, speed_depth=100, depth_step_forward=5, zigzag=True) 
worker = Worker(zadanie, parametry, detali, zagotovka, disk)
print(worker.calculate_coordinates())