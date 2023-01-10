import os

from airflow import DAG

from datetime import datetime

from scripts.readapi import readf1
from scripts.savetos3 import writes3

from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

with DAG('f1de_dag', start_date = datetime(2023,1,1),
        schedule_interval = '@monthly',max_active_runs=1, catchup=False,default_args={'retries': 2}) as dag:

        read_f1_api = PythonOperator(
            task_id = 'read_f1_api',
            python_callable = readf1,
        )

        upload_s3 = PythonOperator(
            task_id = 'upload_to_s3',
            python_callable = writes3,
        )

        write_redshift = BashOperator(
            task_id = 'write_to_redshift',
            bash_command = 'spark-submit --jars https://s3.amazonaws.com/redshift-downloads/drivers/jdbc/2.0.0.4/redshift-jdbc42-2.0.0.4.jar --packages org.apache.hadoop:hadoop-aws:3.3.4,org.apache.spark:spark-avro_2.12:3.3.1,io.github.spark-redshift-community:spark-redshift_2.12:5.1.0 $AIRFLOW_HOME/dags/scripts/sparkredshift.py',
        )


        read_f1_api >> upload_s3 >> write_redshift

