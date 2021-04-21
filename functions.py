import math
from ast import literal_eval
from operations import *


def print_detal(f, detalization, start_date, end_date):
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


def add_info(i, detalization, mode):
    i['operation'] = int(i['operation'])
    i['additional'] = literal_eval(i['additional'])
    if i['operation'] == TOP_UP:
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
