
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

tsrs = Timeseriesresults.objects.all()

for tsr in tsrs:
    numvals = Timeseriesresultvalues.objects.filter(resultid=tsr).count()
    result = Results.objects.filter(resultid=tsr.resultid.resultid)
    if result.count() == 0:
        print('no result related to this time series result?')
        print(tsr)
        print(numvals)
    if numvals == 0:
        print('delete me')
        print(tsr)

        print(result)
