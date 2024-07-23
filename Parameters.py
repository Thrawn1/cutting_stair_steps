class SpeedParameters:
    """
    Класс для хранения информации о параметрах скорости резки:
    - speed_forward (int): скорость прямого хода резки
    - speed_backward (int): скорость обратного хода резки (по умолчанию 0.7 от скорости прямого хода)
    - speed_depth (int): скорость заглубления инструмента
    """
    def __init__(self,speed_forward:int,speed_depth:int,speed_bakword=None) -> None:
        
        self.validate_type(speed_forward, "speed_forward", int)
        self.validate_type(speed_depth, "speed_depth", int)
        if speed_bakword is not None:
            self.validate_type(speed_bakword, "speed_backward", int)
        
        self.speed_forward = speed_forward
        self.speed_backward = speed_bakword if speed_bakword is not None else 0.7 * speed_forward
        self.speed_depth = speed_depth

    @staticmethod
    def validate_type(value, name, type_):
        """
        Проверяет тип значения.

        Параметры:
        - value: значение
        - name (str): имя значения
        - type_: тип значения
        """
        if not isinstance(value, type_):
            raise ValueError(f"{name} должен быть типа {type_}")

class DepthParameters:
    """
    Класс для хранения информации о параметрах глубины резки:
    - depth_step_forward (float): шаг глубины работы инструмента по прямому ходу
    - depth_step_backward (float): шаг глубины работы инструмента по обратному ходу (по умолчанию равен шагу глубины работы инструмента по прямому ходу)
    - extra_depth (int): дополнительная глубина реза (по умолчанию 0)
    """
    def __init__(self,depth_step_forward:float,depth_step_backward:float,extra_depth=0.0) -> None:
        """
        Параметры:
        - depth_step_forward (float): шаг глубины работы инструмента по прямому ходу
        - depth_step_backward (float): шаг глубины работы инструмента по обратному ходу (по умолчанию равен шагу глубины работы инструмента по прямому ходу)
        - extra_depth (int): дополнительная глубина реза (по умолчанию 0)
        """
        self.validate_type(depth_step_forward, "depth_step_forward", float)
        self.validate_type(depth_step_backward, "depth_step_backward", float)
        self.validate_type(extra_depth, "extra_depth", float)


        self.depth_step_forward = depth_step_forward
        self.depth_step_backward = depth_step_backward if depth_step_backward is not None else depth_step_forward
        self.extra_depth = extra_depth

    @staticmethod
    def validate_type(value, name, type_):
        """
        Проверяет тип значения.

        Параметры:
        - value: значение
        - name (str): имя значения
        - type_: тип значения
        """
        if not isinstance(value, type_):
            raise ValueError(f"{name} должен быть типа {type_}")



class Parameters:
    """
    Класс для хранения информации о параметрах резки:
    - speed_parameters (SpeedParameters): параметры скорости резки
    - depth_parameters (DepthParameters): параметры глубины резки
    - zigzag (bool): флаг режима зиг-заг (по умолчанию True)

    """
    
    def __init__(self, speed_parameters:SpeedParameters,
                 depth_parameters:DepthParameters,zigzag=True) -> None:
        """
        Параметры:
        - speed_parameters (SpeedParameters): параметры скорости резки
        - depth_parameters (DepthParameters): параметры глубины резки
        - zigzag (bool): флаг режима зиг-заг (по умолчанию True)
        """

        self.validate_type(speed_parameters, "speed_parameters", SpeedParameters)
        self.validate_type(depth_parameters, "depth_parameters", DepthParameters)
        self.validate_type(zigzag, "zigzag", bool)

        self.speed_parameters = speed_parameters
        self.depth_parameters = depth_parameters        
        self.zigzag = zigzag

    @staticmethod
    def validate_type(value, name, type_):
        """
        Проверяет тип значения.

        Параметры:
        - value: значение
        - name (str): имя значения
        - type_: тип значения
        """
        if not isinstance(value, type_):
            raise ValueError(f"{name} должен быть типа {type_}")
