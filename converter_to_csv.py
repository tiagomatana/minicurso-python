import boto3 
import datetime
import re
import logging
import csv

s3 = boto3.resource("s3")

all_keys = []
bucketName="converter-prd-conversionsbucket-1oq1gn85k16lk" #'original-files-bucket-dev'
bucketName = "jh-operations-bucket-prd"
logging.basicConfig(filename=f'{bucketName}.csv',format='%(message)s')
logging.warning('Key,Size')

all_objects = s3.Bucket(bucketName).objects.all() 

for obj in all_objects:
    if obj.size > 0:
        logging.warning(f"{obj.key},{obj.size}")


