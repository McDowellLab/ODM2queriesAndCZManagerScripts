
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

methods = Methods.objects.filter(methodcode__icontains='hobo')
resultset = []
for method in methods:

    if not 'calibration' in str(method) and not 'retrieval' in str(method):
        # print(str(method.methodid) + ' ' + str(method))
    # print('here')
        actions = Actions.objects.filter(method_id=method.methodid)
        featureactions = Featureactions.objects.filter(action_id__in=actions)
        for featureaction in featureactions:
            # print('here2')
            # print(str(featureaction.featureactionid) + ' ' + str(featureaction))
            if "deployment" in str(featureaction) or 'Observation' in str(featureaction):
                # print(featureaction)
                results = Results.objects.filter(featureactionid=featureaction)
                for result in results:
                    resultset.append(result.resultid)
print(len(resultset))
print(resultset)
results = Results.objects.filter(resultid__in=resultset)
dataset = Datasets.objects.filter(datasetid=3).get()
for result in results:
    dsr = Datasetsresults(datasetid=dataset,resultid=result)
    dsr.save()
    print(dsr)