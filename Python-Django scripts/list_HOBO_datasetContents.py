
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

datasetresults = [3,23,24]
dsr = Datasetsresults.objects.filter(datasetid__in=datasetresults)
rs = Results.objects.filter(resultid__in=dsr.values("resultid"))
sfs = []
for r in rs:
    # print(r)
    # print(r.featureactionid)
    featureaction = Featureactions.objects.get(featureactionid=r.featureactionid.featureactionid)
    sf = Samplingfeatures.objects.get(samplingfeatureid=featureaction.samplingfeatureid.samplingfeatureid)
    if sf not in sfs:
        sfs.append(sf)

for sf in sfs:
    print(sf.samplingfeaturename)