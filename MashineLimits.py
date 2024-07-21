class MachineLimits():

    """Класс описывающий ограничения станка
    Параметры:
    - x_min (float): минимальное значение координаты X
    - x_max (float): максимальное значение координаты X
    - y_min (float): минимальное значение координаты Y
    - y_max (float): максимальное значение координаты Y
    - type_mashine (float): модель станка
    """

    def __init__(self, x_min: float, x_max: float, y_min: float,
                  y_max: float, model_machine: str) -> None:
        if x_min >= x_max:
            raise ValueError("x_min should be less than x_max")
        if y_min >= y_max:
            raise ValueError("y_min should be less than y_max")
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.type_machine = model_machine

    def check_coordinate(self, axis: str, value: float) -> float:
        """
        Проверяет и корректирует координаты в зависимости от ограничений.

        :param axis: Ось ('X' или 'Y').
        :param value: Значение координаты.
        :return: Скорректированное значение координаты.
        """
        if axis == 'X':
            return max(self.x_min, min(value, self.x_max))
        elif axis == 'Y':
            return max(self.y_min, min(value, self.y_max))
        else:
            raise ValueError("Axis must be 'X' or 'Y'")