-- list catagorical values for result with ID of 370
select * from odm2.categoricalresultvalues where resultid=370 order by valuedatetime asc
-- list time series values for result with ID of 37021 
select * from odm2.timeseriesresultvalues where resultid=37021 order by valuedatetime desc


-- list a summary of all catagorical result series by location and variables sorted by count 
-- of total values in the series 
	   SELECT odm2.samplingfeatures.samplingfeaturecode, odm2.samplingfeatures.samplingfeaturename, odm2.results.resultid, 
	   odm2.variables.variablecode, max(odm2.categoricalresultvalues.valuedatetime) as maxdt,
	   min(odm2.categoricalresultvalues.valuedatetime) as mindt,
count(odm2.categoricalresultvalues.datavalue) as valuecount
FROM ((((odm2.results
INNER JOIN odm2.categoricalresultvalues ON odm2.results.resultid = odm2.categoricalresultvalues.resultid)
INNER JOIN odm2.variables ON odm2.results.variableid = odm2.variables.variableid)
	   INNER JOIN odm2.featureactions on odm2.results.featureactionid = odm2.featureactions.featureactionid)
	   INNER JOIN odm2.samplingfeatures on 
	   odm2.featureactions.samplingfeatureid =  odm2.samplingfeatures.samplingfeatureid)
	   group by odm2.samplingfeatures.samplingfeaturecode, odm2.samplingfeatures.samplingfeaturename,odm2.results.resultid, odm2.variables.variablecode
	   order by valuecount desc; 
	   
-- list a summary of all time series result series by location and variables sorted by count 
-- of total values in the series   
	   SELECT odm2.samplingfeatures.samplingfeaturecode, odm2.samplingfeatures.samplingfeaturename, 
	   odm2.results.resultid, odm2.variables.variablecode, 
count(odm2.timeseriesresultvalues.datavalue) as valuecount
FROM ((((odm2.results
INNER JOIN odm2.timeseriesresultvalues ON odm2.results.resultid = odm2.timeseriesresultvalues.resultid)
INNER JOIN odm2.variables ON odm2.results.variableid = odm2.variables.variableid)
	   INNER JOIN odm2.featureactions on odm2.results.featureactionid = odm2.featureactions.featureactionid)
	   INNER JOIN odm2.samplingfeatures on 
	   odm2.featureactions.samplingfeatureid =  odm2.samplingfeatures.samplingfeatureid)
	   group by odm2.samplingfeatures.samplingfeaturecode, odm2.samplingfeatures.samplingfeaturename,odm2.results.resultid, odm2.variables.variablecode
	   order by valuecount desc; 

	   
-- show a subset of results to inspect  
select * from odm2.results where resultid in (15419,15353,15446,15432,15323,15317)
	   
-- list a summary of all time series result series by location and variables sorted by count 
-- of total values in the series   
-- this includes the aggregation statistic - in this case, for PREP, sensor series have an aggregation 
-- statistic of average and sample based series have a value of continous
	   
	   SELECT odm2.samplingfeatures.samplingfeaturecode, odm2.samplingfeatures.samplingfeaturename, 
	   odm2.results.resultid,odm2.timeseriesresults.aggregationstatisticcv, odm2.variables.variablecode, 
	   odm2.units.unitsname, 
count(odm2.timeseriesresultvalues.datavalue) as valuecount, 
max(odm2.timeseriesresultvalues.valuedatetime) as maxdt,
	   min(odm2.timeseriesresultvalues.valuedatetime) as mindt
FROM ((((((odm2.results
INNER JOIN odm2.timeseriesresultvalues ON odm2.results.resultid = odm2.timeseriesresultvalues.resultid)
		INNER JOIN odm2.timeseriesresults ON odm2.results.resultid = odm2.timeseriesresults.resultid)	
	INNER JOIN odm2.variables ON odm2.results.variableid = odm2.variables.variableid)
	   INNER JOIN odm2.units ON odm2.results.unitsid = odm2.units.unitsid)
	   INNER JOIN odm2.featureactions on odm2.results.featureactionid = odm2.featureactions.featureactionid)
	   INNER JOIN odm2.samplingfeatures on 
	   odm2.featureactions.samplingfeatureid =  odm2.samplingfeatures.samplingfeatureid)
	   group by odm2.samplingfeatures.samplingfeaturecode, odm2.samplingfeatures.samplingfeaturename,
	   odm2.results.resultid, odm2.variables.variablecode,odm2.units.unitsname, odm2.timeseriesresults.aggregationstatisticcv
	   order by valuecount desc; 
-- with odm2.actions.actiondescription, odm2.methods.methodname, 

-- list a summary of all time series result series by location and variables sorted by count 
-- of total values in the series.  This adds method description and action description.   

	   SELECT odm2.samplingfeatures.samplingfeaturecode, odm2.samplingfeatures.samplingfeaturename, 
	   odm2.results.resultid,odm2.timeseriesresults.aggregationstatisticcv, odm2.variables.variablecode, 
	   odm2.units.unitsname, odm2.actions.actiondescription as actiondesc, odm2.methods.methoddescription as methoddescription, 
count(odm2.timeseriesresultvalues.datavalue) as valuecount, 
max(odm2.timeseriesresultvalues.valuedatetime) as maxdt,
	   min(odm2.timeseriesresultvalues.valuedatetime) as mindt
FROM ((((((((odm2.results
INNER JOIN odm2.timeseriesresultvalues ON odm2.results.resultid = odm2.timeseriesresultvalues.resultid)
	   INNER JOIN odm2.timeseriesresults ON odm2.results.resultid = odm2.timeseriesresults.resultid)	
	   INNER JOIN odm2.variables ON odm2.results.variableid = odm2.variables.variableid)
	   INNER JOIN odm2.units ON odm2.results.unitsid = odm2.units.unitsid)
	   INNER JOIN odm2.featureactions on odm2.results.featureactionid = odm2.featureactions.featureactionid)
	   INNER JOIN odm2.actions on odm2.actions.actionid = odm2.featureactions.actionid)
	   INNER JOIN odm2.methods on odm2.actions.methodid = odm2.methods.methodid)  
	  INNER JOIN odm2.samplingfeatures on 
	   odm2.featureactions.samplingfeatureid =  odm2.samplingfeatures.samplingfeatureid)
	   group by odm2.samplingfeatures.samplingfeaturecode, odm2.samplingfeatures.samplingfeaturename,
	   odm2.results.resultid,actiondesc, methoddescription, odm2.variables.variablecode,odm2.units.unitsname, odm2.timeseriesresults.aggregationstatisticcv
	   order by valuecount desc; 


/* show Nitrogen (Nitrate, Nitirite, NO2+NO3, etc), Phosphorus, Clay, Silt, and Sand PREP sample based values with location, lat, long,  */

	   SELECT odm2.samplingfeatures.samplingfeaturecode as sfcode, odm2.samplingfeatures.samplingfeaturename, 
	   sites.latitude, sites.longitude, odm2.variables.variabletypecv, 
	   odm2.timeseriesresults.aggregationstatisticcv, odm2.variables.variablecode as variablecode, 
	   odm2.timeseriesresultvalues.datavalue, odm2.timeseriesresultvalues.valuedatetime as datetime
FROM ((((((odm2.results
INNER JOIN odm2.timeseriesresultvalues ON odm2.results.resultid = odm2.timeseriesresultvalues.resultid)
		INNER JOIN odm2.timeseriesresults ON odm2.results.resultid = odm2.timeseriesresults.resultid 
		 and odm2.timeseriesresults.aggregationstatisticcv = 'Continuous')	
	INNER JOIN odm2.variables ON odm2.results.variableid = odm2.variables.variableid and odm2.variables.variablecode SIMILAR TO '(Nitrogen|Phos|Clay|Silt|Sand)%')
	   INNER JOIN odm2.featureactions on odm2.results.featureactionid = odm2.featureactions.featureactionid)
	   INNER JOIN odm2.samplingfeatures on 
	   odm2.featureactions.samplingfeatureid =  odm2.samplingfeatures.samplingfeatureid)
	  	  INNER JOIN odm2.sites on 
	   odm2.samplingfeatures.samplingfeatureid =  odm2.sites.samplingfeatureid)
	   order by sfcode, variablecode, datetime;
	   
/* show Turbidity and Light Attenuation Coefficient PREP sample based values with location, lat, long,  */
	   
	   SELECT odm2.samplingfeatures.samplingfeaturecode as sfcode, odm2.samplingfeatures.samplingfeaturename, 
	   sites.latitude, sites.longitude, odm2.actions.actiondescription, odm2.methods.methodname, 
	   odm2.timeseriesresults.aggregationstatisticcv, odm2.variables.variablecode as variablecode, 
	   odm2.units.unitsname as units,
	   odm2.timeseriesresultvalues.datavalue, odm2.timeseriesresultvalues.valuedatetime as datetime
FROM (((((((((odm2.results
INNER JOIN odm2.timeseriesresultvalues ON odm2.results.resultid = odm2.timeseriesresultvalues.resultid)
		INNER JOIN odm2.timeseriesresults ON odm2.results.resultid = odm2.timeseriesresults.resultid 
		 and odm2.timeseriesresults.aggregationstatisticcv = 'Continuous')	
	INNER JOIN odm2.variables ON odm2.results.variableid = odm2.variables.variableid and odm2.variables.variablecode in 
		('Turbidity', 'Light Attenuation Coefficient'))
	INNER JOIN odm2.units on odm2.results.unitsid = odm2.units.unitsid)
	   INNER JOIN odm2.featureactions on odm2.results.featureactionid = odm2.featureactions.featureactionid)
	   INNER JOIN odm2.actions on odm2.actions.actionid = odm2.featureactions.actionid)
	   INNER JOIN odm2.methods on odm2.methods.methodid = odm2.actions.actionid)
	   INNER JOIN odm2.samplingfeatures on 
	   odm2.featureactions.samplingfeatureid =  odm2.samplingfeatures.samplingfeatureid)
	  	  INNER JOIN odm2.sites on 
	   odm2.samplingfeatures.samplingfeatureid =  odm2.sites.samplingfeatureid)
	   order by sfcode, variablecode, datetime;

-- show variable types used 
select distinct(odm2.variables.variabletypecv) from odm2.variables

/* show water quality (not sediment or other types) PREP sample based values with for location 
with ID 1105 with lat, long,  */

SELECT odm2.samplingfeatures.samplingfeaturecode as sfcode, odm2.samplingfeatures.samplingfeaturename, 
	   sites.latitude, sites.longitude, odm2.actions.actiondescription, odm2.methods.methodname, 
	   odm2.timeseriesresults.aggregationstatisticcv, odm2.variables.variablecode as variablecode, 
	   odm2.units.unitsname as units, odm2.variables.variabletypecv, 
	   odm2.timeseriesresultvalues.datavalue, odm2.timeseriesresultvalues.valuedatetime as datetime
FROM (((((((((odm2.results
INNER JOIN odm2.timeseriesresultvalues ON odm2.results.resultid = odm2.timeseriesresultvalues.resultid)
		INNER JOIN odm2.timeseriesresults ON odm2.results.resultid = odm2.timeseriesresults.resultid)	
	INNER JOIN odm2.variables ON odm2.results.variableid = odm2.variables.variableid 
			and odm2.variables.variabletypecv = 'Water quality')
	INNER JOIN odm2.units on odm2.results.unitsid = odm2.units.unitsid)
	   INNER JOIN odm2.featureactions on odm2.results.featureactionid = odm2.featureactions.featureactionid)
	   INNER JOIN odm2.actions on odm2.actions.actionid = odm2.featureactions.actionid)
	   INNER JOIN odm2.methods on odm2.methods.methodid = odm2.actions.actionid)
	   INNER JOIN odm2.samplingfeatures on 
	   odm2.featureactions.samplingfeatureid =  odm2.samplingfeatures.samplingfeatureid
	  and odm2.samplingfeatures.samplingfeatureid=1105)
	  	  INNER JOIN odm2.sites on 
	   odm2.samplingfeatures.samplingfeatureid =  odm2.sites.samplingfeatureid)
	   order by sfcode, variablecode, datetime;

-- Show a summary of all time series. Sample and sensor based. 
	   SELECT odm2.samplingfeatures.samplingfeaturecode as sfcode, odm2.samplingfeatures.samplingfeaturename, 
	   sites.latitude, sites.longitude, odm2.actions.actiondescription, odm2.methods.methodname, 
	   odm2.timeseriesresults.aggregationstatisticcv, odm2.variables.variablecode as variablecode, 
	   odm2.units.unitsname as units,
	   count(odm2.timeseriesresultvalues.datavalue) as valuecount, 
max(odm2.timeseriesresultvalues.valuedatetime) as maxdt,
	   min(odm2.timeseriesresultvalues.valuedatetime) as mindt
FROM (((((((((odm2.results
INNER JOIN odm2.timeseriesresultvalues ON odm2.results.resultid = odm2.timeseriesresultvalues.resultid)
		INNER JOIN odm2.timeseriesresults ON odm2.results.resultid = odm2.timeseriesresults.resultid)	
	INNER JOIN odm2.variables ON odm2.results.variableid = odm2.variables.variableid)
	INNER JOIN odm2.units on odm2.results.unitsid = odm2.units.unitsid)
	   INNER JOIN odm2.featureactions on odm2.results.featureactionid = odm2.featureactions.featureactionid)
	   INNER JOIN odm2.actions on odm2.actions.actionid = odm2.featureactions.actionid)
	   INNER JOIN odm2.methods on odm2.methods.methodid = odm2.actions.actionid)
	   INNER JOIN odm2.samplingfeatures on 
	   odm2.featureactions.samplingfeatureid =  odm2.samplingfeatures.samplingfeatureid)
	  	  INNER JOIN odm2.sites on 
	   odm2.samplingfeatures.samplingfeatureid =  odm2.sites.samplingfeatureid)
	   order by valuecount, sfcode, variablecode
	   
-- change the sampling feature type for water quality stations to an
-- aggrgation type of Average 
update odm2.samplingfeatures 
set samplingfeaturetypecv = 'Water quality station'
where samplingfeatureid in 
(select samplingfeatureid from odm2.featureactions where featureactionid in 
 (select featureactionid from odm2.results where resultid in 
(select resultid from odm2.timeseriesresults where aggregationstatisticcv = 'Average' ))) 

-- various table queries

select distinct resultid from odm2.timeseriesresultvalues

select count(*) from  odm2.timeseriesresultvalues 

select * from  odm2.samplingfeatures

select count(*) from odm2.categoricalresultvalues
select count(*) from odm2.timeseriesresults where aggregationstatisticcv = 'Continuous' 
select count(*) from odm2.timeseriesresultvalues where resultid in 
(select resultid from odm2.timeseriesresults where aggregationstatisticcv = 'Continuous' ) 

select * from odm2.samplingfeatures where samplingfeatureid in 
(select samplingfeatureid from odm2.featureactions where featureactionid in 
 (select featureactionid from odm2.results where resultid in 
(select resultid from odm2.timeseriesresults where aggregationstatisticcv = 'Average' ))) 

select * from  odm2.samplingfeatures where samplingfeaturecode = 'GRBSQ'

select count(*) from odm2.timeseriesresults where aggregationstatisticcv = 'Average'
select count(*) from odm2.timeseriesresults where aggregationstatisticcv = 'Continuous'

select count(*) from  odm2.samplingfeatures
	   