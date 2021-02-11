import json


def read(path):
    """Прочитать json и вернуть словарь python"""
    try:
        with open(path, 'r', encoding='utf-8') as file:
            jsonstring = json.load(file)
            data = dict(eval(str(jsonstring)))
            return data
    except Exception as err:
        print(err)
