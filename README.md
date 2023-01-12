# F1DE (Formula 1 Data Engineering)
A Batch ETL pipeline built using AWS S3, Redshift, Spark (Databricks) and Airflow to fetch, process and visualize Formula 1 race results data.

## Architecture
1. The F1 race results data (1950-2022) is fetched from [**Ergast F1 API**](https://ergast.com/mrd/) using Python and written into an CSV file
2. The CSV file is loaded into an AWS S3 bucket
3. The CSV from S3 is fetched and read in Databricks setup on AWS using Spark, the data is transformed, split and written as respective Fact and Dimensional tables into AWS Redshift
4. Analysis is performed on data in Redshift using SQL
5. A connection is setup between Redshift and PowerBI desktop to perform visualizations and generate reports.

- Apache Airflow is used to schedule and orchestrate the data pipeline, the pipeline is scheduled to run on monthly basis
- The entire AWS infrastructure was setup using Terraform and Docker was used to containerize airflow and other dependencies.

![architecture](https://github.com/pvp16/F1DE/blob/master/images/f1de.jpg?raw=true)

## Data Model (Fact and Dimension Tables)

![datamodel](https://github.com/pvp16/F1DE/blob/master/images/ERDiagram.png?raw=true)

## Airflow DAG

![airflow](https://github.com/pvp16/F1DE/blob/master/images/AirflowDAG.png?raw=true)

## PowerBI Visualizations

![vis1](https://github.com/pvp16/F1DE/blob/master/images/Report1-1.jpg?raw=true)

![vis2](https://github.com/pvp16/F1DE/blob/master/images/Report2.jpg?raw=true)

## Notes

- The whole pipeline is built on AWS free tier, hence had to use AWS Databricks trial instead of AWS EMR (not available in AWS free tier).

### Things to do to improve the pipeline

- Incremental loading of data into fact and dimension tables
- Add more Fact and Dimension tables to analyze qualifying, sprints and lap times.
- Add tests and CI/CD




