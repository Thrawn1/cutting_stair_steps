import logging

# Создание объекта логгера
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
from BaseShape import Detail, Workpiece
from old_code.v2.Disk import Disk

class Exercise():
    """Класс описывающий задание - объект деталь, объект заготовка, объект диск, количество 
    деталей и отсуп от края заготовки"""
    def __init__(self, detail:Detail, workpiece:Workpiece, disk:Disk, count,offset=0):
        """
        Параметры:
        - detail (Detail): объект деталь
        - workpiece (Workpiece): объект заготовка
        - disk (Disk): объект диск
        - count (int): количество деталей
        - offset (float): отсуп от края заготовки
    """
        self.validate_type(detail, 'detail', Detail)
        self.validate_type(workpiece, 'workpiece', Workpiece)
        self.validate_type(disk, 'disk', Disk)
        self.validate_type(count, 'count', int)
        self.validate_type(offset, 'offset', (int, float))


        self.detail = detail
        self.workpiece = workpiece
        self.disk = disk
        self.count = count
        self.offset = offset
        self.total_number_details = self.calculate_total_number_of_details()
        self.check_total_number_of_details()

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

    #Метод, рассчитывающий количество пилов по осям X и Y 
    def count_cutter(self) -> tuple:
        """
        Рассчитывает количество пилов по осям X и Y.

        Возвращает:
        - tuple: количество пилов по осям X и Y
        """
        X_count = (self.workpiece.length-self.offset) // self.detail.length
        Y_count = (self.workpiece.width-self.offset) // self.detail.width
        if self.offset > 0:
            #Если отступ от края заготовки больше 0,то нужно учесть торцовочные резы
            X_count +=1
            Y_count +=1
        return X_count, Y_count

    
    def calculate_total_number_of_details(self) -> int:
        """
        Рассчитывает общее количество деталей, которые можно изготовить из заготовки.

        Возвращает:
        - int: общее количество деталей
        """
        X_count, Y_count = self.count_cutter()
        if self.offset > 0:
            #Если отступ от края заготовки больше 0, 
            # то общее количество деталей равно произведению количества пилов по осям X и Y минус 1, 
            # так как в случае отступа есть торцовочные резы
            total_number_details = (X_count - 1) * (Y_count - 1)
        else:
            total_number_details = X_count * Y_count
        return total_number_details
    
    def calculation_efficiency(self) -> float:
        """
        Рассчитывает эффективность раскроя.
        """
    
        return (self.calculate_total_number_of_details() * 
                self.detail.calculate_area()*100 / self.workpiece.calculate_area())

    def check_total_number_of_details(self)-> None:
        """
        Проверяет общее количество деталей, которые можно изготовить из заготовки.

        Выводит сообщение о результате проверки.
        """

        if self.total_number_details == 0:
            logging.error("Из заготовки нельзя напилить детали по заданию!")
        elif self.total_number_details < self.count:
            logging.info(
                f"Количество деталей, которые можно изготовить из данной заготовки: "
                f"{self.total_number_details}"
            )
            logging.info(f"Количество деталей, которые нужны по заданию: {self.count}")
            logging.info(f"Нужно напилить еще: {self.count - self.total_number_details}")
        elif self.total_number_details > self.count:
            logging.info(
                f"Количество деталей, которые можно изготовить из данной заготовки: "
                f"{self.total_number_details}"
                         )
            logging.info(f"Количество деталей, которые нужны по заданию: {self.count}")
            logging.info(f"Перееизбыток деталей: {self.total_number_details - self.count}")
            logging.info("Пожалуйста, скорректируйте размер заготовки")
        else:
            logging.info('Задание можно выполнить из заготовки')

    def __str__(self) -> str:
        """
        Возвращает строковое представление объекта Exercise.

        Возвращает:
        - str: строковое представление объекта Exercise
        """
        return (f"Деталь: {self.detail}\n"
                f"Заготовка: {self.workpiece}\n"
                f"Диск: {self.disk}\n"
                f"Количество деталей: {self.count}\n"
                f"Отступ от края заготовки: {self.offset}\n"
                f"Общее количество деталей: {self.total_number_details}\n"
                f"Эффективность раскроя: {self.calculation_efficiency()}%")
    def __repr__(self) -> str:
        """
        Возвращает строковое представление объекта Exercise.

        Возвращает:
        - str: строковое представление объекта Exercise
        """
        return self.__str__()   