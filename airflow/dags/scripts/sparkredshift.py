from pyspark.sql import *
from pyspark import SparkConf
import os
from datetime import date

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
REDSHIFT_USER = os.getenv("REDSHIFT_USER")
REDSHIFT_PASSWORD = os.getenv("REDSHIFT_PASSWORD")

insdt = str(date.today()) 
mnyr = str(date.today().strftime("%Y-%m"))
s3path = "s3a://f1de-data-lake/{}/f1results.csv".format(mnyr)
connection_string = "jdbc:redshift://f1de-redshift-cluster.crqohyu1o55l.ap-south-1.redshift.amazonaws.com:5439/f1de?user={0}&password={1}".format(REDSHIFT_USER,REDSHIFT_PASSWORD)
  


spark = SparkSession.builder.appName('myapp').getOrCreate()
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.impl","org.apache.hadoop.fs.s3a.S3AFileSystem")
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.access.key", AWS_ACCESS_KEY_ID)
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.secret.key", AWS_SECRET_ACCESS_KEY)
#spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.endpoint", "s3.ap-south-1.amazonaws.com")

results = spark.read.format('csv').option('header',True).option('inferSchema',True).load(s3path)

results.na.fill(value="")
results.createOrReplaceTempView('results')

constructor = spark.sql("""select row_number() over(order by constructorId) as constructorKey, *, '{}' as insertDate 
from (select distinct constructorId,constructorName,constructorNationality from results) c""".format(insdt))
constructor.createOrReplaceTempView('constructor')

driver = spark.sql("""select row_number() over(order by driverId) as driverKey, *, '{}' as insertDate 
from (select distinct driverId, driverNumber,permanentNumber,code,concat(givenName,' ',familyName) as driverName,dateOfBirth,driverNationality from results) d""".format(insdt))
driver.createOrReplaceTempView('driver')

race = spark.sql("""select row_number() over(order by circuitId) as raceKey, *, '{}' as insertDate 
from (select distinct raceName,circuitId,circuitName,latitude,longitude,locality,country from results) r""".format(insdt))
race.createOrReplaceTempView('race')

status = spark.sql("""select row_number() over(order by status) as statusKey, *, '{}' as insertDate 
from (select distinct status from results) s""".format(insdt))
status.createOrReplaceTempView('status')

dates = spark.sql("""select distinct replace(date,'-','') as dateKey,date, season as year,'{}' as insertDate from results """.format(insdt))
dates.createOrReplaceTempView('dates')


results = spark.sql("""select row_number() over(order by year,round) as resultKey, constructorKey, driverKey, raceKey,statusKey,dateKey,round,position,positionText,points,grid,laps,millis,raceTime,fastestLapRank,fastestLap,fastestLapTime,averageSpeed, '{}' as insertDate
from (select constructorKey, driverKey, raceKey,statusKey,dateKey,round,position,positionText,points,grid,laps,millis,raceTime,fastestLapRank,fastestLap,fastestLapTime,averageSpeed,year
from results rs
inner join constructor c on c.constructorId = rs.constructorId and c.constructorName = rs.constructorName and c.constructorNationality = rs.constructorNationality
inner join driver d on d.driverId = rs.driverId and coalesce(d.driverNumber,'unknown') = coalesce(rs.driverNumber,'unknown') and d.driverName = concat(rs.givenName,' ',rs.familyName) and d.dateOfBirth=rs.dateOfBirth and d.driverNationality = rs.driverNationality
inner join race r on r.raceName = rs.raceName and r.circuitId = rs.circuitId and r.latitude = rs.latitude and r.longitude = rs.longitude and r.locality = rs.locality and r.country = rs.country
inner join status s on s.status = rs.status
inner join dates d on d.date = rs.date and d.year = rs.season) t""".format(insdt))

constructor.write.format("io.github.spark_redshift_community.spark.redshift").option("url",connection_string).option("dbtable", "f1de.dimConstructors").option("tempdir", "s3a://f1de-data-lake/logs").option("forward_spark_s3_credentials", True).mode("overwrite").save()

driver.write.format("io.github.spark_redshift_community.spark.redshift").option("url",connection_string).option("dbtable", "f1de.dimDrivers").option("tempdir", "s3a://f1de-data-lake/logs").option("forward_spark_s3_credentials", True).mode("overwrite").save()

race.write.format("io.github.spark_redshift_community.spark.redshift").option("url",connection_string).option("dbtable", "f1de.dimRaces").option("tempdir", "s3a://f1de-data-lake/logs").option("forward_spark_s3_credentials", True).mode("overwrite").save()

status.write.format("io.github.spark_redshift_community.spark.redshift").option("url",connection_string).option("dbtable", "f1de.dimStatus").option("tempdir", "s3a://f1de-data-lake/logs").option("forward_spark_s3_credentials", True).mode("overwrite").save()

dates.write.format("io.github.spark_redshift_community.spark.redshift").option("url",connection_string).option("dbtable", "f1de.dimDate").option("tempdir", "s3a://f1de-data-lake/logs").option("forward_spark_s3_credentials", True).mode("overwrite").save()

results.write.format("io.github.spark_redshift_community.spark.redshift").option("url",connection_string).option("dbtable", "f1de.factResults").option("tempdir", "s3a://f1de-data-lake/logs").option("forward_spark_s3_credentials", True).mode("overwrite").save()

