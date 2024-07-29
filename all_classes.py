class Validator():
    pass

class MachineLimits():
    pass
class ModesCutting():
    pass
class Disk():
    pass
class BaseShape():
    pass
class Algorithm():
    pass
class Detail(BaseShape):
    def __init__(self, shape):
        self.shape = shape
class Workpiece(BaseShape):
    def __init__(self, shape):
        self.shape = shape
class Parameters():
    def __init__(self, machine_limits:MachineLimits, disk:Disk,modes_cutting:ModesCutting):
        self.maschine_limits = machine_limits
        self.disk = disk
        self.modes_cutting = modes_cutting
class WorkOrder():
    def __init__(self, workpiece:Workpiece, detail:Detail, parameters:Parameters):
        self.workpiece = workpiece
        self.detail = detail
        self.parameters = parameters
class Cutter():
    def __init__(self, workorder:WorkOrder):
        self.workorder = workorder
    def calculate_algorithm(self)->Algorithm:
        alogorithm = Algorithm()
        return alogorithm

class Postprocessor():
    def __init__(self,algorithm:Algorithm):
        self.algorithm = algorithm
    def get_gcode(self):
        file = open('gcode.txt', 'w')
        file.write('G-code')
        return file
