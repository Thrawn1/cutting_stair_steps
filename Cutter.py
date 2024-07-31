from WorkOrder import WorkOrder
class Algorithm():
    pass

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
    def calculate_coordinates_of_movement(self)->dict:
        pass

