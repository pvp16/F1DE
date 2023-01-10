FROM apache/airflow:2.5.0
USER root

ENV AIRFLOW_HOME=/opt/airflow

RUN apt update && \
    apt-get install -y default-jre && \
    apt-get clean;

ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/
RUN export JAVA_HOME

USER airflow

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt