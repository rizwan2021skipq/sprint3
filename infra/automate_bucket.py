''' This file is used to create an S3 bucket and upload the file containing URLS to it'''

import lambda_folder.constants as constants
import boto3

# Choose S3 as boto client
s3_client=boto3.client('s3')
s3_resource=boto3.resource('s3')

# Finding region of user
region=boto3.Session().region_name
# Choose Bucket name
bucket_name=constants.BUCKET_NAME

file_name=constants.FILE_IN_BUCKET
object_name='website_data'

response = s3_client.list_buckets()

# Listing all buckets
list_of_buckets=[]
for bucket in response['Buckets']:
    a=bucket["Name"]
    list_of_buckets.append(a)

    
# Checking whether Bucket already exists    
if bucket_name in list_of_buckets:
    
    my_bucket = s3_resource.Bucket(bucket_name)
    
    # Checking whether we have the object already present in the bucket
    if object_name in my_bucket.objects.all():
        pass
    else:
    # Uploading File to Bucket    
        s3_client.upload_file(file_name, bucket_name, object_name)

else:
    # Crreating bucket and uploading file to it
    s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint':region})
    s3_client.upload_file(file_name, bucket_name, object_name)
    
