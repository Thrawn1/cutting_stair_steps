from detail import Mashine_limits
def test_mashine_limits():
    ml = Mashine_limits(x_max=3500, x_min=0, y_max=0, y_min=-1898, type_mashine='Denver 4axis')
    
    assert ml.chek_coordinate('X', 3600) == 3500, "Ошибка в проверке координат X (выше максимума)"
    assert ml.chek_coordinate('X', 3220) == 3220, "Ошибка в проверке координат X (в пределах)"
    assert ml.chek_coordinate('X', -344) == 0, "Ошибка в проверке координат X (ниже минимума)"
    assert ml.chek_coordinate('Y', 100) == 0, "Ошибка в проверке координат Y (выше максимума)"
    assert ml.chek_coordinate('Y', -2000) == -1898, "Ошибка в проверке координат Y (ниже минимума)"
    assert ml.chek_coordinate('Y', -1200) == -1200, "Ошибка в проверке координат Y (в пределах)"

test_mashine_limits()
