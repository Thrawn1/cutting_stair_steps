from Parameters import Parameters
from Worker import Worker
from Disk import Disk
from BaseShape import Detail

class BaseCut:
    """Базовый класс для всех режимов резки"""
    def __init__(self, parameters:Parameters, worker:Worker,disk:Disk,detail:Detail):
        self.disk = disk
        self.parameters = parameters
        self.worker = worker
        self.detail = detail


    def calculate_coordinates_z_cuts(self,Z_count:int)-> list:
        """
        Рассчитывает координаты точек распиловки по оси Z.

        Возвращает:
        - list: список с координатами точек распиловки по оси Z
        """
        Z_start = 0
        Z_end = -self.detail.thickness

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
    
    
    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

class ZigZagCut(BaseCut):
    """Класс для режима зиг-заг"""

    def __init__(self, parameters: Parameters, worker: Worker, disk: Disk, detail: Detail):
        super().__init__(parameters, worker, disk, detail)
        self.name = "ZigZagCut"

    
    def calculate_number_of_steps_to_cut(self):
        count = 1
        tickness = self.detail.thickness
        depth_forward = self.parameters.depth_parameters.depth_step_forward
        depth_backward = self.parameters.depth_parameters.depth_step_backward
        while tickness > 0:
            if count % 2 == 0:
                tickness -= depth_backward
            else:
                tickness -= depth_forward
            count += 1
        return count
    

class ForwardCut(BaseCut):
    """Класс для режима постоянного прямого направления"""
    def __init__(self, parameters: Parameters, worker: Worker, disk: Disk, detail: Detail):
        super().__init__(parameters, worker, disk, detail)

    def calculate_number_of_steps_to_cut(self, detail):
        """
        Рассчитывает количество шагов для распила детали.

        Параметры:
        - detail (Detail): деталь

        Возвращает:
        - int: количество шагов для распила детали
        """
        return int(detail.thickness / self.parameters.depth_parameters.depth_step_forward)
