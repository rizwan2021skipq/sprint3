''' This file defines handler function for Lambda function, for this project the function we are using is named health_web'''

# Import files and classes form files that need to be used in the project
import url_retriever
from cloud_watch import CloudWatchMetrics

# Import libraries that need to be used in the project
import urllib3
import datetime
import constants
import json
import boto3



def log_lambda(event, context):
    region=boto3.Session().region_name
    dynamodb = boto3.resource('dynamodb', region)
    table=dynamodb.Table('NEWS')
    #message = json.loads(event['Records'][0]['EventVersion'])
    #print(event)
    print(event["Records"][0]['Sns']['Subject'])
    response = table.put_item(
    Item = { 
     'Name': event["Records"][0]['Sns']['Subject'],
     'Email': event["Records"][0]['Sns']['Message']
       }
    )
    
    '''
    print(event["Records"][0]['Sns']['Type'])
    print(event["Records"][0]['Sns']['Subject'])
    print(event["Records"][0]['Sns']['Message'])
    print(event["Records"][0]['Sns']['Timestamp'])
    print(event["Records"][0]['Sns']['Subject'])
    print(event["Records"][0]['Sns']['Subject'])
    '''
    
    #SnsPublishTime = event.Records[0].Sns.Timestamp;
    #SnsTopicArn = event.Records[0].Sns.TopicArn;
    #LambdaReceiveTime = new Date().toString();
    #itemParams = {Item: {SnsTopicArn: {S: SnsTopicArn},
    #SnsPublishTime: {S: SnsPublishTime}, SnsMessageId: {S: SnsMessageId},
    #LambdaReceiveTime: {S: LambdaReceiveTime}  
    #print(event)
    #dynamodb = boto3.resource('dynamodb')
    #table = dynamodb.Table('Users')    

    #print(table.table_status)
    #print("GARBAGE")
def health_web(event, context):
	'''
	Function health_web(event, context)
	
	Description  : A handler function that finds latency and page availability of each website present in a list
				   retrieved from a S3 bucket
	                
	Parameters   : event, context
	
				   event
				   An event is a JSON-formatted document that contains data for a Lambda function to process. 
	               The Lambda runtime converts the event to an object and passes it to your function code. 
	               It is usually of the Python dict type. It can also be list, str, int, float, or the NoneType type.
	               
	               context
	               A context object is passed to your function by Lambda at runtime. 
	               This object provides methods and properties that provide information about the invocation, function, 
	               and runtime environment.
	   
	Return       : type: dict
				   Returns a dictionary named dict_latency_availability that contains info about latency and page availability of a website.
	   			   The dictionary key "page_available" has key value 1 if website is available else the key
				   has value of 0
				   The dictionary key "latency_in_seconds"  has key value of latency in seconds
	'''

	
	# Initiating CloudWatch metrics
	cw_metric=CloudWatchMetrics()
	# Retrieving list of URl to monitor from a S3 bucket
	list_of_urls=url_retriever.url_list()
	#list_of_urls= ["https://www.skipq.org", "https://www.espn.com.au/", "https://www.bbc.com/news", "https://shaukatkhanum.org.pk/"]
	# Initiating Pool Manager
	http = urllib3.PoolManager()
	# Initiating a dictionary to store latency and availability values
	dict_latency_availability=dict()
	
	# A loop to iterate over all websites in a list and store their latency and availiability values, while also defining their metrics
	for i in list_of_urls:
		
	   # Get latency value
	   latency_url=get_latency(i, http)
	   # get availability value
	   availability_url=get_availability(i, http)
	   # Defining dimensions for metric
	   dimensions=[{
	       'Name':'website name',
	       'Value':i
	   },
	   ]
	   
	   # Defining metrics for availability and latency of a website
	   cw_metric.put_metric(constants.URL_MONITOR_NAMESPACE, dimensions, constants.URL_MONITOR_METRIC_AVAILABILITY, availability_url)
	   cw_metric.put_metric(constants.URL_MONITOR_NAMESPACE, dimensions, constants.URL_MONITOR_METRIC_LATENCY, latency_url)
	   
	   # Storing values of latency and availability in the dictionary
	   dict_latency_availability["latency_in_seconds_of_{}".format(i)]=latency_url
	   dict_latency_availability["page_available_of_{}".format(i)]=availability_url
	   
	return dict_latency_availability


def get_availability(url, http):
	'''
	Function get_availability(url, http)
	
	Description  : A function that finds whether a website is available by taking its URL as input
	                
	Parameters   : url: str
				   The URL of website whose availability need to be checked
				   http 
				   Allows for arbitrary requests while transparently keeping track of necessary connection pools for you.
	   
	Return       : type: int
				   Returns 1 if website is available. If a website in unavailable it returns 0
	 
	Example of Usage:
					url="https://www.skipq.org/"
					get_availability(url)		====> returns 1 if available, else returns 0
	
	'''				
	# request the website
	resp = http.request('GET', url)
	if resp.status==200:
		return 1
	else:
		return 0
		


def get_latency(url, http):
	'''
	Function get_latency(url, http)
	
	Description  : A function that finds latency of a website.
	                
	Parameters   : url: str
				   The URL of website whose latency needs to be found.
				   http
				   Allows for arbitrary requests while transparently keeping track of necessary connection pools for you.
	   
	Return       : type: float
				   Returns time in seconds upto accuracy of three decimal numbers. Decimal numbers can be adjusted in second parameter
				   of round function according to your own needs.
	 
	Example of Usage:
					url="https://www.skipq.org/"
					get_latency(url)		====> returns latency value i.e. 0.034
					
	'''

	# Store current date and time in a variable named start before requesting website
	start = datetime.datetime.now()
	# request the website
	response = http.request('GET', url)
	# Store the current date and time in a variable named end after requesting the website
	end = datetime.datetime.now()
	# Time elapsed can be found by subtracting end date and time from start one and storing it in delta variable
	delta = end - start
	# Now convert that time to seconds
	elapsed_seconds = round(delta.microseconds * 1E-6, 3)
	return elapsed_seconds
