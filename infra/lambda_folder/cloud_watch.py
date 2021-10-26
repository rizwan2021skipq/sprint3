''' This file is used is used to define a class named CloudWatchMetrics that contains a method named put_metric, this method
 is used to define metrics to be observed.'''

# Importing libraries
import boto3

# Defining a class named CloudWatchMetrics with a mthod named put_metric that is used to initialize metrics of availability and 

class CloudWatchMetrics:
    def __init__(self):
        # Selecting cloudwatch client
        self.client=boto3.client('cloudwatch')
    
    def put_metric(self, namespace, dimensions, metric_name, value):
        # latency of a website
        '''
        Function put_metric(scope, namespace, dimensions, metric_name, value)
        
        Description  : A function that is used to initialize metrics
        
        Arguments    : scope
                       namespace: str
                       namespace for containing metrics
                       dimensions:
                       dimesnions of metrics
                       metric_name: str
                       name of metric
                       value: 
                       value of metric
                        
        Return       : Returns a call of put_metric_data function
        
        '''
        # Defining metric data
        metric_data=[ {
        
        'MetricName':metric_name,
        'Dimensions':dimensions,
        'Value':value
      
    },  
    ]
        # Calling the already defined put_metric_data function to initalize the metrics
        metric_call=self.client.put_metric_data(Namespace=namespace,MetricData=metric_data)
        return metric_call