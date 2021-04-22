import datetime
import csv
from functions import *
import sys

data_start_time = datetime.date(2000, 1, 1)
data_end_time = datetime.date(2021, 1, 1)

with open('data.csv') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    dataset = sorted(reader, key=lambda x: x['date'])

mode = 0  # mode = 0 вне роуминга; mode = 1 внутри роуминга
f = open('output.txt', 'w')

while True:
    start = (input('Введите дату начала периода в формате yyyy-mm-dd\n'
                   'Если вы хотите завершить программу - введите 0\n'))
    if start == '0':
        f.close()
        sys.exit()
    end = (input('Введите дату окончания периода в формате yyyy-mm-dd\n'))
    while True:
        try:
            start = list(map(int, start.split('-')))
            end = list(map(int, end.split('-')))
            start_date = datetime.date(start[0], start[1], start[2])
            end_date = datetime.date(end[0], end[1], end[2])
            break
        except Exception:
            print('Некорректная дата')
            start = (input('Введите дату начала периода в формате yyyy-mm-dd\n'
                           'Если вы хотите завершить программу - введите 0\n'))
            if start == '0':
                f.close()
                sys.exit()
            end = (input('Введите дату окончания периода в формате yyyy-mm-dd\n'))

    detalization = {'IN': 0, 'OUT': 0,
                    'INC_CALL': [{'number': 0, 'length': 0, 'sum': 0}, {'number': 0, 'length': 0, 'sum': 0}],
                    'OUT_CALL': [{'number': 0, 'length': 0, 'sum': 0}, {'number': 0, 'length': 0, 'sum': 0}],
                    'INC_SMS': {'number': 0, 'sum': 0},
                    'OUT_SMS': [{'number': 0, 'sum': 0}, {'number': 0, 'sum': 0}],
                    'INT': [{'number': 0, 'sum': 0}, {'number': 0, 'sum': 0}]}

    if start_date > data_end_time or end_date < data_start_time or start_date > end_date:
        print('Нет данных')
    elif start_date > end_date:
        print('Некорректный промежуток')
    else:
        for i in dataset:
            d = i['date'].split()
            d = list(map(int, d[0].split('-')))
            if int(i['operation']) == ROAM_IN:
                mode = 1
            elif int(i['operation']) == ROAM_OUT:
                mode = 0
            elif start_date <= datetime.date(d[0], d[1], d[2]) <= end_date:
                add_info(i, detalization, mode)
        print_detal(f, detalization, start_date, end_date)
