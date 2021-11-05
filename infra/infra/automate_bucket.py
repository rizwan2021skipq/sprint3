
import lambda_folder.constants as constants
import boto3

# Choose S3 as boto client
s3_client=boto3.client('s3')
s3_resource=boto3.resource('s3')
# Finding region of user
region=boto3.Session().region_name
# Choose Bucket name
bucket_name=constants.BUCKET_NAME
file_name='infra/lambda_folder/website_data.json'
object_name='website_data'
response = s3_client.list_buckets()

list_of_buckets=[]
for bucket in response['Buckets']:
    a=bucket["Name"]
    list_of_buckets.append(a)
#print(list_of_buckets)
    
    
if bucket_name in list_of_buckets:
    #print("true")
    my_bucket = s3_resource.Bucket(bucket_name)
    if object_name in my_bucket.objects.all():
        pass
    else:
        s3_client.upload_file(file_name, bucket_name, object_name)
#    print("true")
else:
    #print("false")
    s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint':region})
    s3_client.upload_file(file_name, bucket_name, object_name)
    
#else:
#    pass
    #s3_client.upload_file(file_name, bucket_name, object_name)
 
    

# Create a bucket using function create_bucket, the fucntion needs two arguments bucket name and the location
# Bucket has been named rizwanbucket2021 and location has been chosen as us-east-2
#s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint':region})
#s3_client.upload_file(file_name, bucket_name, object_name)
