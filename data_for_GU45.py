import xlrd, datetime, os, re
from fpdf import FPDF
from database import read_vagon
import datetime

numbers = [87655667, 87655668]
#number = 87655667
#with open('./bin/path.txt', 'r') as file:
#    path = file.readlines()


def count_GU():
    file = "./bin/count_GU.txt"
    with open(file, 'r') as f:
        count = int(f.readlines()[0])
    return count

def count_GU23():
    file = "./bin/count_GU23.txt"
    with open(file, 'r') as f:
        count = int(f.readlines()[0])
    return count

def write_count(count):
    file = "./bin/count_GU.txt"
    with open(file, 'w') as f:
        f.write(str(count+1))

def write_count_GU23(count):
    file = "./bin/count_GU23.txt"
    with open(file, 'w') as f:
        f.write(str(count+1))

def read_numbers_from_excel(path):#определяем номера вагонов которые есть в базе данных
    numbers = []
    try:
        rb = xlrd.open_workbook(path)
        rw = rb.sheet_by_index(0)
        rows = rw.nrows
        #print(rows)
        for row in range (7, rows):
            try:
                cell = int(rw.cell_value(row, 0))
            except ValueError:
                continue
            if numbers.count(cell) == 0:
                numbers.append(cell)
        #print(numbers)
    except FileNotFoundError:
        numbers = False
    return numbers

def read_vagon_from_excel():
    with open('./bin/path_excel.txt', 'r') as file:
        path = file.readlines()[0]
    #print(path)
    vagon = []
    rb = xlrd.open_workbook(path)
    rw = rb.sheet_by_index(0)
    rows = rw.nrows
    for row in range (7, rows): #считывание операций с вагоном
        try:
            cell_num = int(rw.cell_value(row, 0))
            if len(str(cell_num))>= 7 and len(str(cell_num)) < 9:
                cell_op = str(rw.cell_value(row, 1))
                if cell_op == 'Прибытие' or cell_op == 'Отправление' or cell_op == 'Погрузка' or cell_op ==\
                        'Выгрузка' or cell_op == 'Проведение ТО' or cell_op == 'Взвешивание':
                    try:
                        cell_date = xlrd.xldate_as_datetime(rw.cell_value(row, 2), rb.datemode).date()
                        cell_time = xlrd.xldate_as_datetime(rw.cell_value(row, 3), rb.datemode).time()
                        cell_dt = int(datetime.datetime(cell_date.year, cell_date.month, cell_date.day, cell_time.hour,
                        cell_time.minute, tzinfo=datetime.timezone.utc).timestamp()) + 10800
                    except TypeError:
                        cell_dt = (str(rw.cell_value(row, 2)), str(rw.cell_value(row, 2)))
                    try:
                        cell_track = str(int(rw.cell_value(row, 4)))
                    except ValueError:
                        cell_track = str(rw.cell_value(row, 4))
                    cell_park = str(rw.cell_value(row, 5))
                    cell_client = str(rw.cell_value(row, 6))
                    if type(cell_dt) == tuple or cell_track == '' or cell_park == '' or cell_client == '':
                        pass
                    else:
                        vagon.append([cell_num, cell_op, cell_dt, cell_track, cell_park, cell_client])
        except ValueError:
            continue

    #print(vagon[0][1])
    #print(vagon)
    if len(vagon) == 0:
        vagon = False
    #print(vagon)
    return vagon

def sorting (vagon):
    #сортировка операций по времени
    vagon_op = []
    dates = []
    if vagon != False:
        #print(vagon)
        for op in range(len(vagon)):
            if type(vagon[op][1]) == datetime.datetime:
                dates.append(vagon[op][1])
            else:
                dates.append(int(vagon[op][1]))
        min_dates = []
        for op in range (len(vagon)):
            if type(dates[op]) == datetime.datetime:
                min_dates.append(dates.index(min(dates)))
                dates[min_dates[op]] = datetime.datetime(2030, 1, 1)
            else:
                min_dates.append(dates.index(min(dates)))
                dates[min_dates[op]] = 1999999999
        for op in range (len(vagon)):
            vagon_op.append(vagon[min_dates[op]])
        i = 0
        for vag in range(len(vagon_op)):
            if vagon_op[vag].count('Прибытие') == 1:
                i = vag
        return vagon_op[i:]
    else:
        return vagon_op

def sorting_all (vagon):
    #сортировка операций по времени с выводом всех операций
    vagon_op = []
    dates = []
    for op in range(len(vagon)):
        if type(vagon[op][1]) == datetime.datetime:
            dates.append(vagon[op][1])
        else:
            dates.append(int(vagon[op][1]))
    min_dates = []
    for op in range(len(vagon)):
        if type(dates[op]) == datetime.datetime:
            min_dates.append(dates.index(min(dates)))
            dates[min_dates[op]] = datetime.datetime(2030, 1, 1)
        else:
            min_dates.append(dates.index(min(dates)))
            dates[min_dates[op]] = 1999999999
    for op in range(len(vagon)):
        vagon_op.append(vagon[min_dates[op]])
    return vagon_op

def check_operations(vagon):
    operations = [
        'Прибытие',
        'Отправление',
        'Погрузка',
        'Выгрузка',
        'Проведение ТО',
        'ВУ-23',
        'ВУ-36',
        'Взвешивание'
    ]
    arrival = 0
    depature = 0
    loading = 0
    unloading = 0
    TO = 0
    VU_23 = 0
    VU_36 = 0
    error = {
        0 : 0,
        1 : 0,
        2 : 0,
        3 : 0,
        4 : 0,
        5 : 0,
        6 : 0
    }
    #проверка корректности числа операций
    for p in range (len(vagon)):
        arrival += vagon[p].count(operations[0])
        depature += vagon[p].count(operations[1])
        loading += vagon[p].count(operations[2])
        unloading += vagon[p].count(operations[3])
        TO += vagon[p].count(operations[4])
        VU_23 += vagon[p].count(operations[5])
        VU_36 += vagon[p].count(operations[6])
    if arrival == 0:
        error[0] = 'Не введена операция прибытия'
    if depature == 0:
        error[1] = 'Не введена операция отправления'
    elif depature > 1:
        error[1] = 'Введено более 1 операции отправления'
    if loading > 1:
        error[2] = 'Введено более 1 операции погрузки'
    #elif loading == 0 and unloading == 0:
    #    error[2] = 'Не введена операция погрузки'
    #    error[3] = 'Не введена операция выгрузки'
    if unloading > 1:
        error[2] = 'Введено более 1 операции выгрузки'
    if len(vagon) != 0:
        station_time = vagon[len(vagon)-1][1] - vagon[0][1]
    else:
        station_time = datetime.timedelta(seconds=100000)
    if unloading == 1 and TO == 0 and station_time.total_seconds() >= 86400:
        error[4] = 'Не введена операция Проведение ТО'
    elif loading == 1 and TO == 0 and station_time.total_seconds() >= 86400:
        error[4] = 'Не введена операция Проведение ТО'
    if VU_23 > 1:
        error[5] = 'Введено более 1 операции ВУ-23'
    elif VU_23 != VU_36:
        error[5] = 'Несоответствие количества операций ВУ-23 и ВУ-36'
    if VU_36 > 1:
        error[6] = 'Введено более 1 операции ВУ-36'
    #elif TO > 1:
    #    error[4] = 'Введено более 1 операции Проведение ТО'
    count_op = 0
    for op in range (len(vagon)):
        if type(vagon[op][1]) == tuple:
            error[6 + count_op] = 'Введен неверный формат даты/времени'
    errors = 0
    for i in error:
        if error[i] != 0:
            errors += 1
    if errors != 0:
        check = False
        return [error, check]
    else:
        #проверка корректности времени операций
        check = True
        error = ['Операция выполнена успешно!']
        index_op = {}
        for op in range (len(vagon)):
            if vagon[op][0] == operations[0]:
                index_op[0] = op
            elif vagon[op][0] == operations[1]:
                index_op[1] = op
            elif vagon[op][0] == operations[2]:
                index_op[2] = op
            elif vagon[op][0] == operations[3]:
                index_op[3] = op
            elif vagon[op][0] == operations[4]:
                index_op[4] = op
        if index_op[0] != min(index_op.values()) or index_op[1] != max(index_op.values()): #проверка правильности положения прибытия/отправлени
            #print(index_op[0], index_op[1], min(index_op.values()), max(index_op.values()))
            error = ['Нарушена хронология операций']
            check = False
        elif loading == 1 and unloading == 1 and index_op[2] < index_op[3]: #проверка правиильности положения погрузки/выгрузки
            error = ['Нарушена хронология операций']
            check = False
        #elif len(index_op) == 5 and index_op[2] < index_op[4]: #проверка правиильности положения погрузки/ТО
        #    error = ['Нарушена хронология операций']
        #    check = False
        elif TO == 1 and unloading == 1 and index_op[3] > index_op[4]: #проверка правиильности положения выгрузки/ТО
            error = ['Нарушена хронология операций']
            check = False
        #print(vagon)
        for op_1 in range (len(vagon) - 1): #проверка отсутствия одинаковых времен
            for op_2 in range (1 + op_1, len(vagon)):
                if (vagon[op_2][1] - vagon[op_1][1]).total_seconds()//60 < 30:
                    error = ['Разница времени между операциями менее 30 минут!']
                    check = False
                    #print(vagon[op_1][1], vagon[op_2][1], (vagon[op_1][1] - vagon[op_2][1]).total_seconds()//60)
        return [error, check]

def creat_GU(): #создаем форму памятки
    x0 = 20
    y0 = 10
    tab_x = [0, 9, 32, 39, 53, 60, 81, 101, 121, 136, 152, 160, 180]
    tab_y = []
    bord = 0
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('Arial', '', './fonts/arial.ttf', uni=True)
    pdf.add_font('ArialBD', '', './fonts/arialbd.ttf', uni=True)
    pdf.set_font("Arial", size=8)
    pdf.set_xy(x0+136, y0)
    pdf.cell(w=x0+20, h=4, txt="Форма ГУ-45", align="L", border=bord)
    pdf.set_xy(x0+121, y0+4)
    pdf.cell(w=x0, h=4, txt="Утверждена ОАО РЖД в 2004 г.", align="L", border=bord)
    pdf.set_xy(x0, y0 + 4)
    pdf.cell(x0, 4, txt="Станция", align="L", border=bord)
    pdf.set_xy(x0, y0 + 24)
    pdf.cell(x0, 4, txt="Наименование клиента", align="L", border=bord)
    pdf.set_xy(x0, y0 + 32)
    pdf.cell(x0, 4, txt="Подача производилась локомотивом", align="L", border=bord)
    pdf.set_xy(x0+118, y0+24)
    pdf.cell(x0, 4, txt="Место подачи", align="L", border=bord)
    pdf.set_xy(x0+108, y0 + 32)
    pdf.cell(x0, 4, txt="Индекс поезда", align="L", border=bord)

    pdf.set_font("Arial", size=10)
    pdf.set_xy(x0 + 32, y0 + 4)
    pdf.cell(x0, 4, txt="Новосибирск-Главный", align="L", border=bord)
    pdf.set_xy(x0, y0 + 8)
    pdf.cell(x0, 4, txt="Западно-Сибирская ж.д. - филиал ОАО РЖД", align="L", border=bord)
    #pdf.set_xy(x0 + 40, y0 + 24)
    #pdf.cell(x0, 4, txt="АО Глобал Транс", align="L", border=bord)
    pdf.set_xy(x0 + 55, y0 + 32)
    pdf.cell(x0, 4, txt="станции", align="L", border=bord)
    #pdf.set_xy(x0 + 136, y0 + 32)
    #pdf.cell(x0, 4, txt="0000-019-0091", align="L", border=bord)
    pdf.set_font("ArialBD", size=10)
    pdf.set_xy(x0, y0 + 16)
    pdf.cell(x0, 4, txt="ПАМЯТКА ПРИЕМОСДАТЧИКА №", align="L", border=bord)
    pdf.set_font("Arial", size=10)
    #pdf.set_xy(x0 + 60, y0 + 16)
    #pdf.cell(x0, 4, txt="ХХХ", align="L", border=bord)
    pdf.set_xy(x0 + 80, y0 + 16)
    pdf.cell(x0, 4, txt="на подачу и уборку вагонов", align="L", border=bord)
    pdf.set_font("Arial", size=8)
    pdf.set_xy(x0, y0 + 230)
    pdf.cell(x0, 5, txt="Место для отметок", align="L", border=bord)
    pdf.set_xy(x0, y0 + 240)
    pdf.cell(x0, 5, txt="Приемосдатчик (ДСПП)", align="L", border=bord)
    pdf.set_xy(x0 + 30, y0 + 240)
    pdf.cell(x0, 5, txt="_______________", align="L", border=bord)
    pdf.set_xy(x0 + 75, y0 + 240)
    pdf.cell(x0, 5, txt="Грузополучатель", align="L", border=bord)
    pdf.set_xy(x0 + 100, y0 + 240)
    pdf.cell(x0, 5, txt="_______________", align="L", border=bord)
    pdf.set_xy(x0 + 30, y0 + 245)
    pdf.cell(x0, 5, txt="_______________", align="L", border=bord)
    pdf.set_xy(x0 + 75, y0 + 245)
    pdf.cell(x0, 5, txt="Грузоотправитель", align="L", border=bord)
    pdf.set_xy(x0 + 100, y0 + 245)
    pdf.cell(x0, 5, txt="_______________", align="L", border=bord)
    pdf.set_xy(x0, y0 + 250)
    pdf.cell(x0, 5, txt="Памятка проведена по ведомости подачи и уборки №", align="L", border=bord)
    pdf.set_xy(x0 + 90, y0 + 250)
    pdf.cell(x0, 5, txt="_______________", align="L", border=bord)
    pdf.set_xy(x0, y0 + 255)
    pdf.cell(x0, 5, txt="Товарный кассир (агент станции)", align="L", border=bord)
    pdf.set_xy(x0 + 60, y0 + 255)
    pdf.cell(x0, 5, txt="_______________", align="L", border=bord)



    #pdf.set_font("Arial", size=80)
    #pdf.cell(200, 10, txt="krogjsd", ln=1, align="C")
    #Draw head of table
    pdf.line(x0 + tab_x[0], y0 + 36, x0 + tab_x[len(tab_x) - 1], y0 + 36)
    pdf.line(x0 + tab_x[5], y0 + 44, x0 + tab_x[10], y0 + 44)
    pdf.set_xy(x0 + tab_x[0], y0 + 47)
    pdf.multi_cell(tab_x[1]-tab_x[0], 4, txt="№ п/п", align="C", border=bord)
    pdf.set_xy(x0 + tab_x[1], y0 + 49)
    pdf.multi_cell(tab_x[2] - tab_x[1], 4, txt="№ вагона", align="C", border=bord)
    pdf.set_xy(x0 + tab_x[5], y0 + 36)
    pdf.multi_cell(tab_x[8] - tab_x[5], 4, txt="Время выполнения операции день-мес час-мин", align="C", border=bord)
    pdf.set_xy(x0 + tab_x[8], y0 + 36)
    pdf.multi_cell(tab_x[10] - tab_x[8], 4, txt="Задержка окончания груз. операции", align="C", border=bord)
    pdf.set_xy(x0 + tab_x[5], y0 + 49)
    pdf.multi_cell(tab_x[6] - tab_x[5], 4, txt="подача / передача на выст. Путь", align="C", border=bord)
    pdf.set_xy(x0 + tab_x[6], y0 + 45)
    pdf.multi_cell(tab_x[7] - tab_x[6], 4, txt="уведомл. о заверш. гр. операции / возврат на выст. путь", align="C", border=bord)
    pdf.set_xy(x0 + tab_x[7], y0 + 53)
    pdf.multi_cell(tab_x[8] - tab_x[7], 4, txt="уборка", align="C", border=bord)
    pdf.set_xy(x0 + tab_x[8], y0 + 51)
    pdf.multi_cell(tab_x[9] - tab_x[8], 4, txt="время час-мин", align="C", border=bord)
    pdf.set_xy(x0 + tab_x[9], y0 + 51)
    pdf.multi_cell(tab_x[10] - tab_x[9], 4, txt="№ акта ГУ-23", align="C", border=bord)

    pdf.set_xy(x0 + tab_x[2]+1.5, y0 + 66)
    pdf.rotate(90)
    pdf.multi_cell(30, 4, txt="Код ЖД адм.", align="C", border=bord)
    pdf.rotate(0)
    pdf.set_xy(x0 + tab_x[3]+3, y0 + 66)
    pdf.rotate(90)
    pdf.multi_cell(30, 4, txt="Принадлежность вагона", align="C", border=bord)
    pdf.rotate(0)
    pdf.set_xy(x0 + tab_x[4]+1.5, y0 + 66)
    pdf.rotate(90)
    pdf.multi_cell(30, 4, txt="Груз операция", align="C", border=bord)
    pdf.rotate(0)
    pdf.set_xy(x0 + tab_x[10]+2, y0 + 66)
    pdf.rotate(90)
    pdf.multi_cell(30, 4, txt="Кол-во взв.", align="C", border=bord)
    pdf.rotate(0)
    pdf.set_xy(x0 + tab_x[11]+8, y0 + 66)
    pdf.rotate(90)
    pdf.multi_cell(30, 4, txt="Примечание", align="C", border=bord)
    pdf.rotate(0)

    #Draw table
    y_max = 30*5
    #pdf.set_line_width(1)
    for x in range (len(tab_x)):
        if x <= 5 or x >= 10 or x == 8:
            pdf.line(x0+tab_x[x], y0+36, x0+tab_x[x], y0+66+4+y_max)
        else:
            pdf.line(x0 + tab_x[x], y0 + 44, x0 + tab_x[x], y0 + 66 + 4 + y_max)
        if x < len(tab_x)-1:
            pdf.set_xy(x0 + tab_x[x], y0 + 66)
            pdf.cell(tab_x[x+1]-tab_x[x], 4, txt=str(x+1), align="C", border=bord)
    pdf.line(x0 + tab_x[0], y0 + 66, x0 + tab_x[len(tab_x) - 1], y0 + 66)
    pdf.line(x0 + tab_x[0], y0 + 70, x0 + tab_x[len(tab_x) - 1], y0 + 70)
    for y in range (30):
        pdf.line(x0+tab_x[0], y0+75+y*5, x0+tab_x[len(tab_x)-1], y0+75+y*5)
        pdf.set_font("Arial", size=10)

        pdf.set_xy(x0, y0 + 70+y*5)
        pdf.cell(tab_x[1]-tab_x[0], 5, txt=str(y+1), align="C", border=bord)
    #pdf.output("text.pdf")
    return [pdf]

def creat_GU23(): #создание формы акта ГУ-23
    x0 = 20
    y0 = 10
    bord = 0
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('Arial', '', './fonts/arial.ttf', uni=True)
    pdf.add_font('ArialBD', '', './fonts/arialbd.ttf', uni=True)
    pdf.set_font("Arial", size=8)
    pdf.set_xy(x0 + 136, y0)
    pdf.cell(w=x0 + 20, h=4, txt="Форма ГУ-23 ВЦ", align="L", border=bord)
    pdf.set_xy(x0 + 121, y0 + 4)
    pdf.cell(w=x0, h=4, txt="Утверждена ОАО РЖД в 2004 г.", align="L", border=bord)
    pdf.set_font("Arial", size=12)
    pdf.set_xy(x0, y0 + 20)
    pdf.cell(w=180, h=6, txt="АКТ ОБЩЕЙ ФОРМЫ №", align="C", border=bord)
    pdf.set_font("Arial", size=10)
    pdf.set_xy(x0, y0 + 30)
    pdf.cell(w=180, h=5, txt="Станция, код______Новосибирск-Главный, 850609, Зап.-Сиб. ж.д.___________________________________",
             align="L", border=bord)
    pdf.set_xy(x0, y0 + 38)
    pdf.cell(w=180, h=5, txt="Поезд №_________ на перегоне________________________________________________________________",
             align="L", border=bord)
    pdf.set_xy(x0, y0 + 46)
    pdf.cell(w=180, h=5, txt="«_____»______________________г.", align="R", border=bord)
    pdf.set_xy(x0, y0 + 54)
    pdf.cell(w=180, h=5, txt="Настоящий акт составлен в присутствии следующих лиц:", align="L", border=bord)
    pdf.set_xy(x0, y0 + 62)
    pdf.cell(w=180, h=5, txt="___________________________________________________________________________________________",
             align="L", border=bord)
    pdf.set_xy(x0, y0 + 70)
    pdf.cell(w=180, h=5, txt="___________________________________________________________________________________________",
             align="L", border=bord)
    pdf.set_xy(x0, y0 + 78)
    pdf.cell(w=180, h=5, txt="___________________________________________________________________________________________",
             align="L", border=bord)
    pdf.set_xy(x0, y0 + 86)
    pdf.cell(w=180, h=5, txt="Перевозчик___АО «ФПК»_____________________________________________________________________",
             align="L", border=bord)
    pdf.set_xy(x0, y0 + 94)
    pdf.cell(w=180, h=5, txt="Станция отправления__Новосибирск-Главный Зап.-Сиб. железная дорога____________________________",
             align="L", border=bord)
    pdf.set_xy(x0, y0 + 102)
    pdf.cell(w=180, h=5, txt="Станция назначения_________________________________________________________________________",
             align="L", border=bord)
    pdf.set_xy(x0, y0 + 110)
    pdf.cell(w=180, h=5, txt="Отправка №________________________________________________________________________________",
             align="L", border=bord)
    pdf.set_xy(x0, y0 + 118)
    pdf.cell(w=180, h=5, txt="Дата приема груза к перевозке «_____»______________________г.",
             align="L", border=bord)
    pdf.set_xy(x0, y0 + 126)
    pdf.cell(w=180, h=5, txt="___________________________________________________________________________________________",
             align="L", border=bord)
    pdf.set_xy(x0, y0 + 134)
    pdf.cell(w=180, h=5, txt="___________________________________________________________________________________________",
             align="L", border=bord)
    pdf.set_xy(x0, y0 + 142)
    pdf.cell(w=180, h=5, txt="Вагон, контейнер №_________________________________________________________________________",
             align="L", border=bord)
    pdf.set_xy(x0, y0 + 150)
    pdf.cell(w=180, h=5, txt="наименование груза__________________________________________________________________________",
             align="L", border=bord)
    pdf.set_xy(x0, y0 + 158)
    pdf.cell(w=180, h=5, txt="Описание обстоятельств, вызвавших составление акта:",
             align="L", border=bord)
    """pdf.set_xy(x0, y0 + 166)
    pdf.cell(w=180, h=5, txt="___________________________________________________________________________________________",
             align="L", border=bord)
    pdf.set_xy(x0, y0 + 174)
    pdf.cell(w=180, h=5, txt="___________________________________________________________________________________________",
             align="L", border=bord)
    pdf.set_xy(x0, y0 + 182)
    pdf.cell(w=180, h=5, txt="___________________________________________________________________________________________",
             align="L", border=bord)
    pdf.set_xy(x0, y0 + 190)
    pdf.cell(w=180, h=5, txt="___________________________________________________________________________________________",
             align="L", border=bord)
    pdf.set_xy(x0, y0 + 198)
    pdf.cell(w=180, h=5, txt="___________________________________________________________________________________________",
             align="L", border=bord)
    pdf.set_xy(x0, y0 + 206)
    pdf.cell(w=180, h=5, txt="___________________________________________________________________________________________",
             align="L", border=bord)
    pdf.set_xy(x0+100, y0 + 214)
    pdf.cell(w=90, h=5, txt="Подписи:",
             align="L", border=bord)
    pdf.set_xy(x0, y0 + 222)
    pdf.cell(w=180, h=5, txt="__________________________________",
             align="R", border=bord)
    pdf.set_xy(x0, y0 + 230)
    pdf.cell(w=180, h=5, txt="__________________________________",
             align="R", border=bord)
    pdf.set_xy(x0, y0 + 238)
    pdf.cell(w=180, h=5, txt="__________________________________",
             align="R", border=bord)"""


    return pdf

def create_text_for_GU23(vagon, number, client, op):#заполнение акта ГУ-23 для операции ТО
    x0 = 20
    y0 = 10
    bord = 0
    activate = 0
    text = ''
    time = vagon[op - 1][1]# + datetime.timedelta(minutes=30)
    text_0 = str(time.date().strftime("%d.%m.%y")) + "г." + ' ' + str(time.time().strftime("%H:%M"))
    time = vagon[op][1]# + datetime.timedelta(minutes=30)
    text_1 = str(time.date().strftime("%d.%m.%y")) + "г." + ' ' + str(time.time().strftime("%H:%M"))
    text_2 = int((vagon[op][1] - vagon[op - 1][1]).total_seconds())
    if (text_2 / 3600 - text_2 // 3600) >= 0.25:
        text_2 = str(text_2 // 3600 + 1)
    else:
        text_2 = str(text_2 // 3600)

    if len(text_2) >= 2 and text_2[len(text_2) - 2] == '1':
        text_2 = text_2 + ' часов. '
    elif len(text_2) >= 2 and text_2[len(text_2) - 2] != '1':
        if text_2[len(text_2) - 1] == '1':
            text_2 = text_2 + ' час. '
        elif text_2[len(text_2) - 1] == '2' or text_2[len(text_2) - 1] == '3' or text_2[len(text_2) - 1] == '4':
            text_2 = text_2 + ' часа. '
        else:
            text_2 = text_2 + ' часов. '
    else:
        if text_2[len(text_2) - 1] == '1':
            text_2 = text_2 + ' час. '
        elif text_2[len(text_2) - 1] == '2' or text_2[len(text_2) - 1] == '3' or text_2[len(text_2) - 1] == '4':
            text_2 = text_2 + ' часа. '
        else:
            text_2 = text_2 + ' часов. '
    if vagon[op][4] == client:
        if vagon[op][0] == 'Проведение ТО' and vagon[op][4] == 'Почта России':  # операция проведения ТО
            text = "На станции Новосибирск-Главный произведены маневровые работы по подаче вышеуказанного вагона с пути №" \
                   + str(vagon[op - 1][2]) + " (" + str(vagon[op - 1][3]) + ")" + " на путь №" + str(vagon[op][2
                                                                                                     ]) + " (" + str(
                vagon[op][3]) + ")" + " для проведения ТО-1. " + "Произведены маневровые работы по уборке " \
                                                                 "данного вагона с пути №" + str(
                vagon[op][2]) + " (" + str(vagon[op][3]) + ")" + " на путь №" + str(vagon[op + 1
                                                                                          ][2] + " " + "(" + str(
                vagon[op + 1][3]) + ")" + " после проведения ТО-1. ") + "Начало нахождения вагона на пути" \
                                                                        " отстоя " + text_0 + ", окончание нахождения на " \
                                                                                              "пути отстоя " + text_1 + ". Время простоя составило: " + text_2
        elif vagon[op][0] == 'Подача на пути отстоя':  # операция подачи на пути отстоя
            text = "На станции Новосибирск-Главный произведены маневровые работы по подаче вышеуказанного вагона с пути №" \
                   + str(vagon[op - 1][2]) + " (" + str(vagon[op - 1][3]) + ")" + " на путь отстоя №" + str(vagon[op][2                                                                                                            ]) + " (" + str(
                vagon[op][3]) + ")" + " по заявке " + str(client) + ". " + "Произведены маневровые работы по уборке " \
                                                                           "данного вагона с пути отстоя №" + str(
                vagon[op][2]) + " (" + str(vagon[op][3]
                                           ) + ")" + " на путь №" + str(
                vagon[op + 1][2] + " " + "(" + str(vagon[op + 1][3]) + ")" + ". "
                ) + "Начало нахождения вагона на пути отстоя " + text_0 + ", окончание нахождения на пути отстоя " \
                   + text_1 + ". Время простоя составило: " + text_2

        elif vagon[op][0] == 'ВУ-36':  # операция нахождения в ремонте - заведение ВУ-23 и последующее ВУ-36
            time = vagon[op - 1][1]
            text_3 = str(time.date().strftime("%d.%m.%y")) + "г." + ' ' + str(time.time().strftime("%H:%M"))
            time = vagon[op][1]
            text_4 = str(time.date().strftime("%d.%m.%y")) + "г." + ' ' + str(time.time().strftime("%H:%M"))

            text = "На станции Новосибирск-Главный на вагон №" + str(number) + " выписана справка формы ВУ-23 " + text_3 \
                   + ". С " + text_0 + " вагон находится на ответсвенном простое собственника " + str(vagon[op][4]) \
                   + ". Окончание нахождения вагона в ремонте согласно справки ВУ-36 " + text_4 + ". Произведены" \
                   " маневровые работы по подаче вышеуказанного вагона с пути №" + str(vagon[op - 1][2]) +\
                   " (" + str(vagon[op - 1][3]) + ")" + " на путь №" + str(vagon[op][2]) + " (" + str(vagon[op][3]) +\
                   ")" + " по заявке " + str(client) + ". Время простоя составило: " + text_2

        elif vagon[op][0] == 'Отправление':  # операция ожидания отправления
            text = "На станции Новосибирск-Главный произведены маневровые работы по подаче вышеуказанного вагона с пути №" \
                   + str(vagon[op - 1][2]) + " (" + str(vagon[op - 1][3]) + ")" + " на путь отстоя №" + str(vagon[op][2]) \
                   + " (" + str(vagon[op][3]) + ") в ожидании отправления в составе поезда. Начало нахождения вагона на пути отстоя "\
                   + text_0 + ", окончание нахождения на пути отстоя " + text_1 + ". Время простоя составило: " + text_2
        activate = 1

    elif vagon[op - 1][4] == client:
        if vagon[op][0] == 'ВУ-23':  # операция простоя вагона до заведения в ремонт - заведение ВУ-23
            time = vagon[op - 1][1]
            text_3 = str(time.date().strftime("%d.%m.%y")) + "г." + ' ' + str(time.time().strftime("%H:%M"))
            time = vagon[op][1]
            text_4 = str(time.date().strftime("%d.%m.%y")) + "г." + ' ' + str(time.time().strftime("%H:%M"))

            text = "На станции Новосибирск-Главный на вагон №" + str(number) + " выписана справка формы ВУ-23 " + text_4 \
                   + ". С " + text_0 + " вагон находится на ответсвенном простое " + str(vagon[op - 1][4]) \
                   + " на пути №30 Восточного парка. Окончание нахождения вагона на ответственном простое " +\
                   str(vagon[op - 1][4]) + " - " + str(text_4) + ". Время простоя составило: " + text_2
            activate = 1

    return [activate, text]

def write_vagon_GU23(pdf, vagon, text, number, client):
    x0 = 20
    y0 = 10
    bord = 0
    tex = r'\S{1,30}\s'
    text = re.findall(tex, text)
    string = ''
    #row = 0
    strings = []
    pdf.set_font("Arial", size=10)
    pdf.set_xy(x0 + 35, y0 + 142)
    for n in range(8 - len(str(number))):
        number = '0' + str(number)
    pdf.cell(w=180, h=5, txt=str(number), align="L", border=bord)
    pdf.set_xy(x0, y0 + 62)
    pdf.cell(w=180, h=5, txt="Дежурный по парку станции Новосибирск-Главный", align="L", border=bord)
    pdf.set_xy(x0, y0 + 70)
    pdf.cell(w=180, h=5, txt="Приемосдатчик груза и багажа станции Новосибирск-Главный ", align="L",
             border=bord)
    pdf.set_xy(x0, y0 + 78)
    pdf.cell(w=180, h=5, txt="Представитель " + str(client), align="L", border=bord)
    count = count_GU23()
    date_act = vagon[len(vagon) - 1][1]
    pdf.set_xy(x0 + 123, y0 + 46)
    pdf.cell(w=20, h=5, txt=str(date_act.day), align="L", border=bord)
    pdf.set_xy(x0 + 145, y0 + 46)
    month = str(date_act.month)
    if len(month) == 1:
        month = '0' + month
    pdf.cell(w=20, h=5, txt=month, align="L", border=bord)
    pdf.set_xy(x0 + 165, y0 + 46)
    pdf.cell(w=20, h=5, txt=str(date_act.year), align="L", border=bord)

    pdf.set_font("Arial", size=12)
    pdf.set_xy(x0 + 115, y0 + 20)
    pdf.cell(w=10, h=6, txt=str(count + 1), align="L", border=bord)
    write_count_GU23(count)

    pdf.set_font("Arial", size=10)
    for word in range(len(text)):
        if len(string + text[word]) <= 95 and word != len(text) - 1:
            string += text[word]
        elif len(string + text[word]) <= 95 and word == len(text) - 1:
            string += text[word]
            strings.append(string)
        else:
            strings.append(string)
            string = text[word]
            if word == len(text) - 1:
                strings.append(string)
    pages = 1
    for row in range(len(strings)):
        if row <= 9:
            pdf.set_xy(x0, y0 + 166 + row * 8)
            pdf.cell(w=180, h=5, txt=strings[row], align="L", border=bord, ln=2)
        else:
            if pages == 1:
                pdf.add_page()
                pages += 1
            pdf.set_xy(x0, y0 + (row - 9) * 8)
            pdf.cell(w=180, h=5, txt=strings[row], align="L", border=bord)


    if len(strings) <= 7:
        pdf.set_xy(x0 + 100, y0 + 166 + (len(strings) + 1) * 8)
        pdf.cell(w=90, h=5, txt="Подписи:", align="L", border=bord)
        pdf.set_xy(x0, y0 + 166 + (len(strings) + 2) * 8)
        pdf.cell(w=110, h=5, txt="Дежурный по парку станции Новосибирск-Главный", align="R", border=bord)
        pdf.set_xy(x0, y0 + 166 + (len(strings) + 2) * 8)
        pdf.cell(w=180, h=5, txt="__________________________________",
                 align="R", border=bord)
        pdf.set_xy(x0, y0 + 166 + (len(strings) + 3) * 8)
        pdf.cell(w=110, h=5, txt="Приемосдатчик груза и багажа станции Новосибирск-Главный ", align="R",
                 border=bord)
        pdf.set_xy(x0, y0 + 166 + (len(strings) + 3) * 8)
        pdf.cell(w=180, h=5, txt="__________________________________",
                 align="R", border=bord)
        pdf.set_xy(x0, y0 + 166 + (len(strings) + 4) * 8)
        pdf.cell(w=110, h=5, txt="Представитель " + str(client), align="R", border=bord)
        pdf.set_xy(x0, y0 + 166 + (len(strings) + 4) * 8)
        pdf.cell(w=180, h=5, txt="__________________________________",
                 align="R", border=bord)
    else:
        if pages == 1:
            pdf.add_page()
            pages += 1
        pdf.set_xy(x0 + 100, y0 + (len(strings) - 9) * 8)
        pdf.cell(w=90, h=5, txt="Подписи:", align="L", border=bord)
        pdf.set_xy(x0, y0 + (len(strings) - 8) * 8)
        pdf.cell(w=110, h=5, txt="Дежурный по парку станции Новосибирск-Главный", align="R", border=bord)
        pdf.set_xy(x0, y0 + (len(strings) - 8) * 8)
        pdf.cell(w=180, h=5, txt="__________________________________",
                 align="R", border=bord)
        pdf.set_xy(x0, y0 + (len(strings) - 7) * 8)
        pdf.cell(w=110, h=5, txt="Приемосдатчик груза и багажа станции Новосибирск-Главный ", align="R",
                 border=bord)
        pdf.set_xy(x0, y0 + (len(strings) - 7) * 8)
        pdf.cell(w=180, h=5, txt="__________________________________",
                 align="R", border=bord)
        pdf.set_xy(x0, y0 + (len(strings) - 6) * 8)
        pdf.cell(w=110, h=5, txt="Представитель " + str(client), align="R", border=bord)
        pdf.set_xy(x0, y0 + (len(strings) - 6) * 8)
        pdf.cell(w=180, h=5, txt="__________________________________",
                 align="R", border=bord)

    activate = 1

    return [pdf, activate]

def write_vagon_GU(pdf, vagon, number, y, client):#заполняем информацию в памятке ГУ-45 об одном вагоне
    x0 = 20
    y0 = 10
    tab_x = [0, 9, 32, 39, 53, 60, 81, 101, 121, 136, 152, 160, 180]
    bord = 0
    num = 1
    activation = 0
    client_check = False
    for vag in range (1, len(vagon)):
        if vagon[vag][4] == client:
            client_check = True
    if client_check == True:
        for op in range(1, len(vagon)):
            notes = False
            if vagon[op][0] == 'Погрузка':
                oper = 'ПГР'
            elif vagon[op][0] == 'Выгрузка':
                oper = 'ВГР'
            #блок отвечающий за внесение в памятку иных операций, кроме погрузки и выгрузки
            #elif vagon[op][0] == 'Проведение ТО' or vagon[op][0] == 'ВУ-36' or vagon[op][0
            #] == 'Подача на пути отстоя' or vagon[op][0] == 'Отправление' or vagon[op][0] == 'ВУ-23': #or vagon[op][0] == 'Взвешивание'
            #    oper = 'БОП'
            else:
                oper = None
            if oper != None and vagon[op][4] == client and vagon[op][0] != 'ВУ-23':
                notes = True
            elif oper != None and vagon[op][4] != client and vagon[op][0] == 'ВУ-23':
                notes = True
            if notes == True:
                pdf.set_font("Arial", size=10)
                pdf.set_xy(x0 + tab_x[1], y0 + 70 + y * 5)
                for n in range(8 - len(str(number))):
                    number = '0' + str(number)
                pdf.cell(tab_x[2] - tab_x[1], 5, txt=str(number), align="L", border=bord)
                delta_time = vagon[op][1] - vagon[op-1][1]
                if vagon[op][0] == 'Отправление' and delta_time.total_seconds()/3600 >= 1.5:
                    pdf.set_font("Arial", size=8)
                    pdf.set_xy(x0 + tab_x[4], y0 + 65 + num * 5 + y * 5)
                    pdf.cell(tab_x[5] - tab_x[4], 5, txt=oper, align="L", border=bord)
                    pdf.set_font("Arial", size=10)
                    pdf.set_xy(x0 + tab_x[2], y0 + 70 + y * 5)
                    pdf.cell(tab_x[3] - tab_x[2], 5, txt='20', align="L", border=bord)
                    pdf.set_xy(x0 + tab_x[3], y0 + 70 + y * 5)
                    pdf.cell(tab_x[4] - tab_x[3], 5, txt='собств.', align="L", border=bord)
                    pdf.set_xy(x0 + tab_x[5], y0 + 65 + num * 5 + y * 5)
                    if vagon[op - 1][0] != 'Взвешивание':#исключение влияния операции взвешивания
                        time = vagon[op - 1][1]# + datetime.timedelta(minutes=30)
                    else:
                        time = vagon[op - 2][1]# + datetime.timedelta(minutes=30)
                    text = str(time.date().strftime("%d.%m")) + ' ' + str(time.time().strftime("%H:%M"))
                    pdf.cell(tab_x[6] - tab_x[5], 5, txt=text, align="L", border=bord)
                    pdf.set_xy(x0 + tab_x[6], y0 + 65 + num * 5 + y * 5)
                    time = vagon[op][1]# - datetime.timedelta(minutes=30)
                    text = str(time.date().strftime("%d.%m")) + ' ' + str(time.time().strftime("%H:%M"))
                    pdf.cell(tab_x[7] - tab_x[6], 5, txt=text, align="L", border=bord)
                    pdf.set_xy(x0 + tab_x[7], y0 + 65 + num * 5 + y * 5)
                    time = vagon[op][1]# - datetime.timedelta(minutes=30)
                    text = str(time.date().strftime("%d.%m")) + ' ' + str(time.time().strftime("%H:%M"))
                    pdf.cell(tab_x[8] - tab_x[7], 5, txt=text, align="L", border=bord)
                    pdf.set_font("Arial", size=5)
                    pdf.set_xy(x0 + tab_x[11], y0 + 65 + num * 5 + y * 5)
                    if vagon[op][0] == 'ВУ-36':  # добавление примечания (в ремонт) при заведении на больные
                        text = str(vagon[op][2]) + " путь (в ремонт)"
                    else:
                        text = str(vagon[op][2]) + " путь"
                    pdf.cell(tab_x[11] - tab_x[10], 2.5, txt=text, align="L", border=bord)
                    pdf.set_xy(x0 + tab_x[11], y0 + 67.5 + num * 5 + y * 5)
                    text = str(vagon[op][3])
                    pdf.cell(tab_x[11] - tab_x[10], 2.5, txt=text, align="L", border=bord)
                    num += 1
                else:
                    if op != len(vagon) - 1:
                        pdf.set_font("Arial", size=8)
                        pdf.set_xy(x0 + tab_x[4], y0 + 65 + num * 5 + y * 5)
                        pdf.cell(tab_x[5] - tab_x[4], 5, txt=oper, align="L", border=bord)
                        pdf.set_font("Arial", size=10)
                        pdf.set_xy(x0 + tab_x[2], y0 + 70 + y * 5)
                        pdf.cell(tab_x[3] - tab_x[2], 5, txt='20', align="L", border=bord)
                        pdf.set_xy(x0 + tab_x[3], y0 + 70 + y * 5)
                        pdf.cell(tab_x[4] - tab_x[3], 5, txt='собств.', align="L", border=bord)
                        pdf.set_xy(x0 + tab_x[5], y0 + 65 + num * 5 + y * 5)
                        if vagon[op - 1][0] != 'Взвешивание':  # исключение влияния операции взвешивания
                            time = vagon[op - 1][1]# + datetime.timedelta(minutes=30)
                        else:
                            time = vagon[op - 2][1]# + datetime.timedelta(minutes=30)
                        text = str(time.date().strftime("%d.%m")) + ' ' + str(time.time().strftime("%H:%M"))
                        pdf.cell(tab_x[6] - tab_x[5], 5, txt=text, align="L", border=bord)
                        pdf.set_xy(x0 + tab_x[6], y0 + 65 + num * 5 + y * 5)
                        time = vagon[op][1]
                        text = str(time.date().strftime("%d.%m")) + ' ' + str(time.time().strftime("%H:%M"))
                        pdf.cell(tab_x[7] - tab_x[6], 5, txt=text, align="L", border=bord)
                        pdf.set_xy(x0 + tab_x[7], y0 + 65 + num * 5 + y*5)
                        time = vagon[op][1]# + datetime.timedelta(minutes=30)
                        text = str(time.date().strftime("%d.%m")) + ' ' + str(time.time().strftime("%H:%M"))
                        pdf.cell(tab_x[8] - tab_x[7], 5, txt=text, align="L", border=bord)
                        pdf.set_font("Arial", size=5)
                        pdf.set_xy(x0 + tab_x[11], y0 + 65 + num * 5 + y * 5)
                        if vagon[op][0] == 'ВУ-36': #добавление примечания (в ремонт) при заведении на больные
                            text = str(vagon[op][2]) + " путь (в ремонт)"
                        else:
                            text = str(vagon[op][2]) + " путь"
                        pdf.cell(tab_x[11] - tab_x[10], 2.5, txt=text, align="L", border=bord)
                        pdf.set_xy(x0 + tab_x[11], y0 + 67.5 + num * 5 + y * 5)
                        text = str(vagon[op][3])
                        pdf.cell(tab_x[11] - tab_x[10], 2.5, txt=text, align="L", border=bord)
                        num += 1
                activation = 1
    return [pdf, num, activation]

def sorting_client(numbers, path): #сортировка операций по клиентам для создания разных памяток
    clients = []
    for number in numbers:
        vagon = read_vagon(int(number), path)
        vagon_operations = sorting(vagon)
        for op in range (1, len(vagon_operations)):
            if clients.count(vagon_operations[op][4]) == 0:
                clients.append(vagon_operations[op][4])
    #print(clients)
    return clients

def write_GU(numbers, path):#заполняем информацию о всех вагонах
    errores = []
    all_checks = []
    for number in numbers:
        vagon = read_vagon(int(number), path)
        vagon_operations = sorting(vagon)
        check = check_operations(vagon_operations)
        if check[1] == True:
            #checks = True
            all_checks.append(True)
            #errores = check[0]
            errores.append([check[0], number])
        else:
            #checks = False
            all_checks.append(False)
            sort_checks = []
            for i in range (len(check[0])):
                if check[0][i] != 0:
                    sort_checks.append(check[0][i])
                    #errores = [check[0], number]
            errores.append([sort_checks, number])
    if all_checks.count(False) == 0:
        #errores = [check[0], number]
        errores.append([check[0], number])
        clients = sorting_client(numbers, path)
        for client in clients:
            activ_GU = False
            pdf = creat_GU()
            count = count_GU()
            y = 0
            x0 = 20
            y0 = 10
            bord = 0
            for number in numbers:
                #формирование памятки общей формы
                vagon = read_vagon(int(number), path)
                vagon_operations = sorting(vagon)
                pdf = write_vagon_GU(pdf[0], vagon_operations, int(number), y, client)
                #print("!!", number, pdf[2])
                if pdf[2] == 1:
                    activ_GU = True
                    #print("!", number)
                    y += pdf[1] - 1

                #блок отвечающий за формирование актов общей формы на операции с вагонами
                text = ""
                for op in range(len(vagon_operations)):
                    pdf23 = creat_GU23()
                    creted_text = create_text_for_GU23(vagon_operations, int(number), client, op)
                    if creted_text[0] == 1:
                        text += creted_text[1]
                        #count_23 = count_GU23()
                        #pdf23[0].output("./gu_23/gu_23_" + str(count_23) + ".pdf")
                        #os.startfile(os.getcwd() + "./gu_23/gu_23_" + str(count_23) + ".pdf")
                if text != '':
                    pdf23 = write_vagon_GU23(pdf23, vagon_operations, text, number, client)
                    count_23 = count_GU23()
                    pdf23[0].output("./gu_23/gu_23_" + str(count_23) + ".pdf")
                    os.startfile(os.getcwd() + "./gu_23/gu_23_" + str(count_23) + ".pdf")

            #print(client, pdf[2])
            if activ_GU == True:
                pdf[0].set_font("Arial", size=10)
                pdf[0].set_xy(x0 + 40, y0 + 23)
                pdf[0].cell(20, 5, txt=str(client), align="L", border=bord)
                pdf[0].set_xy(x0 + 60, y0 + 16)
                pdf[0].cell(x0, 4, txt=str(count+1), align="L", border=bord)
                write_count(count)
                pdf[0].output("./pamytka/pamytka" + str(count+1) + ".pdf")
                print(os.getcwd())
                os.startfile(os.getcwd() + "./pamytka/pamytka" + str(count+1) + ".pdf")

    return errores



#vagon = read_vagon(number)
#vagon_operations = sorting(vagon)
#check = check_operations(vagon_operations)
#pdf = creat_GU()
#pdf = write_vagon_GU(pdf, vagon_operations, number, 0)
#write_GU(numbers)



