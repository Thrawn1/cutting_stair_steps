class Exercise():
    """Класс описывающий задание - объект деталь, объект заготовка, объект диск, количество 
    деталей и отсуп от края заготовки"""
    def __init__(self, detail, workpiece, disk, count,offset=0):
        self.detail = detail
        self.workpiece = workpiece
        self.disk = disk
        self.count = count
        self.offset = offset
    def __str__(self):
        return f"Деталь: {self.detail.width}x{self.detail.length}x{self.detail.thickness}\n" \
               f"Заготовка: {self.workpiece.width}x{self.workpiece.length}x{self.workpiece.thickness}\n" \
               f"Диск: {self.disk.diameter}x{self.disk.support_thickness}x{self.disk.cutter_thickness}\n" \
               f"Количество: {self.count}"
    #Метод, рассчитывающий количество пилов по осям X и Y 
    def count_cutter(self):
        X_count = (self.workpiece.length-self.offset) // self.detail.length
        Y_count = (self.workpiece.width-self.offset) // self.detail.width
        if self.offset > 0:
            X_count +=1
            Y_count +=1
        return X_count, Y_count