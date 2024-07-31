from Shape import Detail, Workpiece
from Parameters import Parameters, Disk

class WorkOrder():
    def __init__(self, detail:Detail, workpiece:Workpiece, disk:Disk, parameters:Parameters, 
                 count:int, offset:float):
        self.detail = detail
        self.workpiece = workpiece
        self.disk = disk
        self.parameters = parameters
        self.count = count
        self.offset = offset
        self.total_number_details = self.calculate_total_number_of_details()
        self.check_total_number_of_details()

    def count_cutter(self)->tuple:
        X_count = (self.workpiece.length-self.offset) // self.detail.length
        Y_count = (self.workpiece.width-self.offset) // self.detail.width
        if self.offset > 0:
            X_count +=1
            Y_count +=1
        return X_count, Y_count
    
    def calculate_total_number_of_details(self)->int:
        x_count, y_count = self.count_cutter()
        if self.offset > 0:
            return (x_count-1) * (y_count-1)
        else:
            return x_count * y_count

    def calculation_efficiency(self)->float:
        return (self.calculate_total_number_of_details()*self.detail.area *
                 100) / self.workpiece.area

    def check_total_number_of_details(self):
        #Метод будет переписан в будущем
        self.total_number_details = self.calculate_total_number_of_details()
        if self.total_number_details < self.count:
            raise ValueError("Невозможно изготовить такое количество деталей")
        elif self.total_number_details == 0:
            raise ValueError("Из заготовки нельзя напилить детали по заданию!")
        elif self.total_number_details == self.count:
            print("Все детали изготовлены")
        elif self.total_number_details > self.count:
            print("Изготовлено деталей больше чем нужно")