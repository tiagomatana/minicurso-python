import boto3
import boto
import logging

s3 = boto.connect_s3()
logging.basicConfig(filename=f'list_buckets.csv',format='%(message)s', level=logging.INFO)
logging.info('Bucket,Size,Objects')




def get_bucket_size(bucket_name):
    '''Given a bucket name, retrieve the size of each key in the bucket
    and sum them together. Returns the size in gigabytes and
    the number of objects.'''

    bucket = s3.lookup(bucket_name)

    total_bytes = 0
    n = 0
    try:
        for key in bucket:
            total_bytes += key.size
            n += 1
            
    except: 
        logging.info("%s, %i, %i" % (bucket_name, 0, n))

    total_gigs = total_bytes/1024/1024/1024

    logging.info("%s, %i, %i" % (bucket_name, total_gigs, n))

for bucket in boto3.resource('s3').buckets.all():
    # print (bucket.name)
    get_bucket_size(bucket.name)
