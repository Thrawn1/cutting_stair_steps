from Validator import Validator

class MachineLimits:
    """
    Класс описывающий ограничения станка

    Параметры:
    - x_min (float): минимальное значение координаты X
    - x_max (float): максимальное значение координаты X
    - y_min (float): минимальное значение координаты Y
    - y_max (float): максимальное значение координаты Y
    - model_machine (str): модель станка
    """

    def __init__(self, x_min: float, x_max: float, y_min: float,
                 y_max: float, model_machine: str,validator:Validator) -> None:
        if validator.validate_type(x_min, float, 'x_min') and \
            validator.validate_type(x_max, float, 'x_max') and \
            validator.validate_type(y_min, float, 'y_min') and \
            validator.validate_type(y_max, float, 'y_max') and \
            validator.validate_type(model_machine, str, 'model_machine'):
            if validator.validate_min_max(x_min, x_max):
                self.x_min = x_min
                self.x_max = x_max
                self.y_min = y_min
                self.y_max = y_max
                self.model_machine = model_machine
                self.validator = validator

    def check_coordinate_axis_x_y(self, axis: str, value: float) -> float:
        """
        Проверяет и корректирует координаты в зависимости от ограничений.

        :param axis: Ось ('X' или 'Y').
        :param value: Значение координаты.
        :return: Скорректированное значение координаты.
        """
        if self.validator.validate_type(axis, str, 'axis') and \
            self.validator.validate_type(value, float, 'value'):
            if axis == 'X':
                return max(self.x_min, min(value, self.x_max))
            elif axis == 'Y':
                return max(self.y_min, min(value, self.y_max))
            else:
                raise ValueError("Axis must be 'X' or 'Y'")
    def check_coordinate_axis_c(self, value: float,type_mashine: str) -> bool:
        """
        Проверяет, соответствует ли значение координаты оси C ограничениям станка.
        Параметры:
        - value (float): значение координаты
        - type_mashine (str): тип станка
        Возвращает:
        - bool: True, если значение соответствует ограничениям, иначе False
        """
        if self.validator.validate_type(value, float, 'value') and \
            self.validator.validate_type(type_mashine, str, 'type_mashine'):
            if type_mashine == '4Axis' and value >= 0.0 and value <= 180.0:
                return True
            elif type_mashine == '5Axis' and value >= -4.9 and value <= 360.0:
                return True