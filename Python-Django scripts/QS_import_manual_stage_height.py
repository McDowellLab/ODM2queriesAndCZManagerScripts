
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
import pandas

depth = Timeseriesresults.objects.filter(resultid=17273).get()
dpvalue = Timeseriesresultvalues.objects.filter(resultid=17273).first()
print(dpvalue)
manual_depth = Timeseriesresults.objects.filter(resultid=17275).get()

readings = pandas.read_csv('SonadoraStageHeightManualMeasurements3-7-19.csv', sep=',')

print(readings.describe())

stage_heights = readings['stage_ft']
stage_dates = readings['date']
stage_times = readings['time']
for stage_height,stage_date,stage_time in zip(stage_heights,stage_dates,stage_times):
    print(stage_height)
    strdt = str(stage_date) + " " + str(stage_time)
    print(strdt)
    dt = time.strptime(strdt,'%m/%d/%Y %H:%M')
    stfrdt=time.strftime("%Y-%m-%d %H:%M:%S", dt)
    print(stfrdt)
    tsrv = Timeseriesresultvalues(resultid=manual_depth, datavalue=stage_height, valuedatetime=stfrdt,
                                  valuedatetimeutcoffset=dpvalue.valuedatetimeutcoffset,
                                  censorcodecv=dpvalue.censorcodecv,
                                  qualitycodecv=dpvalue.qualitycodecv,
                                  timeaggregationinterval=dpvalue.timeaggregationinterval,
                                  timeaggregationintervalunitsid=dpvalue.timeaggregationintervalunitsid)
    tsrv.save()
    print(tsrv)