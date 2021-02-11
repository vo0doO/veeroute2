import csv
from datetime import datetime
import lib.config as config

class DataWrapper:
    """Подготовка данных"""

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


if __name__ == "__main__":
    wrapper = DataWrapper(config.read("config.json"))
    wrapper.group()
    wrapper.save()