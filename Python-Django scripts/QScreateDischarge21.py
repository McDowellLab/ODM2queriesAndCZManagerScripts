
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

depth_adj_Hobo = Timeseriesresults.objects.filter(resultid=17276).get()
depth_adjusted = Timeseriesresults.objects.filter(resultid=18699).get() #17276
dischargeresult = Timeseriesresults.objects.filter(resultid=18641).get()#17274
# depthtsrvs = Timeseriesresultvalues.objects.filter(resultid=depth).\
#     filter(valuedatetime__lt='2020-10-11 05:47:52').order_by('-valuedatetime')
depth_adj_Hobotsrvs = Timeseriesresultvalues.objects.filter(resultid=depth_adj_Hobo). \
    filter(valuedatetime__lt='2018-03-12 10:14:00').order_by('-valuedatetime')
depth_adjustedtsrvs = Timeseriesresultvalues.objects.filter(resultid=depth_adjusted
                ).filter(valuedatetime__gt='2018-03-12 10:14:00').order_by('-valuedatetime')

i = 0
pivotdatetime = datetime.datetime.strptime(str('2018-03-12 10:14:00'), '%Y-%m-%d %H:%M:%S')
for depthtsrv in depth_adj_Hobotsrvs:
    i+=1
    # qsq$DischargeCFS_new <- ifelse(qsq$stage_adjusted_ft > 5, 0.003823*qsq$stage_adjusted_ft^6.007605,
    #                                2.958219e-06*qsq$stage_adjusted_ft^1.045713e+01)


    if i % 1000 == 0:
        print(depthtsrv.valuedatetime)
        print('%f' % 2.958219e-06)
    H = depthtsrv.datavalue
    if depthtsrv.datavalue > 5.0:
        cfs = 0.003823*(depthtsrv.datavalue^6.007605)
    else:
        cfs = 2.958219e-06*(depthtsrv.datavalue^1.045713e+01)
    if i % 1000 == 0:
        print(cfs)
        # print(adjH)

    # dis = 0.001541*(adjH**b)
    #print('unadjusted ' + str(H))
    #print('adjusted ' + str(adjH))
    #print('discharge cfs ' + str(discharge))
    if cfs >0.0:
        tsrv = Timeseriesresultvalues(resultid=dischargeresult, datavalue=cfs, valuedatetime=depthtsrv.valuedatetime,
                                      valuedatetimeutcoffset=depthtsrv.valuedatetimeutcoffset,
                                      censorcodecv=depthtsrv.censorcodecv,
                                      qualitycodecv=depthtsrv.qualitycodecv,
                                      timeaggregationinterval=depthtsrv.timeaggregationinterval,
                                      timeaggregationintervalunitsid=depthtsrv.timeaggregationintervalunitsid)
        tsrv.save()
i = 0
print('hobo done')
pivotdatetime = datetime.datetime.strptime(str('2018-03-12 10:14:00'), '%Y-%m-%d %H:%M:%S')
for depthtsrv in depth_adjusted:
    i+=1
    # qsq$DischargeCFS_new <- ifelse(qsq$stage_adjusted_ft > 5, 0.003823*qsq$stage_adjusted_ft^6.007605,
    #                                2.958219e-06*qsq$stage_adjusted_ft^1.045713e+01)


    if i % 1000 == 0:
        print(depthtsrv.valuedatetime)
        print('%f' % 2.958219e-06)
    H = depthtsrv.datavalue
    if depthtsrv.datavalue > 5.0:
        cfs = 0.003823*(depthtsrv.datavalue^6.007605)
    else:
        cfs = 2.958219e-06*(depthtsrv.datavalue^1.045713e+01)
    if i % 1000 == 0:
        print(cfs)
        # print(adjH)

    # dis = 0.001541*(adjH**b)
    #print('unadjusted ' + str(H))
    #print('adjusted ' + str(adjH))
    #print('discharge cfs ' + str(discharge))
    if cfs >0.0:
        tsrv = Timeseriesresultvalues(resultid=dischargeresult, datavalue=cfs, valuedatetime=depthtsrv.valuedatetime,
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