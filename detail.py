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
        self.width = width
        self.length = length
        self.thickness = thickness
        self.material = material
        self.rectangle = rectangle
        self.area = width * length
    
    def __str__(self):
        """
        Возвращает строковое представление объекта Detail.
        Возвращает:
        - str: строковое представление объекта Detail
        """
        return (f"Деталь: {self.width}x{self.length}x{self.thickness} "
                f"из материала {self.material}")
    def __repr__(self):
        return self.__str__()
    