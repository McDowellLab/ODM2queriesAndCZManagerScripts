
import os
import csv
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "templatesAndSettings.settings.developmentNO")
application = get_wsgi_application()
from django.db.models import Q
import re
import math
from django.core.exceptions import ObjectDoesNotExist
import datetime
from odm2admin.models import *
import odm2admin.modelHelpers as modelHelpers
from django.db.models import Min, Max
import time as time
import xlrd
import decimal
from django.db.utils import IntegrityError
# http://odm2admin.cuahsi.org/LCZO/graphfa/samplingfeature%3D771/resultidu%3D18632/startdate%3D2018-04-25/enddate%3D2018-05-16/
# CDOM RI 15 min 18632
RICDOM = Timeseriesresults.objects.filter(resultid=18632).get()
tsrvs = Timeseriesresultvalues.objects.filter(resultid=18632).filter(valuedatetime__gte='2018-04-25').\
    filter(valuedatetime__lte='2018-05-15 12:16:00').filter(~Q(datavalue=decimal.Decimal('NaN')))
# tsrvs = Timeseriesresultvalues.objects.filter(resultid=18632).filter(valuedatetime__gte='2018-05-15').filter(valuedatetime__lte='2018-05-15 12:16:00')
print(RICDOM)
for tsrv in tsrvs:
    print(str(tsrv.valuedatetime) + ' ' + str(tsrv.datavalue))
    if not math.isnan(tsrv.datavalue):
        # print('here')
        tsrv.datavalue = decimal.Decimal('NaN')
        try:
            tsrv.save(force_update=True)
        except IntegrityError:
            tsrv.delete()