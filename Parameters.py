class Parameters:
    """Класс для хранения информации о параметрах резки:
    скорости прямого хода резки,
    скорость обратного хода резки,
    скорость заглубления инструмента,
    шаг глубины работы инструмента по прямому ходу,
    шаг глубины работы инструмента по обратному ходу,
    флаг режима зиг-заг"""
    
    def __init__(self, speed_forward, speed_depth, depth_step_forward,
                 speed_backward=None, depth_step_backward=None, zigzag=True,extra_depth=0):
        self.speed_forward = speed_forward
        self.speed_backward = speed_backward if speed_backward is not None else 0.7 * speed_forward
        self.speed_depth = speed_depth
        self.depth_step_forward = depth_step_forward
        self.depth_step_backward = depth_step_backward if depth_step_backward is not None else depth_step_forward
        self.zigzag = zigzag
        self.extra_depth = extra_depth
    def __str__(self):
        return f"Скорость прямого хода: {self.speed_forward}\n" \
               f"Скорость обратного хода: {self.speed_backward}\n" \
               f"Скорость заглубления: {self.speed_depth}\n" \
               f"Шаг глубины по прямому ходу: {self.depth_step_forward}\n" \
               f"Шаг глубины по обратному ходу: {self.depth_step_backward}\n" \
               f"Режим зиг-заг: {self.zigzag}"
    def calculate_number_of_steps_to_cut(self, detail):
        if self.zigzag:
            count = 1
            tickness = detail.thickness
            depth_forward = self.depth_step_forward
            depth_backward = self.depth_step_backward
            while tickness > 0:
                if count % 2 == 0:
                    tickness -= depth_backward
                else:
                    tickness -= depth_forward
                count += 1
            return count
            
        else:
            #Переписать. Нужно учитывать остаток и рассчитывать последний пил отдельно
            return detail.thickness // self.depth_step_forward