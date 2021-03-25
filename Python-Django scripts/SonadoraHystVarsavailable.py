
import os
import csv
import pandas as pd
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "templatesAndSettings.settings.developmentNO")
application = get_wsgi_application()
from django.db.models import Q
import re

from django.core.exceptions import ObjectDoesNotExist
import datetime
from odm2admin.models import *
import odm2admin.modelHelpers as modelHelpers
from django.db.models import Min, Max, Avg
import time as time
import xlrd
from datetime import datetime, timedelta
# sonadora




# find storms
tsrvs = Timeseriesresultvalues.objects.filter(resultid=17274).filter(datavalue__gte=90).order_by('valuedatetime')
samplingfeature = tsrvs.first().resultid.resultid.featureactionid.samplingfeatureid.samplingfeaturename
# Icacos
#tsrvs = Timeseriesresultvalues.objects.filter(resultid=18563).filter(datavalue__gte=250).order_by('valuedatetime')
dischargecount=tsrvs.count()
print('values greater then 90 cfs')
print(dischargecount)
lastdatetime = None
stormcount = 0
fields = ['Stream','start date','end date','discharge count','NO3 count','fDOM count',
          'Specific Conductance count','Turbidity count','pH count','DO count']

startdt = None
enddt = None
with open('Sonadora-storms.csv','w', newline='') as f:
    f.writelines('Sonadora \n')
    f.writelines('Cond URL, Turb URL, discharge URL,')
    header = True
    for tsrv in tsrvs:
        stormdict = {}
        print('here!!!')
        # print(str(tsrv.valuedatetime) + ',' + str(tsrv.datavalue))
        if lastdatetime:
            print('here!!!2')
            dtinterval = tsrv.valuedatetime - lastdatetime
            # print(dtinterval.seconds/60)
            mins = dtinterval.seconds / 60
            if mins > 60:
                stormcount +=1
                print('new storm starting on')
                startdt = tsrv.valuedatetime - timedelta(hours=24, minutes=0)
                print(startdt)
                # print(tsrv)
                enddt = tsrv.valuedatetime + timedelta(hours=24, minutes=0)
                #allDischarge = Timeseriesresultvalues.objects.filter(resultid=17274).filter(
                #    valuedatetime__gt=startdt).filter(
                #    valuedatetime__lt=enddt)

                stormdict['Stream'] = samplingfeature
                stormdict['start date'] = startdt
                stormdict['end date'] = enddt

                dischargetsrv = Timeseriesresultvalues.objects.filter(resultid=17274).filter(
                    valuedatetime__gt=startdt).filter(
                    valuedatetime__lt=enddt)
                dischargecount = dischargetsrv.count()
                print('discharge values')
                print(dischargecount)
                stormdict['discharge count'] = dischargecount

                # NO3 L1 17153
                # fDOM L1 17290
                # spcond L1 17288
                # turb L1 17291
                # pH L1 17299
                # DO L1 17214

                no3tsrv = Timeseriesresultvalues.objects.filter(resultid=17153).filter(
                    valuedatetime__gt=startdt).filter(
                    valuedatetime__lt=enddt)
                no3count = no3tsrv.count()
                print('no3 values')
                print(no3count)
                stormdict['NO3 count'] = no3count

                fDOMtsrv = Timeseriesresultvalues.objects.filter(resultid=17290).filter(
                    valuedatetime__gt=startdt).filter(
                    valuedatetime__lt=enddt)
                fDOMcount = fDOMtsrv.count()
                print('fDOM values')
                print(fDOMcount)
                stormdict['fDOM count'] = fDOMcount

                spcondtsrv = Timeseriesresultvalues.objects.filter(resultid=17288).filter(
                    valuedatetime__gt=startdt).filter(
                    valuedatetime__lt=enddt)
                spcondcount = spcondtsrv.count()
                print('Sp Cond values')
                print(spcondcount)
                stormdict['Specific Conductance count'] = spcondcount
                condid = 17288

                turbtsrv = Timeseriesresultvalues.objects.filter(resultid=17291).filter(
                    valuedatetime__gt=startdt).filter(
                    valuedatetime__lt=enddt)
                turbcount = turbtsrv.count()
                print('Turbidity values')
                print(turbcount)
                stormdict['Turbidity count'] = turbcount
                turbid = 17291

                pHtsrv = Timeseriesresultvalues.objects.filter(resultid=17299).filter(
                    valuedatetime__gt=startdt).filter(
                    valuedatetime__lt=enddt)
                pHcount = pHtsrv.count()
                print('pH values')
                print(pHcount)
                stormdict['pH count'] = pHcount

                DOtsrv = Timeseriesresultvalues.objects.filter(resultid=17214).filter(
                    valuedatetime__gt=startdt).filter(
                    valuedatetime__lt=enddt)
                DOcount = DOtsrv.count()
                print('DO values')
                print(DOcount)
                stormdict['DO count'] = DOcount


                if startdt:
                    startdtime = startdt.strftime('%Y-%m-%d %H:%M')
                    enddttime = enddt.strftime('%Y-%m-%d %H:%M')
                    startd = startdt.strftime('%Y-%m-%d')
                    endd = enddt.strftime('%Y-%m-%d')

                w = csv.DictWriter(f, fieldnames=fields)
                if header:
                    w.writeheader()
                header = False
                if startdt:
                    f.writelines('http://odm2admin.cuahsi.org/LCZO/graphfa/samplingfeature%3D3/resultidu=' + str(condid) + '/' +
                                 'startdate=' + str(startd) + '/enddate=' + str(endd) + ',' +
                                 'http://odm2admin.cuahsi.org/LCZO/graphfa/samplingfeature%3D3/resultidu=' + str(turbid) + '/' +
                                 'startdate=' + str(startd) + '/enddate=' + str(endd)
                                 + ',' +
                                 'http://odm2admin.cuahsi.org/LCZO/graphfa/samplingfeature%3D3/resultidu=17274/startdate=' + str(
                        startd) + '/' +
                                 'enddate=' + str(endd) + '/,')
                w.writerow(stormdict)
        lastdatetime = tsrv.valuedatetime
print('number of storms')
print(stormcount)