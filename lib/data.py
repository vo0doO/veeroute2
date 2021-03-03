import csv
from datetime import datetime


class Wrapper:
    """Подготовка данных"""

    day_with_mount = [
        """[номер_месяца, кол-во дней]"""
        [1, 31],
        [2, 28],
        [3, 31],
        [4, 30],
        [5, 31],
        [6, 30],
        [7, 31],
        [8, 31],
        [9, 30],
        [10, 31],
        [11, 30],
        [12, 31],
    ]

    def __init__(self, config):
        self.config = config
        self.rows = []
        self.string = [0, float(0)]

    def group(self):
        """Группировка суммы по дням"""

        with open(self.config["path"]["data"], "r") as f:
            data = csv.reader(f)
            count = 0
            for row in data:
                if count > 0:
                    date = datetime.fromisoformat(str(row[0]).replace('Z', '')).date()
                    cash = round(float(row[1]), 0)
                    if self.string[0] == date:
                        self.string[1] = int(round(self.string[1] + cash, 0))
                        continue
                    elif self.string[0] == 0:
                        self.string[0] = date
                        self.string[1] = int(cash)
                        continue
                    else:
                        self.string[0] = self.string[0].isoformat()
                        self.rows.append([self.string[0], self.string[1]])
                        self.string[0] = date
                        self.string[1] = int(cash)
                        continue
                else:
                    self.rows.append([row[0], row[1]])
                    count = count + 1
                continue

    def clean(self):

        with open(self.config["path"]["data"], "r") as f:
            data = csv.reader(f) # данные

            count = 1
            rows = []

            # заполняем временный список строк
            for row in data:
                if count > 0:
                    rows.append(row)
                else:
                    continue

            # анализируем текущий датасет и заполняем пробелы
            count = 0
            cleaned_rows = []
            while count < len(rows):
                date = datetime.fromisoformat(rows[count][0])
                date_next = datetime.fromisoformat(rows[count+1][0])
                # если день в первой дате равен максимально возможному числу дней в данном месяце 
                if date.day == Wrapper.day_with_mount[date.month - 1][1]:
                    # если день в следующей дате не равен 1
                    if date_next.day != 1:
                        rows.append([])
                    # TODO: прописать в словарь все исключения
                    #  по месяцам(30 дней или 31 день) а также феврали(по 28 дней)
                    #  для принятия решения о записи строки в массив
                    #  проверять текущею дату на вхождение по массивам исключений
 
                    count = count + 1

    def save(self):
        """Запись сгруппированных данных в новый файл"""
        with open(self.config["path"]["cleaned_data"], encoding="utf-8", mode="w") as new_f:
            for line in self.rows:
                count = 0
                for item in line:
                    new_f.write(str(item))
                    if count == 0:
                        new_f.write(",")
                        count = count + 1
                    else:
                        count = 0
                new_f.write("\n")