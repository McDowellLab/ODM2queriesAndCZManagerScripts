
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

def roundTime(dt=None, roundTo=60):
   """Round a datetime object to any time lapse in seconds
   dt : datetime.datetime object, default now.
   roundTo : Closest number of seconds to round to, default 1 minute.
   Author: Thierry Husson 2012 - Use it as you want but don't blame me.
   """
   if dt == None : dt = datetime.datetime.now()
   seconds = (dt.replace(tzinfo=None) - dt.min).seconds
   rounding = (seconds+roundTo/2) // roundTo * roundTo
   return dt + timedelta(0,rounding-seconds,-dt.microsecond)

with open('hysteresis-analysis-Sonadora-interpall-withdates4.csv','w', newline='') as f:
    f.writelines('Sonadora \n')
    f.writelines('Cond URL, Turb URL, discharge URL,')
    # f.writelines('valuedatetime,discharge CFS,dischargecount,17291-turb count,17293-turb count, 17295-spcond-count'+
    #             ',17216-spcond count,16156-cond-count,Cond URL, Turb URL, discharge URL\n')


    fields = ['Stream','start date','end date','Peak Q CFS', 'Peak Q l/s',
              'average discharge 1-6 hours pre-storm',
              'average discharge 1-12 hours pre-storm',
              'average discharge 1-24 hours pre-storm',
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
              "HI values missing due to no raising limb measurement for SC",
              "HI values missing due to no falling limb measurement for SC",
              "HI values missing due to no raising and no falling limb measurement for SC",
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
              "HI values missing due to no raising and no falling limb measurement for turbidity"]
    header = True
    startdate = []
    enddate = []
    with open('hysteresis-analysis-Sonadora-dates.csv', 'r') as datesfile:
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
            samplingfeature = allDischarge.first().resultid.resultid.featureactionid.samplingfeatureid.samplingfeaturename
            # Icacos
            # tsrvs = Timeseriesresultvalues.objects.filter(resultid=18563).filter(datavalue__gte=250).order_by('valuedatetime')
            dischargecount = allDischarge.count()
            lastdatetime = None
            samplingfeature = allDischarge.first().resultid.resultid.featureactionid.samplingfeatureid.samplingfeaturename
            stormdict['Stream'] = samplingfeature
            stormdict['start date'] = startd
            stormdict['end date'] = endd
            print('start date: ' + str(startd))
            print('end date: ' + str(endd))
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
            if str(startd) == '2017-06-19 15:44:00':
                print('HERE HERE HERE!!!!!!!')
                print(cond17385count)
                print(cond2tsrv.query)
                print(cond17295count)
                print(cond16156count)
            if cond17385count >= cond17295count and cond17385count >= cond16156count and cond17385count > 0:
                condHystDict = modelHelpers.hysteresisMetrics(allDischarge, cond2tsrv)
                condtsrv = cond2tsrv
                condid = 17385
                condcount = cond17385count
            elif cond17295count > cond17385count and cond17295count > cond16156count:
                condHystDict = modelHelpers.hysteresisMetrics(allDischarge, condtsrv)
                condid = 17295
                condcount = cond17295count
            elif cond16156count > cond17295count and cond16156count > cond17385count:
                condHystDict = modelHelpers.hysteresisMetrics(allDischarge, cond3tsrv)
                condtsrv = cond3tsrv
                condid = 16156
                condcount = cond16156count
            print('cond count! :' + str(condcount))
            print('condid' + str(condid))
            stormdict['Mean HI specific conductance'] = None
            stormdict['SD HI specific conductance'] = None
            stormdict['Mean HI specific conductance with Interpolated values'] = None
            stormdict['SD HI specific conductance with Interpolated values'] = None
            stormdict['Peak specific conductance'] = None
            stormdict['minimum specific conductance'] = None
            stormdict['Hysteresis Index specific conductance'] = None
            stormdict['Maximum width of specific conductance'] = None
            stormdict['Interpolated Maximum width of specific conductance'] = None
            stormdict['Direction of specific conductance loop'] = None
            stormdict['Normalized slope of specific conductance'] = None
            stormdict['HI values calculated for specific conductance'] = 0
            stormdict['HI values with interoplated for specific conductance'] = 0
            stormdict["HI values missing due to no raising limb measurement for SC"] = 0
            stormdict["HI values missing due to no falling limb measurement for SC"] = 0
            stormdict["HI values missing due to no raising and no falling limb measurement for SC"] = 0

            if condcount > 0:
                #conductivityfiles
                nfields = ['Stream', 'datetime', 'discharge', 'conductivity']
                ndict = {}
                nHeader = True
                startday = startd.strftime("%Y-%m-%d")
                endday = endd.strftime("%Y-%m-%d")
                nfields = ['Stream', 'datetime', 'Specific conductance mS/cm', 'Discharge CFS', 'Specific conductance normalized',
                           'Discharge normalized']
                with open('data/conductivityfiles/Sonadora-specific conductance-and-discharge' + startday + '.csv', 'w', newline='') as condfile:
                    w2 = csv.DictWriter(condfile, fieldnames=nfields)
                    w2.writeheader()
                    for dis in allDischarge:
                        for cond in condtsrv:
                            maxcond =float(condHystDict['Max response'])
                            mincond = float(condHystDict['Min response'])
                            maxdis = float(condHystDict['Peak Q'])
                            mindis = float(condHystDict['Min Q'])
                            if dis.valuedatetime == cond.valuedatetime:
                                ndict = {}
                                ndict['Stream'] = samplingfeature
                                ndict['datetime'] = dis.valuedatetime
                                ndict['Discharge CFS'] = dis.datavalue
                                ndict['Specific conductance mS/cm'] = cond.datavalue
                                ndict['Discharge normalized'] = (dis.datavalue - mindis) / (maxdis - mindis)
                                ndict['Specific conductance normalized'] = (cond.datavalue - mincond) / (maxcond - mincond)
                                w2.writerow(ndict)
                if condHystDict['discharge_units'] == 'cfs':
                    stormdict['Peak Q CFS'] = condHystDict['Peak Q']
                    stormdict['Peak Q l/s'] = condHystDict['Peak Q'] * 28.316846592
                stormdict['Mean HI specific conductance'] = condHystDict["HI_mean"]
                stormdict['SD HI specific conductance'] = condHystDict['HI_standard_deviation']
                stormdict['Mean HI specific conductance with Interpolated values'] = condHystDict["HI_mean_with_Interp"]
                stormdict['SD HI specific conductance with Interpolated values'] = condHystDict[
                    'HI_standard_deviation_with_Interp']
                HIlist = condHystDict['Hysteresis_Index']
                stormdict['Hysteresis Index specific conductance'] = condHystDict['Hysteresis_Index']
                stormdict['Peak specific conductance'] = condHystDict['Max response']
                stormdict['minimum specific conductance'] = condHystDict['Min response']
                stormdict['Maximum width of specific conductance'] = condHystDict[
                    'Max width of response']  # hystdict['Max width of response'] = maxWidth
                stormdict['Interpolated Maximum width of specific conductance'] = condHystDict[
                    'interpolated Max width of response']
                # clock wise = + HI
                # counter clock wise = -HI
                HIvalsdict = condHystDict['Hysteresis_Index']
                stormdict['Direction of specific conductance loop'] = ''
                stormdict['Normalized slope of specific conductance'] = condHystDict['Normalized slope of response']
                stormdict['HI values calculated for specific conductance'] = condHystDict["HI_count"]
                stormdict['HI values with interoplated for specific conductance'] = condHystDict[
                    "HI_count_and_interp"]
                stormdict["HI values missing due to no raising limb measurement for SC"] = condHystDict[
                    "HI values missing due to no raising limb measurement"]  # countMissingRaising
                stormdict["HI values missing due to no falling limb measurement for SC"] = condHystDict[
                    "HI values missing due to no falling limb measurement"]  # countMissingFalling
                stormdict["HI values missing due to no raising and no falling limb measurement for SC"] = condHystDict[
                    "HI values missing due to no raising and no falling limb measurement"]  # countMissingBoth
                lastHI = None
                # print(HIvalsdict)
                nfields = ['Stream', 'start date', 'end date', 'Cond HI']
                ndict = {}
                nHeader = True

                with open('data/hystfiles/hysteresis-analysis-Sonadora-Specific conductance-' + startday + '.csv', 'w', newline='') as nfile:
                    nfile.writelines('Sonadora \n')
                    w2 = csv.DictWriter(nfile, fieldnames=nfields)
                    for HI, HIval in HIvalsdict.items():
                        ndict = {}
                        ndict['Stream'] = samplingfeature
                        ndict['start date'] = startd
                        ndict['end date'] = endd
                        ndict['Cond HI'] = HIval
                        if nHeader:
                            w2.writeheader()
                        #print('ndict!!!')
                        #print(ndict)
                        w2.writerow(ndict)
                        nHeader = False
                    for HI, HIval in HIvalsdict.items():
                        # HIval = next(iter(HI))
                        # print(HIval)
                        if lastHI:
                            if HIval < 0 and lastHI < 0:
                                if not stormdict['Direction of specific conductance loop']:
                                    stormdict['Direction of specific conductance loop'] = 'counter clock wise | '
                            elif HIval < 0 and lastHI > 0:
                                stormdict['Direction of specific conductance loop'] += 'counter clock wise | '
                            elif HIval > 0 and lastHI > 0:
                                if not stormdict['Direction of specific conductance loop']:
                                    stormdict['Direction of specific conductance loop'] = 'clock wise | '
                            elif HIval > 0 and lastHI < 0:
                                stormdict['Direction of specific conductance loop'] += 'clock wise | '

                        lastHI = HIval

            turbtsrv = Timeseriesresultvalues.objects.filter(resultid=17291).filter(
                valuedatetime__gt=startd).filter(
                valuedatetime__lt=endd)
            turbcount = turbtsrv.count()
            turb2tsrv = Timeseriesresultvalues.objects.filter(resultid=17293).filter(valuedatetime__gt=startd).filter(
                valuedatetime__lt=endd)
            turb2count = turb2tsrv.count()
            print('turbidity 17293 count: ' + str(turb2count))
            turb3tsrv = Timeseriesresultvalues.objects.filter(resultid=17173).filter(valuedatetime__gt=startd).filter(
                valuedatetime__lt=endd)
            turb3count = turb2tsrv.count()
            if turbcount >= turb2count and turbcount >= turb3count:
                turbid = 17291
            elif turb2count > turbcount and turb2count > turb3count:
                turbtsrv = turb2tsrv
                turbcount = turb2count
                turbid = 17293
            elif turb3count > turbcount and turb3count > turb2count:
                turbtsrv = turb3tsrv
                turbcount = turb3count
                turbid = 17173

            stormdict['Mean HI turbidity'] = None
            stormdict['SD HI turbidity'] = None
            stormdict['Mean HI turbidity with Interpolated values'] = None
            stormdict['SD HI turbidity with Interpolated values'] = None
            stormdict['Peak turbidity'] = None #
            stormdict['minimum turbidity'] = None
            stormdict['Maximum width of turbidity'] = None
            stormdict['Interpolated Maximum width of turbidity'] = None
            stormdict['Direction of turbidity loop'] = None
            stormdict['Normalized slope of turbidity'] = None
            stormdict['Hysteresis Index turbidity'] = None
            stormdict['turbidity count'] = 0
            stormdict['HI values calculated for turbidity'] = 0
            stormdict['HI values with interoplated for turbidity'] = 0
            stormdict["HI values missing due to no raising limb measurement for turbidity"] = 0
            stormdict["HI values missing due to no falling limb measurement for turbidity"] = 0
            stormdict["HI values missing due to no raising and no falling limb measurement for turbidity"] = 0

            if turbcount > 0:
                ndict = {}
                nHeader = True
                startday = startd.strftime("%Y-%m-%d")
                endday = endd.strftime("%Y-%m-%d")
                turbHystDict = modelHelpers.hysteresisMetrics(allDischarge, turbtsrv, True)

                nfields = ['Stream', 'datetime', 'turbidity FNU', 'discharge CFS', 'turbidity normalized',
                           'discharge normalized']
                with open('data/tubidityfiles/Sonadora-turbidity-and-discharge' + startday + '.csv', 'w', newline='') as turbfile:
                    turbfile.writelines('Sonadora \n')
                    w2 = csv.DictWriter(turbfile, fieldnames=nfields)
                    w2.writeheader()
                    maxturb = float(turbHystDict['Max response'])
                    minturb = float(turbHystDict['Min response'])
                    maxdis = float(turbHystDict['Peak Q'])
                    mindis = float(turbHystDict['Min Q'])
                    for dis in allDischarge:
                        for turb in turbtsrv:
                            dtimeagg = turb.resultid.intendedtimespacing
                            dtimeaggunit = turb.resultid.intendedtimespacingunitsid.unitsname
                            dtturb = turb.valuedatetime
                            if 'minute' in dtimeaggunit or 'Minutes' in dtimeaggunit:
                                dtturb = roundTime(dtturb,900)
                                print('time minute')
                            elif 'hour' in dtimeaggunit:
                                dtturb = roundTime(dtturb, 3600)
                                print('time hour')

                            dtimeagg = dis.resultid.intendedtimespacing
                            dtimeaggunit = dis.resultid.intendedtimespacingunitsid.unitsname
                            dtdis = dis.valuedatetime
                            if 'minute' in dtimeaggunit or 'Minutes' in dtimeaggunit:
                                dtdis =  roundTime(dtdis,900)
                            elif 'hour' in dtimeaggunit:
                                dtimeagg = dtimeagg * 60
                                dtdis = roundTime(dtdis, 3600)
                            if dtturb == dtdis:
                                ndict = {}
                                ndict['Stream'] = samplingfeature
                                ndict['datetime'] = dtdis
                                ndict['discharge CFS'] = dis.datavalue
                                ndict['discharge normalized'] = (dis.datavalue - mindis) / (maxdis - mindis)
                                ndict['turbidity FNU'] = turb.datavalue
                                # ndict['discharge normalized'] = (dis.datavalue - mindis) / (maxdis - mindis)
                                ndict['turbidity normalized'] = (turb.datavalue - minturb) / (maxturb - minturb)
                                w2.writerow(ndict)


                print('turb count: ' + str(turbcount))
                print('turbid: ' + str(turbid))
                print(turbHystDict)
                stormdict['turbidity count'] = turbcount
                # if turbHystDict['discharge_units'] == 'cfs':
                #     stormdict['Peak Q l/s'] = turbHystDict['Peak Q'] * 28.316846592
                stormdict['Mean HI turbidity'] = turbHystDict["HI_mean"]
                stormdict['SD HI turbidity'] = turbHystDict['HI_standard_deviation']
                stormdict['Mean HI turbidity with Interpolated values'] = turbHystDict["HI_mean_with_Interp"]
                stormdict['SD HI turbidity with Interpolated values'] = turbHystDict['HI_standard_deviation_with_Interp']
                # HIlist = turbHystDict['Hysteresis_Index']
                stormdict['Peak turbidity'] = turbHystDict['Max response']
                stormdict['minimum turbidity'] = turbHystDict['Min response']
                stormdict['Maximum width of turbidity'] = turbHystDict[
                    'Max width of response']  # hystdict['Max width of response'] = maxWidth
                stormdict['Interpolated Maximum width of turbidity'] = turbHystDict['interpolated Max width of response']
                # clock wise = + HI
                # counter clock wise = -HI
                HIvalsdict = turbHystDict['Hysteresis_Index']
                stormdict['Hysteresis Index turbidity'] = turbHystDict['Hysteresis_Index']
                stormdict['Direction of turbidity loop'] = ''
                stormdict['Normalized slope of turbidity'] = turbHystDict['Normalized slope of response']
                stormdict['HI values calculated for turbidity'] = turbHystDict["HI_count"]
                stormdict['HI values with interoplated for turbidity'] = turbHystDict["HI_count_and_interp"]
                stormdict["HI values missing due to no raising limb measurement for turbidity"] = turbHystDict[
                    "HI values missing due to no raising limb measurement"]  # countMissingRaising
                stormdict["HI values missing due to no falling limb measurement for turbidity"] = turbHystDict[
                    "HI values missing due to no falling limb measurement"]  # countMissingFalling
                stormdict["HI values missing due to no raising and no falling limb measurement for turbidity"] = \
                    turbHystDict[
                        "HI values missing due to no raising and no falling limb measurement"]  # countMissingBoth

                lastHI = None
                print(HIvalsdict)
                nfields = ['Stream', 'start date', 'end date', 'Turb HI']
                ndict = {}
                nHeader = True
                with open('data/hystfiles/hysteresis-analysis-Sonadora-Turbidity-' + startday + '.csv', 'w', newline='') as nfile2:
                    nfile2.writelines('Icacos \n')
                    w3 = csv.DictWriter(nfile2, fieldnames=nfields)
                    for HI, HIval in HIvalsdict.items():
                        ndict = {}
                        ndict['Stream'] = samplingfeature
                        ndict['start date'] = startd
                        ndict['end date'] = endd
                        ndict['Turb HI'] = HIval
                        if nHeader:
                            w3.writeheader()
                        w3.writerow(ndict)
                        nHeader = False
                    for HI, HIval in HIvalsdict.items():
                        # HIval = next(iter(HI))
                        print(HIval)
                        if lastHI:
                            if HIval < 0 and lastHI < 0:
                                if not stormdict['Direction of turbidity loop']:
                                    stormdict['Direction of turbidity loop'] = 'counter clock wise | '
                            elif HIval < 0 and lastHI > 0:
                                stormdict['Direction of turbidity loop'] += 'counter clock wise | '
                            elif HIval > 0 and lastHI > 0:
                                if not stormdict['Direction of turbidity loop']:
                                    stormdict['Direction of turbidity loop'] = 'clock wise | '
                            elif HIval > 0 and lastHI < 0:
                                stormdict['Direction of turbidity loop'] += 'clock wise | '

                        lastHI = HIval

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

            # f.writelines(str(tsrv.valuedatetime) + ',' + str(tsrv.datavalue) + ',' + str(dischargecount) + ','+
            #               str(turbcount) +  ',' + str(turb2count) +  ',' +str(cond17163count) + ',' + str(cond18559count) +
            #         ',' + str(spcond17223count) +
            #         ',http://odm2admin.cuahsi.org/LCZO/graphfa/samplingfeature%3D3/resultidu=17216/'+
            #         'dischargeresult=17274/startdate='+str(startdtime)+ '/enddate='+ str(enddttime) + '/popup=hyst/,' +
            #              ',http://odm2admin.cuahsi.org/LCZO/graphfa/samplingfeature%3D3/resultidu=17291/' +
            #              'dischargeresult=17274/startdate=' + str(startdtime) + '/enddate=' + str(enddttime)
            #              + '/popup=hyst/,' +
            # 'http://dm2admin.cuahsi.org/LCZO/graphfa/samplingfeature%3D3/resultidu=17274/startdate='+str(startd)+ '/' +
            #              'enddate='+ str(endd) + '/\n')
