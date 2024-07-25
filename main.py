from Validator import Validator
from MachineLimits import MachineLimits


class Main:
    def __init__(self):
        self.validator = Validator()
        self.recive_data_machine_limits()

    def recive_data_machine_limits(self):
        x_min = float(input('Введите x_min: '))
        x_max = float(input('Введите x_max: '))
        y_min = float(input('Введите y_min: '))
        y_max = float(input('Введите y_max: '))
        model_machine = input('Введите модель станка: ')
        if self.validator.validate_input(x_min, float, 'x_min') and \
            self.validator.validate_input(x_max, float, 'x_max') and \
            self.validator.validate_input(y_min, float, 'y_min') and \
            self.validator.validate_input(y_max, float, 'y_max') and \
            self.validator.validate_input(model_machine, str, 'model_machine'):
                if self.validator.validate_min_max(x_min, x_max):
                    self.MaсhineLimits = MachineLimits(x_min, x_max, y_min, y_max, model_machine)