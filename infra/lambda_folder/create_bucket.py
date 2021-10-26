''' This file can be used to create a S3 bucket'''

# Import boto3 library
import boto3
import constants

# Choose S3 as boto client
s3_client=boto3.client('s3')
# Finding region of user
region=boto3.Session().region_name
# Choose Bucket name
bucket_name=constants.BUCKET_NAME


# Create a bucket using function create_bucket, the fucntion needs two arguments bucket name and the location
# Bucket has been named rizwanbucket2021 and location has been chosen as us-east-2
s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint':region})
