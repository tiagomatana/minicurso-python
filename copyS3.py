#!/usr/bin/python3

import boto3
import sys
import logging
from datetime import datetime

def main(args):
  # if len(args)<2:
  #   sys.exit("Invalid bucket name or not exists")
  try:
    # bucketName = args[1]
    s3 = boto3.client('s3')
    # bucketName = 'converter-prd-conversionsbucket-1oq1gn85k16lk'
    bucketName = 'jh-operations-bucket-prd'
    fileLog = f"{bucketName}-{datetime.now().strftime('%d%m%Y')}.log"
    logging.basicConfig(
      filename=fileLog, 
      format='%(asctime)s %(levelname)-8s %(message)s',
      level=logging.INFO,
      datefmt='%d-%m-%Y %H:%M:%S')

    

    all_objects = boto3.resource("s3").Bucket(bucketName).objects.all()  
    logging.info("Starting transaction")
    # print(len(all_objects))

    for obj in all_objects:
      if obj.size > 0 and obj.storage_class == 'STANDARD':
        copy_source = {
          'Bucket': bucketName,
          'Key': obj.key
        }
        s3.copy(
          copy_source, bucketName, obj.key,
          ExtraArgs = {
            'StorageClass': 'INTELLIGENT_TIERING', #STANDARD_IA
            'MetadataDirective': 'COPY'
          }
        )
        logging.info(f"{obj.key} copied")
    logging.info("Finish transaction")
  except:
    logging.error("Something else went wrong")

if __name__ == "__main__":
  main(sys.argv)
  
  
