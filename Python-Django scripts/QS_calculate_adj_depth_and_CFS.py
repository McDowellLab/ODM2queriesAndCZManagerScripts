
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

depth = Timeseriesresults.objects.filter(resultid=18556).get()
depth_adjusted = Timeseriesresults.objects.filter(resultid=18699).get() #17276
# dischargeresult = Timeseriesresults.objects.filter(resultid=17274).get()#17274
# depthtsrvs = Timeseriesresultvalues.objects.filter(resultid=depth).\
#     filter(valuedatetime__lt='2020-10-11 05:47:52').order_by('-valuedatetime')
depthtsrvs = Timeseriesresultvalues.objects.filter(resultid=depth).order_by('-valuedatetime')
#.filter(valuedatetime__lte='2017-09-13 16:00')
#delete mistakes

# deltsrvs = Timeseriesresultvalues.objects.filter(resultid=dischargeresult)
# for deltsrv in deltsrvs:
#     print(deltsrv)
#     deltsrv.delete()
# deltsrvs = Timeseriesresultvalues.objects.filter(resultid=depth_adjusted)
# for deltsrv in deltsrvs:
#     print(deltsrv)
#     deltsrv.delete()


# deltsrvs = Timeseriesresultvalues.objects.filter(resultid=depth).filter(
#         valuedatetime__gte='2017-05-02 09:00').filter(valuedatetime__lte='2017-05-02 09:30').order_by('-valuedatetime')
# curtime = None
# lasttime = None
# print('depth')
# for deltsrv in deltsrvs:
#     #deltsrv.delete()
#     curtime = deltsrv.valuedatetime
#     if curtime==lasttime:
#         print(deltsrv)
#         deltsrv.delete()
#     lasttime = curtime
i = 0
pivotdatetime = datetime.datetime.strptime(str('2020-05-26 10:00:00'), '%Y-%m-%d %H:%M:%S')
for depthtsrv in depthtsrvs:
    i+=1
    if i % 1000 == 0:
        print(depthtsrv.valuedatetime)
    H = depthtsrv.datavalue
    # adjH = 3.0093 + 2.4063*H + .06942*H**2
    # discharge = -173.4685 + 171.8162 * adjH - 57.4186 * adjH ** 2 + 6.5435 * adjH ** 3
    if depthtsrv.valuedatetime > pivotdatetime:
        adjH = ((H / 30.48) +2.163838)/1.026083
    else:
        adjH = ((H / 30.48) +2.93011)/1.00858
    if i % 1000 == 0:
        print(H)
        print(adjH)

    # dis = 0.001541*(adjH**b)
    #print('unadjusted ' + str(H))
    #print('adjusted ' + str(adjH))
    #print('discharge cfs ' + str(discharge))
    if H >0.0:
        tsrv = Timeseriesresultvalues(resultid=depth_adjusted, datavalue=adjH, valuedatetime=depthtsrv.valuedatetime,
                                      valuedatetimeutcoffset=depthtsrv.valuedatetimeutcoffset,
                                      censorcodecv=depthtsrv.censorcodecv,
                                      qualitycodecv=depthtsrv.qualitycodecv,
                                      timeaggregationinterval=depthtsrv.timeaggregationinterval,
                                      timeaggregationintervalunitsid=depthtsrv.timeaggregationintervalunitsid)
        tsrv.save()
        # tsrv2 = Timeseriesresultvalues(resultid=dischargeresult, datavalue=discharge, valuedatetime=depthtsrv.valuedatetime,
        #                               valuedatetimeutcoffset=depthtsrv.valuedatetimeutcoffset,
        #                               censorcodecv=depthtsrv.censorcodecv,
        #                               qualitycodecv
        #                                =depthtsrv.qualitycodecv,
        #                               timeaggregationinterval=depthtsrv.timeaggregationinterval,
        #                               timeaggregationintervalunitsid=depthtsrv.timeaggregationintervalunitsid)
        # tsrv2.save()