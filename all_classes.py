class Validator():
    pass

class MachineLimits():
    def __init__(self, x_min:float, x_max:float, y_min:float, y_max:float, 
                 model_machine:str,range_c:tuple) -> None:
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.model_machine = model_machine
        self.range_c = range_c
    def check_coordinate_axis_x_y(self, axis:str, value:float)->float:
        if axis == 'X':
            return max(self.x_min, min(value, self.x_max))
        elif axis == 'Y':
            return max(self.y_min, min(value, self.y_max))
        else:
            raise ValueError("Axis must be 'X' or 'Y'")

    def check_coordinate_axis_c(self, value:float)->bool:
        if max(self.range_c) >= value >= min(self.range_c):
            return True
        else:
            return False

class DepthParameters():
    def __init__(self, depth_step_forward:float, depth_step_backward:float, 
                 extra_depth:float) -> None:
        self.depth_step_forward = depth_step_forward
        self.depth_step_backward = depth_step_backward
        self.extra_depth = extra_depth

class SpeedParameters():
    def __init__(self, speed_forward:int, speed_backward:int, speed_depth:int) -> None:
        self.speed_forward = speed_forward
        self.speed_backward = speed_backward
        self.speed_depth = speed_depth

class BaseCuttingMode():
    def __init__(self, speed_parameters:SpeedParameters, depth_parameters:DepthParameters) -> None:
        self.speed_parameters = speed_parameters
        self.depth_parameters = depth_parameters

class ZigzagMode(BaseCuttingMode):
    def __init__(self, speed_parameters:SpeedParameters, depth_parameters:DepthParameters,) -> None:
        super().__init__(speed_parameters, depth_parameters)

class Disk():
    def __init__(self, number:int, diameter:float, support_thickness:float, cutter_thickness:float,
                  processing_material:str,name_disk:str) -> None:
        self.number = number
        self.diameter = diameter
        self.support_thickness = support_thickness
        self.cutter_thickness = cutter_thickness
        self.processing_material = processing_material
        self.name_disk = name_disk

    def get_cutter_extension(self)->float:
        return self.diameter / 2 + self.cutter_thickness
    
    def get_thickness_correction(self,size:float)->float:
        return size + self.cutter_thickness

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

class Algorithm():
    pass

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

class Parameters():
    def __init__(self, machine_limits:MachineLimits, speed_parameters:SpeedParameters, 
                 depth_parameters:DepthParameters, cutting_mode:BaseCuttingMode, height_secure=50,
                 height_approach=5,):
        self.machine_limits = machine_limits
        self.speed_parameters = speed_parameters
        self.depth_parameters = depth_parameters
        self.cutting_mode = cutting_mode
        self.height_secure = height_secure
        self.height_approach = height_approach

class WorkOrder():
    def __init__(self, detail:Detail, workpiece:Workpiece, disk:Disk, parameters:Parameters, 
                 count:int, offset:float):
        self.detail = detail
        self.workpiece = workpiece
        self.disk = disk
        self.parameters = parameters
        self.count = count
        self.offset = offset
        self.total_number_details = self.calculate_total_number_of_details()
        self.check_total_number_of_details()

    def count_cutter(self)->tuple:
        X_count = (self.workpiece.length-self.offset) // self.detail.length
        Y_count = (self.workpiece.width-self.offset) // self.detail.width
        if self.offset > 0:
            X_count +=1
            Y_count +=1
        return X_count, Y_count
    
    def calculate_total_number_of_details(self)->int:
        x_count, y_count = self.count_cutter()
        if self.offset > 0:
            return (x_count-1) * (y_count-1)
        else:
            return x_count * y_count

    def calculation_efficiency(self)->float:
        return (self.calculate_total_number_of_details()*self.detail.area *
                 100) / self.workpiece.area

    def check_total_number_of_details(self):
        #Метод будет переписан в будущем
        self.total_number_details = self.calculate_total_number_of_details()
        if self.total_number_details < self.count:
            raise ValueError("Невозможно изготовить такое количество деталей")
        elif self.total_number_details == 0:
            raise ValueError("Из заготовки нельзя напилить детали по заданию!")
        elif self.total_number_details == self.count:
            print("Все детали изготовлены")
        elif self.total_number_details > self.count:
            print("Изготовлено деталей больше чем нужно")

class Cutter():
    def __init__(self, workorder:WorkOrder):
        self.workorder = workorder
        self.alogorithm = None

    def calculate_algorithm(self)->None:
        pass
    def calculate_coordinates_axis_x_y_cuts(self)->dict:
        pass
    def calculate_coordinates_axis_z_cuts(self)->dict:
        pass
    def get_coordinate_axis_c(self)->float:
        pass
    def get_coordinate_axis_a(self)->float:
        pass
    def coordinates_of_movement(self)->dict:
        pass
    def calculate_algorithm(self)->None:
        pass

class Postprocessor():
    #Класс будет переписан после написания всех остальных классов
    def __init__(self,algorithm:Algorithm):
        self.algorithm = algorithm
    def get_gcode(self):
        file = open('gcode.txt', 'w')
        file.write('G-code')
        return file
