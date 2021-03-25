import argparse
import csv
import io
import itertools
import re
import time
import xlrd
#import utils

import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "templatesAndSettings.settings.developmentNO")
application = get_wsgi_application()
#from contextlib import closing
#import csv
#from cStringIO import StringIO

from django.db import connection

from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.core.management import settings
from django.core.mail import EmailMessage

from django.db import IntegrityError
from django.db import transaction
from django.db.models import Min, Max
from datetime import datetime

from odm2admin.models import CvCensorcode
from odm2admin.models import CvQualitycode
from odm2admin.models import Dataloggerfilecolumns
from odm2admin.models import Dataloggerfiles
from odm2admin.models import Extensionproperties
from odm2admin.models import Resultextensionpropertyvalues
from odm2admin.models import Timeseriesresults
from odm2admin.models import Timeseriesresultvalues
from odm2admin.models import Dataquality
from odm2admin.models import Results
from odm2admin.models import Resultsdataquality
from odm2admin.models import People
from odm2admin.models import CvDataqualitytype
from odm2admin.models import CvAnnotationtype
from odm2admin.models import Annotations
from odm2admin.models import Timeseriesresultvalueannotations
from odm2admin.models import ProcessDataloggerfile
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "templatesAndSettings.settings.developmentNO")

def getEndDate(results):
    #EndDateProperty = Extensionproperties.objects.get(propertyname__icontains="end date")
    #enddate = Resultextensionpropertyvalues.objects.filter(resultid=results.resultid).filter(
    #    propertyid=EndDateProperty).get()
    enddate = None
    try:
        enddate = Timeseriesresultvalues.objects.filter(resultid=results).annotate(
            Max('valuedatetime')). \
            order_by('-valuedatetime')[0].valuedatetime.strftime('%Y-%m-%d %H:%M:%S.%f')
    except IndexError:
        return None
    return enddate


def updateStartDateEndDate(results, startdate, enddate):
    StartDateProperty = Extensionproperties.objects.get(propertyname__icontains="start date")
    EndDateProperty = Extensionproperties.objects.get(propertyname__icontains="end date")
    # result = results#.objects.get(resultid=results.resultid.resultid)
    try:
        # raise CommandError(" start date "str(startdate)))
        #
        repvstart= Resultextensionpropertyvalues.objects.filter(resultid=results.resultid).filter(
            propertyid=StartDateProperty).get() #.update(propertyvalue=startdate)
        repvstart.propertyvalue=startdate
        repvstart.save()
        repvend = Resultextensionpropertyvalues.objects.filter(resultid=results.resultid).filter(
            propertyid=EndDateProperty).get() #.update(propertyvalue=enddate)
        repvend.propertyvalue = enddate
        repvend.save()

    except ObjectDoesNotExist:
        # raise CommandError("couldn't find extension property values " +str(repvstart) + "for " +
        # str(StartDateProperty + "for" + str(results))
        repvstart = Resultextensionpropertyvalues(resultid=results.resultid, propertyid=StartDateProperty,
                                                  propertyvalue=startdate)
        # print(repvstart.propertyvalue)
        repvstart.save()
        repvend = Resultextensionpropertyvalues(resultid=results.resultid, propertyid=EndDateProperty,
                                                propertyvalue=enddate)
        # print(repvend.propertyvalue)
        repvend.save()
        # return repvstart, repvend
# dashboardfaids = [1699, 1784,1782,1780,1701,1802,1704,1781,1707,1778,1779,1702,1703,3054,1784]
dashboardfaids = [3055]
resultids = [18699, 16552]
results = Results.objects.filter(resultid__in=resultids) # filter(resultid=18740) #
tsrs = Timeseriesresults.objects.filter(resultid__in=results)
for result in tsrs:
    enddate = getEndDate(result)
    # print(result)
    # print(result.resultid.resultid)
    # print(result.resultid.featureactionid.samplingfeatureid.samplingfeatureid)
    try:
        startdate = Timeseriesresultvalues.objects.filter(resultid=result).annotate(
            Min('valuedatetime')). \
            order_by('valuedatetime')[0].valuedatetime.strftime(
            '%Y-%m-%d %H:%M:%S.%f')

        updateStartDateEndDate(result,startdate,enddate)
        print(startdate)
        print(enddate)
        print(result)
    except IndexError as e:
        print("ERROR")
        print(result.resultid.resultid)
        print(result.resultid.featureactionid.samplingfeatureid.samplingfeatureid)