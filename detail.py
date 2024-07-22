class Detail():
    """Класс для хранения информации о детали - ее ширине, длине, толщине, углах между сторонами и
     материале"""
    def __init__(self, width, length, thickness, angle1, angle2, material):
        self.width = width
        self.length = length
        self.thickness = thickness
        self.angle1 = angle1
        self.angle2 = angle2
        self.material = material
        self.area = width * length
    def __repr__(self) -> str:
        """
        Возвращает строковое представление объекта Detail.

        Возвращает:
        - str: строковое представление объекта Detail
        """
        return (f"Detail(width={self.width}, length={self.length}, thickness={self.thickness}, "
                f"angle1={self.angle1}, angle2={self.angle2}, material={self.material})")
    def __str__(self) -> str:
        """
        Возвращает строковое представление объекта Detail.

        Возвращает:
        - str: строковое представление объекта Detail
        """
        return (f"Ширина: {self.width}\n"
                f"Длина: {self.length}\n"
                f"Толщина: {self.thickness}\n"
                f"Угол1: {self.angle1}\n"
                f"Угол2: {self.angle2}\n"
                f"Материал: {self.material}\n"
                f"Площадь: {self.area}")
    