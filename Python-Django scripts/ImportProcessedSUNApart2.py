import datetime
from os import listdir
from os.path import isfile, join
import pandas
import os
import csv
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "templatesAndSettings.settings.developmentNO")
application = get_wsgi_application()
from django.db.models import Q
import re
from django.core.exceptions import ObjectDoesNotExist
from odm2admin.models import *
from django.db.models import Min, Max

mypath = "C:/Users/12672/Box/data/SUNA_330_Sondaora/new/SUNA1028_BATCH_pro.csv"
# sunafiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

# numbers = [7, 12, 16, 18]
# hours = [datetime.time(num).strftime("%I:00 %p") for num in numbers]
i = 0
datetimes = []
data = []
with open(mypath, 'r')as tempfile:
    reader = csv.reader(tempfile)
    i = 0
    sumMgL = 0
    sumUm = 0
    rawUm = 0
    rawmgL = 0
    countrows = 0
    dateandtime = None
    lastrow = None
    lastdt = None
    for row in reader:
        i += 1
        # print(row)
        if i> 8:
            date = row[1]
            date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            # print(date)
            time = datetime.datetime.strptime(row[2], '%H:%M:%S.%f').time()
            # subtract UTC offset to convert to AST 4 hours
            delta = datetime.timedelta(hours=-4)
            time = (datetime.datetime.combine(date, time) + delta).time()
            dateandtime = datetime.datetime.combine(date, time)
        if i == 9:
            sumMgL = float(row[6])
            sumUm = float(row[5])
            rawUm = float(row[3])
            rawmgL = float(row[4])
            countrows += 1
        if i > 9:
            difference = dateandtime - lastdt
            minutes = int((difference.total_seconds() / 60) % 60)
            # print(minutes)
            if minutes >5:
                # print(time)
                # dateandtime = datetime.datetime.combine(date, time)
                # print(dateandtime)
                datetimes.append(lastdt)
                countrows += 1
                sumMgL = (float(row[6]) + sumMgL) / countrows
                sumUm = (float(row[5]) + sumUm) / countrows
                rawUm = (float(row[3]) + rawUm) / countrows
                rawmgL = (float(row[4]) + rawmgL) / countrows
                data.append([lastdt, sumMgL, sumUm, rawUm, rawmgL])
                countrows = 0
                rawUm = 0
                sumcol4 = 0
                sumMgL = 0
                sumUm = 0
                if i < 480:
                    print(lastdt)
            else:
                sumMgL += float(row[6])
                sumUm += float(row[5])
                rawUm += float(row[3])
                rawmgL += float(row[4])
                countrows += 1
        if i > 8:
            lastrow = row
            lastdt = dateandtime
        #     break
datetimes.sort()
length = len(datetimes)
print(length)
print(datetimes[0])
print(datetimes[length - 1])
df = pandas.DataFrame(data, columns=['datetime', 'umprocNO3', 'mglprocNO3', 'rawumNO3', 'rawmgLNO3'])
df.to_pickle("SUNAprocessed1028.pkl")
df.to_csv('SUANreprocessed1028.csv')
print(df.head())
print(df.tail())
print(df.describe())
dfvalid = df[df.umprocNO3 > 0]
print('greater then 0 df.umNO3')
print(dfvalid.count())