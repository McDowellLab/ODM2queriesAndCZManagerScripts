
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
depth_adjusted = Timeseriesresults.objects.filter(resultid=17276).get() #17276
waterpressure = Timeseriesresults.objects.filter(resultid=17261).get()
baropressure = Timeseriesresults.objects.filter(resultid=16154).get()
print(depth)
print(waterpressure)
wpvalues = Timeseriesresultvalues.objects.filter(resultid=waterpressure).\
    filter(valuedatetime__gt='2019-04-11 15:20').order_by('-valuedatetime') # .filter(valuedatetime__lte='2017-09-13 16:00')

print(len(wpvalues))
bpvalues = Timeseriesresultvalues.objects.filter(resultid=baropressure).\
    filter(valuedatetime__gt='2019-04-11 15:20').order_by('-valuedatetime') # .filter(valuedatetime__lte='2017-09-13 16:00')
tsrv = None
for wpvalue in wpvalues:
    for bpvalue in bpvalues:
        if wpvalue.valuedatetime == bpvalue.valuedatetime:

            # 1 kpa = 208.85472 lb/ft^2

            Patdepth = wpvalue.datavalue * 208.85472
            Patmo = bpvalue.datavalue *208.85472
            g = 32.17405 #ft/s^2
            D= 62.427965 #lb /ft^3
            H = (Patdepth - Patmo) / (D*g)
            # print(str(Patdepth) + ' water pressure ' + str(Patmo) + ' atmo pressure ')
            # print(str(H) + ' ft')
            tsrv = Timeseriesresultvalues(resultid=depth, datavalue=H,valuedatetime=wpvalue.valuedatetime,
                                   valuedatetimeutcoffset=wpvalue.valuedatetimeutcoffset,censorcodecv=wpvalue.censorcodecv,
                                   qualitycodecv=wpvalue.qualitycodecv,timeaggregationinterval=wpvalue.timeaggregationinterval,
                                   timeaggregationintervalunitsid=wpvalue.timeaggregationintervalunitsid)
            tsrv.save()
            #173.4685 + 171.8162 * B11 - 57.4186 * B11 ^ 2 + 6.5435 * B11 ^ 3
            #stage heights likely need to be adjusted

print(tsrv)