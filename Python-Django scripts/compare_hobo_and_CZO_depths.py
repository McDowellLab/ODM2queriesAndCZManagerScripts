
import os
import csv
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "templatesAndSettings.settings.developmentNO")
application = get_wsgi_application()
from django.db.models import Q
import re

from django.core.exceptions import ObjectDoesNotExist
import datetime
from odm2admin.models import *
import odm2admin.modelHelpers as modelHelpers
from django.db.models import Min, Max
import time as time
import xlrd


depth = Timeseriesresults.objects.filter(resultid=17273).get()
CZO_depth_vals = Timeseriesresultvalues.objects.filter(resultid=depth).\
    filter(valuedatetime__gt='2018-07-05 12:30').order_by('-valuedatetime')

hobo_depth = Timeseriesresults.objects.filter(resultid=18597).get()
hobo_depth_vals = Timeseriesresultvalues.objects.filter(resultid=hobo_depth).\
    filter(valuedatetime__gt='2018-07-05 12:30').order_by('-valuedatetime')
print('czo vals: ' + str(len(CZO_depth_vals)))
print('hobo vals: ' + str(len(hobo_depth_vals)))
totalczodepth = 0
totalhobodepth = 0
mismatch = 0
mismatchpos = 0
mismatchneg = 0
for czo_d, hobo_d in zip(CZO_depth_vals,hobo_depth_vals):
    diff  = hobo_d.datavalue - czo_d.datavalue
    totalczodepth += czo_d.datavalue
    totalhobodepth += hobo_d.datavalue
    # print(diff)
    if diff > 0.001:
        print('czo ' + str(czo_d.datavalue))
        print('hobo ' + str(hobo_d.datavalue))
        print('dif: ' + str(diff))
        mismatch +=1
        mismatchpos +=1
    elif diff < -0.001:
        print('czo ' + str(czo_d.datavalue))
        print('hobo ' + str(hobo_d.datavalue))
        print('dif: ' + str(diff))
        mismatch +=1
        mismatchneg += 1

print(' values that dont match hobo value bigger then CZO value: ' + str(mismatchpos))
print(' values that dont match CZO value bigger then hobo value: ' + str(mismatchneg))
print(' values that dont match : ' + str(mismatch))
print('czo total depth: ' + str(totalczodepth))
print('hobo total depth: ' + str(totalhobodepth))