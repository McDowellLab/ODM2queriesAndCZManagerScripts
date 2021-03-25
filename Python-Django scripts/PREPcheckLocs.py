import sys
import os
import csv
import pandas as pd
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "templatesAndSettings.settings.developmentPREP")
# os.environ.setdefault("GDAL_DATA", 'C:/OSGeo4W64/share/gdal')
os.environ['GDAL_DATA'] = 'C:/OSGeo4W64/share/gdal'
# C:\Program Files\PostgreSQL\12\gdal-data
application = get_wsgi_application()
import datetime
from odm2admin.models import *

import osgeo.osr as osr
from osgeo import ogr
from django.core.exceptions import ObjectDoesNotExist
# GDAL_DATA = 'C:/OSGeo4W/share/gdal' #
sfs = Samplingfeatures.objects.all()
print(os.environ['GDAL_DATA'])
drv = ogr.GetDriverByName('ESRI Shapefile')
print(drv)
ds_in = drv.Open("C:/Users/12672/OneDrive - University of New Hampshire/MachineLearningGroup/EPSCOR_GIS/EPSCoR_wsheds6/EPSCoR_watersheds6.shp")
lyr_in = ds_in.GetLayer(0)
idx_reg = lyr_in.GetLayerDefn().GetFieldIndex("Site_Key")
geo_ref = lyr_in.GetSpatialRef()
point_ref= osr.SpatialReference()
point_ref.ImportFromEPSG(4326)
ctran= osr.CoordinateTransformation(point_ref,geo_ref)

def check(lon, lat):
    #Transform incoming longitude/latitude to the shapefile's projection
    # print(lon)
    # print(lat)
    [lon,lat,z]=ctran.TransformPoint(float(lon),float(lat),float(0))

    #Create a point
    pt = ogr.Geometry(ogr.wkbPoint)
    pt.SetPoint_2D(0, lon, lat)

    #Set up a spatial filter such that the only features we see when we
    #loop through "lyr_in" are those which overlap the point defined above
    lyr_in.SetSpatialFilter(pt)

    #Loop through the overlapped features and display the field of interest
    overlap = []
    for feat_in in lyr_in:
        overlap.append(feat_in.GetFieldAsString(idx_reg))
    return overlap


with open('./PREP/EMDsitesinws.csv', "w",newline='')  as outfile:
    sitewriter = csv.writer(outfile)
    header = ['sf','sfid','ws', 'lat', 'lon']
    sitewriter.writerow(header)

    for sf in sfs:
        try:
            site = Sites.objects.get(samplingfeatureid=sf)
        except ObjectDoesNotExist:
            print('no site')
            print(sf.samplingfeaturecode)
            print(sf.samplingfeatureid)
            continue
        overlap = check( site.longitude, site.latitude)
        if len(overlap) > 0:
            for ws in overlap:
                siterow = []
                print('here')
                print(site.latitude,site.longitude, ws)
                siterow.append(sf.samplingfeaturecode)
                siterow.append(sf.samplingfeatureid)
                siterow.append(ws)
                siterow.append(site.latitude)
                siterow.append(site.longitude)
                sitewriter.writerow(siterow)

