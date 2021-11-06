''' This file defines a function named url_list that retrieves a .json file present in a S3 bucket. The .json file contains list of websites
This file defines a function that retrieves a list of websites to be monitored from a S3 bucket '''

# Import libraries to be used
import boto3
import json
#import constants



def url_list(bucket_name, file_name):
    '''
    Function url_list(bucket_name, file_name)
    
    Description  : A function that accesses a .json file present in a S3 bucket to retrieve a list of websites to be monitored
    
    Inputs       : bucket_name: type: string
                   Name of Bucket contaning filw with URLS
                   file_name: type: string
                   Name of file contaning urs
                    
    
    Return       : type: list
                   Returns a list of websites to be monitored
    
    Example of Usage:
    				url_list() ====> returns ["https://www.skipq.org", "https://www.espn.com.au/", "https://www.bbc.com/news", "https://shaukatkhanum.org.pk/"]
    				
    '''
    
    # Choose S3 resource
    s3 = boto3.resource('s3')
    # Choosing object to access present in a S3 bucket by providing bucket name and the name of file present in the bucket
    content_object = s3.Object(bucket_name, file_name)
    # Reading and decoding content of the json file
    file_content = content_object.get()['Body'].read().decode('utf-8')
    # Loading content of json file in variable named json_content, which itself is a dictionary
    json_content = json.loads(file_content)
    # Getting the list of URLS
    url_list=json_content['URLS_TO_MONITOR']
    
    return url_list

