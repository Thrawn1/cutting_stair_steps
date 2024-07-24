from Exercise import Exercise
from BaseShape import Detail, Workpiece
from Disk import Disk
from Parameters import Parameters
from MachineLimits import MachineLimits


class Worker:
    """Класс Worker для рассчета координат точек распиловки и движения станка.
        Параметры:
        - exercise (Exercise): объект задания
        - parameters (Parameters): объект параметров резки
        - detail (Detail): объект детали
        - workpiece (Workpiece): объект заготовки
        - disk (Disk): объект диска
        - machine_limits (MachineLimits): объект ограничений станка
        - result (optional): результат работы станка (по умолчанию None)
    """

    def __init__(self, exercise: Exercise, parameters: Parameters,
                 detail: Detail, workpiece: Workpiece, disk: Disk, machine_limits: MachineLimits,
                 result=None) -> None:
        # Проверка типов входных данных
        if not isinstance(exercise, Exercise):
            raise ValueError("exercise должен быть типа Exercise")
        if not isinstance(parameters, Parameters):
            raise ValueError("parameters должен быть типа Parameters")
        if not isinstance(detail, Detail):
            raise ValueError("detail должен быть типа Detail")
        if not isinstance(workpiece, Workpiece):
            raise ValueError("workpiece должен быть типа Workpiece")
        if not isinstance(disk, Disk):
            raise ValueError("disk должен быть типа Disk")
        if not isinstance(machine_limits, MachineLimits):
            raise ValueError("machine_limits должен быть типа MachineLimits")

        self.exercise = exercise    
        self.parameters = parameters
        self.detail = detail
        self.workpiece = workpiece
        self.disk = disk
        self.result = result
        self.machine_limits = machine_limits

    def __str__(self) -> str:
        """
        Возвращает строковое представление объекта Worker.

        Возвращает:
        - str: строковое представление объекта Worker
        """
        return (f"Задание: {self.exercise}\n"
                f"Параметры резки: {self.parameters}\n"
                f"Результат: {self.result}")

    @staticmethod
    def round_coordinates(value:float) -> float:
        """
        Округляет координаты до трех знаков после запятой.

        Параметры:
        - value (float): значение координаты

        Возвращает:
        - float: округленное значение координаты
        """
        return round(value, 3)


    def calculate_coordinates_x_y_cuts(self) -> dict:
        """
        Рассчитывает координаты точек распиловки по осям X и Y.

        Возвращает:
        - dict: словарь с координатами точек распиловки по осям X и Y
        """
        intermediate_result_xy = {'X1X2Y': [], 'Y1Y2X': []}
        X_now = self.workpiece.x
        Y_now = self.workpiece.y
        X_count, Y_count = self.exercise.count_cutter()

        for i in range(Y_count):
            if i == 0:
                Y_now -= self.exercise.offset
            else:
                Y_now -= self.disk.tickness_correction(self.detail.width)

            X1 = self.machine_limits.chek_coordinate('X', (X_now - self.disk.cutter_extension()))
            X2 = self.machine_limits.chek_coordinate('X',
                 X_now + self.workpiece.length + self.disk.cutter_extension())
            Y = self.machine_limits.chek_coordinate('Y', Y_now)

            line = {'X1': self.round_coordinates(X1),
                    'X2': self.round_coordinates(X2),
                    'Y': self.round_coordinates(Y)}
            intermediate_result_xy['X1X2Y'].append(line)

        for i in range(X_count):
            if i == 0:
                X_now += self.exercise.offset
            else:
                X_now += self.disk.tickness_correction(self.detail.length)

            Y1 = self.machine_limits.chek_coordinate('Y', Y_now - self.disk.cutter_extension())
            Y2 = self.machine_limits.chek_coordinate('Y',
                 Y_now + self.workpiece.width + self.disk.cutter_extension())
            X = self.machine_limits.chek_coordinate('X', X_now)

            line = {'Y1': self.round_coordinates(Y1),
                    'Y2': self.round_coordinates(Y2),
                    'X': self.round_coordinates(X)}
            intermediate_result_xy['Y1Y2X'].append(line)

        return intermediate_result_xy

    def calculate_coordinates_z_cuts(self)-> list:
        """
        Рассчитывает координаты точек распиловки по оси Z.

        Возвращает:
        - list: список с координатами точек распиловки по оси Z
        """
        Z_start = 0
        Z_end = -self.detail.thickness
        Z_count = self.parameters.calculate_number_of_steps_to_cut(self.detail)

        intermediate_result_z = [
            Z_start - i * self.parameters.depth_step_forward for i in range(Z_count)
        ]

        last_step = Z_end - intermediate_result_z[-1]
        if 0 < last_step < self.parameters.depth_step_forward:
            if last_step < self.parameters.depth_step_forward / 2:
                intermediate_result_z[-1] = Z_end
            else:
                intermediate_result_z.append(Z_end)
        intermediate_result_z.sort(reverse=True)
        return intermediate_result_z

    def calculate_coordinates(self)-> dict:
        """
        Рассчитывает координаты точек распиловки по осям X, Y и Z.

        Возвращает:
        - tuple: кортеж с координатами точек распиловки по осям X, Y и Z
        """
        intermediate_result_xy = self.calculate_coordinates_x_y_cuts()
        intermediate_result_z = self.calculate_coordinates_z_cuts()
        moving_points = self.calculate_coordinates_of_movement()
        result = {
            'work_cuts': intermediate_result_xy, 
            'Z_step': intermediate_result_z,
            'moving_points': moving_points
            }
        self.result = result
        return result

    def calculate_coordinates_of_movement(self)-> dict:
        """
        Рассчитывает координаты точек движения станка.

        Возвращает:
        - dict: словарь с координатами точек движения станка по осям X и Y
        """
        moving_points = {'X1X2Y': [], 'Y1Y2X': []}
        cuts = self.calculate_coordinates_x_y_cuts()

        for line in cuts['X1X2Y']:
            if line['X1'] < line['X2']:
                moving_point = (line['X1'], line['Y'])
                moving_points['X1X2Y'].append(moving_point)
            elif line['X1'] > line['X2']:
                moving_point = (line['X2'], line['Y'])
                moving_points['X1X2Y'].append(moving_point)
            else:
                print("\033[1;31;43mОшибка. Длина реза равна нулю\033[0m")

        for line in cuts['Y1Y2X']:
            if line['Y1'] < line['Y2']:
                moving_point = (line['X'], line['Y1'])
                moving_points['Y1Y2X'].append(moving_point)
            elif line['Y1'] > line['Y2']:
                moving_point = (line['X'], line['Y2'])
                moving_points['Y1Y2X'].append(moving_point)
            else:
                print("\033[1;31;43mОшибка. Длина реза равна нулю\033[0m")

        return moving_points