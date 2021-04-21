import datetime
import csv
from operations import *
import math
from ast import literal_eval
import sys

data_start_time = datetime.date(2000, 1, 1)
data_end_time = datetime.date(2021, 1, 1)

with open('data.csv') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    dataset = sorted(reader, key=lambda x: x['date'])


detalization = {'IN': 0, 'OUT': 0,
                'INC_CALL': [{'number': 0, 'length': 0, 'sum': 0}, {'number': 0, 'length': 0, 'sum': 0}],
                'OUT_CALL': [{'number': 0, 'length': 0, 'sum': 0}, {'number': 0, 'length': 0, 'sum': 0}],
                'INC_SMS': {'number': 0, 'sum': 0},
                'OUT_SMS': [{'number': 0, 'sum': 0}, {'number': 0, 'sum': 0}],
                'INT': [{'number': 0, 'sum': 0}, {'number': 0, 'sum': 0}]}
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

    if start_date > data_end_time or end_date < data_start_time or start_date > end_date:
        print('Нет данных')
    else:
        for i in dataset:
            d = i['date'].split()
            d = list(map(int, d[0].split('-')))
            if start_date <= datetime.date(d[0], d[1], d[2]) <= end_date:
                i['operation'] = int(i['operation'])
                i['additional'] = literal_eval(i['additional'])
                if i['operation'] == ROAM_IN:
                    mode = 1
                elif i['operation'] == ROAM_OUT:
                    mode = 0
                elif i['operation'] == TOP_UP:
                    detalization['IN'] += int(i['additional'][0])
                elif i['operation'] == INC_CALL:
                    detalization['OUT'] += int(i['additional'][-1]) * INC_CALL_PR[mode]
                    detalization['INC_CALL'][mode]['sum'] += (math.ceil(i['additional'][-1] / MAX_CALL)) * INC_CALL_PR[mode]
                    detalization['INC_CALL'][mode]['number'] += 1
                    detalization['INC_CALL'][mode]['length'] += i['additional'][-1]
                elif i['operation'] == OUT_CALL:
                    detalization['OUT'] += (math.ceil(i['additional'][-1] / MAX_CALL) * OUT_CALL_PR[mode])
                    detalization['OUT_CALL'][mode]['sum'] += (math.ceil(i['additional'][-1] / MAX_CALL)) * OUT_CALL_PR[mode]
                    detalization['OUT_CALL'][mode]['number'] += 1
                    detalization['OUT_CALL'][mode]['length'] += int(i['additional'][-1])
                elif i['operation'] == INC_SMS:
                    detalization['OUT'] += (math.ceil(len(i['additional'][-1]) / MAX_SMS) * INC_SMS_PR[mode])
                    detalization['INC_SMS']['sum'] += (math.ceil(len(i['additional'][-1]) / MAX_SMS) * INC_SMS_PR[mode])
                    detalization['INC_SMS']['number'] += 1
                elif i['operation'] == OUT_SMS:
                    detalization['OUT'] += (math.ceil(len(i['additional'][-1]) / MAX_SMS) * INC_SMS_PR[mode])
                    detalization['OUT_SMS'][mode]['sum'] += (
                                math.ceil(len(i['additional'][-1]) / MAX_SMS) * OUT_SMS_PR[mode])
                    detalization['OUT_SMS'][mode]['number'] += 1
                elif i['operation'] == INT_SES:
                    detalization['OUT'] += i['additional'][-1] * INT_SES_PR[mode]
                    detalization['INT'][mode]['sum'] += int(i['additional'][-1]) * INT_SES_PR[mode]
                    detalization['INT'][mode]['number'] += int(i['additional'][-1])

        f.write('Период детализации: ' + str(start_date) + ' - ' + str(end_date) + '\n')
        f.write('Общая сумма пополнения: ' + str(detalization['IN']) + ' руб' + '\n')
        f.write('Общие расходы: ' + str(detalization['OUT']) + ' руб' + '\n')
        f.write('Детализация расходов:\n')
        f.write('Входящие звонки (домашняя сеть): ' + str(detalization['INC_CALL'][0]['number'])
                + ', общая продолжительность: ' + str(detalization['INC_CALL'][0]['length'])
                + ' мин, списано: ' + str(detalization['INC_CALL'][0]['sum']) + ' руб\n')
        f.write('Входящие звонки (роуминг): ' + str(detalization['INC_CALL'][1]['number'])
                + ', общая продолжительность: ' + str(detalization['INC_CALL'][1]['length'])
                + ' мин, списано: ' + str(detalization['INC_CALL'][1]['sum']) + ' руб\n')
        f.write('Исходящие звонки (домашняя сеть): ' + str(detalization['OUT_CALL'][0]['number'])
                + ', общая продолжительность: ' + str(detalization['OUT_CALL'][0]['length'])
                + ' мин, списано: ' + str(detalization['OUT_CALL'][0]['sum']) + ' руб\n')
        f.write('Исходящие звонки (роуминг): ' + str(detalization['OUT_CALL'][1]['number'])
                + ', общая продолжительность: ' + str(detalization['OUT_CALL'][1]['length'])
                + ' мин, списано: ' + str(detalization['OUT_CALL'][1]['sum']) + ' руб\n')
        f.write('Входящие SMS: ' + str(detalization['INC_SMS']['number']) + ', списано: '
                + str(detalization['INC_SMS']['sum']) + ' руб\n')
        f.write('Исходящие SMS (домашняя сеть): ' + str(detalization['OUT_SMS'][0]['number']) + ', списано: '
                + str(detalization['OUT_SMS'][0]['sum']) + ' руб\n')
        f.write('Исходящие SMS (роуминг): ' + str(detalization['OUT_SMS'][1]['number']) + ', списано: '
                + str(detalization['OUT_SMS'][1]['sum']) + ' руб\n')
        f.write('Мобильный интернет (домашняя сеть): ' + str(detalization['INT'][0]['number']) + ' Мб, списано: '
                + str(detalization['INT'][0]['sum']) + ' руб\n')
        f.write('Мобильный интернет (роуминг): ' + str(detalization['INT'][1]['number']) + ' Мб, списано: '
                + str(detalization['INT'][1]['sum']) + ' руб\n')
        f.write('\n')
