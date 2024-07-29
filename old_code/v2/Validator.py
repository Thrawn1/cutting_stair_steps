import logging

logging.basicConfig(level=logging.INFO)

class Validator:
    """
    Класс для валидации данных
    Проверяет на пустоту, тип и длину данных
    """
    def __init__(self):
        self.errors = []

    def validate_not_empty(self, data, field_name):
        """
        Проверяет, что данные не пустые
        :param data: данные для проверки
        :param field_name: название поля
        :return: True, если данные не пустые, иначе False
        """
        if not data:
            self.errors.append(f'{field_name} is empty')
        return not self.errors

    def validate_min_max(self, min_value, max_value):
        """
        Проверяет, что минимальное значение меньше максимального
        :param min_value: минимальное значение
        :param max_value: максимальное значение
        :param field_name: название поля
        :return: True, если минимальное значение меньше максимального, иначе False
        """
        if not min_value < max_value:
            self.errors.append(f'Минимальное значение больше максимального.',
                                f'Минимальное значение: {min_value}', 
                                f'Максимальное значение: {max_value}')

    def validate_type(self, data, expected_type, field_name):
        """
        Проверяет, что данные имеют ожидаемый тип
        :param data: данные для проверки
        :param expected_type: ожидаемый тип данных
        :param field_name: название поля
        :return: True, если данные имеют ожидаемый тип, иначе False
        """
        if not isinstance(data, expected_type):
            self.errors.append(f'{field_name} is not of type {expected_type.__name__}')
        return not self.errors

    def validate_input (self, data, expected_type, field_name):
        """
        Проверяет, что данные имеют ожидаемый тип
        :param data: данные для проверки
        :param expected_type: ожидаемый тип данных
        :param field_name: название поля
        :return: True, если данные имеют ожидаемый тип, иначе False
        """
        try:
            data = expected_type(data)
        except ValueError:
            self.errors.append(f'{field_name} is not of type {expected_type.__name__}')
        return not self.errors

    def checking_value_positive(self, data, field_name):
        """
        Проверяет, что данные положительные
        :param data: данные для проверки
        :param field_name: название поля
        :return: True, если данные положительные, иначе False
        """
        if not data > 0:
            self.errors.append(f'{field_name} is not positive')
        return not self.errors

    def get_errors(self):
        """
        Возвращает список ошибок
        :return: список ошибок
        """
        return self.errors

    def clear_errors(self):
        """
        Очищает список ошибок
        """
        self.errors = []
    
    def save_to_file(self, file_name):
        """
        Сохраняет список ошибок в файл
        :param file_name: имя файла
        """
        with open(file_name, 'w') as file:
            for error in self.errors:
                file.write(error + '\n')

    def __str__(self) -> str:
        """
        Возвращает список ошибок в строковом виде, выводя каждую ошибку с новой строки
        :return: список ошибок в строковом виде
        """
        return '\n'.join(self.errors)
