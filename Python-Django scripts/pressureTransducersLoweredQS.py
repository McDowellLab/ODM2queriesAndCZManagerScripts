
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

depth = Timeseriesresults.objects.filter(resultid=18699).get()
# depth_adjusted = Timeseriesresults.objects.filter(resultid=18699).get() #17276
# dischargeresult = Timeseriesresults.objects.filter(resultid=17274).get()#17274
depthtsrvs = Timeseriesresultvalues.objects.filter(resultid=depth).\
    filter(valuedatetime__gt='2020-05-26 09:45').filter(valuedatetime__lt='2020-12-08 01:02')\
    .order_by('-valuedatetime')

for tsrv in depthtsrvs:
    tsrv.datavalue = tsrv.datavalue - 0.76
    tsrv.save()

# depthHOBO = Timeseriesresults.objects.filter(resultid=17273).get()

# depthHOBOtsrvs = Timeseriesresultvalues.objects.filter(resultid=depthHOBO).\
#     filter(valuedatetime__gt='2020-05-26 09:45').order_by('-valuedatetime')
