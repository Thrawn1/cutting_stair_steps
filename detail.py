class Detail():
    """Класс Detail для хранения информации о детали."""
    def __init__(self, width:float, length:float, thickness:float, 
                 material='Granite', rectangle=True):
        """
        Инициализация объекта Detail.
        Параметры:
        - width (float): ширина детали
        - length (float): длина детали
        - thickness (float): толщина детали
        - material (str): материал детали
        - rectangle (bool): является ли деталь прямоугольной (по умолчанию True)
        """
        if width <= 0 or length <= 0 or thickness <= 0:
                    raise ValueError("Ширина, длина и толщина должны быть положительными числами.")
        if not isinstance(width, (int, float)):
            raise ValueError("Ширина должна быть числом.")
        if not isinstance(length, (int, float)):
            raise ValueError("Длина должна быть числом.")
        if not isinstance(thickness, (int, float)):
            raise ValueError("Толщина должна быть числом.")
        if not isinstance(material, str):
            raise ValueError("Материал должен быть строкой.")
        if not isinstance(rectangle, bool):
            raise ValueError("rectangle должен быть булевым значением.")
        

        self.width = width
        self.length = length
        self.thickness = thickness
        self.material = material
        self.rectangle = rectangle
        self.area = self.calculate_area()
    
    def calculate_area(self):
        """
        Рассчитывает площадь детали.
        Возвращает:
        - float: площадь детали
        """
        l = self.length/1000
        w = self.width/1000
        return l * w
    
    def __str__(self):
        """
        Возвращает строковое представление объекта Detail.
        Возвращает:
        - str: строковое представление объекта Detail
        """
        return (f"Деталь: {self.width}x{self.length}x{self.thickness} "
                f"из материала {self.material}, площадь {self.area} м^2")
    def __repr__(self):
        return self.__str__()
    