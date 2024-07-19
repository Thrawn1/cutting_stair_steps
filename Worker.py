from detail import Exercise, Parameters, Detail,Workpiece, Disk, MaсhineLimits

class Worker():
    """Класс для рассчета работы станка. Принимает объект задания, заготовки , детали, 
    объект параметров резки"""
    def __init__(self, exercise:Exercise, parameters:Parameters,
                 detail:Detail,workpiece:Workpiece,disk:Disk,mashine_limits:MaсhineLimits,
                 result=None):
        self.exercise = exercise
        self.parameters = parameters
        self.detail = detail
        self.workpiece = workpiece
        self.disk = disk
        self.result = result
        self.mashine_limits = mashine_limits
    def __str__(self):
        return f"Задание: {self.exercise}\n" \
               f"Параметры резки: {self.parameters}\n" \
               f"Результат: {self.result}"
    def round_coordinates(self, value):
        return round(value, 3)
    def calculation_of_completely_finished_details(self):
        X_count,Y_count = self.exercise.count_cutter()
        if self.exercise.offset>0:
            total_number_details = (X_count-1)*(Y_count-1)
        else:
            total_number_details = X_count*Y_count
        self.total_number_details = total_number_details
        if total_number_details == 0:
            print("\033[1;31;43mИз заготовки нельзя напилить детали по заданию!\033[0m")
        elif total_number_details < self.exercise.count:
            print(f"""Количество деталей, которые можно изготовить из данной заготовки: 
                   {total_number_details}/nКоличество деталей, которые нужны по заданию:
                  {self.exercise.count}/n
                  Нужно напилить еще: {self.exercise.count-total_number_details}""")
        elif total_number_details>total_number_details:
            print(f"""Количество деталей, которые можно изготовить из данной заготовки: 
                   {total_number_details}/nКоличество деталей, которые нужны по заданию:
                  {self.exercise.count}/n
                  Перееизбыток деталей: {total_number_details-self.exercise.count}/n
                  Пожалуйста, скорректируйте размер заготовки""")
        else:
            print('Задание можно выполнить из заготовки')

    def calculate_coordinates_X_Y_cuts(self):
        intermediate_result_xy = {}
        #'X1X2Y' - Движения по оси X - распиловка вдоль длинной части стола
        #'Y1Y2X' - Движения по оси Y - распиловка вдоль ширины стола
        intermediate_result_xy['X1X2Y'] = []
        intermediate_result_xy['Y1Y2X'] = []
        X_NOW = self.workpiece.x
        Y_NOW = self.workpiece.y
        X_count, Y_count = self.exercise.count_cutter()
        for i in range(Y_count):
            if i == 0:
                Y_NOW -= self.exercise.offset
            else:
                Y_NOW -= self.disk.tickness_correction(self.detail.width)
            # X1 - координата первой точки по оси X
            # X2 - координата второй точки по оси X
            # Y - координата по оси Y
            #В зависимости от того, куда направлено движение, X1 и X2 
            # попеременно являются начальной и конечной точкой
            X1 = self.maсhine_limits.chek_coordinate('X', \
            (X_NOW - self.disk.cutter_extension()))
            X2 = self.maсhine_limits.chek_coordinate('X', \
            (X_NOW + self.workpiece.length + self.disk.cutter_extension()))
            Y = self.maсhine_limits.chek_coordinate('Y',Y_NOW) 
            line = {'X1':self.round_coordinates(X1),
                    'X2':self.round_coordinates(X2),
                    'Y':self.round_coordinates(Y)}            

            intermediate_result_xy['X1X2Y'].append(line)
        for i in range(X_count):
            if i == 0:
                X_NOW += self.exercise.offset
            else:
                X_NOW += self.disk.tickness_correction(self.detail.length)
            # Y1 - координата первой точки по оси Y
            # Y2 - координата второй точки по оси Y
            # X - координата по оси X
            #В зависимости от того, куда направлено движение, Y1 и Y2
            # попеременно являются начальной и конечной точкой
            Y1 = self.maсhine_limits.chek_coordinate('Y', \
            Y_NOW - self.disk.cutter_extension())
            Y2 = self.maсhine_limits.chek_coordinate('Y', \
            Y_NOW + self.workpiece.width + self.disk.cutter_extension())
            X = self.maсhine_limits.chek_coordinate('X',X_NOW)
            line = {'Y1':self.round_coordinates(Y1),
                    'Y2':self.round_coordinates(Y2),
                    'X':self.round_coordinates(X)}
            intermediate_result_xy['Y1Y2X'].append(line)       
        return intermediate_result_xy

    def calculate_coordinates_Z_cuts(self):
        Z_START = 0
        Z_END = -self.detail.thickness
        Z_count = self.parameters.calculate_number_of_steps_to_cut(self.detail)
        
        # Используем генератор списка для создания списка координат Z
        intermediate_result_z = [Z_START - i * self.parameters.depth_step_forward 
                                 for i in range(Z_count)]
        
        # Проверяем, нужно ли добавить последний не полный шаг
        last_step = Z_END - intermediate_result_z[-1]
        if 0 < last_step < self.parameters.depth_step_forward:
            if last_step < self.parameters.depth_step_forward / 2:
                # Если последний шаг меньше половины глубины шага, просто добавляем Z_END
                intermediate_result_z[-1] = Z_END
            else:
                # Если последний шаг больше или равен половине, добавляем его как отдельный шаг
                intermediate_result_z.append(Z_END)
        intermediate_result_z.sort(reverse=True)
        return intermediate_result_z

    def calculate_coordinates(self):
        intermediate_result_xy = self.calculate_coordinates_X_Y_cuts()
        intermediate_result_z = self.calculate_coordinates_Z_cuts()
        return intermediate_result_xy, intermediate_result_z

    def Calculation_of_coordinates_of_movement(self):
        moving_points = {}
        moving_points['X1X2Y'] = []
        moving_points['Y1Y2X'] = []
        cuts = self.calculate_coordinates_X_Y_cuts()
        if len(cuts['X1X2Y']) != 0:
            for line in cuts['X1X2Y']:
                if cuts['X1X2Y']['X1']<cuts['X1X2Y']['X2']:
                    moving_point = (cuts['X1X2Y']['X1'],cuts['X1X2Y']['Y'])
                    moving_points['X1X2Y'].append(moving_point)
                elif cuts['X1X2Y']['X1']>cuts['X1X2Y']['X2']:
                    moving_point = (cuts['X1X2Y']['X2'],cuts['X1X2Y']['Y'])
                    moving_points['X1X2Y'].append(moving_point)
                else:
                    print("\033[1;31;43mОшибка. Длинна реза равна нулю\033[0m")

        elif len(cuts['Y1Y2X']) != 0:
            for line in cuts['Y1Y2X']:
                if cuts['Y1Y2X']['Y1']<cuts['Y1Y2X']['Y2']:
                    moving_point = (cuts['Y1Y2X']['X'],cuts['Y1Y2X']['Y1'])
                    moving_points['Y1Y2X'].append(moving_point)
                elif cuts['Y1Y2X']['Y1']>cuts['Y1Y2X']['Y2']:
                    moving_point = (cuts['Y1Y2X']['X'],cuts['Y1Y2X']['Y2'])
                    moving_points['Y1Y2X'].append(moving_point)
                else:
                    print("\033[1;31;43mОшибка. Длинна реза равна нулю\033[0m")
    