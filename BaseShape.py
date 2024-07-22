class BaseShape:
    """Базовый класс для хранения информации о форме."""
    def __init__(self, width: float, length: float, thickness: float, material: str = 'Granite'):
        self.validate_positive_number(width, 'width')
        self.validate_positive_number(length, 'length')
        self.validate_positive_number(thickness, 'thickness')
        self.validate_string(material, 'material')
        
        self.width = width
        self.length = length
        self.thickness = thickness
        self.material = material
        self.area = self.calculate_area()
        self.type = self.__class__.__name__

    def calculate_area(self):
        """Рассчитывает площадь."""
        l = self.length / 1000
        w = self.width / 1000
        return l * w

    @staticmethod
    def validate_positive_number(value, name):
        if value <= 0:
            raise ValueError(f"{name} должно быть положительным числом.")
        if not isinstance(value, (int, float)):
            raise ValueError(f"{name} должно быть числом.")
    
    @staticmethod
    def validate_string(value, name):
        if not isinstance(value, str):
            raise ValueError(f"{name} должно быть строкой.")
    
    def __str__(self):
        return (f"{self.type}: {self.width}x{self.length}x{self.thickness} "
                f"из материала {self.material}, площадь {self.area} м^2")
    
    def __repr__(self):
        return self.__str__()


class Detail(BaseShape):
    """Класс для хранения информации о детали."""
    def __init__(self, width: float, length: float, thickness: float, material: str = 'Granite', rectangle: bool = True):
        super().__init__(width, length, thickness, material)
        self.validate_boolean(rectangle, 'rectangle')
        self.rectangle = rectangle
        self.type = 'Деталь'

    @staticmethod
    def validate_boolean(value, name):
        if not isinstance(value, bool):
            raise ValueError(f"{name} должно быть булевым значением.")



class Workpiece(BaseShape):
    """Класс для хранения информации о заготовке."""
    def __init__(self, x: float, y: float, width: float, length: float, thickness: float, material: str = 'Granite', rectangle: bool = True):
        super().__init__(width, length, thickness, material)
        self.validate_positive_number(x, 'x')
        self.validate_positive_number(y, 'y')
        self.validate_boolean(rectangle, 'rectangle')

        self.x = x
        self.y = y
        self.rectangle = rectangle
        self.type = 'Заготовка'

    @staticmethod
    def validate_boolean(value, name):
        if not isinstance(value, bool):
            raise ValueError(f"{name} должно быть булевым значением.")
    
    def get_limits_workpiece(self):
        x_min = self.x
        y_max = self.y
        x_max = self.x + self.length
        y_min = self.y - self.width
        return x_max, y_max, x_min, y_min



