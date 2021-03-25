library('RPostgreSQL')
pg = dbDriver("PostgreSQL")
con = dbConnect(pg, user="postgres", password="",
                host="127.0.0.1", port=5432, dbname="ODM2LCZO2")
waterdepthI9 = dbGetQuery(con, "select to_char(valuedatetime, 'MM-DD-YYYY HH24:MI:SS') as valuedateandtime,datavalue 
                     from odm2.timeseriesresultvalues where resultid=18738 
                      order by valuedatetime") # and valuedatetime >= '2019-09-27 21:31:02' and valuedatetime <='2019-12-18 14:31:02'

waterdepthI23 = dbGetQuery(con, "select to_char(valuedatetime, 'MM-DD-YYYY HH24:MI:SS') as valuedateandtime,datavalue 
                     from odm2.timeseriesresultvalues where resultid=18739 
                      order by valuedatetime") # and valuedatetime >= '2019-09-27 21:31:02' and valuedatetime <='2019-12-18 14:31:02'


waterdepthI6 = dbGetQuery(con, "select to_char(valuedatetime, 'MM-DD-YYYY HH24:MI:SS') as valuedateandtime,datavalue 
                     from odm2.timeseriesresultvalues where resultid=18737 
                      order by valuedatetime") # and valuedatetime >= '2019-09-27 21:31:02' and valuedatetime <='2019-12-18 14:31:02'


waterdepthI4 = dbGetQuery(con, "select to_char(valuedatetime, 'MM-DD-YYYY HH24:MI:SS') as valuedateandtime,datavalue 
                     from odm2.timeseriesresultvalues where resultid=18736 
                      order by valuedatetime") # and valuedatetime >= '2019-09-27 21:31:02' and valuedatetime <='2019-12-18 14:31:02'
waterdepthI4["depth_to_water"] <- 1.922 - waterdepthI4["datavalue"]
waterdepthI6["depth_to_water"] <- 1.816 - waterdepthI6["datavalue"]
waterdepthI9["depth_to_water"] <- 1.784 - waterdepthI9["datavalue"]
waterdepthI23["depth_to_water"] <- 2.623 - waterdepthI23["datavalue"]

waterdepthI23["water_elevation"] <- 627.41 - waterdepthI23["depth_to_water"]
waterdepthI4["water_elevation"] <- 624.454 - waterdepthI4["depth_to_water"]
waterdepthI6["water_elevation"] <- 624.407 - waterdepthI6["depth_to_water"]
waterdepthI9["water_elevation"] <- 625.274 - waterdepthI9["depth_to_water"]

summary(waterdepthI4)
summary(waterdepthI6)
summary(waterdepthI9)
summary(waterdepthI23)

write.csv(waterdepthI4, 'I4WaterDepth.csv')
write.csv(waterdepthI6, 'I6WaterDepth.csv')
write.csv(waterdepthI9, 'I9WaterDepth.csv')
write.csv(waterdepthI23, 'I23WaterDepth.csv')

# I-4 depth to water = 18742
# I-4 water elevation = 18743


# I-9 depth to water = 18744
# I-9 water elevation = 18745

# I-6 depth to water = 18746
# I-6 water elevation = 18747


# I-23 depth to water = 18748
# I-23 water elevation = 18749