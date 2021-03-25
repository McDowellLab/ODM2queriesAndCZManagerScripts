
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
import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy.optimize import curve_fit
import pickle

def func_powerlaw(x, m, c, c0):
    return c0 + x**m * c

# 17278
# start date = "2018-03-26 16:46:09.000000"
# end date = "2019-09-03 12:46:36.000000"
with open('./data3/cs451depth.pickle', 'rb') as pickle_file:
    cs451depth = pickle.load(pickle_file)
with open('./data3/manualdepth.pickle', 'rb') as pickle_file2:
    manual_depth = pickle.load(pickle_file2)
# cs451depth = Timeseriesresultvalues.objects.filter(resultid=17278)
# manual_depth = Timeseriesresultvalues.objects.filter(resultid=17275).filter(valuedatetime__gte="2018-03-26 16:46:09.000000")
# with open('./data3/cs451depth.pickle', 'wb') as pickle_file:
#     pickle.dump(cs451depth, pickle_file)
# with open('./data3/manualdepth.pickle', 'wb') as pickle_file2:
#     pickle.dump(manual_depth, pickle_file2)

cs451depth = cs451depth.order_by('valuedatetime')
manual_depth = manual_depth.order_by('valuedatetime')
cs451depthpdf = pd.DataFrame(list(cs451depth.values()))
manual_depthpdf = pd.DataFrame(list(manual_depth.values()))

with open('./data3/cs451depthdf.pickle', 'wb') as pickle_file:
    pickle.dump(cs451depthpdf, pickle_file)
with open('./data3/manualdepthdf.pickle', 'wb') as pickle_file2:
    pickle.dump(manual_depthpdf, pickle_file2)
i=0
for val in cs451depth:
    i+=1
    print(val)
    if i >15:
        break
i=0
for val in manual_depth:
    i+=1
    print(val)
    if i >15:
        break

idx = np.searchsorted(cs451depthpdf['valuedatetime'], manual_depthpdf['valuedatetime']) - 1
mask = idx >= 0
print(idx)
dfdtsorted = pd.DataFrame({"cs451depthpdf":cs451depthpdf[idx][mask], "manual_depthpdf":manual_depthpdf[mask]})
print(dfdtsorted.head())

i = 0
matchedautodepths = []
for csd in cs451depth:
    for id in idx:
        if i == id:
            matchedautodepths.append(csd)
    i+=1

print(matchedautodepths)