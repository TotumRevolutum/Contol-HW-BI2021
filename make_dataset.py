import csv
import random
import datetime
from operations import *

'''Т.к выход в роуминг невозможно выставить рандомно, иначе будет неправильная скобочная последовательность,
то команды по входу и выходу в роуминг вручную добавлены в конечный файл'''


def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + datetime.timedelta(seconds=random_second)


def random_line():
    start_date = datetime.datetime(2000, 1, 1, 0, 0, 0)
    end_date = datetime.datetime(2021, 1, 1, 0, 0, 0)
    random_number_of_days = random_date(start_date, end_date)
    k = random.randint(1, 6)
    add = [None]
    if k == TOP_UP:
        add = [random.randint(1, 1000)]
    elif k == INC_CALL or k == OUT_CALL:
        add = ['8' + str(random.randint(9000000000, 9999999999)), random.randint(1, 200)]
    elif k == INC_SMS or k == OUT_SMS:
        out_str = ''
        for _ in range(0, random.randint(1, 100)):
            out_str += chr(random.randint(65, 90))
        add = ['8' + str(random.randint(9000000000, 9999999999)), out_str.lower()]
    elif k == INT_SES:
        add = [random.randint(1, 1000)]
    return [random_number_of_days, k, add]


oper_data = ["date", "operation", "additional"]
myFile = open('data.csv', 'w')
with myFile:
    file_writer = csv.writer(myFile, delimiter=',')
    file_writer.writerow(oper_data)
    for i in range(200):
        file_writer.writerow(random_line())
