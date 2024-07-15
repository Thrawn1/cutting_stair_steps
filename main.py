import tkinter as tk
from tkinter import filedialog, messagebox

def generate_gcode():
    # Получаем значения из полей ввода
    disk_number = entry_disk_number.get()
    start_x = entry_start_x.get()
    start_y = entry_start_y.get()
    start_z = entry_start_z.get()
    thickness = entry_thickness.get()
    length = entry_length.get()
    width = entry_width.get()
    count = entry_count.get()
    
    try:
        # Преобразуем входные данные к числовому типу
        start_x = float(start_x)
        start_y = float(start_y)
        start_z = float(start_z)
        thickness = float(thickness)
        length = float(length)
        width = float(width)
        count = int(count)
    except ValueError:
        messagebox.showerror("Ошибка ввода", "Пожалуйста, введите числовые значения для координат, толщины, размеров и количества.")
        return
    
    # Формируем содержимое G-кода
    gcode = f"""
;(CUTDOCUMENT.TXT)
N1 (UAO,1)
N2 G331 S60
N3 (UIO,Z(E31))
;(SORMA GRANIT [D. 370 ] D. 370)
N4 G398
N5 #G0 C0
N6 T{disk_number}
N7 M52
N8 G376
N9 G17
N10 G317 P12
N11 L365=3
N12 M41
;(TAGLIO LASTRA 56)
N13 M44
N14 G397 A0
N15 M41
N16 #G00 X{start_x} Y{start_y} C0
N17 G00 Z{start_z + 50}
N18 M07 M08
N19 S1750 M04
N20 G00 Z{start_z + 5}
"""
    
    step_y = (width + 10) / count  # Расстояние между изделиями по оси Y

    current_y = start_y
    for i in range(count):
        gcode += f"""
N21 G1 Y{current_y} Z{start_z - thickness / 6} F300
N22 M140[1]
N23 X{start_x + length} F1000
N24 X{start_x + length - 17.4143} Z{start_z - thickness / 3} F300
N25 X{start_x + 25.72727} F1000
N26 X{start_x + 38.79562} Z{start_z - thickness / 2} F300
N27 X{start_x + length - 30.48273} F1000
N28 X{start_x + length - 41.25061} Z{start_z - 2 * thickness / 3} F300
N29 X{start_x + 49.5635} F1000
N30 X{start_x + 58.82839} Z{start_z - 5 * thickness / 6} F300
N31 X{start_x + length - 50.75837} F1000
N32 X{start_x + length - 58.93163} Z{start_z - thickness} F300
N33 X{start_x + 67.00164} F1000
N34 X{start_x + 74.32891} Z{start_z - thickness - 5.58333} F300
N35 X{start_x + length - 65.2589} F1000
N36 X{start_x + length - 71.901} Z{start_z - thickness - 10.66667} F300
N37 X{start_x + 80.971} F1000
N38 X{start_x + 87.04005} Z{start_z - thickness - 15.75} F300
N39 X{start_x + length - 78.96005} F1000
N40 X{start_x + length - 84.53799} Z{start_z - thickness - 20.83333} F300
N41 X{start_x + 92.61801} F1000
N42 X{start_x + 97.7669} Z{start_z - thickness - 25.91667} F300
N43 X{start_x + length - 83.43311} F1000
N44 X{start_x + length - 88.20121} Z{start_z - thickness - 31} F300
N45 X{start_x + 102.53501} F1000
N46 M140[0]
N47 #G00 Z50
N48 G00 X{start_x} Y{current_y + step_y}
N49 G00 Z5
"""
        current_y += step_y
    
    gcode += """
N312 M44
N313 M05
N314 M09 M10
N315 G398
N316 #G0 G79 X0 Y0 C0
N317 M30
"""
    
    # Записываем G-код в файл
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(gcode)
        messagebox.showinfo("Успех", "G-код успешно сгенерирован и сохранен.")

# Создаем графический интерфейс
root = tk.Tk()
root.title("G-code Generator")

tk.Label(root, text="Номер диска:").grid(row=0, column=0)
entry_disk_number = tk.Entry(root)
entry_disk_number.grid(row=0, column=1)

tk.Label(root, text="Начальная координата X:").grid(row=1, column=0)
entry_start_x = tk.Entry(root)
entry_start_x.grid(row=1, column=1)

tk.Label(root, text="Начальная координата Y:").grid(row=2, column=0)
entry_start_y = tk.Entry(root)
entry_start_y.grid(row=2, column=1)

tk.Label(root, text="Начальная координата Z:").grid(row=3, column=0)
entry_start_z = tk.Entry(root)
entry_start_z.grid(row=3, column=1)

tk.Label(root, text="Толщина:").grid(row=4, column=0)
entry_thickness = tk.Entry(root)
entry_thickness.grid(row=4, column=1)

tk.Label(root, text="Длина изделия:").grid(row=5, column=0)
entry_length = tk.Entry(root)
entry_length.grid(row=5, column=1)

tk.Label(root, text="Ширина изделия:").grid(row=6, column=0)
entry_width = tk.Entry(root)
entry_width.grid(row=6, column=1)

tk.Label(root, text="Количество изделий:").grid(row=7, column=0)
entry_count = tk.Entry(root)
entry_count.grid(row=7, column=1)

tk.Button(root, text="Сгенерировать G-код", command=generate_gcode).grid(row=8, columnspan=2)

root.mainloop()
