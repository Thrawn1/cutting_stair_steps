from Disk import Disk
from Worker import Worker
from Parameters import Parameters

class Block4AxisDenver():
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
        line = f'N{self.count_line} G00 X0 Y0'



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