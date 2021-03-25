
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



with open('data2/hysteresis-analysis-Sonadora-interpall-withdates5-1-2019.csv','w', newline='') as f:
    f.writelines('Sonadora \n')
    f.writelines('Cond URL, Turb URL, discharge URL,')
    # f.writelines('valuedatetime,discharge CFS,dischargecount,17291-turb count,17293-turb count, 17295-spcond-count'+
    #             ',17216-spcond count,16156-cond-count,Cond URL, Turb URL, discharge URL\n')


    fields = ['Stream','start date','end date','Peak Q CFS', 'Peak Q l/s',
              'average discharge 1-6 hours pre-storm',
              'average discharge 1-12 hours pre-storm',
              'average discharge 1-24 hours pre-storm',
              'specific conductance count',
              'Mean HI specific conductance',
              'SD HI specific conductance',
              'Mean HI specific conductance with Interpolated values',
              'SD HI specific conductance with Interpolated values',
              'Peak specific conductance',
              'minimum specific conductance',
              'Hysteresis Index specific conductance',
              'Maximum width of specific conductance',
              'Interpolated Maximum width of specific conductance',
              'Direction of specific conductance loop',
              'Normalized slope of specific conductance',
              'HI values calculated for specific conductance',
              'HI values with interoplated for specific conductance',
              "HI values missing due to no raising limb measurement for specific conductance",
              "HI values missing due to no falling limb measurement for specific conductance",
              "HI values missing due to no raising and no falling limb measurement for specific conductance",
              'turbidity count',
              'Mean HI turbidity',
              'SD HI turbidity',
              'Mean HI turbidity with Interpolated values',
              'SD HI turbidity with Interpolated values',
              'Peak turbidity',
              'minimum turbidity',
              'Hysteresis Index turbidity',
              'Maximum width of turbidity',
              'Interpolated Maximum width of turbidity',
              'Direction of turbidity loop', 'Normalized slope of turbidity', 'HI values calculated for turbidity',
              'HI values with interoplated for turbidity',
              "HI values missing due to no raising limb measurement for turbidity",
              "HI values missing due to no falling limb measurement for turbidity",
              "HI values missing due to no raising and no falling limb measurement for turbidity",
              'pH count',
              'Mean HI pH',
              'SD HI pH',
              'Mean HI pH with Interpolated values',
              'SD HI pH with Interpolated values',
              'Peak pH',
              'minimum pH',
              'Hysteresis Index pH',
              'Maximum width of pH',
              'Interpolated Maximum width of pH',
              'Direction of pH loop',
              'Normalized slope of pH',
              'HI values calculated for pH',
              'HI values with interoplated for pH',
              "HI values missing due to no raising limb measurement for pH",
              "HI values missing due to no falling limb measurement for pH",
              "HI values missing due to no raising and no falling limb measurement for pH",
              'NO3 count',
              'Mean HI NO3',
              'SD HI NO3',
              'Mean HI NO3 with Interpolated values',
              'SD HI NO3 with Interpolated values',
              'Peak NO3',
              'minimum NO3',
              'Hysteresis Index NO3',
              'Maximum width of NO3',
              'Interpolated Maximum width of NO3',
              'Direction of NO3 loop',
              'Normalized slope of NO3',
              'HI values calculated for NO3',
              'HI values with interoplated for NO3',
              "HI values missing due to no raising limb measurement for NO3",
              "HI values missing due to no falling limb measurement for NO3",
              "HI values missing due to no raising and no falling limb measurement for NO3",
              'fDOM count',
              'Mean HI fDOM',
              'SD HI fDOM',
              'Mean HI fDOM with Interpolated values',
              'SD HI fDOM with Interpolated values',
              'Peak fDOM',
              'minimum fDOM',
              'Hysteresis Index fDOM',
              'Maximum width of fDOM',
              'Interpolated Maximum width of fDOM',
              'Direction of fDOM loop',
              'Normalized slope of fDOM',
              'HI values calculated for fDOM',
              'HI values with interoplated for fDOM',
              "HI values missing due to no raising limb measurement for fDOM",
              "HI values missing due to no falling limb measurement for fDOM",
              "HI values missing due to no raising and no falling limb measurement for fDOM",
              'DO count',
              'Mean HI DO',
              'SD HI DO',
              'Mean HI DO with Interpolated values',
              'SD HI DO with Interpolated values',
              'Peak DO',
              'minimum DO',
              'Hysteresis Index DO',
              'Maximum width of DO',
              'Interpolated Maximum width of DO',
              'Direction of DO loop',
              'Normalized slope of DO',
              'HI values calculated for DO',
              'HI values with interoplated for DO',
              "HI values missing due to no raising limb measurement for DO",
              "HI values missing due to no falling limb measurement for DO",
              "HI values missing due to no raising and no falling limb measurement for DO"]
    header = True
    startdate = []
    enddate = []
    with open('Sonadora-storms-AW.csv', 'r') as datesfile:
        csv_datesfile = csv.reader(datesfile, delimiter=',')
        for r in csv_datesfile:
            if not r[0] == 'Start_AW' and not r[0] =='':
                print(r[0])
                print(r[1])
                if not r[0] == 'NA':
                    dtstart = datetime.strptime(r[0], "%m/%d/%Y %H:%M")
                else:
                    dtstart = 'NA'
                if not r[1] == 'NA':
                    dtend = datetime.strptime(r[1], "%m/%d/%Y %H:%M")
                else:
                    dtend = 'NA'
                startdate.append(dtstart)
                enddate.append(dtend)
    print(len(startdate))
    print(len(enddate))
    

    for startd, endd in zip(startdate,enddate):
        stormdict = {}
        if not startd =='NA':
            startdt = startd.strftime("%Y-%m-%d %H:%M")
            enddt = endd.strftime("%Y-%m-%d %H:%M")
            # .aggregate(Avg('price'))
            startd = startd - timedelta(hours=0, minutes=1)
            endd = endd + timedelta(hours=0, minutes=1)
            allDischarge = Timeseriesresultvalues.objects.filter(resultid=17274).filter(valuedatetime__gte=startd).filter(valuedatetime__lte=endd).order_by('valuedatetime')
            samplingfeature = allDischarge.first().resultid.resultid.featureactionid.samplingfeatureid.samplingfeaturename
            stormdict['start date'] = startd
            stormdict['end date'] = endd
            print('start date: ' + str(startd))
            print('end date: ' + str(endd))


            startdt1to6 = startd - timedelta(hours=6, minutes=0)
            enddt1to6 = endd - timedelta(hours=1, minutes=0)
            dis1to6 = Timeseriesresultvalues.objects.filter(resultid=17274).filter(valuedatetime__gte=startdt1to6).filter(valuedatetime__lte=enddt1to6).order_by('valuedatetime')

            startdt6to12 = startd - timedelta(hours=12, minutes=0)
            enddt6to12 = endd - timedelta(hours=1, minutes=0)
            dis6to12 = Timeseriesresultvalues.objects.filter(resultid=17274).filter(valuedatetime__gte=startdt6to12).filter(valuedatetime__lte=enddt6to12).order_by('valuedatetime')

            startdt12to24 = startd - timedelta(hours=24, minutes=0)
            enddt12to24 = endd - timedelta(hours=1, minutes=0)
            dis12to24 = Timeseriesresultvalues.objects.filter(resultid=17274).filter(
                valuedatetime__gte=startdt12to24).filter(valuedatetime__lte=enddt12to24).order_by('valuedatetime')

            stormdict['average discharge 1-6 hours pre-storm'] = dis1to6.aggregate(Avg('datavalue'))['datavalue__avg']
            stormdict['average discharge 1-12 hours pre-storm'] = dis6to12.aggregate(Avg('datavalue'))['datavalue__avg']
            stormdict['average discharge 1-24 hours pre-storm'] = dis12to24.aggregate(Avg('datavalue'))['datavalue__avg']

            spcondtsrv = Timeseriesresultvalues.objects.filter(resultid=17288).filter(
                valuedatetime__gt=startdt).filter(
                valuedatetime__lt=enddt)
            cond17288count = spcondtsrv.count()
            print('Sp Cond 17288 values')
            print(cond17288count)
            stormdict['specific conductance count'] = cond17288count
            condid = 17288

            condtsrv = Timeseriesresultvalues.objects.filter(resultid=17295).filter(
                valuedatetime__gt=startd).filter(
                valuedatetime__lt=endd)
            cond17295count = condtsrv.count()
            # print('conductivity count: ' + str(cond17295count) + 'resultid=17295')

            cond2tsrv = Timeseriesresultvalues.objects.filter(resultid=17385).filter(
                valuedatetime__gt=startd).filter(
                valuedatetime__lt=endd)
            cond17385count = cond2tsrv.count()

            # print('conductivity count: ' + str(cond17216count) + 'resultid=17216')

            # 17223
            cond3tsrv = Timeseriesresultvalues.objects.filter(resultid=16156).filter(
                valuedatetime__gt=startd).filter(
                valuedatetime__lt=endd)
            cond16156count = cond3tsrv.count()
            # print('conductivity count: ' + str(cond16156count) + 'resultid=16156')
            condcount = 0
            condHystDict = {}
            condid = 0
            # cond17288count
            if cond17385count >= cond17295count and cond17385count >= cond16156count and cond17385count >= cond17288count and cond17385count > 0:
                condtsrv = cond2tsrv
                condid = 17385
                condcount = cond17385count
            elif cond17295count > cond17385count and cond17295count > cond16156count and cond17295count>= cond17288count:
                condtsrv = condtsrv
                condid = 17295
                condcount = cond17295count
            elif cond16156count > cond17295count and cond16156count > cond17385count and cond16156count>= cond17288count:
                condtsrv = cond3tsrv
                condid = 16156
                condcount = cond16156count
            elif cond17288count > cond16156count and cond17288count > cond17385count and cond17288count > cond17295count:
                condtsrv = spcondtsrv
                condid = 16156
                condcount = cond16156count
            # condHystDict = modelHelpers.hysteresisMetrics(allDischarge, spcondtsrv)

            print('cond count! :' + str(condcount))
            print('condid ' + str(condid))
            name = 'specific conductance'
            stormdict = modelHelpers.runHysteresis(stormdict, condcount, name, startd, endd, condtsrv, allDischarge, samplingfeature)

            turbtsrv = Timeseriesresultvalues.objects.filter(resultid=17291).filter(
                valuedatetime__gt=startdt).filter(
                valuedatetime__lt=enddt)
            turbcount = turbtsrv.count()
            print('Turbidity values')
            print(turbcount)
            stormdict['turbidity count'] = turbcount
            turbid = 17291

            name = 'turbidity'
            stormdict = modelHelpers.runHysteresis(stormdict, turbcount, name, startd, endd, turbtsrv, allDischarge, samplingfeature)


            pHtsrv = Timeseriesresultvalues.objects.filter(resultid=17299).filter(
                valuedatetime__gt=startdt).filter(
                valuedatetime__lt=enddt)
            pHcount = pHtsrv.count()
            print('pH values')
            print(pHcount)
            stormdict['pH count'] = pHcount

            name = 'pH'
            stormdict = modelHelpers.runHysteresis(stormdict, pHcount, name, startd, endd, pHtsrv, allDischarge, samplingfeature)


            DOtsrv = Timeseriesresultvalues.objects.filter(resultid=17214).filter(
                valuedatetime__gt=startdt).filter(
                valuedatetime__lt=enddt)
            DOcount = DOtsrv.count()
            print('DO values')
            print(DOcount)
            stormdict['DO count'] = DOcount

            name = 'DO'
            stormdict = modelHelpers.runHysteresis(stormdict, DOcount, name, startd, endd, DOtsrv, allDischarge, samplingfeature)


            no3tsrv = Timeseriesresultvalues.objects.filter(resultid=17153).filter(
                valuedatetime__gt=startdt).filter(
                valuedatetime__lt=enddt)
            no3count = no3tsrv.count()
            print('no3 values')
            print(no3count)
            stormdict['NO3 count'] = no3count

            name = 'NO3'
            stormdict = modelHelpers.runHysteresis(stormdict, no3count, name, startd, endd, no3tsrv, allDischarge, samplingfeature)


            fDOMtsrv = Timeseriesresultvalues.objects.filter(resultid=17290).filter(
                valuedatetime__gt=startdt).filter(
                valuedatetime__lt=enddt)
            fDOMcount = fDOMtsrv.count()
            print('fDOM values')
            print(fDOMcount)
            stormdict['fDOM count'] = fDOMcount

            name = 'fDOM'
            stormdict = modelHelpers.runHysteresis(stormdict, fDOMcount, name, startd, endd, fDOMtsrv, allDischarge, samplingfeature)

            startdtime = startdt# .strftime('%Y-%m-%d %H:%M')
            enddttime = enddt# .strftime('%Y-%m-%d %H:%M')
            startday = startd.strftime("%Y-%m-%d")
            endday = endd.strftime("%Y-%m-%d")

            w = csv.DictWriter(f, fieldnames=fields)
            if header:
                w.writeheader()
            f.writelines('http://odm2admin.cuahsi.org/LCZO/graphfa/samplingfeature%3D3/resultidu=' + str(condid) + '/' +
                         'dischargeresult=17274/startdate=' + str(startdtime) + '/enddate=' + str(
                enddttime) + '/popup=hyst/,' +
                         'http://odm2admin.cuahsi.org/LCZO/graphfa/samplingfeature%3D3/resultidu=' + str(turbid) + '/' +
                         'dischargeresult=17274/startdate=' + str(startdtime) + '/enddate=' + str(enddttime)
                         + '/popup=hyst/,' +
                         'http://odm2admin.cuahsi.org/LCZO/graphfa/samplingfeature%3D3/resultidu=17274/startdate=' + str(
                startday) + '/' +
                         'enddate=' + str(endday) + '/,')
            w.writerow(stormdict)
            header = False
