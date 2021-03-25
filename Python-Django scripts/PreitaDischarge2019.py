import os
import csv
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "templatesAndSettings.settings.developmentNO")
application = get_wsgi_application()
from django.db.models import Q
import re
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime as dt
from datetime import timedelta
from odm2admin.models import *
from django.db.models import Min, Max

## STAGE COMES FROM ALONSO RAMIREZ
stageheightr = Results.objects.filter(resultid=18560).get()
stageheighttsr = Timeseriesresults.objects.filter(resultid=18560).get()
## STAGE COMES FROM ALONSO RAMIREZ
stagetsrvs = Timeseriesresultvalues.objects.filter(resultid=18560).filter(valuedatetime__gt='2019-11-15 10:45')
dischargetsr = Timeseriesresults.objects.get(resultid=18657)


for stagetsrv in stagetsrvs:
    if stagetsrv.datavalue > 0:
        cfs = 0.0005*((stagetsrv.datavalue+0.31)**8.8846) *35.314666212661
        newdischarge = Timeseriesresultvalues(resultid=dischargetsr, datavalue=cfs,valuedatetime=stagetsrv.valuedatetime,
                                       valuedatetimeutcoffset=stagetsrv.valuedatetimeutcoffset,censorcodecv=stagetsrv.censorcodecv,
                                       qualitycodecv=stagetsrv.qualitycodecv,timeaggregationinterval=stagetsrv.timeaggregationinterval,
                                       timeaggregationintervalunitsid=stagetsrv.timeaggregationintervalunitsid)
        newdischarge.save()