import boto3 
from io import BytesIO
import zipfile
import os
from datetime import datetime
import sys
import logging

s3 = boto3.client("s3")

ObjectKeys = []
keys = []
key = ''
fmt = '%d/%m/%Y'

def zipResults(bucketName, ObjectKeys, key):
    logging.info(f"Creating zip file with {len(ObjectKeys)} objects.")
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, 'w', compression=zipfile.ZIP_DEFLATED) as zip_file:
        for ObjectKey in ObjectKeys:
            objectContent = boto3.resource('s3').Object(bucketName, ObjectKey).get()['Body'].read()
            fileName = os.path.basename(ObjectKey)
            zip_file.writestr(fileName, objectContent)
            logging.info(f"{ObjectKey} downloaded")

    buffer.seek(0)
    logging.info('Zip file created.')
    uploadObject(bucketName, buffer, key)
    
    

def uploadObject(bucketName, body, key):
    logging.info(f"Uploading file {key}")
    try:
        response = s3.put_object(
            Bucket=bucketName,
            Body=body,
            Key=key,
            StorageClass='GLACIER'
        )
    except:
        logging.error('UPLOADING FAIL')
        return None

    print(response)

def clearObjects():
    s3.delete_objects(
        Bucket=bucketName,
        Delete={
            'Objects': keys,
            'Quiet': False
        }
    )


def handler(bucketName, date):

    logging.info(f"Starting backup.")

    try:
        logging.info("Fetching objects")
        all_objects = boto3.resource("s3").Bucket(bucketName).objects.all()
        logging.info("Creating buffer...")
        key = f"backup_{date.strftime('%d%m%Y%H%M%S')}.zip"
        logging.info('Finding...')

        for obj in all_objects:
            if datetime(obj.last_modified.year, obj.last_modified.month, obj.last_modified.day) == date:
                if obj.size > 0 and obj.storage_class != 'GLACIER':
                    ObjectKeys.append(obj.key)
                    logging.info(f"{obj.key} ({obj.last_modified}) included")
                    if len(ObjectKeys) > 99:
                        break       
        
    except:
        print('Error to create list')

    
    try:
        logging.info(f'{bucketName} - {len(ObjectKeys)}')
        zipResults(bucketName, ObjectKeys, key)
    except:
        print('Error on download objects to buffer')




if __name__ == "__main__":
    if len(sys.argv) > 2:
        try:
            bucketName: str = sys.argv[1]
            date: datetime = datetime.strptime(str(sys.argv[2]), fmt)
            fileLog = f"{bucketName}.log"
            logging.basicConfig(
                filename=fileLog, 
                filemode='a',
                format='%(asctime)s %(levelname)-8s %(message)s', 
                level=logging.INFO, 
                datefmt='%d-%m-%Y %H:%M:%S')

            handler(bucketName, date)
        except:
            print('ERROR when parsing parameters.')
    else:
        print('Parameters missing.')
    # handler()
#     logging.info("Starting")
#     main(sys.argv)
   
#     logging.info("Ending ")
   
