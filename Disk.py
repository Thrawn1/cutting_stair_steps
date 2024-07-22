class Disk():
    """Класс для хранения информации о диске - его номере, диаметре, толщине суппорта,
    толщине резца и указание какой материал он режет"""
    def __init__(self, number, diameter, support_thickness, cutter_thickness, material,name,Z_sec=50,Z_approach=5):
        self.number = number
        self.diameter = diameter
        self.support_thickness = support_thickness
        self.cutter_thickness = cutter_thickness
        self.material = material
        self.name = name
        self.Z_sec = Z_sec
        self.Z_approach = Z_approach
    #Метод, рассчитвающий на сколько продлевается пил в зависимости от диаметра диска
    def cutter_extension(self):
        return self.diameter / 2 + self.cutter_thickness
    def tickness_correction(self, size):
        return size + self.cutter_thickness