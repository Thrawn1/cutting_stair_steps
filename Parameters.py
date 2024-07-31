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