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

    def validate_length(self, data, min_length, max_length, field_name):
        """
        Проверяет, что длина данных находится в заданных пределах
        :param data: данные для проверки
        :param min_length: минимальная длина данных
        :param max_length: максимальная длина данных
        :param field_name: название поля
        :return: True, если длина данных находится в заданных пределах, иначе False
        """
        if not (min_length <= len(data) <= max_length):
            self.errors.append(f'{field_name} length is not between {min_length} and {max_length}')
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

    def __str__(self) -> str:
        """
        Возвращает список ошибок в строковом виде, выводя каждую ошибку с новой строки
        :return: список ошибок в строковом виде
        """
        return '\n'.join(self.errors)