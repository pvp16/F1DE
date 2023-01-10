import os
import boto3
from datetime import date

def writes3():
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = os.getenv("AWS_REGION")
    insdt = str(date.today().strftime("%Y-%m"))
    key = "{}/f1results.csv".format(insdt)
    
    session = boto3.Session(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY,region_name=AWS_REGION)


    s3 = session.resource('s3')
    BUCKET = "f1de-data-lake"

    s3.Bucket(BUCKET).upload_file("./f1results.csv", key)

    if os.path.isfile('f1results.csv'):
        os.remove('f1results.csv')
    