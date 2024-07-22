class Disk():
    """Класс для хранения информации о диске - его номере, диаметре, толщине суппорта,
    толщине резца и указание какой материал он режет"""
    def __init__(self, number:int, diameter:float, support_thickness:float, cutter_thickness:float, material:str,name:str,Z_sec=50,Z_approach=5):
        """
        Параметры:
        - number (int): номер диска
        - diameter (float): диаметр диска
        - support_thickness (float): толщина суппорта диска
        - cutter_thickness (float): толщина режушей части диска
        - material (str): материал, который режет диск
        - name (str): название диска
        - Z_sec (float): Высота безопасного перемещения диска
        - Z_approach (float): скорость подхода диска
        """

        if diameter <= 0:
            raise ValueError("Диаметр должен быть положительным числом.")
        if support_thickness <= 0:
            raise ValueError("Толщина суппорта должна быть положительным числом.")
        if cutter_thickness <= 0:
            raise ValueError("Толщина резца должна быть положительным числом.")

        self.number = number
        self.diameter = diameter
        self.support_thickness = support_thickness
        self.cutter_thickness = cutter_thickness
        self.material = material
        self.name = name
        self.Z_sec = Z_sec
        self.Z_approach = Z_approach

    #Метод, рассчитвающий на сколько продлевается пил в зависимости от диаметра диска

    def get_cutter_extension(self) -> float:
        """
        Рассчитывает на сколько продлевается пил в зависимости от диаметра диска."""
        return self.diameter / 2 + self.cutter_thickness

    def get_tickness_correction(self, size:float) -> float: 
        """
        Рассчитывает на сколько нужно увеличить размер детали, чтобы учесть толщину резца."""
        return size + self.cutter_thickness

    def __str__(self) -> str:
        """
        Возвращает строковое представление объекта Disk.

        Возвращает:
        - str: строковое представление объекта Disk
        """
        return (f"Диск: {self.name}\n"
                f"Диаметр: {self.diameter}\n"
                f"Толщина суппорта: {self.support_thickness}\n"
                f"Толщина резца: {self.cutter_thickness}\n"
                f"Для какого материала: {self.material}")

    def __repr__(self) -> str:
        return self.__str__()