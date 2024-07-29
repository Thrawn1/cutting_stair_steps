from old_code.v2.Disk import Disk
from Worker import Worker
from Parameters import Parameters

class Block4AxisDenver:
    """Класс для генерации блоков кода для станка Denver с 4-мя осями"""
    
    def __init__(self, name_programm, disk: Disk, worker: Worker, parameters: Parameters, count_line=1):
        self.count_line = count_line
        self.name_programm = name_programm
        self.disk = disk 
        self.worker = worker
        self.parameters = parameters

    @staticmethod
    def get_coordinates_axis_c(key):
        """Получение координаты по оси С"""
        if key == 'X1X2Y':
            return 0
        elif key == 'Y1Y2X':
            return 90
        else:
            raise ValueError("Неверный ключ")


    def start_block(self):
        """Генерация стартового блока команд"""
        start_move_key = self.worker.get_start_move_key()
        start_block = [
            f";({self.name_programm})",
            f"N{self.count_line} (UAO,1)", 
            f"N{self.count_line + 1} G331 S60",
            f"N{self.count_line + 2} (UIO,Z(E31))",
            f";{self.disk.name} [D. {self.disk.diameter} ] D. {self.disk.diameter}",
            f"N{self.count_line + 3} G398",
            f"N{self.count_line + 4} #G0 C{self.get_coordinates_axis_c(start_move_key)}",
            f"N{self.count_line + 5} T{self.disk.number}",
            f"N{self.count_line + 6} M52",
            f"N{self.count_line + 7} G376",
            f"N{self.count_line + 8} G17",
            f"N{self.count_line + 9} G317 P12",
            f"N{self.count_line + 10} L365=3",
            f"N{self.count_line + 11} M41"
        ]
        self.count_line += len(start_block)
        return start_block

    def work_block(self):
        """Генерация рабочего блока команд"""
        work_block = [f'N{self.count_line} M140[1]']
        self.count_line += 1
        
        line_end = f'N{self.count_line} M140[0]'
        self.count_line += 1
        
        f_speed = self.parameters.speed_forward
        b_speed = self.parameters.speed_backward
        zf_speed = self.parameters.speed_depth
        all_coordinate_xy, all_coordinate_z = self.worker.calculate_coordinates()

        for coordinate in all_coordinate_xy:
            for count, z in enumerate(all_coordinate_z, start=1):
                if count % 2 != 0:
                    work_block.append(f'N{self.count_line} X{coordinate[0]} F{f_speed}')
                    self.count_line += 1
                    work_block.append(f'N{self.count_line} X{coordinate[0]} Z{z} F{zf_speed}')
                else:
                    work_block.append(f'N{self.count_line} X{coordinate[1]} F{b_speed}')
                    self.count_line += 1
                    work_block.append(f'N{self.count_line} X{coordinate[1]} Z{z} F{zf_speed}')
                self.count_line += 1

        work_block.append(line_end)
        return work_block

    def moving_between_work_blok(self):
        """Генерация блока команд для перемещения между рабочими блоками"""
        moving_between_work_blok = [f'N{self.count_line} Z{self.disk.Z_sec}']
        self.count_line += 1
        moving_between_work_blok.append(f'N{self.count_line} G00 X0 Y0')
        self.count_line += 1
        moving_between_work_blok.append(f'N{self.count_line} G00 Z{self.disk.Z_approach}')
        self.count_line += 1
        return moving_between_work_blok

# """
# N47 #G00 Z50
# N48 G00 X708.31298 Y-1341.1325
# N49 G00 Z5
# N50 G1 Y-1341.1325 Z-5.08333 F300"""
# """
# N16 #G00 X708.31298 Y-1545.3325 C0
# N17 G00 Z50
# N18 M07 M08
# N19 S1750 M04
# N20 G00 Z5
# """