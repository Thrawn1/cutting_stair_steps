from detail import Exercise, Parameters, Detail,Workpiece, Disk, MashineLimits

class Worker():
    """Класс для рассчета работы станка. Принимает объект задания, заготовки , детали, 
    объект параметров резки"""
    def __init__(self, exercise:Exercise, parameters:Parameters,
                 detail:Detail,workpiece:Workpiece,disk:Disk,mashine_limits:MashineLimits,result=None):
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

    
    def calculate_coordinates(self,count,coordinate_now,axis):
        for i in range(count):
            if i ==0:
                if axis == 'X':
                    coordinate_now+=self.exercise.offset
                    main_axis_coordinate = self.workpiece.x
                elif axis == 'Y':
                    coordinate_now-=self.exercise.offset
                    main_axis_coordinate = self.workpiece.y
  
    
    
    
    def calculate_coordinates_X_Y_cuts(self):
        intermediate_result_xy = []
        X_NOW = self.workpiece.x
        Y_NOW = self.workpiece.y
        X_count, Y_count = self.exercise.count_cutter()
        for i in range(Y_count):
            if i == 0:
                Y_NOW -= self.exercise.offset
            line = (self.round_coordinates(X_NOW-self.disk.cutter_extension()), 
                    self.round_coordinates(X_NOW + self.workpiece.length + self.disk.cutter_extension()),
                    self.round_coordinates(Y_NOW))
            intermediate_result_xy.append(line)
            Y_NOW -= self.disk.tickness_correction(self.detail.width)
        for i in range(X_count):
            if i == 0:
                X_NOW += self.exercise.offset
            if (Y_NOW - self.workpiece.width - self.disk.cutter_extension()) < -1898:
                Y = -1898
            else:
                Y = Y_NOW - self.workpiece.width - self.disk.cutter_extension()
            line = {'Y1':self.round_coordinates(Y_NOW + self.disk.cutter_extension()),
                    'Y2':self.round_coordinates(Y),'X':self.round_coordinates(X_NOW)}
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

    def Calculation_of_coordinates_of_movement(self):
        cuts = self.calculate_coordinates_X_Y_cuts()