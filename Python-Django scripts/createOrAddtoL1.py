
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

# parser.add_argument('createorupdateL1', nargs=1, type=str)
# parser.add_argument('resultid', nargs=1, type=str)
# parser.add_argument('email', nargs=1, type=str)
series = [16156] # 17172, 18700,16158
# createseries = [18702]
# TIME SERIES END DATE PROBABLY DID NOT MATCH
for ts in series:
    print(ts)
    # startdate = '2019-01-11 13:15:00'
    # enddate = '2019-09-20 12:00:00'
    # management.call_command('UpdateMissingL1vals','update',str(ts),startdate,enddate,  '')
    # startdate = '2019-09-20 12:15:00'
    # enddate = '2019-09-27 17:00:00'

    # management.call_command('UpdateMissingL1vals','update',str(ts), startdate,enddate,  '')
    # startdate = '2019-09-27 17:15:00'
    # enddate = '2019-10-17 10:30:00'
    # management.call_command('UpdateMissingL1vals','update',str(ts), startdate,enddate,  '')
    # startdate = '2019-10-17 10:30:00'
    # enddate = '2020-01-15 14:45:00'
    # management.call_command('UpdateMissingL1vals','update',str(ts), startdate,enddate,  '')
# for ts in createseries:
#     management.call_command('create_l1_timeseries', 'create', str(ts), '')

# 17385, 18627,18569,18559, 18643,
series = [18647,18648,18646,18558] # ,18644, 17280,
# series = [17219] # this is an L2
for ts in series:
    print(ts)
    lents = len(Timeseriesresultvalues.objects.filter(resultid=ts))
    # 18643
    startdate = '2020-10-28 08:47:00'
    enddate = '2020-11-14 08:15:00'
    # 17280
    startdate = '2019-01-28 01:16:00'
    enddate = '2020-07-18 08:29:00'
    #18569
    startdate = '2019-04-08 23:47:00'
    enddate = '2019-05-09 23:00:00'
    # 2019-01-10 13:31
    # 2019-01-28 01:29
    startdate = '2019-01-11 13:31:00'
    enddate = '2019-01-28 01:29:00'
    if lents > 0:
        print('update')
        management.call_command('create_l1_timeseries','update',str(ts),  '') #
    else:
        print('create')
        management.call_command('create_l1_timeseries','create',str(ts),  '') #
    # startdate = '2020-09-18 23:45:00'
    # enddate = '2020-12-21 13:00:00'
    # management.call_command('UpdateMissingL1vals','update','17280', startdate,enddate,  '')
